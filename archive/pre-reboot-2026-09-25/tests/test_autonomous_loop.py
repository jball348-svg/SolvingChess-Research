"""Synthetic end-to-end tests for the one-G-per-process autonomous controller."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[1]
CONTROLLER = PROJECT / "scripts" / "orchestration" / "autonomous_g_loop.py"
MOCK_CODEX = PROJECT / "tests" / "fixtures" / "mock_codex.py"
ORCHESTRATION = PROJECT / "scripts" / "orchestration"
if str(ORCHESTRATION) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATION))

import codex_runtime  # noqa: E402
from codex_runtime import (  # noqa: E402
    LEGACY_SECURITY,
    PREFERRED_SECURITY,
    CliInfo,
    build_command,
)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@pytest.fixture
def repository(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    (repo / "docs").mkdir()
    (repo / "schemas").mkdir()
    (repo / "state").mkdir()
    (repo / "roadmap" / "normalized").mkdir(parents=True)
    (repo / "handoffs" / "normalized").mkdir(parents=True)
    (repo / "references").mkdir()
    (repo / ".gitattributes").write_text(
        "* text=auto eol=lf\n/logs/orchestration/** -text\n",
        encoding="utf-8",
    )
    (repo / "AGENTS.md").write_text("# Synthetic agent contract\n", encoding="utf-8")
    (repo / "docs" / "RESEARCH_PROTOCOL.md").write_text("# Synthetic protocol\n", encoding="utf-8")
    (repo / "roadmap" / "normalized" / "roadmap.md").write_text("# Synthetic roadmap\n", encoding="utf-8")
    (repo / "handoffs" / "normalized" / "G89_Technical_Handoff.md").write_text(
        "# Synthetic previous handoff\n", encoding="utf-8"
    )
    (repo / "references" / "REFERENCE_MAP.md").write_text("# No references\n", encoding="utf-8")
    write_json(repo / "state" / "REFERENCE_REGISTRY.json", {"references": []})
    write_json(
        repo / "state" / "PROGRAM_STATE.json",
        {
            "project_id": "synthetic-solving-chess",
            "schema_version": "1.0",
            "latest_completed_programme": "G89",
            "latest_frozen_handoff": "handoffs/normalized/G89_Technical_Handoff.md",
            "permanent_roadmap_path": "roadmap/normalized/roadmap.md",
            "next_programme": {
                "programme": "G90",
                "authorized": True,
                "started": False,
            },
            "repository_bootstrap": {
                "completion_status": "COMPLETE",
                "autonomous_loop_readiness": "READY",
                "real_loop_running": False,
            },
        },
    )
    write_json(
        repo / "state" / "AUTONOMY_STATE.json",
        {
            "schema_version": "1.0",
            "orchestrator_state": "STOPPED",
            "real_research_loop_started": False,
        },
    )
    write_json(
        repo / "schemas" / "program_state.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": [
                "latest_completed_programme",
                "next_programme",
            ],
            "properties": {
                "latest_completed_programme": {"type": "string", "pattern": "^G[0-9]+$"},
                "next_programme": {
                    "type": "object",
                    "required": ["programme", "authorized", "started"],
                    "properties": {
                        "programme": {"type": "string", "pattern": "^G[0-9]+$"},
                        "authorized": {"type": "boolean"},
                        "started": {"type": "boolean"},
                    },
                },
            },
            "additionalProperties": True,
        },
    )
    required_completion = [
        "run_id",
        "programme",
        "status",
        "gate_result",
        "handoff_path",
        "freeze_manifest_path",
        "program_state_path",
        "tests_run",
        "validation_summary",
        "blockers",
        "next_programme",
        "next_programme_authorized",
        "human_input_required",
        "human_input_reason",
        "final_summary",
    ]
    write_json(
        repo / "schemas" / "g_completion.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": required_completion,
            "properties": {
                "run_id": {"type": "string"},
                "programme": {"type": "string", "pattern": "^G[0-9]+$"},
                "status": {"enum": ["PASS", "HOLD", "BLOCKED", "FAILED"]},
                "gate_result": {"type": "string"},
                "handoff_path": {"type": "string"},
                "freeze_manifest_path": {"type": "string"},
                "program_state_path": {"type": "string"},
                "tests_run": {"type": "array"},
                "validation_summary": {"type": "string"},
                "blockers": {"type": "array"},
                "next_programme": {"type": "string"},
                "next_programme_authorized": {"type": "boolean"},
                "human_input_required": {"type": "boolean"},
                "human_input_reason": {"type": "string"},
                "final_summary": {"type": "string"},
            },
            "additionalProperties": False,
        },
    )
    (repo / "schemas" / "g_completion.output.schema.json").write_bytes(
        (repo / "schemas" / "g_completion.schema.json").read_bytes()
    )
    write_json(
        repo / "schemas" / "autonomy_state.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["orchestrator_state", "real_research_loop_started"],
            "properties": {
                "orchestrator_state": {"enum": ["STOPPED", "RUNNING"]},
                "real_research_loop_started": {"type": "boolean"},
            },
            "additionalProperties": True,
        },
    )
    write_json(
        repo / "schemas" / "freeze_manifest.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["schema_version", "programme", "run_id", "status", "files"],
            "properties": {
                "schema_version": {"type": "string"},
                "programme": {"type": "string"},
                "run_id": {"type": "string"},
                "status": {"type": "string"},
                "files": {"type": "array"},
            },
            "additionalProperties": False,
        },
    )
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Synthetic Test")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "add", "--all")
    git(repo, "commit", "-m", "synthetic base")
    git(tmp_path, "init", "--bare", str(remote))
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-u", "origin", "main")
    return repo, remote


def run_controller(
    repo: Path,
    scenario: str,
    *extra: str,
    retries: int = 0,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["MOCK_CODEX_SCENARIO"] = scenario
    return subprocess.run(
        [
            sys.executable,
            str(CONTROLLER),
            "--start",
            "--codex-bin",
            str(MOCK_CODEX),
            "--security-mode",
            "legacy-workspace",
            "--max-retries",
            str(retries),
            *extra,
        ],
        cwd=repo,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )


def resume_controller(repo: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["MOCK_CODEX_SCENARIO"] = "pass"
    return subprocess.run(
        [
            sys.executable,
            str(CONTROLLER),
            "--resume",
            "--codex-bin",
            str(MOCK_CODEX),
            "--security-mode",
            "legacy-workspace",
            *extra,
        ],
        cwd=repo,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )


def ledger(repo: Path) -> dict:
    return json.loads((repo / ".git" / "solving-chess-autonomy" / "controller.json").read_text(encoding="utf-8"))


def state(repo: Path) -> dict:
    return json.loads((repo / "state" / "PROGRAM_STATE.json").read_text(encoding="utf-8"))


def assert_no_g14(repo: Path) -> None:
    assert not (repo / "research" / "G14").exists()


def test_pass_advances_once(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "pass", "--max-programmes", "1")
    assert result.returncode == 0, result.stdout + result.stderr
    assert state(repo)["next_programme"]["programme"] == "G91"
    assert ledger(repo)["last_status"] == "PASS"
    assert (repo / "research" / "G90" / "G90_Completion.json").is_file()
    assert json.loads((repo / "state" / "AUTONOMY_STATE.json").read_text(encoding="utf-8"))[
        "current_run"
    ] is None
    assert_no_g14(repo)


def test_accepted_controller_evidence_is_frozen(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "pass", "--max-programmes", "1")
    assert result.returncode == 0, result.stdout + result.stderr
    record = ledger(repo)
    evidence = repo / record["accepted_evidence"]["directory"]
    expected = {
        "prompt.md",
        "final.json",
        "metadata.json",
        "process_result.json",
        "validation.json",
        "evidence_manifest.json",
    }
    assert {path.name for path in evidence.iterdir()} == expected
    manifest = json.loads((evidence / "evidence_manifest.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        artifact = repo / item["path"]
        assert hashlib.sha256(artifact.read_bytes()).hexdigest() == item["sha256"], item["path"]
    process = json.loads((evidence / "process_result.json").read_text(encoding="utf-8"))
    output_schema_index = process["command"].index("--output-schema") + 1
    assert process["command"][output_schema_index].endswith("g_completion.output.schema.json")
    assert not git(repo, "status", "--porcelain=v1").stdout.strip()


@pytest.mark.parametrize(("scenario", "status"), [("blocked", "BLOCKED"), ("hold", "HOLD")])
def test_scientific_stop_is_not_retried(repository: tuple[Path, Path], scenario: str, status: str) -> None:
    repo, _ = repository
    result = run_controller(repo, scenario, retries=2)
    assert result.returncode == 0, result.stdout + result.stderr
    record = ledger(repo)
    assert record["last_status"] == status
    assert record["process_attempt"] == 1
    assert state(repo)["next_programme"]["programme"] == "G90"
    assert state(repo)["next_programme"]["authorized"] is False
    expected_tag = f"g90-{status.lower()}"
    assert git(repo, "rev-parse", "--verify", f"refs/tags/{expected_tag}").returncode == 0
    assert_no_g14(repo)


def test_process_crash_is_infrastructure_failure(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    original = git(repo, "rev-parse", "HEAD").stdout.strip()
    result = run_controller(repo, "crash")
    assert result.returncode == 2
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == original
    assert "exited 23" in ledger(repo)["stop_reason"]
    assert_no_g14(repo)


def test_malformed_final_json_is_rejected(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "malformed_json")
    assert result.returncode == 2
    assert "final output is invalid" in ledger(repo)["stop_reason"]
    assert_no_g14(repo)


def test_malformed_jsonl_is_rejected(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "malformed_jsonl")
    assert result.returncode == 2
    assert "JSONL event stream is invalid" in ledger(repo)["stop_reason"]
    assert_no_g14(repo)


def test_claimed_pass_missing_handoff_is_rejected(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "missing_handoff")
    assert result.returncode == 2
    errors = ledger(repo)["validation_errors"]
    assert any("handoff_path does not exist" in error for error in errors)
    assert_no_g14(repo)


def test_invalid_state_transition_is_rejected(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "invalid_transition")
    assert result.returncode == 2
    errors = ledger(repo)["validation_errors"]
    assert any("advance exactly one" in error for error in errors)
    assert state(repo)["next_programme"]["programme"] == "G90"
    assert_no_g14(repo)


def test_manifest_identity_mismatch_is_rejected(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "manifest_mismatch")
    assert result.returncode == 2
    errors = ledger(repo)["validation_errors"]
    assert any("freeze manifest run_id" in error for error in errors)
    assert any("freeze manifest status" in error for error in errors)
    assert_no_g14(repo)


def test_same_g_retries_in_fresh_process_then_passes(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "retry_then_pass", "--max-programmes", "1", retries=2)
    assert result.returncode == 0, result.stdout + result.stderr
    record = ledger(repo)
    assert record["process_attempt"] == 2
    assert record["retry_count"] == 1
    assert record["last_completed_run_id"].startswith("G90-a02-")
    archives = record["archived_attempts"]
    assert len(archives) == 1
    assert archives[0]["run_id"].startswith("G90-a01-")
    assert git(repo, "cat-file", "-t", archives[0]["stash_commit"]).stdout.strip() == "commit"
    assert state(repo)["next_programme"]["programme"] == "G91"
    assert_no_g14(repo)


def test_until_is_inclusive_maximum_g(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    result = run_controller(repo, "pass", "--until", "G91")
    assert result.returncode == 0, result.stdout + result.stderr
    record = ledger(repo)
    assert record["accepted_programmes"] == 2
    assert "G91" in record["stop_reason"]
    assert state(repo)["next_programme"]["programme"] == "G92"
    assert git(repo, "rev-parse", "--verify", "refs/tags/g91-frozen").returncode == 0
    assert_no_g14(repo)


def test_commit_annotated_tag_and_atomic_push_are_remote_verified(repository: tuple[Path, Path]) -> None:
    repo, remote = repository
    result = run_controller(repo, "pass", "--max-programmes", "1")
    assert result.returncode == 0, result.stdout + result.stderr
    metadata_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    content_head = git(repo, "rev-parse", "HEAD^").stdout.strip()
    remote_head = git(repo, "ls-remote", str(remote), "refs/heads/main").stdout.split()[0]
    peeled = git(repo, "ls-remote", str(remote), "refs/tags/g90-frozen^{}").stdout.split()[0]
    assert remote_head == metadata_head
    assert peeled == content_head
    assert metadata_head != content_head
    assert git(repo, "cat-file", "-t", "refs/tags/g90-frozen").stdout.strip() == "tag"
    record = ledger(repo)
    assert record["remote_verified"] is True
    assert record["git_content_commit"] == content_head
    assert record["git_metadata_commit"] == metadata_head
    assert state(repo)["last_frozen_git"] == {
        "status": "FROZEN",
        "commit": content_head,
        "tag": "g90-frozen",
    }
    autonomy = json.loads((repo / "state" / "AUTONOMY_STATE.json").read_text(encoding="utf-8"))
    assert autonomy["last_accepted_freeze"]["commit"] == content_head
    assert_no_g14(repo)


def test_failed_push_is_resumable_without_rerunning_codex(repository: tuple[Path, Path]) -> None:
    repo, remote = repository
    missing_remote = repo.parent / "temporarily-unavailable.git"
    git(repo, "remote", "set-url", "origin", str(missing_remote))
    first = run_controller(repo, "pass", "--max-programmes", "1")
    assert first.returncode == 3
    first_record = ledger(repo)
    assert first_record["state"] == "PUBLISH_PENDING"
    assert first_record["process_attempt"] == 1
    accepted_head = git(repo, "rev-parse", "HEAD").stdout.strip()
    assert state(repo)["next_programme"]["programme"] == "G91"

    git(repo, "remote", "set-url", "origin", str(remote))
    resumed = resume_controller(repo)
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    recovered = ledger(repo)
    assert recovered["state"] == "STOPPED"
    assert recovered["remote_verified"] is True
    assert recovered["process_attempt"] == 1
    assert git(repo, "ls-remote", str(remote), "refs/heads/main").stdout.split()[0] == accepted_head
    assert_no_g14(repo)


def test_bootstrap_gate_blocks_live_and_dry_starts(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    value = state(repo)
    value["repository_bootstrap"]["completion_status"] = "IN_PROGRESS"
    write_json(repo / "state" / "PROGRAM_STATE.json", value)
    live = run_controller(repo, "pass")
    assert live.returncode == 1
    assert "repository bootstrap is not COMPLETE" in live.stdout
    dry = run_controller(repo, "pass", "--dry-run")
    assert dry.returncode == 1
    assert "repository bootstrap is not COMPLETE" in dry.stdout
    assert not (repo / ".run").exists()
    assert_no_g14(repo)


def test_retry_recovery_has_no_destructive_reset_or_clean() -> None:
    source = CONTROLLER.read_text(encoding="utf-8")
    assert "reset\", \"--hard" not in source
    assert "clean\", \"-ffd" not in source
    assert "stash\", \"push\", \"--all" in source


def test_preferred_and_legacy_security_are_explicitly_separate(tmp_path: Path) -> None:
    cli = CliInfo(("codex",), "codex-cli 0.147.0", (0, 147, 0), "", "0" * 64)
    schema = tmp_path / "schema.json"
    final = tmp_path / "final.json"
    preferred = build_command(cli, tmp_path, schema, final, PREFERRED_SECURITY)
    legacy = build_command(cli, tmp_path, schema, final, LEGACY_SECURITY)
    assert "--sandbox" not in preferred
    assert 'default_permissions="workspace-only"' in preferred
    assert 'approvals_reviewer="auto_review"' in preferred
    assert "--sandbox" in legacy
    assert "workspace-write" in legacy
    assert 'default_permissions="workspace-only"' not in legacy
    assert 'approvals_reviewer="auto_review"' not in legacy


@pytest.mark.skipif(os.name != "nt", reason="Windows ACL handoff is Windows-specific")
def test_controller_handoff_rejects_parent_escape(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    outside = tmp_path / "outside"
    allowed.mkdir()
    outside.mkdir()
    with pytest.raises(codex_runtime.CodexRuntimeError, match="outside the declared runtime root"):
        codex_runtime.establish_controller_handoff(outside, allowed)
    with pytest.raises(codex_runtime.CodexRuntimeError, match="runtime root itself"):
        codex_runtime.establish_controller_handoff(allowed, allowed)


@pytest.mark.skipif(os.name != "nt", reason="Windows ACL handoff is Windows-specific")
def test_controller_handoff_uses_argument_vector_and_exact_sid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parent = tmp_path / "runtime"
    root = parent / "worktree"
    root.mkdir(parents=True)
    sid = "S-1-5-21-1-2-3-1001"
    calls: list[tuple[list[str], dict[str, object]]] = []

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        if command[0] == "whoami.exe":
            return subprocess.CompletedProcess(command, 0, f'"DOMAIN\\user","{sid}"\n', "")
        return subprocess.CompletedProcess(command, 0, "Successfully processed 1 files\n", "")

    monkeypatch.setattr(codex_runtime.subprocess, "run", fake_run)
    assert codex_runtime.establish_controller_handoff(root, parent) == sid
    assert calls[0][0] == ["whoami.exe", "/user", "/fo", "csv", "/nh"]
    assert calls[1][0] == [
        "icacls.exe",
        str(root.resolve()),
        "/grant:r",
        f"*{sid}:(OI)(CI)(F)",
    ]
    assert all(isinstance(command, list) for command, _ in calls)
    assert all(kwargs.get("shell") in {None, False} for _, kwargs in calls)


def test_dry_run_and_status_do_not_launch_programme(repository: tuple[Path, Path]) -> None:
    repo, _ = repository
    env = os.environ.copy()
    env["MOCK_CODEX_SCENARIO"] = "pass"
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    result = subprocess.run(
        [
            sys.executable,
            str(CONTROLLER),
            "--start",
            "--dry-run",
            "--codex-bin",
            str(MOCK_CODEX),
            "--security-mode",
            "legacy-workspace",
        ],
        cwd=repo,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["mutation_performed"] is False
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before
    assert not (repo / "research").exists()
    assert_no_g14(repo)
