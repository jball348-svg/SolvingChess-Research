"""Validate the repository routing contract before an autonomous G is launched."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import zipfile
from collections import Counter
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

ORCHESTRATION = Path(__file__).resolve().parents[1] / "orchestration"
if str(ORCHESTRATION) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATION))

from build_g_prompt import (  # noqa: E402
    format_programme,
    next_authorized,
    next_started,
    resolve_latest_completed,
    resolve_next_programme,
)
from io_utils import ensure_within, load_json, sha256_file  # noqa: E402

try:
    import jsonschema
except ImportError:  # pragma: no cover - fail-closed branch for minimal hosts
    jsonschema = None


def _schema_validate(instance: Any, schema_path: Path, errors: list[str], label: str) -> None:
    if not schema_path.is_file():
        errors.append(f"missing schema: {schema_path.relative_to(schema_path.parents[1])}")
        return
    if jsonschema is None:
        errors.append("jsonschema package is unavailable")
        return
    try:
        schema = load_json(schema_path)
        jsonschema.Draft202012Validator.check_schema(schema)
        validation_errors = sorted(
            jsonschema.Draft202012Validator(schema).iter_errors(instance),
            key=lambda item: list(item.absolute_path),
        )
        for error in validation_errors:
            location = "/".join(str(part) for part in error.absolute_path) or "$"
            errors.append(f"{label} schema {location}: {error.message}")
    except (OSError, ValueError, json.JSONDecodeError, jsonschema.SchemaError) as error:
        errors.append(f"invalid programme-state schema: {error}")


_KNOWN_FLAT_CORPUS_NAMES = frozenset(
    {
        "corrected_neutral.cpp",
        "corrected_rank.bin",
        "krk_cert.cpp",
        "neutral_rank.bin",
        "original_rank.bin",
        "pilot1_gate0.cpp",
    }
)
_FLAT_CORPUS_SUFFIXES = (
    ".bin",
    ".cpp",
    ".csv",
    ".docx",
    ".json",
    ".md",
    ".tar.gz",
    ".txt",
    ".zip",
)
_G_PREFIX = re.compile(r"^[Gg](\d+)(?:_|\.)")
_PRIMARY_OCCURRENCES = 129
_PRIMARY_BYTES = 59_994_517
_PRIMARY_UNIQUE_CONTENTS = 124
_PRIMARY_NAMESET_SHA256 = "9c1437cf878ce2a3e99f9896dbb2094c93ec3a7f269872b95214c335c856df59"
_ARCHIVE_MEMBERS = 334
_EXPECTED_MISSING = 63
_DOCX_CONVERSIONS = 29


def _run_git(repo: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _repository_path(
    repo: Path,
    value: object,
    errors: list[str],
    label: str,
) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} is not a non-empty repository path")
        return None
    posix = PurePosixPath(value.replace("\\", "/"))
    if posix.is_absolute() or any(part == ".." for part in posix.parts):
        errors.append(f"{label} escapes the repository: {value}")
        return None
    try:
        return ensure_within(repo, Path(*posix.parts))
    except ValueError as error:
        errors.append(f"{label}: {error}")
        return None


def _load_object(path: Path, errors: list[str], label: str) -> dict[str, Any] | None:
    try:
        value = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"invalid {label}: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"invalid {label}: root must be an object")
        return None
    return value


def _validate_declared_sha256(
    path: Path,
    expected: object,
    errors: list[str],
    label: str,
    *,
    required: bool,
) -> None:
    if expected is None:
        if required:
            errors.append(f"{label} SHA-256 is not frozen")
        return
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        errors.append(f"{label} SHA-256 is malformed")
        return
    if path.is_file() and sha256_file(path) != expected:
        errors.append(f"{label} SHA-256 does not match {path.relative_to(path.parents[1])}")


def _validate_hashed_repository_object(
    repo: Path,
    value: object,
    errors: list[str],
    label: str,
    *,
    path_key: str,
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} binding is malformed")
        return
    path = _repository_path(repo, value.get(path_key), errors, f"{label} path")
    if path is None or not path.is_file():
        errors.append(f"{label} path is missing")
        return

    # The routed Markdown path is agent-facing, while the inherited DOCX is
    # the controlling frozen byte authority.  Bind the declared identity to
    # that original whenever the state supplies one; the artifact registry
    # separately binds the normalized derivative and its conversion audit.
    identity_key = (
        "original_path"
        if value.get("original_path") is not None
        else "original_authority_path"
        if value.get("original_authority_path") is not None
        else path_key
    )
    identity_path = _repository_path(
        repo,
        value.get(identity_key),
        errors,
        f"{label} identity path",
    )
    if identity_path is None or not identity_path.is_file():
        errors.append(f"{label} controlling identity path is missing")
        return
    _validate_declared_sha256(
        identity_path,
        value.get("sha256"),
        errors,
        label,
        required=True,
    )


def _validate_authority_bindings(
    repo: Path,
    state: dict[str, Any],
    errors: list[str],
) -> None:
    _validate_hashed_repository_object(
        repo,
        state.get("permanent_roadmap"),
        errors,
        "permanent roadmap original authority",
        path_key="original_path",
    )
    _validate_hashed_repository_object(
        repo,
        state.get("latest_frozen_handoff"),
        errors,
        "latest frozen handoff original authority",
        path_key="original_path",
    )
    for label, binding in (
        ("permanent roadmap normalized", state.get("permanent_roadmap")),
        ("latest frozen handoff normalized", state.get("latest_frozen_handoff")),
    ):
        if isinstance(binding, dict):
            normalized = _repository_path(
                repo, binding.get("path"), errors, f"{label} path"
            )
            if normalized is None or not normalized.is_file():
                errors.append(f"{label} is missing")
    contracts = state.get("active_contracts")
    if not isinstance(contracts, dict):
        errors.append("active contract bindings are malformed")
        return
    for key, value in contracts.items():
        bindings = value if isinstance(value, list) else [value]
        for index, binding in enumerate(bindings):
            suffix = f"[{index}]" if isinstance(value, list) else ""
            _validate_hashed_repository_object(
                repo,
                binding,
                errors,
                f"active contract {key}{suffix} original authority",
                path_key="original_authority_path",
            )
            if isinstance(binding, dict):
                normalized = _repository_path(
                    repo,
                    binding.get("authority_path"),
                    errors,
                    f"active contract {key}{suffix} normalized path",
                )
                if normalized is None or not normalized.is_file():
                    errors.append(f"active contract {key}{suffix} normalized path is missing")


def _flat_corpus_name(name: str) -> bool:
    if not name.endswith(_FLAT_CORPUS_SUFFIXES):
        return False
    if name in _KNOWN_FLAT_CORPUS_NAMES or name.startswith("Pilot_"):
        return True
    match = _G_PREFIX.match(name)
    return bool(match and 2 <= int(match.group(1)) <= 13)


def _safe_member_path(value: str) -> str | None:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or not path.parts or any(part == ".." for part in path.parts):
        return None
    return path.as_posix()


def _actual_archive_members(path: Path, errors: list[str]) -> Counter[tuple[str, int, str]]:
    actual: Counter[tuple[str, int, str]] = Counter()
    try:
        if path.name.lower().endswith(".zip"):
            with zipfile.ZipFile(path) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    errors.append(f"archive CRC failure: {path.name}!{bad_member}")
                    return actual
                for info in archive.infolist():
                    if info.is_dir():
                        continue
                    member_path = _safe_member_path(info.filename)
                    if member_path is None:
                        errors.append(f"unsafe archive member: {path.name}!{info.filename}")
                        continue
                    payload = archive.read(info)
                    actual[(member_path, len(payload), hashlib.sha256(payload).hexdigest())] += 1
        elif path.name.lower().endswith(".tar.gz"):
            with tarfile.open(path, "r:gz") as archive:
                for info in archive.getmembers():
                    if not info.isfile():
                        continue
                    member_path = _safe_member_path(info.name)
                    if member_path is None:
                        errors.append(f"unsafe archive member: {path.name}!{info.name}")
                        continue
                    stream = archive.extractfile(info)
                    if stream is None:
                        errors.append(f"unreadable archive member: {path.name}!{info.name}")
                        continue
                    payload = stream.read()
                    actual[(member_path, len(payload), hashlib.sha256(payload).hexdigest())] += 1
        else:
            errors.append(f"registered archive has unsupported type: {path.name}")
    except (OSError, tarfile.TarError, zipfile.BadZipFile, RuntimeError) as error:
        errors.append(f"cannot inspect archive {path.name}: {error}")
    return actual


def _validate_artifact_registry(
    repo: Path,
    state: dict[str, Any],
    errors: list[str],
    evidence: dict[str, Any],
    *,
    freeze_required: bool,
) -> None:
    registry_pointer = state.get("registries", {})
    if not isinstance(registry_pointer, dict):
        errors.append("PROGRAM_STATE registries must be an object")
        return
    relative = registry_pointer.get("artifact_registry_path", "state/ARTIFACT_REGISTRY.json")
    path = _repository_path(repo, relative, errors, "artifact registry path")
    if path is None:
        return
    if not path.is_file():
        errors.append(f"missing artifact registry: {relative}")
        return
    registry = _load_object(path, errors, "artifact registry")
    if registry is None:
        return
    _schema_validate(
        registry,
        repo / "schemas" / "artifact_registry.schema.json",
        errors,
        "ARTIFACT_REGISTRY",
    )
    _validate_declared_sha256(
        path,
        registry_pointer.get("artifact_registry_sha256"),
        errors,
        "artifact registry",
        required=freeze_required,
    )

    occurrences = registry.get("occurrences")
    contents = registry.get("contents")
    archive_members = registry.get("archive_members")
    expected_missing = registry.get("expected_missing")
    if not all(isinstance(value, list) for value in (occurrences, contents, archive_members, expected_missing)):
        errors.append("artifact registry inventory arrays are malformed")
        return

    occurrence_by_id: dict[str, dict[str, Any]] = {}
    occurrence_paths: set[str] = set()
    placement: Counter[str] = Counter()
    observed_bytes = 0
    for item in occurrences:
        if not isinstance(item, dict):
            errors.append("artifact occurrence is not an object")
            continue
        occurrence_id = item.get("id")
        relative_path = item.get("repository_path")
        if not isinstance(occurrence_id, str) or occurrence_id in occurrence_by_id:
            errors.append(f"duplicate or malformed artifact occurrence id: {occurrence_id}")
            continue
        occurrence_by_id[occurrence_id] = item
        if not isinstance(relative_path, str) or relative_path in occurrence_paths:
            errors.append(f"duplicate or malformed artifact path: {relative_path}")
            continue
        occurrence_paths.add(relative_path)
        artifact = _repository_path(repo, relative_path, errors, f"artifact {occurrence_id}")
        if artifact is None or not artifact.is_file():
            errors.append(f"missing registered artifact: {relative_path}")
            continue
        expected_size = item.get("size")
        expected_hash = item.get("sha256")
        observed_size = artifact.stat().st_size
        observed_bytes += observed_size
        if expected_size != observed_size:
            errors.append(f"registered artifact size mismatch: {relative_path}")
        if not isinstance(expected_hash, str) or sha256_file(artifact) != expected_hash:
            errors.append(f"registered artifact SHA-256 mismatch: {relative_path}")
        if artifact.name != item.get("source_name"):
            errors.append(f"registered artifact filename changed: {relative_path}")
        parts = PurePosixPath(relative_path).parts
        placement["/".join(parts[:2])] += 1

    content_by_id = {
        item.get("content_id"): item
        for item in contents
        if isinstance(item, dict) and isinstance(item.get("content_id"), str)
    }
    if len(content_by_id) != len(contents):
        errors.append("artifact content identities are duplicated or malformed")
    for content_id, content in content_by_id.items():
        expected_ids = sorted(content.get("occurrence_ids", []))
        actual_ids = sorted(
            occurrence_id
            for occurrence_id, occurrence in occurrence_by_id.items()
            if occurrence.get("content_id") == content_id
        )
        if expected_ids != actual_ids:
            errors.append(f"artifact content occurrence backlinks differ: {content_id}")
        if content.get("immutability") != "FROZEN_ORIGINAL_BYTES":
            errors.append(f"artifact content lacks frozen-original identity: {content_id}")
    for occurrence_id, occurrence in occurrence_by_id.items():
        if occurrence.get("content_id") not in content_by_id:
            errors.append(f"artifact occurrence has no content identity: {occurrence_id}")

    summary = registry.get("source_summary", {})
    if isinstance(summary, dict):
        if summary.get("observed_count") != len(occurrences):
            errors.append("artifact registry observed occurrence count differs")
        if summary.get("observed_total_bytes") != observed_bytes:
            errors.append("artifact registry observed byte total differs")
        if summary.get("observed_unique_content_count") != len(contents):
            errors.append("artifact registry unique-content count differs")
        for key, expected in (
            ("expected_count", _PRIMARY_OCCURRENCES),
            ("observed_count", _PRIMARY_OCCURRENCES),
            ("expected_total_bytes", _PRIMARY_BYTES),
            ("observed_total_bytes", _PRIMARY_BYTES),
            ("observed_unique_content_count", _PRIMARY_UNIQUE_CONTENTS),
            ("observed_duplicate_occurrence_count", 5),
            ("expected_nameset_sha256", _PRIMARY_NAMESET_SHA256),
            ("observed_nameset_sha256", _PRIMARY_NAMESET_SHA256),
        ):
            if summary.get(key) != expected:
                errors.append(f"frozen migration seam differs at source_summary.{key}")
    nameset = "".join(
        f"{name}\n"
        for name in sorted(
            (str(item.get("source_name")) for item in occurrences if isinstance(item, dict)),
            key=lambda value: value.encode("utf-8"),
        )
    ).encode("utf-8")
    if hashlib.sha256(nameset).hexdigest() != _PRIMARY_NAMESET_SHA256:
        errors.append("frozen migration source name-set identity differs")
    if len(occurrences) != _PRIMARY_OCCURRENCES or observed_bytes != _PRIMARY_BYTES:
        errors.append("frozen migration occurrence/byte seam differs")
    if len(contents) != _PRIMARY_UNIQUE_CONTENTS:
        errors.append("frozen migration unique-content seam differs")
    if len(archive_members) != _ARCHIVE_MEMBERS or len(expected_missing) != _EXPECTED_MISSING:
        errors.append("frozen archive/missing inventory seam differs")
    expected_placement = Counter(
        {"roadmap/originals": 4, "handoffs/originals": 14, "legacy/originals": 111}
    )
    if placement != expected_placement:
        errors.append(f"frozen original placement differs: {dict(placement)}")

    audits = registry.get("audits", {})
    if not isinstance(audits, dict):
        errors.append("artifact registry audits are malformed")
    else:
        copy_policy = audits.get("copy_policy", {})
        if not isinstance(copy_policy, dict) or copy_policy.get("status") != "PASS":
            errors.append("artifact copy/preservation audit is not PASS")
        if isinstance(copy_policy, dict) and copy_policy.get("scope") != "PRIMARY_INHERITED_CORPUS_ONLY":
            errors.append("artifact copy/preservation audit scope is ambiguous")
        if isinstance(copy_policy, dict) and any(
            copy_policy.get(key) is not False
            for key in ("original_bytes_changed", "archives_exploded", "other_projects_touched")
        ):
            errors.append("artifact copy/preservation boundary was violated")
        checksum = audits.get("checksum_references", {})
        if not isinstance(checksum, dict) or checksum.get("present_hash_mismatches") != []:
            errors.append("artifact checksum-reference audit has mismatches")
        internal = audits.get("internal_archive_checksum_manifests", {})
        if not isinstance(internal, dict) or internal.get("status") != "PASS":
            errors.append("internal archive checksum audit is not PASS")
        target = audits.get("target_g12_bundle", {})
        if not isinstance(target, dict) or target.get("status") != "FOUND_EXACTLY_ONCE":
            errors.append("recovered G12 bundle cardinality/integrity audit failed")

        conversion = audits.get("docx_conversion", {})
        records = conversion.get("records", []) if isinstance(conversion, dict) else []
        if not isinstance(records, list) or conversion.get("conversion_count") != len(records):
            errors.append("DOCX conversion audit count differs")
            records = []
        elif len(records) != _DOCX_CONVERSIONS:
            errors.append("frozen DOCX conversion count differs")
        for record in records:
            if not isinstance(record, dict):
                errors.append("DOCX conversion record is malformed")
                continue
            source = occurrence_by_id.get(str(record.get("source_occurrence_id")))
            if source is None or source.get("sha256") != record.get("source_sha256"):
                errors.append(f"DOCX conversion source identity differs: {record.get('source_occurrence_id')}")
            derivative = _repository_path(
                repo, record.get("derivative_path"), errors, "DOCX derivative path"
            )
            audit_path = _repository_path(repo, record.get("audit_path"), errors, "DOCX audit path")
            if derivative is None or not derivative.is_file():
                errors.append(f"missing DOCX derivative: {record.get('derivative_path')}")
            elif sha256_file(derivative) != record.get("derivative_sha256"):
                errors.append(f"DOCX derivative SHA-256 mismatch: {record.get('derivative_path')}")
            if audit_path is None or not audit_path.is_file():
                errors.append(f"missing DOCX conversion audit: {record.get('audit_path')}")
            else:
                audit = _load_object(audit_path, errors, f"DOCX conversion audit {audit_path.name}")
                if audit is not None:
                    if audit.get("status") != record.get("status"):
                        errors.append(f"DOCX conversion status mismatch: {audit_path.name}")
                    source_audit = audit.get("source", {})
                    derivative_audit = audit.get("derivative", {})
                    if not isinstance(source_audit, dict) or source_audit.get("sha256") != record.get("source_sha256"):
                        errors.append(f"DOCX audit source hash mismatch: {audit_path.name}")
                    if not isinstance(derivative_audit, dict) or derivative_audit.get("sha256") != record.get("derivative_sha256"):
                        errors.append(f"DOCX audit derivative hash mismatch: {audit_path.name}")

    members_by_occurrence: dict[str, list[dict[str, Any]]] = {}
    for member in archive_members:
        if not isinstance(member, dict):
            errors.append("archive-member record is malformed")
            continue
        members_by_occurrence.setdefault(str(member.get("container_occurrence_id")), []).append(member)
    for occurrence_id, members in members_by_occurrence.items():
        occurrence = occurrence_by_id.get(occurrence_id)
        if occurrence is None:
            errors.append(f"archive members have missing container: {occurrence_id}")
            continue
        archive_path = _repository_path(
            repo, occurrence.get("repository_path"), errors, f"archive container {occurrence_id}"
        )
        if archive_path is None or not archive_path.is_file():
            continue
        expected = Counter(
            (str(member.get("path")), int(member.get("size", -1)), str(member.get("sha256")))
            for member in members
        )
        for member in members:
            if member.get("container_sha256") != occurrence.get("sha256"):
                errors.append(f"archive member container identity differs: {member.get('id')}")
            if member.get("content_id") != f"sha256:{member.get('sha256')}":
                errors.append(f"archive member content identity differs: {member.get('id')}")
        actual = _actual_archive_members(archive_path, errors)
        if actual != expected:
            errors.append(f"archive member inventory differs: {occurrence.get('repository_path')}")

    for missing in expected_missing:
        if not isinstance(missing, dict):
            errors.append("expected-missing record is malformed")
            continue
        if (
            missing.get("availability") != "EXPECTED_ONLY_MISSING_FROM_MIGRATION_INPUT"
            or missing.get("integrity_status") != "NOT_CORRUPTION_NO_BYTES_SUPPLIED"
            or missing.get("repository_path") is not None
        ):
            errors.append(f"expected-missing boundary differs: {missing.get('id')}")

    residual = sorted(path.name for path in repo.iterdir() if path.is_file() and _flat_corpus_name(path.name))
    if residual:
        errors.append("flat source corpus remains at repository root: " + ", ".join(residual))
    if (repo / "Other projects").exists():
        errors.append("legacy Other projects staging directory still exists")

    evidence["artifact_registry"] = {
        "occurrences": len(occurrences),
        "unique_contents": len(contents),
        "archive_members": len(archive_members),
        "expected_missing": len(expected_missing),
        "observed_bytes": observed_bytes,
        "placement": dict(sorted(placement.items())),
    }


def _gitlink_identity(repo: Path, relative: str) -> tuple[str | None, str | None]:
    stage = _run_git(repo, "ls-files", "--stage", "--", relative)
    if stage.returncode != 0 or not stage.stdout.strip():
        return None, None
    fields = stage.stdout.strip().split()
    if len(fields) < 2:
        return None, None
    return fields[0], fields[1]


def _validate_structural_snapshot(
    repo: Path,
    project: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    evidence: dict[str, Any],
) -> None:
    reproducibility = project.get("reproducibility", {})
    source = project.get("source", {})
    if not isinstance(reproducibility, dict) or not isinstance(source, dict):
        errors.append("structural reference metadata is malformed")
        return
    metadata_path = _repository_path(
        repo,
        reproducibility.get("metadata_manifest_path"),
        errors,
        "structural snapshot metadata path",
    )
    manifest_path = _repository_path(
        repo, reproducibility.get("manifest_path"), errors, "structural per-file manifest path"
    )
    if metadata_path is None or not metadata_path.is_file():
        errors.append("structural snapshot metadata manifest is missing")
        return
    if manifest_path is None or not manifest_path.is_file():
        errors.append("structural per-file manifest is missing")
        return
    metadata = _load_object(metadata_path, errors, "structural snapshot metadata")
    if metadata is None:
        return
    if (
        metadata.get("manifest_status") != "MATERIALIZED_LOCAL_PRIVATE_SNAPSHOT"
        or metadata.get("durable_snapshot_status") != "PENDING_DURABLE_HOSTING"
        or reproducibility.get("availability") != "LOCAL_PRIVATE_ONLY"
        or reproducibility.get("status") != "PENDING_DURABLE_HOSTING"
    ):
        errors.append("structural snapshot availability/hosting status differs")
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    per_file_metadata = metadata.get("per_file_manifest", {})
    snapshot_metadata = metadata.get("snapshot_archive", {})
    if not isinstance(per_file_metadata, dict):
        errors.append("structural per-file manifest metadata is malformed")
        per_file_metadata = {}
    if not isinstance(snapshot_metadata, dict):
        errors.append("structural snapshot archive metadata is malformed")
        snapshot_metadata = {}
    if per_file_metadata.get("path") != reproducibility.get("manifest_path"):
        errors.append("structural per-file manifest locators disagree")
    if per_file_metadata.get("size") != len(manifest_bytes):
        errors.append("structural per-file manifest byte size differs")
    declared_manifest_hashes = {
        reproducibility.get("manifest_sha256"),
        source.get("snapshot_manifest_sha256"),
        metadata.get("content_identity", {}).get("sha256")
        if isinstance(metadata.get("content_identity"), dict)
        else None,
        metadata.get("per_file_manifest", {}).get("sha256")
        if isinstance(metadata.get("per_file_manifest"), dict)
        else None,
    }
    if declared_manifest_hashes != {manifest_hash}:
        errors.append("structural per-file manifest identities disagree")
    if not manifest_bytes.endswith(b"\n") or b"\r" in manifest_bytes:
        errors.append("structural per-file manifest is not canonical LF text")
    records: list[tuple[str, int, str]] = []
    try:
        for line in manifest_bytes.decode("utf-8").splitlines():
            relative, size, digest = line.split("\t")
            if _safe_member_path(relative) != relative:
                raise ValueError(f"unsafe or noncanonical path: {relative}")
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError(f"malformed SHA-256: {relative}")
            records.append((relative, int(size), digest))
    except (UnicodeDecodeError, ValueError) as error:
        errors.append(f"invalid structural per-file manifest: {error}")
        return
    if [item[0] for item in records] != sorted(
        (item[0] for item in records), key=lambda value: value.encode("utf-8")
    ) or len({item[0] for item in records}) != len(records):
        errors.append("structural per-file manifest paths are not unique ordinal order")
    scope = metadata.get("snapshot_scope", {})
    if not isinstance(scope, dict) or scope.get("file_count") != len(records):
        errors.append("structural snapshot file count differs")
    if not isinstance(scope, dict) or scope.get("total_bytes") != sum(item[1] for item in records):
        errors.append("structural snapshot byte total differs")

    local_path = _repository_path(repo, source.get("local_path"), errors, "structural local path")
    if local_path is not None and local_path.is_dir():
        for relative, size, digest in records:
            path = local_path / Path(*PurePosixPath(relative).parts)
            if not path.is_file():
                errors.append(f"missing structural snapshot file: {relative}")
            elif path.stat().st_size != size or sha256_file(path) != digest:
                errors.append(f"structural snapshot file identity differs: {relative}")
        selected = _run_git(
            repo,
            "-c",
            f"safe.directory={local_path.as_posix()}",
            "-C",
            str(local_path),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        )
        if selected.returncode != 0:
            errors.append(f"cannot inventory local structural snapshot: {selected.stderr.strip()}")
        else:
            selected_paths = sorted(
                {item for item in selected.stdout.split("\0") if item},
                key=lambda value: value.encode("utf-8"),
            )
            if selected_paths != [item[0] for item in records]:
                errors.append("local structural snapshot selection differs from manifest")
    else:
        warnings.append("local private structural snapshot tree is unavailable")

    snapshot_path = _repository_path(
        repo, reproducibility.get("locator"), errors, "structural snapshot archive path"
    )
    expected_snapshot_hash = reproducibility.get("snapshot_sha256")
    expected_snapshot_size = reproducibility.get("snapshot_size")
    if (
        snapshot_metadata.get("local_path") != reproducibility.get("locator")
        or snapshot_metadata.get("sha256") != expected_snapshot_hash
        or snapshot_metadata.get("size") != expected_snapshot_size
        or snapshot_metadata.get("availability") != "LOCAL_PRIVATE_ONLY"
        or snapshot_metadata.get("tracked") is not False
    ):
        errors.append("structural snapshot archive identities/status disagree")
    if snapshot_path is not None and snapshot_path.is_file():
        if sha256_file(snapshot_path) != expected_snapshot_hash:
            errors.append("structural snapshot ZIP SHA-256 differs")
        if snapshot_path.stat().st_size != expected_snapshot_size:
            errors.append("structural snapshot ZIP size differs")
        expected_members = Counter(records)
        actual_members = _actual_archive_members(snapshot_path, errors)
        if actual_members != expected_members:
            errors.append("structural snapshot ZIP contents differ from per-file manifest")
    else:
        warnings.append("local private structural snapshot ZIP is unavailable")

    for private_path, label in ((local_path, "structural working tree"), (snapshot_path, "structural ZIP")):
        if private_path is None or not private_path.exists():
            continue
        relative = private_path.relative_to(repo).as_posix()
        tracked = _run_git(repo, "ls-files", "--error-unmatch", "--", relative)
        if tracked.returncode == 0:
            errors.append(f"private {label} is tracked by the main repository")
        ignored = _run_git(repo, "check-ignore", "-q", "--", relative)
        if ignored.returncode != 0:
            errors.append(f"private {label} is not covered by .gitignore")

    evidence["structural_snapshot"] = {
        "manifest_sha256": manifest_hash,
        "files": len(records),
        "bytes": sum(item[1] for item in records),
        "snapshot_sha256": expected_snapshot_hash,
        "snapshot_size": expected_snapshot_size,
    }


def _validate_reference_registry(
    repo: Path,
    state: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    evidence: dict[str, Any],
    *,
    freeze_required: bool,
) -> None:
    registry_pointer = state.get("registries", {})
    if not isinstance(registry_pointer, dict):
        return
    relative = registry_pointer.get("reference_registry_path", "state/REFERENCE_REGISTRY.json")
    path = _repository_path(repo, relative, errors, "reference registry path")
    if path is None:
        return
    if not path.is_file():
        errors.append(f"missing reference registry: {relative}")
        return
    registry = _load_object(path, errors, "reference registry")
    if registry is None:
        return
    _schema_validate(
        registry,
        repo / "schemas" / "reference_registry.schema.json",
        errors,
        "REFERENCE_REGISTRY",
    )
    _validate_declared_sha256(
        path,
        registry_pointer.get("reference_registry_sha256"),
        errors,
        "reference registry",
        required=freeze_required,
    )
    projects = registry.get("projects")
    if not isinstance(projects, list):
        errors.append("reference registry projects must be an array")
        return

    modules_path = repo / ".gitmodules"
    parser = configparser.ConfigParser(interpolation=None)
    if modules_path.is_file():
        try:
            parser.read(modules_path, encoding="utf-8")
        except configparser.Error as error:
            errors.append(f"invalid .gitmodules: {error}")
    submodule_declarations: dict[str, str] = {}
    for section in parser.sections():
        if not section.startswith('submodule "'):
            continue
        locator = parser.get(section, "path", fallback="")
        url = parser.get(section, "url", fallback="")
        if locator:
            submodule_declarations[PurePosixPath(locator).as_posix()] = url

    project_ids: set[str] = set()
    submodule_evidence: dict[str, str] = {}
    expected_submodule_locators: set[str] = set()
    for project in projects:
        if not isinstance(project, dict):
            errors.append("reference project is not an object")
            continue
        project_id = project.get("id")
        if not isinstance(project_id, str) or project_id in project_ids:
            errors.append(f"duplicate or malformed reference project id: {project_id}")
            continue
        project_ids.add(project_id)
        if project.get("authority_classification") != "NON_AUTHORITATIVE_REFERENCE":
            errors.append(f"reference project authority is not quarantined: {project_id}")
        reproducibility = project.get("reproducibility", {})
        source = project.get("source", {})
        if not isinstance(reproducibility, dict) or not isinstance(source, dict):
            errors.append(f"reference project metadata is malformed: {project_id}")
            continue
        mechanism = reproducibility.get("mechanism")
        if mechanism == "PINNED_GIT_SUBMODULE":
            locator = reproducibility.get("locator")
            commit = reproducibility.get("commit")
            url = source.get("repository_url")
            if source.get("local_path", locator) != locator:
                errors.append(f"reference source locator is stale: {project_id}")
            if not isinstance(locator, str) or submodule_declarations.get(locator) != url:
                errors.append(f"submodule declaration differs from reference registry: {project_id}")
                continue
            expected_submodule_locators.add(locator)
            mode, index_commit = _gitlink_identity(repo, locator)
            if mode != "160000" or index_commit != commit:
                errors.append(f"superproject gitlink pin differs: {project_id}")
            checkout = _repository_path(repo, locator, errors, f"submodule locator {project_id}")
            if checkout is None or not checkout.is_dir() or not (checkout / ".git").exists():
                warnings.append(
                    f"submodule checkout is not materialized; immutable gitlink remains available: {project_id}"
                )
            else:
                head = _run_git(
                    repo,
                    "-c",
                    f"safe.directory={checkout.as_posix()}",
                    "-C",
                    str(checkout),
                    "rev-parse",
                    "HEAD",
                )
                if head.returncode != 0 or head.stdout.strip() != commit:
                    errors.append(f"submodule worktree pin differs: {project_id}")
                remote = _run_git(
                    repo,
                    "-c",
                    f"safe.directory={checkout.as_posix()}",
                    "-C",
                    str(checkout),
                    "remote",
                    "get-url",
                    "origin",
                )
                if remote.returncode != 0 or remote.stdout.strip() != url:
                    errors.append(f"submodule origin differs: {project_id}")
                status = _run_git(
                    repo,
                    "-c",
                    f"safe.directory={checkout.as_posix()}",
                    "-C",
                    str(checkout),
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                )
                if status.returncode != 0:
                    errors.append(f"cannot inspect submodule worktree: {project_id}")
                elif status.stdout.strip():
                    errors.append(f"submodule tracked/nonignored worktree is dirty: {project_id}")
            if isinstance(commit, str):
                submodule_evidence[project_id] = commit
        elif mechanism == "PRIVATE_SNAPSHOT_MANIFEST":
            _validate_structural_snapshot(repo, project, errors, warnings, evidence)
        else:
            errors.append(f"unknown reference reproducibility mechanism: {project_id}")

    expected_ids = {
        "decision-coordinates",
        "structural-invariants-endgames",
        "solvingchess-public-legacy",
    }
    if project_ids != expected_ids:
        errors.append(f"reference registry project set differs: {sorted(project_ids)}")
    if set(submodule_declarations) != expected_submodule_locators:
        errors.append(".gitmodules contains missing or unregistered submodule declarations")
    evidence["submodule_pins"] = submodule_evidence


def _validate_bootstrap_boundary(repo: Path, state: dict[str, Any], errors: list[str]) -> None:
    latest = resolve_latest_completed(state)
    next_programme = resolve_next_programme(state)
    if latest != 13 or next_programme != 14 or next_started(state):
        return
    g14 = repo / "research" / "G14"
    if g14.is_dir():
        forbidden = sorted(
            path.relative_to(repo).as_posix()
            for path in g14.rglob("*")
            if path.is_file() and path.name != "README.md"
        )
        if forbidden:
            errors.append("G14 scientific output exists before start: " + ", ".join(forbidden))
    for forbidden in (
        repo / "research" / "G14" / "G14_Technical_Handoff.md",
        repo / "research" / "G14" / "G14_Freeze_Manifest.json",
    ):
        if forbidden.exists():
            errors.append(f"G14 closeout artifact exists before start: {forbidden.relative_to(repo)}")


def validate_repository(repo: Path, *, require_clean: bool = False) -> dict[str, Any]:
    repo = Path(repo).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    evidence: dict[str, Any] = {}
    required = (
        "AGENTS.md",
        "docs/RESEARCH_PROTOCOL.md",
        "state/PROGRAM_STATE.json",
        "state/AUTONOMY_STATE.json",
        "schemas/program_state.schema.json",
        "schemas/autonomy_state.schema.json",
        "schemas/g_completion.schema.json",
        "schemas/g_completion.output.schema.json",
    )
    for relative in required:
        if not (repo / relative).is_file():
            errors.append(f"missing required file: {relative}")

    state: dict[str, Any] | None = None
    state_path = repo / "state" / "PROGRAM_STATE.json"
    if state_path.is_file():
        try:
            loaded = load_json(state_path)
            if not isinstance(loaded, dict):
                raise ValueError("root must be an object")
            state = loaded
            _schema_validate(state, repo / "schemas" / "program_state.schema.json", errors, "PROGRAM_STATE")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"invalid state/PROGRAM_STATE.json: {error}")

    autonomy_path = repo / "state" / "AUTONOMY_STATE.json"
    if autonomy_path.is_file():
        try:
            autonomy = load_json(autonomy_path)
            if not isinstance(autonomy, dict):
                raise ValueError("root must be an object")
            _schema_validate(
                autonomy,
                repo / "schemas" / "autonomy_state.schema.json",
                errors,
                "AUTONOMY_STATE",
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"invalid state/AUTONOMY_STATE.json: {error}")

    programme = None
    latest = None
    if state is not None:
        try:
            programme = resolve_next_programme(state)
            latest = resolve_latest_completed(state)
            if latest is not None and programme != latest + 1:
                errors.append(
                    f"non-sequential route: latest {format_programme(latest)}, next {format_programme(programme)}"
                )
            if not next_authorized(state):
                errors.append(f"{format_programme(programme)} is not authorized")
            if next_started(state):
                errors.append(f"{format_programme(programme)} is already marked started")
        except ValueError as error:
            errors.append(str(error))

        if state.get("project_id") == "solving-chess":
            bootstrap = state.get("repository_bootstrap", {})
            freeze_required = bool(
                isinstance(bootstrap, dict)
                and bootstrap.get("completion_status") == "COMPLETE"
                and bootstrap.get("autonomous_loop_readiness") == "READY"
            )
            _validate_authority_bindings(repo, state, errors)
            _validate_artifact_registry(
                repo,
                state,
                errors,
                evidence,
                freeze_required=freeze_required,
            )
            _validate_reference_registry(
                repo,
                state,
                errors,
                warnings,
                evidence,
                freeze_required=freeze_required,
            )
            try:
                _validate_bootstrap_boundary(repo, state, errors)
            except ValueError as error:
                errors.append(str(error))

    git_check = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if git_check.returncode != 0 or git_check.stdout.strip() != "true":
        errors.append("repository is not a Git worktree")
    elif require_clean:
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if status.returncode != 0:
            errors.append(f"cannot inspect Git status: {status.stderr.strip()}")
        elif status.stdout.strip():
            errors.append("starting worktree is not clean")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "evidence": evidence,
        "next_programme": format_programme(programme) if programme is not None else None,
        "latest_completed_programme": format_programme(latest) if latest is not None else None,
        "repository": str(repo),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    result = validate_repository(args.repo, require_clean=args.require_clean)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
