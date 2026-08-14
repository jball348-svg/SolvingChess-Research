"""Run one isolated, non-programme Codex CLI capability smoke test."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ORCHESTRATION = Path(__file__).resolve().parents[1] / "orchestration"
import sys

if str(ORCHESTRATION) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATION))

from codex_runtime import (  # noqa: E402
    LEGACY_SECURITY,
    PREFERRED_SECURITY,
    SECURITY_MODES,
    RunFiles,
    establish_controller_handoff,
    probe_cli,
    run_codex,
    windows_sandbox_for,
)
from io_utils import atomic_write_bytes, atomic_write_json, load_json, sha256_file, utc_now  # noqa: E402

try:
    import jsonschema
except ImportError:  # pragma: no cover - reported as a failed smoke prerequisite
    jsonschema = None


MARKER_TEXT = "CODEX_CLI_WORKSPACE_WRITE_OK\n"
NETWORK_URL = "https://example.com"
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_SCHEMA_SOURCE = REPOSITORY_ROOT / "schemas" / "g_completion.output.schema.json"


def _schema() -> dict[str, Any]:
    value = load_json(OUTPUT_SCHEMA_SOURCE)
    if not isinstance(value, dict):
        raise RuntimeError("completion output schema root is not an object")
    return value


def _prompt() -> str:
    return f"""# Isolated Codex CLI infrastructure smoke

This is a synthetic capability check in a disposable directory. Do not inspect parent
directories, Git repositories, project state, or unrelated files.

1. Write `marker.txt` with exactly this single line: `CODEX_CLI_WORKSPACE_WRITE_OK`.
2. Perform an HTTP GET of `{NETWORK_URL}`. Verify status 200 and that the response body
   contains the text `Example Domain`.
3. Write `network_receipt.json` as a JSON object with exactly these fields and values:
   `url` = `{NETWORK_URL}`, `http_status` = 200, `contains_example_domain` = true.
4. Return only the final JSON object required by `output.schema.json`. Use these exact
   synthetic envelope values: schema_version `1.0.0`; run_id `synthetic-cli-smoke`;
   programme `SYNTHETIC`; status and gate_result `PASS`; state_transition from/to
   `SYNTHETIC`; handoff_path `marker.txt`; freeze_manifest_path
   `network_receipt.json`; program_state_path `marker.txt`; one tests_run item with
   command `synthetic-cli-smoke`, exit_code 0, result `PASS`, and a nonempty summary;
   validation_summary result `PASS` with nonempty checks; empty blockers;
   next_programme null; next_programme_authorized false; human_input_required false;
   human_input_reason null; and a nonempty final_summary. Do no other work.
"""


def run_smoke(codex_bin: str | None, timeout: float, security_mode: str) -> dict[str, Any]:
    # Exercise the same in-repository boundary and narrow controller-SID handoff
    # as the real `.run/wt` worktrees. A generic Temp root, or a broad group ACE,
    # does not prove that elevated-sandbox outputs are safely controller-readable.
    smoke_parent = REPOSITORY_ROOT / ".run" / "smoke"
    smoke_parent.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="cli-", dir=smoke_parent))
    initialized = subprocess.run(
        ["git", "init", "-b", "smoke"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if initialized.returncode != 0:
        raise RuntimeError(f"cannot initialize disposable smoke repository: {initialized.stderr.strip()}")
    controller_sid = establish_controller_handoff(root, smoke_parent)
    schema_path = root / "output.schema.json"
    output_schema = _schema()
    atomic_write_bytes(schema_path, OUTPUT_SCHEMA_SOURCE.read_bytes())
    files = RunFiles(
        prompt=str(root / "prompt.md"),
        events=str(root / "events.jsonl"),
        final=str(root / "final.json"),
        stderr=str(root / "stderr.log"),
    )
    cli = probe_cli(codex_bin, security_mode)
    started_at = utc_now()
    run = run_codex(
        cli,
        root,
        _prompt(),
        files,
        schema_path,
        security_mode,
        timeout_seconds=timeout,
        stop_requested=lambda: False,
        environment={"SOLVING_CHESS_SYNTHETIC_SMOKE": "1"},
    )
    completed_at = utc_now()
    errors: list[str] = []
    if run.returncode != 0:
        errors.append(f"Codex exited {run.returncode}")
    if run.timed_out:
        errors.append("Codex smoke timed out")
    if not run.jsonl_valid:
        errors.extend(run.jsonl_errors)
    if run.completion_error:
        errors.append(f"invalid final JSON: {run.completion_error}")
    expected_completion = {
        "schema_version": "1.0.0",
        "run_id": "synthetic-cli-smoke",
        "programme": "SYNTHETIC",
        "status": "PASS",
        "gate_result": "PASS",
        "state_transition": {"from": "SYNTHETIC", "to": "SYNTHETIC"},
        "handoff_path": "marker.txt",
        "freeze_manifest_path": "network_receipt.json",
        "program_state_path": "marker.txt",
        "blockers": [],
        "next_programme": None,
        "next_programme_authorized": False,
        "human_input_required": False,
        "human_input_reason": None,
    }
    if not isinstance(run.completion, dict):
        errors.append("final completion is not an object")
    else:
        if jsonschema is None:
            errors.append("jsonschema package is unavailable for independent final validation")
        else:
            try:
                jsonschema.Draft202012Validator.check_schema(output_schema)
                for error in sorted(
                    jsonschema.Draft202012Validator(output_schema).iter_errors(run.completion),
                    key=lambda item: list(item.absolute_path),
                ):
                    location = "/".join(str(part) for part in error.absolute_path) or "$"
                    errors.append(f"final schema {location}: {error.message}")
            except jsonschema.SchemaError as error:
                errors.append(f"invalid smoke output schema: {error.message}")
        for key, value in expected_completion.items():
            if run.completion.get(key) != value:
                errors.append(f"final field {key} is not {value!r}")
        tests_run = run.completion.get("tests_run")
        if not (
            isinstance(tests_run, list)
            and len(tests_run) == 1
            and isinstance(tests_run[0], dict)
            and tests_run[0].get("command") == "synthetic-cli-smoke"
            and tests_run[0].get("exit_code") == 0
            and tests_run[0].get("result") == "PASS"
            and isinstance(tests_run[0].get("summary"), str)
            and tests_run[0]["summary"].strip()
        ):
            errors.append("final tests_run does not contain the required synthetic check")
        validation_summary = run.completion.get("validation_summary")
        if not (
            isinstance(validation_summary, dict)
            and validation_summary.get("result") == "PASS"
            and isinstance(validation_summary.get("checks"), list)
            and validation_summary["checks"]
            and all(isinstance(item, str) and item.strip() for item in validation_summary["checks"])
        ):
            errors.append("final validation_summary lacks the required synthetic checks")
        if not isinstance(run.completion.get("final_summary"), str) or not run.completion[
            "final_summary"
        ].strip():
            errors.append("final summary is empty")

    marker = root / "marker.txt"
    if not marker.is_file() or marker.read_bytes() != MARKER_TEXT.encode("utf-8"):
        errors.append("workspace marker is missing or has incorrect bytes")
    receipt_path = root / "network_receipt.json"
    try:
        receipt = load_json(receipt_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"network receipt is invalid: {error}")
    else:
        expected_receipt = {
            "url": NETWORK_URL,
            "http_status": 200,
            "contains_example_domain": True,
        }
        if receipt != expected_receipt:
            errors.append("network receipt does not match the required observed result")

    evidence = {}
    for name in (
        "output.schema.json",
        "prompt.md",
        "events.jsonl",
        "final.json",
        "stderr.log",
        "marker.txt",
        "network_receipt.json",
    ):
        path = root / name
        if path.is_file():
            evidence[name] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    result = {
        "schema_version": "1.0",
        "synthetic_only": True,
        "programme_routing_used": False,
        "started_at": started_at,
        "completed_at": completed_at,
        "workspace": str(root),
        "security_mode": security_mode,
        "windows_sandbox": windows_sandbox_for(security_mode),
        "controller_handoff_sid": controller_sid,
        "codex_version": cli.version_output,
        "codex_executable_sha256": cli.executable_sha256,
        "output_schema": {
            "path": "schemas/g_completion.output.schema.json",
            "sha256": sha256_file(OUTPUT_SCHEMA_SOURCE),
        },
        "valid": not errors,
        "errors": errors,
        "process": {
            "returncode": run.returncode,
            "timed_out": run.timed_out,
            "stop_requested": run.stop_requested,
            "duration_seconds": run.duration_seconds,
            "jsonl_valid": run.jsonl_valid,
            "jsonl_errors": list(run.jsonl_errors),
            "completion_error": run.completion_error,
        },
        "evidence": evidence,
    }
    atomic_write_json(root / "smoke_result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", help="explicit Codex executable path")
    parser.add_argument("--timeout", type=float, default=240.0)
    parser.add_argument(
        "--security-mode",
        choices=SECURITY_MODES,
        default=LEGACY_SECURITY,
        help=(
            f"default: {LEGACY_SECURITY}; {PREFERRED_SECURITY} remains available for "
            "hosts where the elevated permission-profile handoff is controller-readable"
        ),
    )
    parser.add_argument(
        "--result-path",
        type=Path,
        help="optional path for the compact, machine-readable smoke result",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    result = run_smoke(args.codex_bin, args.timeout, args.security_mode)
    if args.result_path is not None:
        atomic_write_json(args.result_path.resolve(), result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
