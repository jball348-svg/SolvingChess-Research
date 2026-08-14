"""Deterministically resolve and build the instruction for exactly one G programme."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

from io_utils import canonical_json_bytes, load_json, sha256_bytes


PROGRAMME_RE = re.compile(r"^G?(\d+)$", re.IGNORECASE)


def parse_programme(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError(f"invalid programme: {value!r}")
    if isinstance(value, int) and value >= 0:
        return value
    match = PROGRAMME_RE.fullmatch(str(value).strip())
    if not match:
        raise ValueError(f"invalid programme: {value!r}")
    return int(match.group(1))


def format_programme(number: int) -> str:
    return f"G{int(number)}"


def _lookup(state: Any, names: Iterable[str]) -> Any:
    """Find a routing field without assuming one historical schema spelling."""

    wanted = {name.casefold() for name in names}
    queue = [state]
    while queue:
        node = queue.pop(0)
        if isinstance(node, dict):
            for key, value in node.items():
                if str(key).casefold() in wanted:
                    return value
            queue.extend(value for value in node.values() if isinstance(value, (dict, list)))
        elif isinstance(node, list):
            queue.extend(value for value in node if isinstance(value, (dict, list)))
    return None


def resolve_next_programme(state: dict[str, Any]) -> int:
    value = _lookup(
        state,
        (
            "next_programme",
            "next_program",
            "next_g",
            "next_sequential_programme",
        ),
    )
    if isinstance(value, dict):
        value = _lookup(value, ("programme", "program", "id", "number", "g"))
    if value is None:
        latest = _lookup(state, ("latest_completed_programme", "latest_completed_g", "latest_completed"))
        if latest is None:
            raise ValueError("PROGRAM_STATE has no next programme routing field")
        return parse_programme(latest) + 1
    return parse_programme(value)


def resolve_latest_completed(state: dict[str, Any]) -> int | None:
    value = _lookup(state, ("latest_completed_programme", "latest_completed_g", "latest_completed"))
    if isinstance(value, dict):
        value = _lookup(value, ("programme", "program", "id", "number", "g"))
    return None if value is None else parse_programme(value)


def next_authorized(state: dict[str, Any]) -> bool:
    names = ("next_programme_authorized", "next_programme_authorization_status", "next_authorized")
    next_object = state.get("next_programme")
    value = next_object.get("authorized") if isinstance(next_object, dict) else None
    if value is None:
        value = next((state[name] for name in names if name in state), None)
    if value is None:
        value = _lookup(state, names)
    if isinstance(value, dict):
        value = _lookup(value, ("authorized", "status", "value"))
    if isinstance(value, str):
        return value.strip().upper() in {"AUTHORIZED", "TRUE", "YES", "PERMITTED", "READY"}
    return value is True


def next_started(state: dict[str, Any]) -> bool:
    names = ("next_programme_started", "next_programme_started_status", "next_started")
    next_object = state.get("next_programme")
    value = next_object.get("started") if isinstance(next_object, dict) else None
    if value is None:
        value = next((state[name] for name in names if name in state), None)
    if value is None:
        value = _lookup(state, names)
    if isinstance(value, dict):
        value = _lookup(value, ("started", "status", "value"))
    if isinstance(value, str):
        return value.strip().upper() in {"STARTED", "TRUE", "YES", "ACTIVE", "RUNNING"}
    return value is True


def _authority_path(state: dict[str, Any], names: tuple[str, ...], fallback: str) -> str:
    value = _lookup(state, names)
    if isinstance(value, dict):
        value = _lookup(value, ("path", "file", "relative_path"))
    return str(value) if value else fallback


def git_head(repo: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "NO_GIT_HEAD"


def make_run_id(
    programme: int,
    attempt: int,
    base_commit: str,
    state: dict[str, Any],
) -> str:
    seed = {
        "programme": format_programme(programme),
        "attempt": int(attempt),
        "base_commit": base_commit,
        "program_state_sha256": sha256_bytes(canonical_json_bytes(state)),
        "protocol": "solving-chess-autonomous-g/v1",
    }
    suffix = hashlib.sha256(canonical_json_bytes(seed)).hexdigest()[:12]
    return f"{format_programme(programme)}-a{attempt:02d}-{suffix}"


def build_prompt(
    repo: Path,
    programme: int | None = None,
    attempt: int = 1,
    base_commit: str | None = None,
) -> tuple[str, str, str]:
    repo = Path(repo).resolve()
    state = load_json(repo / "state" / "PROGRAM_STATE.json")
    resolved = resolve_next_programme(state)
    if programme is not None and int(programme) != resolved:
        raise ValueError(
            f"requested {format_programme(programme)} but repository routes {format_programme(resolved)}"
        )
    programme = resolved
    if not next_authorized(state):
        raise ValueError(f"{format_programme(programme)} is not authorized")
    if next_started(state):
        raise ValueError(f"{format_programme(programme)} is already marked started")

    base_commit = base_commit or git_head(repo)
    run_id = make_run_id(programme, attempt, base_commit, state)
    roadmap = _authority_path(
        state,
        ("permanent_roadmap_path", "roadmap_path", "permanent_roadmap"),
        "roadmap/normalized/G9_G10_Onwards_Long_Range_Plan.md",
    )
    handoff = _authority_path(
        state,
        ("latest_frozen_handoff", "latest_handoff_path", "technical_authority"),
        "the immediately preceding frozen technical handoff identified by PROGRAM_STATE.json",
    )
    g = format_programme(programme)
    successor = format_programme(programme + 1)
    reference_map_instruction = (
        "6. `state/REFERENCE_REGISTRY.json` and `references/REFERENCE_MAP.md` only as retrieval maps."
        if (repo / "references" / "REFERENCE_MAP.md").is_file()
        else "6. `state/REFERENCE_REGISTRY.json` only as a retrieval map."
    )
    prompt = f"""# Solving Chess autonomous programme instruction

Run identity: `{run_id}`
Authorized programme: `{g}`
Base Git commit: `{base_commit}`

Begin exactly {g}, the next authorized programme in `state/PROGRAM_STATE.json`.
This process owns one programme only. Never begin, create research outputs for, or mark
started the successor {successor}. Do not commit, tag, push, create branches, or alter
Git metadata; the outer controller owns every Git transaction.

Before work, read and obey:

1. `AGENTS.md`;
2. `state/PROGRAM_STATE.json`;
3. `{roadmap}` as permanent strategic authority;
4. `{handoff}` as current technical authority;
5. `docs/RESEARCH_PROTOCOL.md`;
{reference_map_instruction} Open only references
   materially relevant to {g}; they remain non-authoritative unless explicitly
   imported with provenance and verified to the current proof standard.

Reconstruct the exact, conditional, empirical, failed, blocked, and open state. Preserve
frozen exceptions and negative results. Execute {g} autonomously through its legitimate
PASS, HOLD, BLOCKED, or FAILED condition. Actively falsify claims and perform independent
replay where the current authority requires it. Do not ask for work that is locally
resolvable.

Close {g} according to `docs/RESEARCH_PROTOCOL.md`. At minimum create exactly
`research/{g}/{g}_Technical_Handoff.md` and
`research/{g}/{g}_Freeze_Manifest.json`, plus required hashes, validation/replay
instructions, claim classes, negative results, blockers, successor contract, and update
`state/PROGRAM_STATE.json`. Write only inside this worktree. Treat inherited originals,
controller/validator code, schemas, frozen historical handoffs, and previous research as
read-only.

Your final response must be only one JSON object satisfying the API-admission shape in
`schemas/g_completion.output.schema.json`. It must also satisfy the stricter local
`schemas/g_completion.schema.json`, which the outer controller applies independently to
the response, artifacts and state transition. Use run_id `{run_id}` and programme `{g}`
exactly.
On acceptance it will copy the final object to
`research/{g}/{g}_Completion.json`; do not create that controller-owned copy yourself.
After emitting the completion object, stop without starting {successor}.
"""
    prompt = prompt.replace("\r\n", "\n")
    return prompt, run_id, hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--programme", type=parse_programme)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--base-commit")
    parser.add_argument("--metadata", action="store_true", help="print JSON metadata instead")
    args = parser.parse_args()
    prompt, run_id, prompt_hash = build_prompt(args.repo, args.programme, args.attempt, args.base_commit)
    if args.metadata:
        print(json.dumps({"run_id": run_id, "prompt_sha256": prompt_hash}, sort_keys=True))
    else:
        print(prompt, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
