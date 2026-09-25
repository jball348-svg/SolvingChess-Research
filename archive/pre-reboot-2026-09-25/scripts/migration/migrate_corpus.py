#!/usr/bin/env python3
"""Plan or apply the immutable Solving Chess historical-corpus migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import zipfile
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

try:
    from .docx_to_markdown import TOOL_NAME, TOOL_VERSION, convert_docx
    from .inventory import (
        EXPECTED_PRIMARY_BYTES,
        EXPECTED_PRIMARY_COUNT,
        SourceFile,
        canonical_json_bytes,
        discover_primary_corpus,
        sha256_bytes,
        sha256_file,
        source_summary,
    )
except ImportError:  # pragma: no cover
    from docx_to_markdown import TOOL_NAME, TOOL_VERSION, convert_docx
    from inventory import (
        EXPECTED_PRIMARY_BYTES,
        EXPECTED_PRIMARY_COUNT,
        SourceFile,
        canonical_json_bytes,
        discover_primary_corpus,
        sha256_bytes,
        sha256_file,
        source_summary,
    )

REGISTRY_SCHEMA_VERSION = "1.0.0"
REGISTRY_KIND = "MIGRATION_ARTIFACT_REGISTRY"
DEFAULT_MIGRATION_TIMESTAMP = "2026-08-13T00:00:00Z"
TARGET_G12_SHA256 = "7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c"

ROADMAP_FILES = frozenset(
    {
        "G9_G10_Onwards_Long_Range_Plan.docx",
        "G9_Review_Road_to_100_Planning_Kickoff_Memo.docx",
        "G9_Road_to_100_Assessment.docx",
        "G9_What_We_Have_Done_Plain_English.docx",
    }
)

_CHECKSUM = re.compile(r"^\s*([0-9a-fA-F]{64})\s+\*?(.+?)\s*$")


class MigrationError(RuntimeError):
    pass


@dataclass(frozen=True)
class MigrationPlan:
    registry: dict[str, object]
    original_writes: tuple[tuple[Path, Path], ...]
    derivative_writes: tuple[tuple[Path, bytes], ...]
    audit_writes: tuple[tuple[Path, bytes], ...]
    strict_source_verified: bool


def _utf8_key(value: str) -> bytes:
    return value.encode("utf-8")


def _programme(name: str) -> str | None:
    if name.startswith(("Pilot_", "pilot")):
        return "PILOT"
    match = re.match(r"^[Gg](\d+)", name)
    return f"G{int(match.group(1))}" if match else None


def _role(name: str) -> str:
    lowered = name.lower()
    if name in ROADMAP_FILES:
        return "ROADMAP_OR_STRATEGIC_DOCUMENT"
    if "technical_handoff" in lowered and lowered.endswith(".docx"):
        return "TECHNICAL_HANDOFF"
    if lowered.endswith(".docx"):
        return "HUMAN_DOCUMENT"
    if lowered.endswith((".zip", ".tar.gz")):
        return "ARCHIVE"
    if lowered.endswith(".bin"):
        return "BINARY_ARTIFACT"
    if lowered.endswith((".json", ".csv", ".txt")):
        return "MACHINE_OR_LEDGER_ARTIFACT"
    if lowered.endswith(".cpp"):
        return "SOURCE_CODE"
    if lowered.endswith(".md"):
        return "HUMAN_OR_LEDGER_DOCUMENT"
    return "LEGACY_ARTIFACT"


def destination_for(name: str) -> tuple[PurePosixPath, PurePosixPath | None]:
    if name in ROADMAP_FILES:
        category = "roadmap"
    elif "technical_handoff" in name.lower() and name.lower().endswith(".docx"):
        category = "handoffs"
    else:
        category = "legacy"
    original = PurePosixPath(category, "originals", name)
    normalized = (
        PurePosixPath(category, "normalized", f"{Path(name).stem}.md")
        if name.lower().endswith(".docx")
        else None
    )
    return original, normalized


def _archive_members(source: SourceFile, occurrence_id: str) -> list[dict[str, object]]:
    lowered = source.name.lower()
    if not lowered.endswith((".zip", ".tar.gz")):
        return []
    members: list[dict[str, object]] = []
    if lowered.endswith(".zip"):
        try:
            with zipfile.ZipFile(source.path) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    raise MigrationError(f"archive CRC failure in {source.name}!{bad_member}")
                for member in sorted(
                    (info for info in archive.infolist() if not info.is_dir()),
                    key=lambda info: _utf8_key(PurePosixPath(info.filename).as_posix()),
                ):
                    path = _safe_archive_member_path(source.name, member.filename)
                    payload = archive.read(member)
                    digest = sha256_bytes(payload)
                    members.append(
                        _archive_member_record(
                            source, occurrence_id, path, len(payload), digest
                        )
                    )
        except zipfile.BadZipFile as exc:
            raise MigrationError(f"invalid ZIP {source.name}: {exc}") from exc
        return members

    try:
        with tarfile.open(source.path, "r:gz") as archive:
            for member in sorted(
                (item for item in archive.getmembers() if item.isfile()),
                key=lambda item: _utf8_key(PurePosixPath(item.name).as_posix()),
            ):
                stream = archive.extractfile(member)
                if stream is None:
                    raise MigrationError(
                        f"cannot read regular archive member {source.name}!{member.name}"
                    )
                digest = hashlib.sha256()
                observed_size = 0
                while True:
                    chunk = stream.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    observed_size += len(chunk)
                if observed_size != member.size:
                    raise MigrationError(
                        f"archive member size mismatch {source.name}!{member.name}: "
                        f"read {observed_size}, header says {member.size}"
                    )
                members.append(
                    _archive_member_record(
                        source,
                        occurrence_id,
                        _safe_archive_member_path(source.name, member.name),
                        observed_size,
                        digest.hexdigest(),
                    )
                )
    except (tarfile.TarError, OSError) as exc:
        raise MigrationError(f"invalid TAR.GZ {source.name}: {exc}") from exc
    return members


def _safe_archive_member_path(container: str, value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or not path.parts or any(part == ".." for part in path.parts):
        raise MigrationError(f"unsafe archive member path {container}!{value}")
    return path.as_posix()


def _archive_member_record(
    source: SourceFile,
    occurrence_id: str,
    path: str,
    size: int,
    digest: str,
) -> dict[str, object]:
    return {
        "id": f"archive-member:sha256:{source.sha256}:{path}",
        "container_occurrence_id": occurrence_id,
        "container_sha256": source.sha256,
        "path": path,
        "size": size,
        "sha256": digest,
        "content_id": f"sha256:{digest}",
        "availability": "PRESENT_INSIDE_ARCHIVE",
    }


def _checksum_references(source: SourceFile) -> list[tuple[str, str, int]]:
    if "sha" not in source.name.lower() or not source.name.lower().endswith(".txt"):
        return []
    try:
        text = source.path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = source.path.read_text(encoding="cp1252")
    result: list[tuple[str, str, int]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = _CHECKSUM.match(line)
        if match:
            result.append(
                (match.group(1).lower(), PurePosixPath(match.group(2)).name, line_number)
            )
    return result


def _parse_checksum_payload(payload: bytes) -> list[tuple[str, str, int]]:
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            text = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:  # pragma: no cover - cp1252 decodes all byte sequences
        text = payload.decode("utf-8", "replace")
    result: list[tuple[str, str, int]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = _CHECKSUM.match(line)
        if match:
            result.append(
                (
                    match.group(1).lower(),
                    PurePosixPath(match.group(2).replace("\\", "/")).as_posix(),
                    line_number,
                )
            )
    return result


def _archive_checksum_payloads(source: SourceFile) -> list[tuple[str, bytes]]:
    lowered = source.name.lower()
    result: list[tuple[str, bytes]] = []
    if lowered.endswith(".zip"):
        with zipfile.ZipFile(source.path) as archive:
            for member in sorted(archive.infolist(), key=lambda item: _utf8_key(item.filename)):
                if member.is_dir() or "sha" not in PurePosixPath(member.filename).name.lower():
                    continue
                payload = archive.read(member)
                if _parse_checksum_payload(payload):
                    result.append(
                        (_safe_archive_member_path(source.name, member.filename), payload)
                    )
    elif lowered.endswith(".tar.gz"):
        with tarfile.open(source.path, "r:gz") as archive:
            for member in sorted(archive.getmembers(), key=lambda item: _utf8_key(item.name)):
                if not member.isfile() or "sha" not in PurePosixPath(member.name).name.lower():
                    continue
                stream = archive.extractfile(member)
                if stream is None:
                    raise MigrationError(
                        f"cannot read checksum member {source.name}!{member.name}"
                    )
                payload = stream.read()
                if _parse_checksum_payload(payload):
                    result.append(
                        (_safe_archive_member_path(source.name, member.name), payload)
                    )
    return result


def _audit_internal_archive_checksums(
    files: Iterable[SourceFile],
    occurrence_by_name: dict[str, str],
    archive_members: list[dict[str, object]],
    *,
    strict_source: bool,
) -> dict[str, object]:
    members_by_container: dict[str, list[dict[str, object]]] = defaultdict(list)
    for member in archive_members:
        members_by_container[str(member["container_occurrence_id"])].append(member)

    manifests: list[dict[str, object]] = []
    reference_count = 0
    resolved_exact = 0
    missing: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    for source in files:
        occurrence_id = occurrence_by_name[source.name]
        container_members = members_by_container.get(occurrence_id, [])
        for manifest_path, payload in _archive_checksum_payloads(source):
            entries = _parse_checksum_payload(payload)
            manifest_exact = 0
            manifest_missing = 0
            manifest_mismatches = 0
            manifest_directory = PurePosixPath(manifest_path).parent
            for expected_hash, referenced_path, line_number in entries:
                reference_count += 1
                supplied = PurePosixPath(referenced_path)
                relative = (
                    supplied.as_posix().lstrip("/")
                    if supplied.is_absolute()
                    else (manifest_directory / supplied).as_posix()
                )
                basename = supplied.name
                candidates = [
                    member
                    for member in container_members
                    if str(member["path"]) in {referenced_path.lstrip("/"), relative}
                    or PurePosixPath(str(member["path"])).name == basename
                ]
                exact = [member for member in candidates if member["sha256"] == expected_hash]
                if exact:
                    resolved_exact += 1
                    manifest_exact += 1
                elif candidates:
                    manifest_mismatches += 1
                    mismatches.append(
                        {
                            "container_occurrence_id": occurrence_id,
                            "manifest_path": manifest_path,
                            "line": line_number,
                            "referenced_path": referenced_path,
                            "expected_sha256": expected_hash,
                            "observed": [
                                {"path": item["path"], "sha256": item["sha256"]}
                                for item in candidates
                            ],
                        }
                    )
                else:
                    manifest_missing += 1
                    missing.append(
                        {
                            "container_occurrence_id": occurrence_id,
                            "manifest_path": manifest_path,
                            "line": line_number,
                            "referenced_path": referenced_path,
                            "expected_sha256": expected_hash,
                        }
                    )
            manifests.append(
                {
                    "container_occurrence_id": occurrence_id,
                    "container_source_name": source.name,
                    "path": manifest_path,
                    "sha256": sha256_bytes(payload),
                    "entry_count": len(entries),
                    "resolved_exact": manifest_exact,
                    "missing": manifest_missing,
                    "mismatches": manifest_mismatches,
                    "status": (
                        "PASS"
                        if manifest_exact == len(entries)
                        else "FAIL"
                    ),
                }
            )

    if strict_source and (len(manifests) != 11 or reference_count != 152):
        raise MigrationError(
            "internal archive checksum invariant failed: "
            f"manifests={len(manifests)} (expected 11), "
            f"references={reference_count} (expected 152)"
        )
    if missing or mismatches:
        raise MigrationError(
            "internal archive checksum failure: "
            f"missing={len(missing)}, mismatches={len(mismatches)}"
        )
    return {
        "status": "PASS",
        "manifest_occurrences": len(manifests),
        "reference_count": reference_count,
        "resolved_exact": resolved_exact,
        "missing": missing,
        "mismatches": mismatches,
        "manifests": manifests,
    }


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=destination.name + ".", dir=destination.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as output, source.open("rb") as input_stream:
            shutil.copyfileobj(input_stream, output)
            output.flush()
            os.fsync(output.fileno())
        if sha256_file(Path(temporary_name)) != sha256_file(source):
            raise MigrationError(f"post-copy hash mismatch for {source}")
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _atomic_write(destination: Path, payload: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=destination.name + ".", dir=destination.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _check_safe_target(root: Path, destination: Path) -> None:
    try:
        relative = destination.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise MigrationError(f"migration destination escapes repository: {destination}") from exc
    if not relative.parts or relative.parts[0] not in {"roadmap", "handoffs", "legacy"}:
        raise MigrationError(f"migration destination is outside approved roots: {destination}")


def _check_safe_registry_target(root: Path, destination: Path) -> None:
    try:
        relative = destination.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise MigrationError(f"registry destination escapes repository: {destination}") from exc
    if relative != "state/ARTIFACT_REGISTRY.json":
        raise MigrationError(
            "registry destination must be exactly state/ARTIFACT_REGISTRY.json: "
            f"{destination}"
        )


def _ensure_not_conflicting(destination: Path, expected: bytes | Path) -> None:
    if not destination.exists():
        return
    observed = sha256_file(destination)
    expected_hash = sha256_file(expected) if isinstance(expected, Path) else sha256_bytes(expected)
    if observed != expected_hash:
        raise MigrationError(
            f"refusing to replace different existing bytes at {destination}; "
            f"observed {observed}, expected {expected_hash}"
        )


def build_plan(
    root: Path,
    *,
    generated_at: str = DEFAULT_MIGRATION_TIMESTAMP,
    strict_source: bool = True,
    include_archive_members: bool = True,
) -> MigrationPlan:
    root = root.resolve()
    files = discover_primary_corpus(root, strict=strict_source)
    present_by_basename: dict[str, list[SourceFile]] = defaultdict(list)
    for source in files:
        present_by_basename[source.name].append(source)

    contents: dict[str, dict[str, object]] = {}
    occurrences: list[dict[str, object]] = []
    archive_members: list[dict[str, object]] = []
    original_writes: list[tuple[Path, Path]] = []
    derivative_writes: list[tuple[Path, bytes]] = []
    audit_writes: list[tuple[Path, bytes]] = []
    conversion_audits: list[dict[str, object]] = []
    occurrence_by_name: dict[str, str] = {}

    for index, source in enumerate(files, 1):
        original_rel, normalized_rel = destination_for(source.name)
        occurrence_id = f"occurrence:{index:04d}"
        occurrence_by_name[source.name] = occurrence_id
        occurrences.append(
            {
                "id": occurrence_id,
                "source_name": source.name,
                "repository_path": original_rel.as_posix(),
                "sha256": source.sha256,
                "size": source.size,
                "role": _role(source.name),
                "availability": "PRESENT",
                "content_id": f"sha256:{source.sha256}",
                "programme": _programme(source.name),
                "source_scope": "PRIMARY_INHERITED_CORPUS",
            }
        )
        content = contents.setdefault(
            source.sha256,
            {
                "content_id": f"sha256:{source.sha256}",
                "sha256": source.sha256,
                "size": source.size,
                "media_type": source.media_type,
                "occurrence_ids": [],
                "immutability": "FROZEN_ORIGINAL_BYTES",
            },
        )
        content["occurrence_ids"].append(occurrence_id)  # type: ignore[index]
        original_writes.append((source.path, root / Path(*original_rel.parts)))

        if include_archive_members:
            archive_members.extend(_archive_members(source, occurrence_id))

        if normalized_rel is not None:
            result = convert_docx(
                source.path,
                derivative_filename=normalized_rel.name,
                conversion_timestamp=generated_at,
            )
            normalized_path = root / Path(*normalized_rel.parts)
            audit_rel = PurePosixPath(
                normalized_rel.parent,
                normalized_rel.name + ".conversion.json",
            )
            audit = dict(result.audit)
            audit["source"]["repository_path"] = original_rel.as_posix()  # type: ignore[index]
            audit["derivative"]["repository_path"] = normalized_rel.as_posix()  # type: ignore[index]
            audit["audit_path"] = audit_rel.as_posix()
            derivative_writes.append((normalized_path, result.markdown))
            audit_writes.append(
                (root / Path(*audit_rel.parts), canonical_json_bytes(audit))
            )
            conversion_audits.append(
                {
                    "source_occurrence_id": occurrence_id,
                    "source_sha256": source.sha256,
                    "derivative_path": normalized_rel.as_posix(),
                    "derivative_sha256": sha256_bytes(result.markdown),
                    "audit_path": audit_rel.as_posix(),
                    "status": audit["status"],
                }
            )

    # Resolve checksum references against both supplied outer files and ZIP members.
    member_by_basename: dict[str, list[dict[str, object]]] = defaultdict(list)
    for member in archive_members:
        member_by_basename[PurePosixPath(str(member["path"])).name].append(member)
    expected_missing_map: dict[tuple[str, str], dict[str, object]] = {}
    resolved_checksum_references = 0
    checksum_mismatches: list[dict[str, object]] = []
    checksum_reference_count = 0
    for source in files:
        for expected_hash, expected_name, line_number in _checksum_references(source):
            checksum_reference_count += 1
            candidates: list[tuple[str, str]] = []
            candidates.extend(
                (candidate.sha256, candidate.name)
                for candidate in present_by_basename.get(expected_name, [])
            )
            candidates.extend(
                (str(candidate["sha256"]), f"{candidate['container_occurrence_id']}!{candidate['path']}")
                for candidate in member_by_basename.get(expected_name, [])
            )
            if any(digest == expected_hash for digest, _ in candidates):
                resolved_checksum_references += 1
            elif candidates:
                checksum_mismatches.append(
                    {
                        "checksum_file": source.name,
                        "line": line_number,
                        "expected_name": expected_name,
                        "expected_sha256": expected_hash,
                        "observed_candidates": [
                            {"location": location, "sha256": digest}
                            for digest, location in candidates
                        ],
                    }
                )
            else:
                key = expected_hash, expected_name
                record = expected_missing_map.setdefault(
                    key,
                    {
                        "id": f"expected:sha256:{expected_hash}:{expected_name}",
                        "source_name": expected_name,
                        "repository_path": None,
                        "sha256": expected_hash,
                        "size": None,
                        "role": "EXPECTED_HISTORICAL_ARTIFACT",
                        "availability": "EXPECTED_ONLY_MISSING_FROM_MIGRATION_INPUT",
                        "content_id": f"sha256:{expected_hash}",
                        "programme": "G7" if expected_name.lower().startswith("g7") else None,
                        "referenced_by": [],
                        "integrity_status": "NOT_CORRUPTION_NO_BYTES_SUPPLIED",
                    },
                )
                record["referenced_by"].append(  # type: ignore[index]
                    {"checksum_file": source.name, "line": line_number}
                )

    expected_missing = sorted(
        expected_missing_map.values(), key=lambda item: _utf8_key(str(item["id"]))
    )
    if strict_source and len(expected_missing) != 63:
        raise MigrationError(
            f"expected 63 absent checksum references at frozen seam, found {len(expected_missing)}"
        )
    if checksum_mismatches:
        raise MigrationError(
            f"present checksum candidates disagree for {len(checksum_mismatches)} references"
        )

    internal_archive_checksum_audit = _audit_internal_archive_checksums(
        files,
        occurrence_by_name,
        archive_members,
        strict_source=strict_source,
    ) if include_archive_members else {
        "status": "NOT_RUN",
        "reason": "archive member inventory disabled",
        "manifest_occurrences": 0,
        "reference_count": 0,
        "resolved_exact": 0,
        "missing": [],
        "mismatches": [],
        "manifests": [],
    }

    registry: dict[str, object] = {
        "schema_version": REGISTRY_SCHEMA_VERSION,
        "registry_kind": REGISTRY_KIND,
        "generated_at": generated_at,
        "source_summary": source_summary(files),
        "contents": sorted(contents.values(), key=lambda item: str(item["sha256"])),
        "occurrences": occurrences,
        "archive_members": sorted(
            archive_members, key=lambda item: _utf8_key(str(item["id"]))
        ),
        "expected_missing": expected_missing,
        "audits": {
            "source_invariants": {
                "status": "PASS",
                "count_and_byte_size_checked_before_apply": True,
            },
            "copy_policy": {
                "status": "PASS",
                "scope": "PRIMARY_INHERITED_CORPUS_ONLY",
                "verification_basis": (
                    "destination originals are byte-for-byte copies; archives remain "
                    "opaque; adjacent reference projects are outside migration scope"
                ),
                "original_bytes_changed": False,
                "archives_exploded": False,
                "other_projects_touched": False,
            },
            "checksum_references": {
                "total": checksum_reference_count,
                "resolved_exact": resolved_checksum_references,
                "expected_only": len(expected_missing),
                "present_hash_mismatches": checksum_mismatches,
            },
            "internal_archive_checksum_manifests": internal_archive_checksum_audit,
            "target_g12_bundle": {
                "expected_sha256": TARGET_G12_SHA256,
                "matching_occurrence_ids": [
                    occurrence["id"]
                    for occurrence in occurrences
                    if occurrence["sha256"] == TARGET_G12_SHA256
                ],
                "status": (
                    "FOUND_EXACTLY_ONCE"
                    if sum(
                        occurrence["sha256"] == TARGET_G12_SHA256
                        for occurrence in occurrences
                    )
                    == 1
                    else "UNEXPECTED_CARDINALITY"
                ),
            },
            "docx_conversion": {
                "method": TOOL_NAME,
                "tool_version": TOOL_VERSION,
                "conversion_count": len(conversion_audits),
                "records": conversion_audits,
            },
        },
    }
    return MigrationPlan(
        registry=registry,
        original_writes=tuple(original_writes),
        derivative_writes=tuple(derivative_writes),
        audit_writes=tuple(audit_writes),
        strict_source_verified=strict_source,
    )


def _verify_strict_relocation_sources(root: Path, plan: MigrationPlan) -> None:
    if not plan.strict_source_verified:
        raise MigrationError(
            "source removal is forbidden for a plan built without strict corpus verification"
        )
    if len(plan.original_writes) != EXPECTED_PRIMARY_COUNT:
        raise MigrationError(
            f"source removal requires exactly {EXPECTED_PRIMARY_COUNT} files, "
            f"plan contains {len(plan.original_writes)}"
        )
    planned_sources = [source.resolve() for source, _ in plan.original_writes]
    if len(set(planned_sources)) != len(planned_sources):
        raise MigrationError("source removal plan contains duplicate source paths")
    total_bytes = sum(source.stat().st_size for source in planned_sources)
    if total_bytes != EXPECTED_PRIMARY_BYTES:
        raise MigrationError(
            f"source removal requires exactly {EXPECTED_PRIMARY_BYTES} bytes, "
            f"plan contains {total_bytes}"
        )
    rediscovered = discover_primary_corpus(root, strict=True)
    if {item.path.resolve() for item in rediscovered} != set(planned_sources):
        raise MigrationError("source removal plan differs from freshly verified strict corpus")
    for source, destination in plan.original_writes:
        if source.parent.resolve() != root or source.is_symlink() or not source.is_file():
            raise MigrationError(f"unsafe relocation source: {source}")
        if destination.resolve() == source.resolve():
            raise MigrationError(f"relocation source equals destination: {source}")
        if not destination.is_file() or sha256_file(destination) != sha256_file(source):
            raise MigrationError(
                f"relocation destination is absent or differs from source: {destination}"
            )


def _finalize_relocation(root: Path, plan: MigrationPlan) -> None:
    """Remove the exact flat staging occurrences after all copies are verified.

    This intentionally uses explicit ``Path.unlink`` calls over the freshly
    rediscovered strict set.  It never accepts globs, directories, or computed
    paths outside the repository root.
    """

    _verify_strict_relocation_sources(root, plan)
    for source, _ in plan.original_writes:
        source.unlink()


def apply_plan(
    root: Path,
    plan: MigrationPlan,
    registry_path: Path,
    *,
    finalize_relocation: bool = False,
) -> None:
    root = root.resolve()
    for source, destination in plan.original_writes:
        _check_safe_target(root, destination)
        _ensure_not_conflicting(destination, source)
    for destination, payload in plan.derivative_writes + plan.audit_writes:
        _check_safe_target(root, destination)
        _ensure_not_conflicting(destination, payload)
    _check_safe_registry_target(root, registry_path)
    registry_payload = canonical_json_bytes(plan.registry)
    _ensure_not_conflicting(registry_path, registry_payload)

    for source, destination in plan.original_writes:
        if not destination.exists():
            _atomic_copy(source, destination)
        if sha256_file(destination) != sha256_file(source):
            raise MigrationError(f"post-apply original-byte mismatch at {destination}")
    for destination, payload in plan.derivative_writes + plan.audit_writes:
        if not destination.exists():
            _atomic_write(destination, payload)
    if not registry_path.exists():
        _atomic_write(registry_path, registry_payload)
    for destination, payload in plan.derivative_writes + plan.audit_writes:
        if sha256_file(destination) != sha256_bytes(payload):
            raise MigrationError(f"post-apply generated-byte mismatch at {destination}")
    if sha256_file(registry_path) != sha256_bytes(registry_payload):
        raise MigrationError(f"post-apply registry mismatch at {registry_path}")
    if finalize_relocation:
        _finalize_relocation(root, plan)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="plan and print only (default)")
    mode.add_argument("--apply", action="store_true", help="perform the planned copies/conversions")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("state/ARTIFACT_REGISTRY.json"),
    )
    parser.add_argument("--generated-at", default=DEFAULT_MIGRATION_TIMESTAMP)
    parser.add_argument(
        "--finalize-relocation",
        action="store_true",
        help=(
            "after --apply and complete hash verification, remove only the exact "
            "strict 129-file flat staging set"
        ),
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.finalize_relocation and not args.apply:
        parser.error("--finalize-relocation requires --apply")
    root = args.root.resolve()
    plan = build_plan(
        root,
        generated_at=args.generated_at,
        strict_source=True,
        include_archive_members=True,
    )
    registry_path = args.registry
    if not registry_path.is_absolute():
        registry_path = root / registry_path
    if args.apply:
        apply_plan(
            root,
            plan,
            registry_path,
            finalize_relocation=args.finalize_relocation,
        )
    summary = plan.registry["source_summary"]
    checksum = plan.registry["audits"]["checksum_references"]  # type: ignore[index]
    print(
        json.dumps(
            {
                "mode": (
                    "apply-finalize-relocation"
                    if args.finalize_relocation
                    else "apply" if args.apply else "dry-run"
                ),
                "source_count": summary["observed_count"],  # type: ignore[index]
                "source_bytes": summary["observed_total_bytes"],  # type: ignore[index]
                "original_occurrences": len(plan.registry["occurrences"]),
                "unique_contents": len(plan.registry["contents"]),
                "normalized_docx": plan.registry["audits"]["docx_conversion"][  # type: ignore[index]
                    "conversion_count"
                ],
                "archive_members": len(plan.registry["archive_members"]),
                "internal_archive_checksum_manifests": plan.registry["audits"][  # type: ignore[index]
                    "internal_archive_checksum_manifests"
                ]["manifest_occurrences"],
                "expected_missing": checksum["expected_only"],  # type: ignore[index]
                "sources_relocated": bool(args.finalize_relocation),
                "registry_path": registry_path.relative_to(root).as_posix(),
                "g14_started": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
