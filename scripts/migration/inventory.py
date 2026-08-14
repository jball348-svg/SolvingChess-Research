#!/usr/bin/env python3
"""Discover and inventory the immutable inherited Solving Chess corpus.

The inherited corpus is a flat, top-level staging collection.  Discovery is
deliberately narrower than "all files in the repository" so that bootstrap
files created alongside it cannot accidentally become historical artifacts.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

EXPECTED_PRIMARY_COUNT = 129
EXPECTED_PRIMARY_BYTES = 59_994_517
EXPECTED_PRIMARY_NAMESET_SHA256 = (
    "9c1437cf878ce2a3e99f9896dbb2094c93ec3a7f269872b95214c335c856df59"
)

_KNOWN_UNPREFIXED = frozenset(
    {
        "corrected_neutral.cpp",
        "corrected_rank.bin",
        "krk_cert.cpp",
        "neutral_rank.bin",
        "original_rank.bin",
        "pilot1_gate0.cpp",
    }
)
_ALLOWED_SUFFIXES = (
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


class CorpusInvariantError(RuntimeError):
    """Raised when the staging corpus no longer matches the frozen seam."""


@dataclass(frozen=True)
class SourceFile:
    path: Path
    name: str
    size: int
    sha256: str
    media_type: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def primary_name_is_eligible(name: str) -> bool:
    """Return whether *name* belongs to the inherited flat corpus.

    G14 and later names are intentionally rejected.  Files are considered only
    by callers that already established they are regular top-level files.
    """

    if not name.endswith(_ALLOWED_SUFFIXES):
        return False
    if name in _KNOWN_UNPREFIXED or name.startswith("Pilot_"):
        return True
    match = _G_PREFIX.match(name)
    return bool(match and 2 <= int(match.group(1)) <= 13)


def nameset_sha256(names: Iterable[str]) -> str:
    payload = "".join(f"{name}\n" for name in sorted(names, key=_utf8_key))
    return sha256_bytes(payload.encode("utf-8"))


def _utf8_key(value: str) -> bytes:
    return value.encode("utf-8")


def infer_media_type(name: str) -> str:
    lowered = name.lower()
    if lowered.endswith(".tar.gz"):
        return "application/gzip"
    overrides = {
        ".bin": "application/octet-stream",
        ".cpp": "text/x-c++src",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".md": "text/markdown",
    }
    suffix = Path(name).suffix.lower()
    return overrides.get(suffix) or mimetypes.guess_type(name)[0] or "application/octet-stream"


def discover_primary_corpus(root: Path, *, strict: bool = True) -> list[SourceFile]:
    root = root.resolve()
    if not root.is_dir():
        raise CorpusInvariantError(f"corpus root is not a directory: {root}")

    paths = sorted(
        (
            path
            for path in root.iterdir()
            if path.is_file() and primary_name_is_eligible(path.name)
        ),
        key=lambda path: _utf8_key(path.name),
    )
    total_bytes = sum(path.stat().st_size for path in paths)
    observed_nameset = nameset_sha256(path.name for path in paths)

    if strict:
        failures: list[str] = []
        if len(paths) != EXPECTED_PRIMARY_COUNT:
            failures.append(
                f"count {len(paths)} != expected {EXPECTED_PRIMARY_COUNT}"
            )
        if total_bytes != EXPECTED_PRIMARY_BYTES:
            failures.append(
                f"bytes {total_bytes} != expected {EXPECTED_PRIMARY_BYTES}"
            )
        if observed_nameset != EXPECTED_PRIMARY_NAMESET_SHA256:
            failures.append(
                "sorted name-set SHA-256 "
                f"{observed_nameset} != expected {EXPECTED_PRIMARY_NAMESET_SHA256}"
            )
        if failures:
            raise CorpusInvariantError("primary corpus invariant failed: " + "; ".join(failures))

    return [
        SourceFile(
            path=path,
            name=path.name,
            size=path.stat().st_size,
            sha256=sha256_file(path),
            media_type=infer_media_type(path.name),
        )
        for path in paths
    ]


def source_summary(files: Sequence[SourceFile]) -> dict[str, object]:
    hashes = {item.sha256 for item in files}
    return {
        "expected_count": EXPECTED_PRIMARY_COUNT,
        "expected_total_bytes": EXPECTED_PRIMARY_BYTES,
        "expected_nameset_sha256": EXPECTED_PRIMARY_NAMESET_SHA256,
        "observed_count": len(files),
        "observed_total_bytes": sum(item.size for item in files),
        "observed_unique_content_count": len(hashes),
        "observed_duplicate_occurrence_count": len(files) - len(hashes),
        "observed_nameset_sha256": nameset_sha256(item.name for item in files),
        "selection_policy": (
            "regular top-level Pilot and G2-G13 historical files plus six "
            "explicitly known unprefixed legacy files; future repository files "
            "and directories are excluded"
        ),
    }
