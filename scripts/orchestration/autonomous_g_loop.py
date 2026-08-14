"""Restartable one-fresh-Codex-process-per-G autonomous Solving Chess controller."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
VALIDATION_DIR = HERE.parent / "validation"
for module_dir in (HERE, VALIDATION_DIR):
    if str(module_dir) not in sys.path:
        sys.path.insert(0, str(module_dir))

from build_g_prompt import (  # noqa: E402
    build_prompt,
    format_programme,
    next_authorized,
    next_started,
    parse_programme,
    resolve_next_programme,
)
from codex_runtime import (  # noqa: E402
    LEGACY_SECURITY,
    PREFERRED_SECURITY,
    SECURITY_MODES,
    RunFiles,
    establish_controller_handoff,
    probe_cli,
    run_codex,
    terminate_process_identity,
    windows_sandbox_for,
)
from git_freeze import (  # noqa: E402
    GitError,
    Worktree,
    create_isolated_worktree,
    freeze_and_publish,
    head,
    load_worktree,
    runtime_dir,
)
from io_utils import (  # noqa: E402
    ExclusiveFileLock,
    LockUnavailable,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    sha256_file,
    utc_now,
)
from validate_g_completion import inspect_changed_path_policy, validate_g_completion  # noqa: E402
from validate_repository import validate_repository  # noqa: E402


LEDGER_NAME = "controller.json"
STOP_AFTER_NAME = "stop-after-current.json"
STOP_NOW_NAME = "stop-now.json"


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def _nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return parsed


def _positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    modes = result.add_mutually_exclusive_group()
    modes.add_argument("--start", action="store_true", help="start a new isolated controller run")
    modes.add_argument("--resume", action="store_true", help="resume the saved isolated worktree")
    modes.add_argument("--status", action="store_true", help="print the durable controller ledger")
    modes.add_argument("--validate-only", action="store_true", help="validate the current repository only")
    modes.add_argument("--request-stop", action="store_true", help="stop after the current G attempt")
    modes.add_argument("--stop-now", action="store_true", help="terminate the active Codex process tree")
    result.add_argument("--until", type=parse_programme, help="execute through this G, then stop")
    result.add_argument("--max-programmes", type=_positive_int, help="optional accepted-programme cap")
    result.add_argument("--max-retries", type=_nonnegative_int, default=2)
    result.add_argument("--max-runtime", type=_positive_float, help="optional wall-clock cap in seconds")
    result.add_argument("--dry-run", action="store_true", help="preflight and render metadata without mutation")
    result.add_argument("--codex-bin", help="path to codex executable (or a Python mock in tests)")
    result.add_argument(
        "--security-mode",
        choices=SECURITY_MODES,
        default=PREFERRED_SECURITY,
        help=(
            f"default: {PREFERRED_SECURITY}; {LEGACY_SECURITY} is an explicit "
            "compatibility fallback"
        ),
    )
    return result


def _paths(repo: Path) -> tuple[Path, Path, Path, Path]:
    base = runtime_dir(repo)
    return base, base / LEDGER_NAME, base / STOP_AFTER_NAME, base / STOP_NOW_NAME


def _request(repo: Path, immediate: bool) -> int:
    base, _, after, now = _paths(repo)
    base.mkdir(parents=True, exist_ok=True)
    marker = now if immediate else after
    atomic_write_json(
        marker,
        {"requested_at": utc_now(), "pid": os.getpid(), "mode": "immediate" if immediate else "after-current"},
    )
    _print({"accepted": True, "request": "stop-now" if immediate else "stop-after-current", "path": str(marker)})
    return 0


def _status(repo: Path) -> int:
    try:
        _, ledger_path, after, now = _paths(repo)
    except GitError as error:
        _print({"state": "UNAVAILABLE", "error": str(error)})
        return 1
    if not ledger_path.is_file():
        _print({"state": "IDLE", "repository": str(repo), "ledger": str(ledger_path)})
        return 0
    try:
        value = load_json(ledger_path)
    except Exception as error:
        _print({"state": "INVALID_LEDGER", "error": str(error), "ledger": str(ledger_path)})
        return 1
    value["stop_after_current_requested"] = after.exists()
    value["stop_now_requested"] = now.exists()
    _print(value)
    return 0


def _update(ledger_path: Path, ledger: dict[str, Any], **changes: Any) -> None:
    ledger.update(changes)
    ledger["updated_at"] = utc_now()
    atomic_write_json(ledger_path, ledger)


def _live_start_readiness(repo: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        programme_state = load_json(repo / "state" / "PROGRAM_STATE.json")
        bootstrap = programme_state.get("repository_bootstrap")
        if not isinstance(bootstrap, dict):
            errors.append("PROGRAM_STATE.repository_bootstrap is missing")
        else:
            if bootstrap.get("completion_status") != "COMPLETE":
                errors.append("repository bootstrap is not COMPLETE")
            if bootstrap.get("autonomous_loop_readiness") != "READY":
                errors.append("autonomous loop readiness is not READY")
            if bootstrap.get("real_loop_running") is not False:
                errors.append("PROGRAM_STATE says the real loop is already running")
    except Exception as error:
        errors.append(f"cannot read PROGRAM_STATE readiness: {error}")
    try:
        autonomy = load_json(repo / "state" / "AUTONOMY_STATE.json")
        if autonomy.get("orchestrator_state") != "STOPPED":
            errors.append("AUTONOMY_STATE is not STOPPED")
        if autonomy.get("real_research_loop_started") is not False:
            errors.append("AUTONOMY_STATE says the real research loop is already started")
    except Exception as error:
        errors.append(f"cannot read AUTONOMY_STATE readiness: {error}")
    return {"ready": not errors, "errors": errors}


def _resume_consistency(ledger: dict[str, Any], worktree: Worktree) -> list[str]:
    errors: list[str] = []
    ledger_state = ledger.get("state")
    active_states = {
        "STARTING",
        "RUNNING",
        "RUNNING_ATTEMPT",
        "RETRYING",
        "PASS",
        "PUBLISH_PENDING",
    }
    if ledger_state not in active_states:
        errors.append(f"ledger state {ledger_state!r} is not resumable")
    try:
        autonomy = load_json(Path(worktree.path) / "state" / "AUTONOMY_STATE.json")
        autonomy_state = autonomy.get("orchestrator_state")
        real_started = autonomy.get("real_research_loop_started")
        active_pair = autonomy_state in {"RUNNING", "RECOVERING"} and real_started is True
        checkpoint_pair = (
            ledger_state
            in {"STARTING", "PASS", "RETRYING", "RUNNING", "RUNNING_ATTEMPT", "PUBLISH_PENDING"}
            and autonomy_state == "STOPPED"
            and real_started is False
        )
        if not (active_pair or checkpoint_pair):
            errors.append(
                "ledger and isolated AUTONOMY_STATE are not a consistent active/recovery checkpoint"
            )
    except Exception as error:
        errors.append(f"cannot validate isolated AUTONOMY_STATE: {error}")
    return errors


def _set_autonomy_running(
    repo: Path,
    args: argparse.Namespace,
    cli: Any,
    run_id: str,
    programme: int,
    attempt: int,
    prompt_hash: str,
    base_commit: str,
    started_at: str,
) -> str:
    path = repo / "state" / "AUTONOMY_STATE.json"
    value = load_json(path)
    value.update(
        {
            "orchestrator_state": "RUNNING",
            "updated_at": utc_now(),
            "current_run": {
                "run_id": run_id,
                "programme": format_programme(programme),
                "process_attempt": attempt,
                "started_at": started_at,
                "ended_at": None,
                "prompt_sha256": prompt_hash,
                "result_sha256": None,
                "git_commit_before": base_commit,
                "git_commit_after": None,
            },
            "codex": {
                "version": cli.version_output,
                "executable_sha256": cli.executable_sha256,
                "sandbox": (
                    f"permission-profile:workspace-only; windows-{windows_sandbox_for(args.security_mode)}"
                )
                if args.security_mode == PREFERRED_SECURITY
                else f"workspace-write; windows-{windows_sandbox_for(args.security_mode)}",
                "approval_policy": "on-request+auto-review"
                if args.security_mode == PREFERRED_SECURITY
                else "never",
                "network": "CONTROLLED" if args.security_mode == PREFERRED_SECURITY else "ENABLED",
            },
            "retry_count": attempt - 1,
            "guardrails": {
                "max_retries": args.max_retries,
                "max_programmes": args.max_programmes,
                "until_programme": format_programme(args.until) if args.until is not None else None,
                "runtime_budget_seconds": args.max_runtime,
            },
            "validation_result": "NOT_RUN",
            "exit_status": None,
            "stop_reason": "NONE",
            "real_research_loop_started": True,
        }
    )
    atomic_write_json(path, value)
    return sha256_file(path)


def _set_autonomy_stopped(
    repo: Path,
    status: str,
    run_result_sha256: str,
    exit_status: int,
) -> None:
    path = repo / "state" / "AUTONOMY_STATE.json"
    value = load_json(path)
    current = value.get("current_run")
    if isinstance(current, dict):
        current["ended_at"] = utc_now()
        current["result_sha256"] = run_result_sha256
        current["git_commit_after"] = None
    stop_reason = {
        "PASS": "NONE",
        "HOLD": "VALIDATED_HOLD",
        "BLOCKED": "VALIDATED_BLOCKED",
        "FAILED": "VALIDATED_FAILED",
    }[status]
    value.update(
        {
            "orchestrator_state": "STOPPED",
            "updated_at": utc_now(),
            # Completed-run details are frozen in the accepted evidence and the
            # controller ledger. The state schema intentionally requires no active
            # current_run while STOPPED.
            "current_run": None,
            "validation_result": "PASS",
            "exit_status": exit_status,
            "stop_reason": stop_reason,
            "real_research_loop_started": False,
        }
    )
    atomic_write_json(path, value)


def _looks_like_security_startup_failure(stderr_path: Path) -> bool:
    try:
        content = stderr_path.read_bytes()[:1024 * 1024].lower()
    except OSError:
        return False
    markers = (b"strict config", b"configuration", b"permission profile", b"sandbox", b"approval")
    return any(marker in content for marker in markers)


def _archive_isolated_attempt(worktree: Worktree, commit: str, run_id: str) -> dict[str, Any]:
    """Stash a rejected attempt so retries are clean without destroying audit evidence."""

    path = Path(worktree.path).resolve()
    expected_parent = Path(worktree.source_repo).resolve() / ".run" / "wt"
    try:
        path.relative_to(expected_parent.resolve())
    except ValueError as error:
        raise GitError(f"refusing recovery outside the controller worktree root: {path}") from error
    if head(path) != commit:
        raise GitError("refusing to archive an attempt after Git history changed")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if status.returncode != 0:
        raise GitError(f"cannot inspect rejected attempt: {status.stderr.strip()}")
    if not status.stdout.strip():
        return {"run_id": run_id, "stash_commit": None, "reason": "no changed files"}
    message = f"solving-chess rejected attempt {run_id}"
    archived = subprocess.run(
        ["git", "stash", "push", "--all", "--message", message],
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if archived.returncode != 0:
        raise GitError(f"cannot archive rejected attempt: {archived.stderr.strip()}")
    stash = subprocess.run(
        ["git", "rev-parse", "refs/stash"],
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if stash.returncode != 0 or not stash.stdout.strip():
        raise GitError("rejected attempt was not recoverably recorded in refs/stash")
    if head(path) != commit:
        raise GitError("archiving a rejected attempt unexpectedly changed HEAD")
    remaining = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if remaining.returncode != 0 or remaining.stdout.strip():
        raise GitError("rejected attempt archive did not leave a clean retry worktree")
    return {
        "run_id": run_id,
        "stash_commit": stash.stdout.strip(),
        "message": message,
        "archived_at": utc_now(),
    }


def _copy_accepted_evidence(
    repo: Path,
    programme: int,
    run_id: str,
    run_dir: Path,
    files: RunFiles,
) -> dict[str, Any]:
    """Copy the compact accepted controller evidence into the frozen transaction."""

    destination = repo / "logs" / "orchestration" / format_programme(programme) / run_id
    sources = {
        "prompt.md": Path(files.prompt),
        "final.json": Path(files.final),
        "metadata.json": run_dir / "metadata.json",
        "process_result.json": run_dir / "process_result.json",
        "validation.json": run_dir / "validation.json",
    }
    copied: list[dict[str, str]] = []
    for name, source in sources.items():
        if not source.is_file():
            raise RuntimeError(f"accepted evidence source is missing: {source}")
        target = destination / name
        source_bytes = source.read_bytes()
        if target.is_file():
            if target.read_bytes() != source_bytes:
                raise RuntimeError(f"accepted evidence collision has different bytes: {target}")
        else:
            atomic_write_bytes(target, source_bytes)
        copied.append({"path": target.relative_to(repo).as_posix(), "sha256": sha256_file(target)})
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "programme": format_programme(programme),
        "files": copied,
    }
    atomic_write_json(destination / "evidence_manifest.json", manifest)
    return {
        "directory": destination.relative_to(repo).as_posix(),
        "manifest_sha256": sha256_file(destination / "evidence_manifest.json"),
    }


def _stop_reason_for_boundary(
    programme: int,
    accepted_count: int,
    args: argparse.Namespace,
    started_monotonic: float,
    stop_after: Path,
) -> str | None:
    if args.until is not None and programme >= args.until:
        return f"configured maximum programme {format_programme(args.until)} reached"
    if args.max_programmes is not None and accepted_count >= args.max_programmes:
        return f"configured maximum count {args.max_programmes} reached"
    if args.max_runtime is not None and time.monotonic() - started_monotonic >= args.max_runtime:
        return "configured maximum runtime reached"
    if stop_after.exists():
        return "operator requested stop after current programme"
    return None


def _preflight_dry_run(repo: Path, args: argparse.Namespace) -> int:
    readiness = _live_start_readiness(repo)
    if not readiness["ready"]:
        _print({"dry_run": True, "valid": False, "live_start_readiness": readiness})
        return 1
    validation = validate_repository(repo, require_clean=True)
    if not validation["valid"]:
        _print({"dry_run": True, "validation": validation})
        return 1
    try:
        cli = probe_cli(args.codex_bin, args.security_mode)
        programme = parse_programme(validation["next_programme"])
        prompt, run_id, prompt_hash = build_prompt(repo, programme, 1, head(repo))
    except Exception as error:
        _print({"dry_run": True, "valid": False, "error": str(error)})
        return 1
    _print(
        {
            "dry_run": True,
            "valid": True,
            "programme": format_programme(programme),
            "run_id": run_id,
            "prompt_sha256": prompt_hash,
            "prompt_bytes": len(prompt.encode("utf-8")),
            "codex_version": cli.version_output,
            "codex_command": cli.display_command(),
            "security_mode": args.security_mode,
            "windows_sandbox": windows_sandbox_for(args.security_mode),
            "mutation_performed": False,
        }
    )
    return 0


def _run_loop(source_repo: Path, args: argparse.Namespace) -> int:
    base_dir, ledger_path, stop_after, stop_now = _paths(source_repo)
    base_dir.mkdir(parents=True, exist_ok=True)
    with ExclusiveFileLock(base_dir / "controller.lock"):
        pending_publish: dict[str, Any] | None = None
        if args.start:
            readiness = _live_start_readiness(source_repo)
            if not readiness["ready"]:
                _print({"valid": False, "live_start_readiness": readiness})
                return 1
            validation = validate_repository(source_repo, require_clean=True)
            if not validation["valid"]:
                _print(validation)
                return 1
            programme = parse_programme(validation["next_programme"])
            worktree = create_isolated_worktree(source_repo, programme)
            controller_handoff_sid = establish_controller_handoff(
                Path(worktree.path), source_repo / ".run" / "wt"
            )
            ledger: dict[str, Any] = {
                "schema_version": "1.0",
                "state": "STARTING",
                "source_repository": str(source_repo),
                "worktree": worktree.as_dict(),
                "started_at": utc_now(),
                "started_epoch": time.time(),
                "accepted_programmes": 0,
                "retry_count": 0,
                "security_mode": args.security_mode,
                "windows_sandbox": windows_sandbox_for(args.security_mode),
                "controller_handoff_sid": controller_handoff_sid,
                "codex_bin": args.codex_bin,
                "guardrails": {
                    "max_retries": args.max_retries,
                    "max_programmes": args.max_programmes,
                    "until": format_programme(args.until) if args.until is not None else None,
                    "max_runtime": args.max_runtime,
                },
            }
            resume_programme = None
            first_attempt = 1
            # Persist the worktree identity before probing external executables so
            # even a startup failure has a resumable controller checkpoint.
            atomic_write_json(ledger_path, ledger)
        else:
            if not ledger_path.is_file():
                raise RuntimeError("there is no durable controller ledger to resume")
            ledger = load_json(ledger_path)
            if not isinstance(ledger, dict) or not isinstance(ledger.get("worktree"), dict):
                raise RuntimeError("durable controller ledger is invalid")
            worktree = load_worktree(ledger["worktree"])
            if Path(worktree.source_repo).resolve() != source_repo:
                raise RuntimeError("saved controller belongs to another source repository")
            controller_handoff_sid = establish_controller_handoff(
                Path(worktree.path), source_repo / ".run" / "wt"
            )
            saved_controller_sid = ledger.get("controller_handoff_sid")
            if saved_controller_sid and saved_controller_sid != controller_handoff_sid:
                raise RuntimeError("resume controller identity differs from the saved run")
            ledger["controller_handoff_sid"] = controller_handoff_sid
            resume_errors = _resume_consistency(ledger, worktree)
            if resume_errors:
                raise RuntimeError("resume validation failed: " + "; ".join(resume_errors))
            saved_guardrails = ledger.get("guardrails") if isinstance(ledger.get("guardrails"), dict) else {}
            if args.max_retries == 2 and saved_guardrails.get("max_retries") is not None:
                args.max_retries = int(saved_guardrails["max_retries"])
            if args.max_programmes is None and saved_guardrails.get("max_programmes") is not None:
                args.max_programmes = int(saved_guardrails["max_programmes"])
            if args.until is None and saved_guardrails.get("until") is not None:
                args.until = parse_programme(saved_guardrails["until"])
            if args.max_runtime is None and saved_guardrails.get("max_runtime") is not None:
                args.max_runtime = float(saved_guardrails["max_runtime"])
            if args.codex_bin is None:
                args.codex_bin = ledger.get("codex_bin")
            saved_security = ledger.get("security_mode")
            if saved_security and args.security_mode != saved_security:
                raise RuntimeError(
                    "resume security mode differs from the saved run; pass the original --security-mode"
                )
            saved_windows_sandbox = ledger.get("windows_sandbox")
            if saved_windows_sandbox and saved_windows_sandbox != windows_sandbox_for(
                args.security_mode
            ):
                raise RuntimeError(
                    "resume Windows sandbox differs from the saved run; start a fresh controller run"
                )
            pid = ledger.get("process_pid")
            create_time = ledger.get("process_create_time")
            if isinstance(pid, int) and isinstance(create_time, (int, float)):
                cleaned = terminate_process_identity(pid, float(create_time))
                ledger["stale_process_tree_cleaned"] = cleaned
                ledger["process_pid"] = None
                ledger["process_create_time"] = None
            resume_programme = None
            first_attempt = 1
            if ledger.get("state") == "PUBLISH_PENDING":
                candidate = ledger.get("pending_publish")
                if not isinstance(candidate, dict):
                    raise RuntimeError("pending publication ledger record is missing")
                required = ("programme", "status", "run_id", "base_commit")
                if any(not isinstance(candidate.get(key), str) or not candidate[key] for key in required):
                    raise RuntimeError("pending publication ledger record is invalid")
                pending_publish = candidate
            elif ledger.get("state") in {"RUNNING_ATTEMPT", "RETRYING"}:
                resume_programme = parse_programme(ledger.get("active_programme"))
                base_commit = str(ledger.get("git_commit_before", ""))
                run_id = str(ledger.get("current_run_id") or "")
                raw_run_dir = ledger.get("log_directory")
                accepted_checkpoint = False
                if isinstance(raw_run_dir, str):
                    run_dir = Path(raw_run_dir).resolve()
                    try:
                        run_dir.relative_to((base_dir / "runs").resolve())
                    except ValueError:
                        raise RuntimeError("saved run directory escapes the controller ledger root")
                    validation_path = run_dir / "validation.json"
                    process_path = run_dir / "process_result.json"
                    if validation_path.is_file() and process_path.is_file():
                        validation_result = load_json(validation_path)
                        process_result = load_json(process_path)
                        accepted_checkpoint = bool(
                            isinstance(validation_result, dict)
                            and validation_result.get("valid") is True
                            and validation_result.get("run_id") == run_id
                            and parse_programme(validation_result.get("programme")) == resume_programme
                            and isinstance(process_result, dict)
                            and process_result.get("returncode") == 0
                            and process_result.get("jsonl_valid") is True
                            and process_result.get("completion_error") is None
                        )
                if accepted_checkpoint:
                    status = str(validation_result.get("status"))
                    if status not in {"PASS", "HOLD", "BLOCKED", "FAILED"}:
                        raise RuntimeError("accepted recovery checkpoint has an invalid status")
                    files = RunFiles(
                        prompt=str(run_dir / "prompt.md"),
                        events=str(run_dir / "events.jsonl"),
                        final=str(run_dir / "final.json"),
                        stderr=str(run_dir / "stderr.log"),
                    )
                    final_hash = sha256_file(Path(files.final))
                    accepted_evidence = _copy_accepted_evidence(
                        Path(worktree.path),
                        resume_programme,
                        run_id,
                        run_dir,
                        files,
                    )
                    if head(Path(worktree.path)) == base_commit:
                        _set_autonomy_stopped(Path(worktree.path), status, final_hash, 0)
                    else:
                        autonomy = load_json(Path(worktree.path) / "state" / "AUTONOMY_STATE.json")
                        if not (
                            autonomy.get("orchestrator_state") == "STOPPED"
                            and autonomy.get("real_research_loop_started") is False
                        ):
                            raise RuntimeError(
                                "pending controller commit has inconsistent AUTONOMY_STATE; audit preserved"
                            )
                    pending_publish = {
                        "programme": format_programme(resume_programme),
                        "status": status,
                        "run_id": run_id,
                        "base_commit": base_commit,
                        "validation": validation_result,
                        "result_sha256": final_hash,
                        "accepted_evidence": accepted_evidence,
                    }
                    ledger["state"] = "PUBLISH_PENDING"
                    ledger["pending_publish"] = pending_publish
                else:
                    if head(Path(worktree.path)) != base_commit:
                        raise RuntimeError("interrupted agent changed Git history; audit worktree preserved")
                    policy = inspect_changed_path_policy(Path(worktree.path), resume_programme, base_commit)
                    if not policy["valid"]:
                        raise RuntimeError(
                            "interrupted worktree violates fatal path/security policy; audit preserved: "
                            + "; ".join(policy["errors"])
                        )
                    archive = _archive_isolated_attempt(
                        worktree,
                        base_commit,
                        run_id or f"interrupted-{resume_programme}",
                    )
                    archives = list(ledger.get("archived_attempts", []))
                    archives.append(archive)
                    ledger["archived_attempts"] = archives
                    first_attempt = int(ledger.get("process_attempt", 0)) + 1
                    ledger["state"] = "RETRYING"
            ledger["resumed_at"] = utc_now()
        if args.start:
            stop_after.unlink(missing_ok=True)
            stop_now.unlink(missing_ok=True)
        atomic_write_json(ledger_path, ledger)

        if pending_publish is not None:
            programme = parse_programme(pending_publish["programme"])
            status = str(pending_publish["status"])
            try:
                freeze = freeze_and_publish(
                    worktree,
                    programme,
                    status,
                    str(pending_publish["run_id"]),
                    str(pending_publish["base_commit"]),
                )
            except GitError as error:
                _update(
                    ledger_path,
                    ledger,
                    state="PUBLISH_PENDING",
                    stop_reason=f"pending Git publication retry failed: {error}",
                    ended_at=utc_now(),
                    audit_worktree_preserved=True,
                    remote_verified=False,
                )
                return 3
            _update(
                ledger_path,
                ledger,
                state="STOPPED",
                last_status=status,
                last_completed_run_id=pending_publish["run_id"],
                active_programme=None,
                accepted_programmes=int(ledger.get("accepted_programmes", 0)) + 1,
                validation=pending_publish.get("validation"),
                git_commit_after=freeze["metadata_commit"],
                git_content_commit=freeze["content_commit"],
                git_metadata_commit=freeze["metadata_commit"],
                git_tag=freeze["tag"],
                git_branch=freeze["branch"],
                remote_verified=True,
                result_sha256=pending_publish.get("result_sha256"),
                accepted_evidence=pending_publish.get("accepted_evidence"),
                pending_publish=None,
                stop_reason="recovered pending publication; stopped at a durable programme boundary",
                ended_at=utc_now(),
            )
            return 0

        cli = probe_cli(args.codex_bin, args.security_mode)
        _update(
            ledger_path,
            ledger,
            state="RUNNING",
            codex_version=cli.version_output,
            codex_command=cli.display_command(),
            codex_executable_sha256=cli.executable_sha256,
            security_mode=args.security_mode,
            windows_sandbox=windows_sandbox_for(args.security_mode),
        )
        print(
            f"Codex {cli.version_output}; security={args.security_mode}; "
            f"windows-sandbox={windows_sandbox_for(args.security_mode)}; "
            f"worktree={worktree.path}",
            flush=True,
        )
        elapsed_before_resume = max(0.0, time.time() - float(ledger.get("started_epoch", time.time())))
        started_monotonic = time.monotonic() - elapsed_before_resume
        accepted_count = int(ledger.get("accepted_programmes", 0))

        while True:
            repo = Path(worktree.path)
            repository_check = validate_repository(repo, require_clean=True)
            if not repository_check["valid"]:
                _update(
                    ledger_path,
                    ledger,
                    state="STOPPED",
                    stop_reason="repository validation failed before launch",
                    validation=repository_check,
                    ended_at=utc_now(),
                )
                return 2
            programme = parse_programme(repository_check["next_programme"])
            if resume_programme is not None and programme != resume_programme:
                _update(
                    ledger_path,
                    ledger,
                    state="STOPPED",
                    stop_reason="resume programme contradicts repository routing",
                    ended_at=utc_now(),
                    audit_worktree_preserved=True,
                )
                return 3
            if args.until is not None and programme > args.until:
                _update(
                    ledger_path,
                    ledger,
                    state="STOPPED",
                    stop_reason=f"next programme exceeds {format_programme(args.until)}",
                    ended_at=utc_now(),
                )
                return 0

            accepted = False
            attempt_start = first_attempt if resume_programme == programme else 1
            if attempt_start > args.max_retries + 1:
                _update(
                    ledger_path,
                    ledger,
                    state="STOPPED",
                    stop_reason="same-G retry limit was exhausted before resume",
                    ended_at=utc_now(),
                )
                return 2
            for attempt in range(attempt_start, args.max_retries + 2):
                base_commit = head(repo)
                before_state = load_json(repo / "state" / "PROGRAM_STATE.json")
                prompt, run_id, prompt_hash = build_prompt(repo, programme, attempt, base_commit)
                run_dir = base_dir / "runs" / format_programme(programme) / run_id
                files = RunFiles(
                    prompt=str(run_dir / "prompt.md"),
                    events=str(run_dir / "events.jsonl"),
                    final=str(run_dir / "final.json"),
                    stderr=str(run_dir / "stderr.log"),
                )
                remaining = None
                if args.max_runtime is not None:
                    remaining = args.max_runtime - (time.monotonic() - started_monotonic)
                    if remaining <= 0:
                        _update(
                            ledger_path,
                            ledger,
                            state="STOPPED",
                            stop_reason="configured maximum runtime reached",
                            ended_at=utc_now(),
                        )
                        return 0
                metadata = {
                    "run_id": run_id,
                    "programme": format_programme(programme),
                    "attempt": attempt,
                    "base_commit": base_commit,
                    "prompt_sha256": prompt_hash,
                    "started_at": utc_now(),
                    "security_mode": args.security_mode,
                    "windows_sandbox": windows_sandbox_for(args.security_mode),
                    "controller_handoff_sid": ledger.get("controller_handoff_sid"),
                    "codex_version": cli.version_output,
                    "codex_executable_sha256": cli.executable_sha256,
                }
                atomic_write_json(run_dir / "metadata.json", metadata)
                autonomy_hash = _set_autonomy_running(
                    repo,
                    args,
                    cli,
                    run_id,
                    programme,
                    attempt,
                    prompt_hash,
                    base_commit,
                    metadata["started_at"],
                )
                _update(
                    ledger_path,
                    ledger,
                    state="RUNNING_ATTEMPT",
                    current_run_id=run_id,
                    active_programme=format_programme(programme),
                    process_attempt=attempt,
                    retry_count=attempt - 1,
                    git_commit_before=base_commit,
                    prompt_sha256=prompt_hash,
                    log_directory=str(run_dir),
                )
                run = run_codex(
                    cli,
                    repo,
                    prompt,
                    files,
                    repo / "schemas" / "g_completion.output.schema.json",
                    args.security_mode,
                    timeout_seconds=remaining,
                    stop_requested=stop_now.exists,
                    environment={
                        "SOLVING_CHESS_ATTEMPT": str(attempt),
                        "SOLVING_CHESS_PROGRAMME": format_programme(programme),
                        "SOLVING_CHESS_RUN_ID": run_id,
                    },
                    on_start=lambda pid, created: _update(
                        ledger_path,
                        ledger,
                        process_pid=pid,
                        process_create_time=created,
                    ),
                )
                _update(ledger_path, ledger, process_pid=None, process_create_time=None)
                atomic_write_json(run_dir / "process_result.json", run.as_dict())

                invalid_reason: str | None = None
                fatal_invalidity = False
                validation_result: dict[str, Any] | None = None
                if head(repo) != base_commit:
                    invalid_reason = "Codex changed Git history; agent Git operations are forbidden"
                    fatal_invalidity = True
                elif sha256_file(repo / "state" / "AUTONOMY_STATE.json") != autonomy_hash:
                    invalid_reason = "Codex changed controller-owned AUTONOMY_STATE"
                    fatal_invalidity = True
                elif run.stop_requested:
                    invalid_reason = "operator requested immediate stop"
                elif run.timed_out:
                    invalid_reason = "Codex attempt exceeded runtime limit"
                elif run.returncode != 0:
                    invalid_reason = f"Codex process exited {run.returncode}"
                    fatal_invalidity = _looks_like_security_startup_failure(Path(files.stderr))
                elif not run.jsonl_valid:
                    invalid_reason = "Codex JSONL event stream is invalid"
                elif run.completion is None:
                    invalid_reason = f"Codex final output is invalid: {run.completion_error}"
                else:
                    completion_copy = repo / "research" / format_programme(programme) / f"{format_programme(programme)}_Completion.json"
                    atomic_write_json(completion_copy, run.completion)
                    validation_result = validate_g_completion(
                        repo,
                        programme,
                        run_id,
                        base_commit,
                        before_state,
                        run.completion,
                    )
                    atomic_write_json(run_dir / "validation.json", validation_result)
                    if not validation_result["valid"]:
                        invalid_reason = "independent G completion validation failed"
                        fatal_invalidity = validation_result.get("classification") == "fatal_contradiction"

                if invalid_reason is not None:
                    errors = [] if validation_result is None else validation_result.get("errors", [])
                    _update(
                        ledger_path,
                        ledger,
                        state="RETRYING"
                        if attempt <= args.max_retries and not run.stop_requested and not fatal_invalidity
                        else "STOPPED",
                        validation=validation_result,
                        last_invalid_reason=invalid_reason,
                        validation_errors=errors,
                        process_result=run.as_dict(),
                    )
                    if fatal_invalidity:
                        _update(
                            ledger_path,
                            ledger,
                            state="STOPPED",
                            stop_reason=f"fatal contradiction/security failure: {invalid_reason}",
                            ended_at=utc_now(),
                            audit_worktree_preserved=True,
                        )
                        return 3
                    archive = _archive_isolated_attempt(worktree, base_commit, run_id)
                    archives = list(ledger.get("archived_attempts", []))
                    archives.append(archive)
                    _update(ledger_path, ledger, archived_attempts=archives)
                    if run.stop_requested:
                        _update(ledger_path, ledger, stop_reason=invalid_reason, ended_at=utc_now())
                        return 130
                    if attempt <= args.max_retries:
                        continue
                    _update(
                        ledger_path,
                        ledger,
                        state="STOPPED",
                        stop_reason=f"same-G retry limit exhausted: {invalid_reason}",
                        ended_at=utc_now(),
                    )
                    return 2

                assert validation_result is not None and run.completion is not None
                status = validation_result["status"]
                final_hash = sha256_file(Path(files.final))
                accepted_evidence = _copy_accepted_evidence(
                    repo,
                    programme,
                    run_id,
                    run_dir,
                    files,
                )
                _set_autonomy_stopped(repo, status, final_hash, 0)
                try:
                    freeze = freeze_and_publish(worktree, programme, status, run_id, base_commit)
                except GitError as error:
                    pending = {
                        "programme": format_programme(programme),
                        "status": status,
                        "run_id": run_id,
                        "base_commit": base_commit,
                        "validation": validation_result,
                        "result_sha256": final_hash,
                        "accepted_evidence": accepted_evidence,
                    }
                    _update(
                        ledger_path,
                        ledger,
                        state="PUBLISH_PENDING",
                        stop_reason=f"Git freeze/publish transaction failed: {error}",
                        ended_at=utc_now(),
                        audit_worktree_preserved=True,
                        remote_verified=False,
                        pending_publish=pending,
                    )
                    return 3
                accepted_count += 1
                accepted = True
                _update(
                    ledger_path,
                    ledger,
                    state=status,
                    last_status=status,
                    last_completed_run_id=run_id,
                    active_programme=None,
                    accepted_programmes=int(ledger.get("accepted_programmes", 0)) + 1,
                    validation=validation_result,
                    git_commit_after=freeze["metadata_commit"],
                    git_content_commit=freeze["content_commit"],
                    git_metadata_commit=freeze["metadata_commit"],
                    git_tag=freeze["tag"],
                    git_branch=freeze["branch"],
                    remote_verified=True,
                    result_sha256=final_hash,
                    accepted_evidence=accepted_evidence,
                    pending_publish=None,
                )
                if status != "PASS":
                    _update(
                        ledger_path,
                        ledger,
                        state="STOPPED",
                        stop_reason=f"validated scientific status {status}",
                        ended_at=utc_now(),
                    )
                    return 0

                boundary = _stop_reason_for_boundary(programme, accepted_count, args, started_monotonic, stop_after)
                if boundary:
                    _update(ledger_path, ledger, state="STOPPED", stop_reason=boundary, ended_at=utc_now())
                    return 0
                after_state = load_json(repo / "state" / "PROGRAM_STATE.json")
                successor = resolve_next_programme(after_state)
                if successor != programme + 1:
                    _update(
                        ledger_path,
                        ledger,
                        state="STOPPED",
                        stop_reason="accepted repository no longer routes a sequential successor",
                        ended_at=utc_now(),
                    )
                    return 2
                if not next_authorized(after_state) or next_started(after_state):
                    _update(
                        ledger_path,
                        ledger,
                        state="STOPPED",
                        stop_reason="successor contract does not authorize a fresh next G",
                        ended_at=utc_now(),
                    )
                    return 0
                resume_programme = None
                first_attempt = 1
                break
            if not accepted:
                raise RuntimeError("controller invariant: attempt loop exited without a result")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    repo = Path.cwd().resolve()
    if not any((args.start, args.resume, args.status, args.validate_only, args.request_stop, args.stop_now)):
        if args.dry_run:
            args.start = True
        else:
            parser().error("choose one of --start, --resume, --status, --validate-only, --request-stop, or --stop-now")
    try:
        if args.status:
            return _status(repo)
        if args.validate_only:
            result = validate_repository(repo, require_clean=False)
            _print(result)
            return 0 if result["valid"] else 1
        if args.request_stop:
            return _request(repo, immediate=False)
        if args.stop_now:
            return _request(repo, immediate=True)
        if args.dry_run:
            return _preflight_dry_run(repo, args)
        return _run_loop(repo, args)
    except (GitError, LockUnavailable, RuntimeError, ValueError, OSError) as error:
        _print({"state": "ERROR", "error": str(error)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
