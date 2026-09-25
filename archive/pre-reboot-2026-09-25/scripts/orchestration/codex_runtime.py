"""One-shot Codex CLI runtime with fail-closed security and process-tree cleanup."""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

try:
    import psutil
except ImportError:  # pragma: no cover - reported by preflight
    psutil = None


PREFERRED_SECURITY = "profile-auto-review"
LEGACY_SECURITY = "legacy-workspace"
SECURITY_MODES = (PREFERRED_SECURITY, LEGACY_SECURITY)
PROFILE_MIN_VERSION = (0, 138, 0)
# Permission profiles require the elevated backend to enforce path-level read
# restrictions. The controller establishes one explicit inheritable ACE for its
# own SID so elevated-sandbox outputs remain available for validation and freeze.
PREFERRED_WINDOWS_SANDBOX = "elevated"
LEGACY_WINDOWS_SANDBOX = "unelevated"


def windows_sandbox_for(security_mode: str) -> str:
    if security_mode == PREFERRED_SECURITY:
        return PREFERRED_WINDOWS_SANDBOX
    if security_mode == LEGACY_SECURITY:
        return LEGACY_WINDOWS_SANDBOX
    raise CodexRuntimeError(f"unknown security mode: {security_mode}")


def establish_controller_handoff(root: Path, allowed_parent: Path) -> str | None:
    """Give only the invoking controller identity inheritable access to sandbox output.

    The elevated Windows backend replaces the worktree ACL with a sandbox-user
    boundary.  An explicit ACE for the invoking SID is preserved, allowing the
    controller to validate and freeze newly created files after Codex exits.
    """

    if os.name != "nt":
        return None
    raw_root = Path(root)
    is_junction = getattr(raw_root, "is_junction", lambda: False)
    if raw_root.is_symlink() or is_junction():
        raise CodexRuntimeError(f"controller handoff target cannot be a link: {raw_root}")
    resolved = raw_root.resolve()
    parent = Path(allowed_parent).resolve()
    try:
        relative = resolved.relative_to(parent)
    except ValueError as error:
        raise CodexRuntimeError(
            f"refusing controller handoff outside the declared runtime root: {resolved}"
        ) from error
    if not relative.parts:
        raise CodexRuntimeError("refusing to grant controller handoff on the runtime root itself")
    if not resolved.is_dir():
        raise CodexRuntimeError(f"controller handoff target is not a real directory: {resolved}")
    identity = subprocess.run(
        ["whoami.exe", "/user", "/fo", "csv", "/nh"],
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    if identity.returncode != 0:
        raise CodexRuntimeError(f"cannot resolve controller SID: {identity.stderr.strip()}")
    rows = list(csv.reader(identity.stdout.splitlines()))
    if len(rows) != 1 or len(rows[0]) < 2 or not re.fullmatch(
        r"S-1-(?:\d+-)+\d+", rows[0][1]
    ):
        raise CodexRuntimeError("cannot parse controller SID")
    sid = rows[0][1]
    grant = subprocess.run(
        ["icacls.exe", str(resolved), "/grant:r", f"*{sid}:(OI)(CI)(F)"],
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if grant.returncode != 0:
        raise CodexRuntimeError(f"cannot establish controller handoff ACL: {grant.stderr.strip()}")
    return sid


class CodexRuntimeError(RuntimeError):
    pass


@dataclass(frozen=True)
class CliInfo:
    command: tuple[str, ...]
    version_output: str
    version: tuple[int, int, int]
    exec_help: str
    executable_sha256: str

    def display_command(self) -> str:
        return " ".join(self.command)


@dataclass(frozen=True)
class RunFiles:
    prompt: str
    events: str
    final: str
    stderr: str


@dataclass(frozen=True)
class RunResult:
    command: tuple[str, ...]
    returncode: int
    timed_out: bool
    stop_requested: bool
    duration_seconds: float
    jsonl_valid: bool
    jsonl_errors: tuple[str, ...]
    completion: dict | None
    completion_error: str | None

    def as_dict(self) -> dict:
        value = asdict(self)
        value["command"] = list(self.command)
        value["jsonl_errors"] = list(self.jsonl_errors)
        return value


def command_candidates(codex_bin: str | None = None) -> list[tuple[str, ...]]:
    candidates: list[Path] = []
    explicit = codex_bin or os.environ.get("SOLVING_CHESS_CODEX_BIN") or os.environ.get("CODEX_CLI_PATH")
    if explicit:
        candidates.append(Path(explicit).expanduser())
    discovered = shutil.which("codex")
    if discovered:
        candidates.append(Path(discovered))
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates.extend(
                sorted(
                    Path(local).glob("OpenAI/Codex/bin/*/codex.exe"),
                    key=lambda path: path.stat().st_mtime_ns if path.exists() else 0,
                    reverse=True,
                )
            )
    commands: list[tuple[str, ...]] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate.is_file():
            identity = str(candidate.resolve()).casefold()
            if identity in seen:
                continue
            seen.add(identity)
            if candidate.suffix.casefold() == ".py":
                commands.append((sys.executable, str(candidate.resolve())))
            else:
                commands.append((str(candidate.resolve()),))
    if commands:
        return commands
    if explicit:
        raise CodexRuntimeError(f"Codex executable does not exist: {explicit}")
    raise CodexRuntimeError("cannot locate Codex CLI; pass --codex-bin")


def _probe(command: Sequence[str], suffix: Sequence[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [*command, *suffix],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise CodexRuntimeError(f"Codex CLI preflight failed: {error}") from error


def probe_cli(codex_bin: str | None, security_mode: str) -> CliInfo:
    if security_mode not in SECURITY_MODES:
        raise CodexRuntimeError(f"unknown security mode: {security_mode}")
    failures: list[str] = []
    command = None
    version_probe = None
    for candidate in command_candidates(codex_bin):
        try:
            candidate_probe = _probe(candidate, ("--version",))
        except CodexRuntimeError as error:
            failures.append(f"{' '.join(candidate)}: {error}")
            continue
        if candidate_probe.returncode != 0:
            failures.append(f"{' '.join(candidate)}: {candidate_probe.stdout.strip()}")
            continue
        command = candidate
        version_probe = candidate_probe
        break
    if command is None or version_probe is None:
        raise CodexRuntimeError("no usable Codex CLI candidate: " + "; ".join(failures))
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_probe.stdout)
    if not match:
        raise CodexRuntimeError(f"cannot parse Codex version: {version_probe.stdout.strip()!r}")
    version = tuple(int(part) for part in match.groups())
    help_probe = _probe(command, ("exec", "--help"))
    if help_probe.returncode != 0:
        raise CodexRuntimeError(f"codex exec --help failed: {help_probe.stdout.strip()}")
    required = (
        "--json",
        "--output-schema",
        "--output-last-message",
        "--ephemeral",
        "--strict-config",
        "--ignore-user-config",
        "--model",
        "--cd",
    )
    missing = [flag for flag in required if flag not in help_probe.stdout]
    if missing:
        raise CodexRuntimeError(f"Codex CLI lacks required automation flags: {', '.join(missing)}")
    if security_mode == PREFERRED_SECURITY and version < PROFILE_MIN_VERSION:
        raise CodexRuntimeError(
            "preferred permission profiles require Codex >= 0.138.0; "
            "upgrade or explicitly choose --security-mode legacy-workspace"
        )
    if security_mode == LEGACY_SECURITY:
        # Approval policy is passed through the stable strict-config surface because
        # current alpha.6.6 help exposes --sandbox but no longer exposes `-a`.
        legacy_required = ("--sandbox",)
        missing = [flag for flag in legacy_required if flag not in help_probe.stdout]
        if missing:
            raise CodexRuntimeError(f"Codex CLI lacks legacy security flags: {', '.join(missing)}")
    if psutil is None:
        raise CodexRuntimeError("psutil is required for reliable process-tree cleanup")
    executable_path = Path(command[-1] if Path(command[-1]).suffix.casefold() == ".py" else command[0])
    from io_utils import sha256_file

    return CliInfo(tuple(command), version_probe.stdout.strip(), version, help_probe.stdout, sha256_file(executable_path))


def _profile_overrides() -> list[str]:
    # A single inline profile avoids accidental composition with any user sandbox config.
    profile = (
        '{ extends = ":workspace", filesystem = { ":root" = "deny", '
        '":minimal" = "read", ":workspace_roots" = { "." = "write", '
        '"AGENTS.md" = "read", "docs" = "read", "references" = "read", '
        '"schemas" = "read", "scripts/orchestration" = "read", '
        '"scripts/validation" = "read", "roadmap/originals" = "read", '
        '"roadmap" = "read", "handoffs" = "read", "legacy" = "read", '
        '"logs/orchestration" = "read", '
        '"state/ARTIFACT_REGISTRY.json" = "read", '
        '"state/REFERENCE_REGISTRY.json" = "read", '
        '"state/AUTONOMY_STATE.json" = "read", '
        '"**/*.env" = "deny", "**/.env" = "deny", "**/*credential*" = "deny" }, '
        'glob_scan_max_depth = 6 }, network = { enabled = true, '
        'domains = { "*" = "allow" }, allow_local_binding = false } }'
    )
    return [
        "-c",
        'default_permissions="workspace-only"',
        "-c",
        f"permissions.workspace-only={profile}",
        "-c",
        'approval_policy="on-request"',
        "-c",
        'approvals_reviewer="auto_review"',
        "-c",
        f'windows.sandbox="{PREFERRED_WINDOWS_SANDBOX}"',
        "-c",
        'shell_environment_policy.inherit="core"',
        "-c",
        "shell_environment_policy.ignore_default_excludes=false",
    ]


def build_command(
    cli: CliInfo,
    repo: Path,
    schema_path: Path,
    final_path: Path,
    security_mode: str,
    *,
    model: str = "gpt-5.6-sol",
) -> tuple[str, ...]:
    command = [
        *cli.command,
        "exec",
        "--strict-config",
        "--ignore-user-config",
        "--ephemeral",
        "--json",
        "--color",
        "never",
        "--cd",
        str(Path(repo).resolve()),
        "--model",
        model,
        "-c",
        'model_reasoning_effort="ultra"',
        "--output-schema",
        str(Path(schema_path).resolve()),
        "--output-last-message",
        str(Path(final_path).resolve()),
    ]
    if security_mode == PREFERRED_SECURITY:
        command.extend(_profile_overrides())
    elif security_mode == LEGACY_SECURITY:
        command.extend(
            (
                "--sandbox",
                "workspace-write",
                "-c",
                'approval_policy="never"',
                "-c",
                "sandbox_workspace_write.network_access=true",
                "-c",
                f'windows.sandbox="{LEGACY_WINDOWS_SANDBOX}"',
                "-c",
                'shell_environment_policy.inherit="core"',
                "-c",
                "shell_environment_policy.ignore_default_excludes=false",
            )
        )
    else:
        raise CodexRuntimeError(f"unknown security mode: {security_mode}")
    command.append("-")
    return tuple(command)


def _terminate_process_tree(process: subprocess.Popen, grace_seconds: float = 4.0) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        try:
            process.send_signal(signal.CTRL_BREAK_EVENT)
            process.wait(timeout=min(grace_seconds, 2.0))
            return
        except (OSError, subprocess.TimeoutExpired):
            pass
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=min(grace_seconds, 2.0))
            return
        except (OSError, subprocess.TimeoutExpired):
            pass

    try:
        parent = psutil.Process(process.pid)
        descendants = parent.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        descendants = []
        parent = None
    for child in descendants:
        try:
            child.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if parent is not None:
        try:
            parent.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    _, alive = psutil.wait_procs(descendants + ([parent] if parent is not None else []), timeout=grace_seconds)
    for item in alive:
        try:
            item.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def terminate_process_identity(pid: int, create_time: float, grace_seconds: float = 4.0) -> bool:
    """Terminate a recorded process tree only if the PID still has the same identity."""

    if psutil is None:
        raise CodexRuntimeError("psutil is required for process identity cleanup")
    try:
        parent = psutil.Process(int(pid))
        observed = parent.create_time()
    except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
        return False
    if abs(observed - float(create_time)) > 0.01:
        return False
    descendants = parent.children(recursive=True)
    for process in descendants:
        try:
            process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    try:
        parent.terminate()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    _, alive = psutil.wait_procs([*descendants, parent], timeout=grace_seconds)
    for process in alive:
        try:
            process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    psutil.wait_procs(alive, timeout=2)
    return True


def validate_jsonl(path: Path, returncode: int) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    types: list[str] = []
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    errors.append(f"line {number}: malformed JSON: {error.msg}")
                    continue
                if not isinstance(event, dict) or not isinstance(event.get("type"), str):
                    errors.append(f"line {number}: event must be an object with a string type")
                    continue
                types.append(event["type"])
    except OSError as error:
        errors.append(f"cannot read JSONL events: {error}")
    if not types:
        errors.append("JSONL event stream is empty")
    if "thread.started" not in types:
        errors.append("JSONL has no thread.started event")
    if returncode == 0 and "turn.completed" not in types:
        errors.append("successful process has no turn.completed event")
    return not errors, tuple(errors)


def _read_completion(path: Path) -> tuple[dict | None, str | None]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, str(error)
    if not isinstance(value, dict):
        return None, "final output root is not a JSON object"
    return value, None


def run_codex(
    cli: CliInfo,
    repo: Path,
    prompt_text: str,
    files: RunFiles,
    schema_path: Path,
    security_mode: str,
    *,
    timeout_seconds: float | None,
    stop_requested: Callable[[], bool],
    environment: Mapping[str, str] | None = None,
    on_start: Callable[[int, float], None] | None = None,
) -> RunResult:
    for raw in asdict(files).values():
        Path(raw).parent.mkdir(parents=True, exist_ok=True)
    prompt_path = Path(files.prompt)
    from io_utils import atomic_write_text

    atomic_write_text(prompt_path, prompt_text.replace("\r\n", "\n"))
    final_path = Path(files.final)
    final_path.unlink(missing_ok=True)
    command = build_command(cli, repo, schema_path, final_path, security_mode)
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    start = time.monotonic()
    timed_out = False
    stopped = False
    env = dict(os.environ)
    if environment:
        env.update({str(key): str(value) for key, value in environment.items()})
    with prompt_path.open("rb") as stdin, Path(files.events).open("wb") as stdout, Path(files.stderr).open(
        "wb"
    ) as stderr:
        try:
            process = subprocess.Popen(
                command,
                cwd=Path(repo),
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                shell=False,
                env=env,
                creationflags=creationflags,
                start_new_session=os.name != "nt",
            )
        except OSError as error:
            raise CodexRuntimeError(f"cannot start Codex CLI: {error}") from error
        if on_start is not None:
            try:
                create_time = psutil.Process(process.pid).create_time()
                on_start(process.pid, create_time)
            except Exception:
                _terminate_process_tree(process)
                raise
        while process.poll() is None:
            elapsed = time.monotonic() - start
            if timeout_seconds is not None and elapsed >= timeout_seconds:
                timed_out = True
                _terminate_process_tree(process)
                break
            if stop_requested():
                stopped = True
                _terminate_process_tree(process)
                break
            time.sleep(0.1)
        returncode = process.wait()
    duration = time.monotonic() - start
    jsonl_valid, jsonl_errors = validate_jsonl(Path(files.events), returncode)
    completion, completion_error = _read_completion(final_path)
    return RunResult(
        command=command,
        returncode=returncode,
        timed_out=timed_out,
        stop_requested=stopped,
        duration_seconds=round(duration, 3),
        jsonl_valid=jsonl_valid,
        jsonl_errors=jsonl_errors,
        completion=completion,
        completion_error=completion_error,
    )
