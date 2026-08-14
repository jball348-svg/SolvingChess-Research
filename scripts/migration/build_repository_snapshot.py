#!/usr/bin/env python3
"""Build a deterministic repository file manifest and local ZIP snapshot."""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
import tempfile
import zipfile
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

try:
    from .inventory import sha256_file
except ImportError:  # pragma: no cover
    from inventory import sha256_file

FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class SnapshotError(RuntimeError):
    pass


@dataclass(frozen=True)
class SnapshotResult:
    file_count: int
    total_bytes: int
    manifest_sha256: str
    zip_sha256: str
    skipped_gitlinks: tuple[str, ...]


def _run_git(root: Path, *arguments: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        check=False,
    )
    if process.returncode:
        raise SnapshotError(
            f"git {' '.join(arguments)} failed: "
            + process.stderr.decode("utf-8", "replace").strip()
        )
    return process.stdout


def git_snapshot_paths(root: Path) -> tuple[list[str], list[str]]:
    """Return regular tracked/nonignored paths and separately pinned gitlinks."""

    raw = _run_git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    candidates = sorted(
        {part.decode("utf-8") for part in raw.split(b"\0") if part},
        key=lambda value: value.encode("utf-8"),
    )
    index = _run_git(root, "ls-files", "--stage", "-z")
    gitlinks: set[str] = set()
    for record in index.split(b"\0"):
        if not record:
            continue
        metadata, _, path = record.partition(b"\t")
        if metadata.startswith(b"160000 "):
            gitlinks.add(path.decode("utf-8"))

    regular: list[str] = []
    skipped: list[str] = []
    for value in candidates:
        normalized = PurePosixPath(value).as_posix()
        if normalized in gitlinks:
            skipped.append(normalized)
            continue
        path = root / Path(*PurePosixPath(normalized).parts)
        if not path.is_file():
            raise SnapshotError(f"git-listed path is not a regular file: {normalized}")
        regular.append(normalized)
    return regular, skipped


def manifest_bytes(root: Path, paths: Sequence[str]) -> bytes:
    lines: list[str] = []
    for relative in sorted(set(paths), key=lambda value: value.encode("utf-8")):
        posix = PurePosixPath(relative).as_posix()
        if posix.startswith(("../", "/")):
            raise SnapshotError(f"path escapes repository: {relative}")
        path = root / Path(*PurePosixPath(posix).parts)
        if not path.is_file():
            raise SnapshotError(f"snapshot path is not a regular file: {posix}")
        if "\t" in posix or "\n" in posix or "\r" in posix:
            raise SnapshotError(f"path cannot be represented in manifest: {posix!r}")
        lines.append(f"{posix}\t{path.stat().st_size}\t{sha256_file(path)}\n")
    return "".join(lines).encode("utf-8")


def _relative_if_inside(root: Path, path: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def build_snapshot(
    root: Path,
    manifest_path: Path,
    zip_path: Path,
    *,
    paths: Sequence[str] | None = None,
    extra_excludes: Iterable[str] = (),
) -> SnapshotResult:
    root = root.resolve()
    skipped_gitlinks: list[str] = []
    if paths is None:
        selected, skipped_gitlinks = git_snapshot_paths(root)
    else:
        selected = list(paths)

    excluded = {PurePosixPath(value).as_posix() for value in extra_excludes}
    for output in (manifest_path, zip_path):
        relative = _relative_if_inside(root, output)
        if relative:
            excluded.add(relative)
    selected = [value for value in selected if PurePosixPath(value).as_posix() not in excluded]
    manifest = manifest_bytes(root, selected)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=zip_path.name + ".", dir=zip_path.parent)
    os.close(descriptor)
    try:
        with zipfile.ZipFile(
            temporary_name,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            archive.comment = b""
            for relative in sorted(set(selected), key=lambda value: value.encode("utf-8")):
                posix = PurePosixPath(relative).as_posix()
                payload = (root / Path(*PurePosixPath(posix).parts)).read_bytes()
                info = zipfile.ZipInfo(posix, FIXED_ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.flag_bits |= 0x800
                info.extra = b""
                info.comment = b""
                archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(temporary_name, zip_path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise

    _atomic_write(manifest_path, manifest)
    return SnapshotResult(
        file_count=len(set(selected)),
        total_bytes=sum(
            (root / Path(*PurePosixPath(value).parts)).stat().st_size
            for value in set(selected)
        ),
        manifest_sha256=sha256_file(manifest_path),
        zip_sha256=sha256_file(zip_path),
        skipped_gitlinks=tuple(sorted(skipped_gitlinks, key=lambda value: value.encode("utf-8"))),
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True)
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = build_snapshot(
        args.root,
        args.manifest,
        args.zip_path,
        extra_excludes=args.exclude,
    )
    print(
        f"files={result.file_count} bytes={result.total_bytes} "
        f"manifest_sha256={result.manifest_sha256} zip_sha256={result.zip_sha256}"
    )
    if result.skipped_gitlinks:
        print("skipped_gitlinks=" + ",".join(result.skipped_gitlinks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
