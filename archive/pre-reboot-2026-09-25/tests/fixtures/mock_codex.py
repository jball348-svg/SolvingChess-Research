"""Synthetic Codex CLI used by the autonomous-controller integration tests."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path


HELP = """Usage: codex exec [OPTIONS] [PROMPT]
--json --output-schema <FILE> --output-last-message <FILE> --ephemeral
--strict-config --ignore-user-config --model <MODEL> --cd <DIR> --sandbox <MODE>
--ask-for-approval <POLICY> --color <COLOR> --config <KEY=VALUE>
"""


def option(args: list[str], name: str) -> str:
    try:
        return args[args.index(name) + 1]
    except (ValueError, IndexError) as error:
        raise SystemExit(f"mock missing required option {name}") from error


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def emit(event_type: str, **values: object) -> None:
    print(json.dumps({"type": event_type, **values}, sort_keys=True), flush=True)


def main() -> int:
    args = sys.argv[1:]
    if args == ["--version"]:
        print("codex-cli 0.147.0-alpha.mock")
        return 0
    if args[:2] == ["exec", "--help"]:
        print(HELP)
        return 0
    if not args or args[0] != "exec":
        print("unsupported mock invocation", file=sys.stderr)
        return 64

    repo = Path(option(args, "--cd")).resolve()
    final_path = Path(option(args, "--output-last-message")).resolve()
    prompt = sys.stdin.read()
    run_id = os.environ["SOLVING_CHESS_RUN_ID"]
    programme = os.environ["SOLVING_CHESS_PROGRAMME"]
    attempt = int(os.environ["SOLVING_CHESS_ATTEMPT"])
    scenario = os.environ.get("MOCK_CODEX_SCENARIO", "pass")
    if run_id not in prompt or programme not in prompt:
        print("deterministic prompt identity missing", file=sys.stderr)
        return 31

    emit("thread.started", thread_id=f"mock-{run_id}")
    if scenario == "crash" or (scenario == "retry_then_pass" and attempt == 1):
        print("synthetic subprocess crash", file=sys.stderr)
        return 23

    if scenario == "malformed_json":
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_text("{ definitely not json", encoding="utf-8")
        emit("turn.completed", usage={})
        return 0
    if scenario == "malformed_jsonl":
        print("this is not json", flush=True)

    number_match = re.fullmatch(r"G(\d+)", programme)
    if not number_match:
        return 32
    number = int(number_match.group(1))
    research = repo / "research" / programme
    research.mkdir(parents=True, exist_ok=True)
    handoff = research / f"{programme}_Technical_Handoff.md"
    manifest_path = research / f"{programme}_Freeze_Manifest.json"
    state_path = repo / "state" / "PROGRAM_STATE.json"
    if scenario != "missing_handoff":
        handoff.write_text(
            f"# {programme} synthetic handoff\n\nRun `{run_id}`. Synthetic evidence only.\n",
            encoding="utf-8",
        )

    state = json.loads(state_path.read_text(encoding="utf-8"))
    status = {"blocked": "BLOCKED", "hold": "HOLD", "failed": "FAILED"}.get(scenario, "PASS")
    if status == "PASS":
        state["latest_completed_programme"] = programme
        if scenario == "invalid_transition":
            state["next_programme"]["programme"] = f"G{number + 2}"
        else:
            state["next_programme"]["programme"] = f"G{number + 1}"
        state["next_programme"]["authorized"] = True
        state["next_programme"]["started"] = False
    else:
        state["next_programme"]["authorized"] = False
        state["next_programme"]["started"] = False
    write_json(state_path, state)

    files = []
    if handoff.is_file():
        files.append(
            {
                "path": handoff.relative_to(repo).as_posix(),
                "sha256": hashlib.sha256(handoff.read_bytes()).hexdigest(),
            }
        )
    write_json(
        manifest_path,
        {
            "schema_version": "1.0",
            "programme": programme,
            "run_id": "wrong-run" if scenario == "manifest_mismatch" else run_id,
            "status": "FAILED" if scenario == "manifest_mismatch" else status,
            "files": files,
        },
    )
    next_programme = state["next_programme"]["programme"]
    completion = {
        "run_id": run_id,
        "programme": programme,
        "status": status,
        "gate_result": status,
        "handoff_path": handoff.relative_to(repo).as_posix(),
        "freeze_manifest_path": manifest_path.relative_to(repo).as_posix(),
        "program_state_path": "state/PROGRAM_STATE.json",
        "tests_run": ["synthetic-mock"],
        "validation_summary": "synthetic completion for controller integration testing",
        "blockers": ["synthetic blocker"] if status in {"BLOCKED", "HOLD"} else [],
        "next_programme": next_programme,
        "next_programme_authorized": bool(state["next_programme"]["authorized"]),
        "human_input_required": status in {"BLOCKED", "HOLD"},
        "human_input_reason": "synthetic external action" if status in {"BLOCKED", "HOLD"} else "",
        "final_summary": f"Synthetic {status} for {programme}",
    }
    write_json(final_path, completion)
    emit("item.completed", item={"type": "agent_message", "text": json.dumps(completion)})
    emit("turn.completed", usage={"input_tokens": 1, "output_tokens": 1})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
