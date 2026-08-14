"""Fail-closed Git worktree, freeze, tag, push, and remote-verification helpers."""

from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from io_utils import atomic_write_json, atomic_write_text, load_json, utc_now


class GitError(RuntimeError):
    pass


@dataclass(frozen=True)
class Worktree:
    source_repo: str
    path: str
    branch: str
    canonical_branch: str
    base_commit: str
    git_common_dir: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def _run(
    repo: Path,
    args: Iterable[str],
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        command = "git " + " ".join(args)
        raise GitError(f"{command} failed ({completed.returncode}): {completed.stderr.strip()}")
    return completed


def git_common_dir(repo: Path) -> Path:
    repo = Path(repo).resolve()
    value = _run(repo, ("rev-parse", "--git-common-dir")).stdout.strip()
    path = Path(value)
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def runtime_dir(repo: Path) -> Path:
    return git_common_dir(repo) / "solving-chess-autonomy"


def head(repo: Path) -> str:
    return _run(Path(repo), ("rev-parse", "HEAD")).stdout.strip()


def current_branch(repo: Path) -> str:
    return _run(Path(repo), ("symbolic-ref", "--short", "HEAD")).stdout.strip()


def status_porcelain(repo: Path) -> str:
    return _run(Path(repo), ("status", "--porcelain=v1", "--untracked-files=all")).stdout


def ensure_clean(repo: Path) -> None:
    status = status_porcelain(repo)
    if status.strip():
        preview = "\n".join(status.splitlines()[:20])
        raise GitError(f"source worktree must be clean before --start:\n{preview}")


def create_isolated_worktree(source_repo: Path, programme: int) -> Worktree:
    source_repo = Path(source_repo).resolve()
    ensure_clean(source_repo)
    base = head(source_repo)
    canonical = current_branch(source_repo)
    common = git_common_dir(source_repo)
    identity = hashlib.sha256(f"{base}\0G{programme}\0v1".encode()).hexdigest()[:10]
    branch = f"autonomy/g{programme}-{identity}"
    worktree_path = source_repo / ".run" / "wt" / f"g{programme}-{identity}"
    if worktree_path.exists():
        raise GitError(f"isolated worktree already exists; use --resume: {worktree_path}")
    branch_exists = _run(
        source_repo,
        ("show-ref", "--verify", "--quiet", f"refs/heads/{branch}"),
        check=False,
    ).returncode == 0
    if branch_exists:
        raise GitError(f"controller branch already exists; use --resume or inspect manually: {branch}")
    exclude_path = common / "info" / "exclude"
    exclude_text = exclude_path.read_text(encoding="utf-8") if exclude_path.is_file() else ""
    if ".run/" not in {line.strip() for line in exclude_text.splitlines()}:
        atomic_write_text(exclude_path, exclude_text.rstrip("\r\n") + "\n.run/\n")
    worktree_path.parent.mkdir(parents=True, exist_ok=True)
    _run(source_repo, ("worktree", "add", "--no-track", "-b", branch, str(worktree_path), base))
    return Worktree(
        source_repo=str(source_repo),
        path=str(worktree_path),
        branch=branch,
        canonical_branch=canonical,
        base_commit=base,
        git_common_dir=str(common),
    )


def load_worktree(value: dict[str, Any]) -> Worktree:
    required = ("source_repo", "path", "branch", "canonical_branch", "base_commit", "git_common_dir")
    missing = [key for key in required if not isinstance(value.get(key), str) or not value[key]]
    if missing:
        raise GitError(f"invalid saved worktree record; missing: {', '.join(missing)}")
    worktree = Worktree(**{key: value[key] for key in required})
    path = Path(worktree.path)
    if not path.is_dir():
        raise GitError(f"saved worktree is unavailable: {path}")
    if current_branch(path) != worktree.branch:
        raise GitError("saved worktree branch does not match controller ledger")
    return worktree


def _tag_for(programme: int, status: str) -> str:
    suffix = "frozen" if status == "PASS" else status.lower()
    return f"g{programme}-{suffix}"


def _content_commit_for_run(
    repo: Path,
    commit: str,
    expected_parent: str,
    programme: int,
    status: str,
    run_id: str,
) -> bool:
    """Recognize only the controller commit created for this exact transaction."""

    parent = _run(repo, ("rev-parse", f"{commit}^"), check=False)
    if parent.returncode != 0 or parent.stdout.strip() != expected_parent:
        return False
    message = _run(repo, ("show", "-s", "--format=%B", commit), check=False)
    if message.returncode != 0:
        return False
    lines = message.stdout.splitlines()
    return bool(
        lines
        and lines[0] == f"Freeze G{programme}: {status}"
        and f"Controller-Run: {run_id}" in lines[1:]
    )


def _metadata_commit_for_run(
    repo: Path,
    commit: str,
    content_commit: str,
    programme: int,
    status: str,
    run_id: str,
) -> bool:
    parent = _run(repo, ("rev-parse", f"{commit}^"), check=False)
    if parent.returncode != 0 or parent.stdout.strip() != content_commit:
        return False
    message = _run(repo, ("show", "-s", "--format=%B", commit), check=False)
    if message.returncode != 0:
        return False
    lines = message.stdout.splitlines()
    return bool(
        lines
        and lines[0] == f"Record G{programme} freeze identity: {status}"
        and f"Controller-Run: {run_id}" in lines[1:]
        and f"Content-Commit: {content_commit}" in lines[1:]
    )


def _write_freeze_identity(
    repo: Path,
    programme: int,
    content_commit: str,
    tag: str,
) -> None:
    programme_state_path = repo / "state" / "PROGRAM_STATE.json"
    autonomy_state_path = repo / "state" / "AUTONOMY_STATE.json"
    programme_state = load_json(programme_state_path)
    autonomy_state = load_json(autonomy_state_path)
    if not isinstance(programme_state, dict) or not isinstance(autonomy_state, dict):
        raise GitError("freeze identity state roots must be JSON objects")
    programme_state["last_frozen_git"] = {
        "status": "FROZEN",
        "commit": content_commit,
        "tag": tag,
    }
    autonomy_state.update(
        {
            "orchestrator_state": "STOPPED",
            "updated_at": utc_now(),
            "current_run": None,
            "last_accepted_freeze": {
                "programme": f"G{programme}",
                "commit": content_commit,
                "tag": tag,
                "validation_result": "PASS",
            },
            "real_research_loop_started": False,
        }
    )
    atomic_write_json(programme_state_path, programme_state)
    atomic_write_json(autonomy_state_path, autonomy_state)


def _valid_ref_component(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._/-]+", value)) and ".." not in value


def verify_remote(
    repo: Path,
    branch: str,
    tag: str,
    content_commit: str,
    branch_commit: str,
    remote: str = "origin",
) -> None:
    if not _valid_ref_component(branch) or not _valid_ref_component(tag):
        raise GitError("unsafe Git ref name")
    query = _run(
        repo,
        (
            "ls-remote",
            remote,
            f"refs/heads/{branch}",
            f"refs/tags/{tag}",
            f"refs/tags/{tag}^{{}}",
        ),
    )
    refs: dict[str, str] = {}
    for line in query.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2:
            refs[parts[1]] = parts[0]
    if refs.get(f"refs/heads/{branch}") != branch_commit:
        raise GitError("remote branch verification failed")

    peeled = _run(repo, ("ls-remote", remote, f"refs/tags/{tag}^{{}}")).stdout.split()
    if not peeled or peeled[0] != content_commit:
        raise GitError("remote annotated tag does not peel to the accepted content commit")
    if f"refs/tags/{tag}" not in refs:
        raise GitError("remote annotated tag verification failed")


def freeze_and_publish(
    worktree: Worktree,
    programme: int,
    status: str,
    run_id: str,
    expected_head: str,
    *,
    remote: str = "origin",
) -> dict[str, str]:
    if status not in {"PASS", "HOLD", "BLOCKED", "FAILED"}:
        raise GitError(f"invalid freeze status: {status!r}")
    repo = Path(worktree.path)
    observed_head = head(repo)
    content_commit: str
    metadata_commit: str | None = None
    if observed_head == expected_head:
        if not status_porcelain(repo).strip():
            raise GitError("validated G produced no repository transaction to freeze")
        _run(repo, ("add", "--all"))
        staged = _run(repo, ("diff", "--cached", "--quiet"), check=False)
        if staged.returncode == 0:
            raise GitError("no staged G changes remain after validation")
        if staged.returncode not in (0, 1):
            raise GitError(f"cannot inspect staged changes: {staged.stderr.strip()}")

        message = f"Freeze G{programme}: {status}\n\nController-Run: {run_id}"
        _run(
            repo,
            (
                "-c",
                "user.name=Solving Chess Autonomous Controller",
                "-c",
                "user.email=autonomy@solving-chess.invalid",
                "commit",
                "-m",
                message,
            ),
        )
        content_commit = head(repo)
    elif _content_commit_for_run(
        repo,
        observed_head,
        expected_head,
        programme,
        status,
        run_id,
    ):
        # A prior publish attempt may have stopped while recording identity metadata.
        content_commit = observed_head
    else:
        parent = _run(repo, ("rev-parse", f"{observed_head}^"), check=False)
        candidate_content = parent.stdout.strip() if parent.returncode == 0 else ""
        if _content_commit_for_run(
            repo,
            candidate_content,
            expected_head,
            programme,
            status,
            run_id,
        ) and _metadata_commit_for_run(
            repo,
            observed_head,
            candidate_content,
            programme,
            status,
            run_id,
        ):
            content_commit = candidate_content
            metadata_commit = observed_head
            if status_porcelain(repo).strip():
                raise GitError("pending publication metadata commit has uncommitted changes")
        else:
            raise GitError(
                "worktree history is not the expected base or pending controller transaction "
                f"(expected {expected_head}, observed {observed_head})"
            )

    tag = _tag_for(programme, status)
    existing = _run(repo, ("rev-parse", "--verify", f"refs/tags/{tag}^{{}}"), check=False)
    if existing.returncode == 0:
        if existing.stdout.strip() != content_commit:
            raise GitError(f"freeze tag already exists at another commit: {tag}")
    else:
        annotation = f"G{programme} {status}\nrun_id={run_id}\ncommit={content_commit}"
        _run(
            repo,
            (
                "-c",
                "user.name=Solving Chess Autonomous Controller",
                "-c",
                "user.email=autonomy@solving-chess.invalid",
                "tag",
                "-a",
                tag,
                "-m",
                annotation,
                content_commit,
            ),
        )

    if metadata_commit is None:
        changed = {
            line[3:].replace("\\", "/")
            for line in status_porcelain(repo).splitlines()
            if len(line) >= 4
        }
        allowed_metadata = {"state/PROGRAM_STATE.json", "state/AUTONOMY_STATE.json"}
        if changed - allowed_metadata:
            raise GitError(
                "pending content commit has unexpected uncommitted paths: "
                + ", ".join(sorted(changed - allowed_metadata))
            )
        _write_freeze_identity(repo, programme, content_commit, tag)
        _run(repo, ("add", "--", *sorted(allowed_metadata)))
        staged = _run(repo, ("diff", "--cached", "--quiet"), check=False)
        if staged.returncode != 1:
            if staged.returncode == 0:
                raise GitError("freeze identity metadata produced no commit transaction")
            raise GitError(f"cannot inspect freeze identity metadata: {staged.stderr.strip()}")
        message = (
            f"Record G{programme} freeze identity: {status}\n\n"
            f"Controller-Run: {run_id}\nContent-Commit: {content_commit}"
        )
        _run(
            repo,
            (
                "-c",
                "user.name=Solving Chess Autonomous Controller",
                "-c",
                "user.email=autonomy@solving-chess.invalid",
                "commit",
                "-m",
                message,
            ),
        )
        metadata_commit = head(repo)

    source = Path(worktree.source_repo)
    if current_branch(source) != worktree.canonical_branch:
        raise GitError("source repository is no longer on the saved canonical branch")
    source_head = head(source)
    if source_head not in {expected_head, content_commit, metadata_commit}:
        raise GitError("canonical branch moved outside the pending G transaction; refusing to integrate")
    if status_porcelain(source).strip():
        raise GitError("canonical source worktree became dirty during the G run")
    if source_head != metadata_commit:
        _run(source, ("merge", "--ff-only", metadata_commit))
    if head(source) != metadata_commit:
        raise GitError("canonical branch fast-forward verification failed")
    _run(
        source,
        (
            "push",
            "--atomic",
            remote,
            f"HEAD:refs/heads/{worktree.canonical_branch}",
            f"refs/tags/{tag}:refs/tags/{tag}",
        ),
    )
    verify_remote(
        source,
        worktree.canonical_branch,
        tag,
        content_commit,
        metadata_commit,
        remote,
    )
    return {
        "commit": content_commit,
        "content_commit": content_commit,
        "metadata_commit": metadata_commit,
        "tag": tag,
        "branch": worktree.canonical_branch,
        "remote": remote,
    }
