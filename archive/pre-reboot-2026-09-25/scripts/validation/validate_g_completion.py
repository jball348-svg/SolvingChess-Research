"""Independently validate one G completion object and its repository transaction."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

ORCHESTRATION = Path(__file__).resolve().parents[1] / "orchestration"
if str(ORCHESTRATION) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATION))

from build_g_prompt import (  # noqa: E402
    format_programme,
    next_authorized,
    next_started,
    parse_programme,
    resolve_latest_completed,
    resolve_next_programme,
)
from io_utils import ensure_within, load_json, sha256_file  # noqa: E402

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


ALLOWED_STATUSES = {"PASS", "HOLD", "BLOCKED", "FAILED"}
HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")
MAX_ORDINARY_GIT_FILE_BYTES = 95 * 1024 * 1024
PRIVATE_KEY_RE = re.compile(
    rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----",
    re.IGNORECASE,
)
ASSIGNED_SECRET_RE = re.compile(
    rb"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{12,})"
)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def changed_paths(repo: Path, base_commit: str) -> list[str]:
    changed: set[str] = set()
    for arguments in (
        ("diff", "--name-only", "--diff-filter=ACDMRTUXB", base_commit, "--"),
        ("ls-files", "--others", "--exclude-standard"),
    ):
        completed = _git(repo, *arguments)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "git path inspection failed")
        changed.update(line.strip().replace("\\", "/") for line in completed.stdout.splitlines() if line.strip())
    return sorted(changed)


def _normal(path: str) -> str:
    value = str(PurePosixPath(path.replace("\\", "/")))
    return value.removeprefix("./")


def _protected_reason(path: str, programme: int) -> str | None:
    normalized = _normal(path)
    lowered = normalized.casefold()
    exact = {
        "agents.md",
        "state/artifact_registry.json",
        "state/reference_registry.json",
    }
    if lowered in exact:
        return "controller authority is protected"
    protected_prefixes = (
        "scripts/orchestration/",
        "scripts/validation/",
        "schemas/",
        "docs/",
        "roadmap/",
        "handoffs/",
        "legacy/",
        "references/",
        "logs/orchestration/",
    )
    if lowered.startswith(protected_prefixes):
        return "immutable/controller path is protected"
    match = re.match(r"^research/g(\d+)(?:/|$)", lowered)
    if match and int(match.group(1)) != programme:
        return f"research path belongs to G{int(match.group(1))}, not G{programme}"
    return None


def _schema_errors(instance: Any, schema_path: Path) -> list[str]:
    if not schema_path.is_file():
        return [f"missing completion schema: {schema_path}"]
    if jsonschema is None:
        return ["jsonschema package is unavailable"]
    try:
        schema = load_json(schema_path)
        jsonschema.Draft202012Validator.check_schema(schema)
        return [
            f"completion schema {'/'.join(str(p) for p in error.absolute_path) or '$'}: {error.message}"
            for error in sorted(
                jsonschema.Draft202012Validator(schema).iter_errors(instance),
                key=lambda item: list(item.absolute_path),
            )
        ]
    except Exception as error:  # schema parsing/checking must fail closed
        return [f"cannot validate completion schema: {error}"]


def _find_hash_entries(node: Any) -> Iterable[tuple[str, str]]:
    if isinstance(node, dict):
        path = node.get("path") or node.get("relative_path") or node.get("artifact_path")
        digest = node.get("sha256") or node.get("sha_256") or node.get("hash")
        if isinstance(path, str) and isinstance(digest, str) and HASH_RE.fullmatch(digest):
            yield path, digest.lower()
        for value in node.values():
            yield from _find_hash_entries(value)
    elif isinstance(node, list):
        for value in node:
            yield from _find_hash_entries(value)


def _required_path(
    repo: Path,
    completion: dict[str, Any],
    key: str,
    expected_programme: int,
    errors: list[str],
) -> Path | None:
    value = completion.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"completion field {key} is missing")
        return None
    try:
        absolute = ensure_within(repo, Path(value))
    except ValueError as error:
        errors.append(f"{key}: {error}")
        return None
    if not absolute.is_file():
        errors.append(f"{key} does not exist: {_normal(value)}")
        return None
    if key in {"handoff_path", "freeze_manifest_path"} and format_programme(expected_programme).casefold() not in absolute.name.casefold():
        errors.append(f"{key} filename does not identify {format_programme(expected_programme)}")
    return absolute


def _program_from_completion(value: Any) -> int | None:
    try:
        return parse_programme(value)
    except ValueError:
        return None


def inspect_changed_path_policy(repo: Path, programme: int, base_commit: str) -> dict[str, Any]:
    repo = Path(repo).resolve()
    errors: list[str] = []
    try:
        paths = changed_paths(repo, base_commit)
    except RuntimeError as error:
        return {
            "valid": False,
            "fatal": True,
            "errors": [f"cannot inspect changed paths: {error}"],
            "changed_paths": [],
        }
    for path in paths:
        reason = _protected_reason(path, programme)
        if reason:
            errors.append(f"protected path changed: {path} ({reason})")
        absolute = repo / path
        if absolute.is_file():
            size = absolute.stat().st_size
            if size > MAX_ORDINARY_GIT_FILE_BYTES:
                errors.append(f"changed file exceeds 95 MiB ordinary-Git limit: {path}")
                continue
            if size <= 4 * 1024 * 1024:
                content = absolute.read_bytes()
                if b"\0" not in content:
                    if PRIVATE_KEY_RE.search(content):
                        errors.append(f"possible private key in changed file: {path}")
                    for match in ASSIGNED_SECRET_RE.finditer(content):
                        token = match.group(1).casefold()
                        if not any(
                            marker in token
                            for marker in (b"example", b"redacted", b"changeme", b"not-a-secret")
                        ):
                            errors.append(f"possible assigned credential in changed file: {path}")
                            break
    successor_prefix = f"research/G{programme + 1}/".casefold()
    for path in paths:
        if (_normal(path) + "/").casefold().startswith(successor_prefix):
            errors.append(f"successor path was touched: {path}")
    return {"valid": not errors, "fatal": bool(errors), "errors": errors, "changed_paths": paths}


def validate_g_completion(
    repo: Path,
    expected_programme: int,
    expected_run_id: str,
    base_commit: str,
    before_state: dict[str, Any],
    completion: dict[str, Any],
) -> dict[str, Any]:
    repo = Path(repo).resolve()
    errors: list[str] = []
    errors.extend(_schema_errors(completion, repo / "schemas" / "g_completion.schema.json"))

    if completion.get("run_id") != expected_run_id:
        errors.append("completion run_id does not match the deterministic attempt identity")
    if _program_from_completion(completion.get("programme")) != expected_programme:
        errors.append(f"completion programme is not {format_programme(expected_programme)}")
    status = str(completion.get("status", "")).upper()
    if status not in ALLOWED_STATUSES:
        errors.append(f"invalid completion status: {completion.get('status')!r}")

    handoff = _required_path(repo, completion, "handoff_path", expected_programme, errors)
    manifest_path = _required_path(repo, completion, "freeze_manifest_path", expected_programme, errors)
    state_path = _required_path(repo, completion, "program_state_path", expected_programme, errors)
    expected_state_path = (repo / "state" / "PROGRAM_STATE.json").resolve()
    if state_path is not None and state_path != expected_state_path:
        errors.append("program_state_path must be state/PROGRAM_STATE.json")

    after_state: dict[str, Any] | None = None
    if expected_state_path.is_file():
        try:
            loaded = load_json(expected_state_path)
            if not isinstance(loaded, dict):
                raise ValueError("root must be an object")
            after_state = loaded
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"invalid updated PROGRAM_STATE: {error}")

    before_next = None
    try:
        before_next = resolve_next_programme(before_state)
        if before_next != expected_programme:
            errors.append("pre-run state does not route the expected programme")
    except ValueError as error:
        errors.append(f"invalid pre-run state: {error}")

    if after_state is not None and status in ALLOWED_STATUSES:
        try:
            after_next = resolve_next_programme(after_state)
            after_latest = resolve_latest_completed(after_state)
            if status == "PASS":
                if after_latest != expected_programme:
                    errors.append("PASS did not set latest completed to the current programme")
                if after_next != expected_programme + 1:
                    errors.append("PASS did not advance exactly one sequential programme")
                if next_started(after_state):
                    errors.append("PASS marked the successor started")
                completion_next = _program_from_completion(completion.get("next_programme"))
                if completion_next != expected_programme + 1:
                    errors.append("PASS completion has an invalid successor")
                if bool(completion.get("next_programme_authorized")) != next_authorized(after_state):
                    errors.append("completion successor authorization disagrees with PROGRAM_STATE")
            else:
                if after_next != expected_programme:
                    errors.append(f"{status} must not advance the next programme")
                if resolve_latest_completed(before_state) != after_latest:
                    errors.append(f"{status} must not change latest completed programme")
                if next_authorized(after_state):
                    errors.append(f"{status} must leave the current programme unauthorized")
                if next_started(after_state):
                    errors.append(f"{status} must not leave the current programme started")
                completion_next = _program_from_completion(completion.get("next_programme"))
                if completion_next is not None and completion_next != expected_programme:
                    errors.append(f"{status} completion points past the blocked/current programme")
                if bool(completion.get("next_programme_authorized")) != next_authorized(after_state):
                    errors.append("completion authorization disagrees with PROGRAM_STATE")
        except ValueError as error:
            errors.append(f"invalid updated programme routing: {error}")

    manifest: dict[str, Any] | None = None
    if manifest_path is not None:
        try:
            loaded_manifest = load_json(manifest_path)
            if not isinstance(loaded_manifest, dict):
                raise ValueError("root must be an object")
            manifest = loaded_manifest
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"invalid freeze manifest: {error}")
    if manifest is not None:
        manifest_schema_errors = _schema_errors(manifest, repo / "schemas" / "freeze_manifest.schema.json")
        errors.extend(error.replace("completion schema", "freeze manifest schema") for error in manifest_schema_errors)
        if manifest.get("run_id") != expected_run_id:
            errors.append("freeze manifest run_id does not match the deterministic attempt identity")
        if _program_from_completion(manifest.get("programme")) != expected_programme:
            errors.append(f"freeze manifest programme is not {format_programme(expected_programme)}")
        manifest_status = manifest.get("gate_result", manifest.get("status"))
        if str(manifest_status).upper() != status:
            errors.append("freeze manifest status disagrees with completion status")
        git_record = manifest.get("git")
        if isinstance(git_record, dict):
            expected_tag = f"g{expected_programme}-{'frozen' if status == 'PASS' else status.lower()}"
            if git_record.get("planned_tag") != expected_tag:
                errors.append(f"freeze manifest planned tag is not {expected_tag}")
        for relative, expected_hash in _find_hash_entries(manifest):
            try:
                artifact = ensure_within(repo, Path(relative))
            except ValueError as error:
                errors.append(f"manifest entry {relative!r}: {error}")
                continue
            if not artifact.is_file():
                errors.append(f"manifest artifact missing: {_normal(relative)}")
            elif sha256_file(artifact) != expected_hash:
                errors.append(f"manifest hash mismatch: {_normal(relative)}")

    path_policy = inspect_changed_path_policy(repo, expected_programme, base_commit)
    paths = path_policy["changed_paths"]
    errors.extend(path_policy["errors"])

    # The required closure evidence and state must themselves be part of this transaction.
    path_set = {_normal(path).casefold() for path in paths}
    for required in (handoff, manifest_path, expected_state_path):
        if required is not None:
            relative = required.relative_to(repo).as_posix().casefold()
            if relative not in path_set and required != expected_state_path:
                errors.append(f"required G artifact was not created or changed: {relative}")

    fatal_markers = (
        "protected path changed:",
        "successor path was touched:",
        "changed file exceeds 95 MiB",
        "possible private key",
        "possible assigned credential",
        "pre-run state does not route",
        "invalid pre-run state:",
        "cannot inspect changed paths:",
    )
    if not errors and status in ALLOWED_STATUSES:
        classification = "scientific"
    elif any(error.startswith(fatal_markers) for error in errors):
        classification = "fatal_contradiction"
    else:
        classification = "infrastructure_invalid"
    return {
        "valid": not errors,
        "status": status if status in ALLOWED_STATUSES else "INVALID",
        "classification": classification,
        "errors": errors,
        "changed_paths": paths,
        "programme": format_programme(expected_programme),
        "run_id": expected_run_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--programme", required=True, type=parse_programme)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--before-state", type=Path, required=True)
    parser.add_argument("--completion", type=Path, required=True)
    args = parser.parse_args()
    result = validate_g_completion(
        args.repo,
        args.programme,
        args.run_id,
        args.base_commit,
        load_json(args.before_state),
        load_json(args.completion),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
