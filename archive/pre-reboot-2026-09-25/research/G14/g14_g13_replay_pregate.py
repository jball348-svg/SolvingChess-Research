"""Deterministic G14.0 diagnostic for the inherited G12-through-G13 replay gate.

This standard-library-only tool verifies the exact inherited G12 and G13 archives,
runs the frozen G13 input adapter in a temporary directory, and records why adapter
``READY`` is not the mandatory distributed/checkpoint acceptance replay.  It never
modifies or repacks an inherited artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path
from typing import Any


SCHEMA = "G14.G13.REPLAY.PREGATE.DIAGNOSTIC.v1"
G12_ARCHIVE = "G12_Final_Rules_Reference_Bundle.zip"
G13_ARCHIVE = "G13_Distributed_Compute_Bundle.zip"
G12_ARCHIVE_SHA256 = (
    "7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c"
)
G13_ARCHIVE_SHA256 = (
    "584a22452cdbc6b296e229d69bb1b1b01672ab0c840816dd5614aacda58ec3a5"
)
G12_SUMS = "G12_SHA256SUMS.txt"
G13_SUMS = "G13_SHA256SUMS.txt"
G12_SUMS_SHA256 = (
    "0ea65a5cea38867670f06a265afe016a30fb4e06952c1accba14258783226da3"
)
G13_SUMS_SHA256 = (
    "4a7f5e0bb12a8ddb9f7c95522e9b927c09e6d899f1e5de8a90b9e0b792d89324"
)
SUM_LINE_RE = re.compile(r"^([0-9a-f]{64})  ([^\r\n]+)$")

FROZEN_SOURCES: dict[str, dict[str, str]] = {
    G12_ARCHIVE: {
        "g12_suite.cpp": (
            "d759ccf161637a4b612a48f04f7ecab26b1fcab4204711030fe1c304ac40dfec"
        ),
        "g12_verifier.cpp": (
            "99cd9a3466169d558128df49a31416c54e380d10133740cb9c8f44fa00ed34ef"
        ),
    },
    G13_ARCHIVE: {
        "g13_failure_injection.py": (
            "343c22e18f30d8dbda5deab8e5ea3ab8d8ba5c4ac69c107d8040c458a784eed9"
        ),
        "g13_g12_adapter.py": (
            "1cc4bd229964f40d28feb84835b82df869838f604d031abdc87abccbb72c9530"
        ),
        "g13_platform.py": (
            "251989338b314ab3804b4fdf8f7a1fd7a90bcbd1e3a576708ea16588dc1feb00"
        ),
        "g13_reference_campaign.py": (
            "6044286ad3111b6818635240c36703952e84f5e9357f9cc19afac042411642e4"
        ),
        "g13_reference_verifier.py": (
            "091a50337700f40e3c038e1c7854afeb930972d8415246302fa6e5e5d8ff1739"
        ),
    },
}

ADAPTER_INVENTORY = [
    "G12_Superseding_State_Contract_v2.json",
    "G12_Conformance_Vectors_v2.json",
    "g12_suite.cpp",
    "g12_verifier.cpp",
    "G12_Arena_Ledger.json",
    "G12_Verification_Ledger.json",
    "G12_History_Rules_Ledger.json",
    "G12_KQK_Certificate_v2.bin",
    "G12_KRK_Certificate_v2.bin",
    "G12_KPK_Certificate_v2.bin",
]


class DiagnosticError(RuntimeError):
    """Fail-closed diagnostic error with a stable explanation."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _check_json_value(value: Any, location: str = "$") -> None:
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float):
        raise DiagnosticError(f"{location}: floats are prohibited")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise DiagnosticError(f"{location}: string is not NFC")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _check_json_value(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise DiagnosticError(f"{location}: non-string object key")
            if unicodedata.normalize("NFC", key) != key:
                raise DiagnosticError(f"{location}: object key is not NFC")
            _check_json_value(item, f"{location}.{key}")
        return
    raise DiagnosticError(f"{location}: unsupported JSON value")


def canonical_json_bytes(value: Any) -> bytes:
    _check_json_value(value)
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
        + b"\n"
    )


def strict_json_loads(data: bytes) -> Any:
    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise DiagnosticError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DiagnosticError("invalid adapter JSON output") from error


def write_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical_json_bytes(value)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def safe_member_name(name: str) -> bool:
    if not name or "\x00" in name or "\\" in name:
        return False
    if name.startswith("/") or re.match(r"^[A-Za-z]:", name):
        return False
    if unicodedata.normalize("NFC", name) != name:
        return False
    parts = name.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def safe_zip_member(info: zipfile.ZipInfo) -> bool:
    unix_mode = (info.external_attr >> 16) & 0xFFFF
    is_symlink = bool(unix_mode and stat.S_ISLNK(unix_mode))
    is_encrypted = bool(info.flag_bits & 0x1)
    return (
        safe_member_name(info.filename)
        and not info.is_dir()
        and not is_symlink
        and not is_encrypted
    )


def parse_sums(data: bytes) -> list[tuple[str, str]]:
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as error:
        raise DiagnosticError("embedded SHA256SUMS ledger is not ASCII") from error
    lines = text.splitlines()
    if not lines:
        raise DiagnosticError("embedded SHA256SUMS ledger is empty")
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in lines:
        match = SUM_LINE_RE.fullmatch(line)
        if match is None:
            raise DiagnosticError("malformed embedded SHA256SUMS line")
        expected, name = match.groups()
        if not safe_member_name(name):
            raise DiagnosticError("unsafe path in embedded SHA256SUMS ledger")
        portable_name = unicodedata.normalize("NFC", name).casefold()
        if portable_name in seen:
            raise DiagnosticError("duplicate path in embedded SHA256SUMS ledger")
        seen.add(portable_name)
        entries.append((name, expected))
    return entries


def verify_archive(
    path: Path,
    *,
    source_name: str,
    expected_archive_sha256: str,
    sums_name: str,
    expected_sums_sha256: str,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    if not path.is_file():
        raise DiagnosticError(f"missing inherited archive: {source_name}")
    observed_archive_sha256 = sha256_file(path)
    if observed_archive_sha256 != expected_archive_sha256:
        raise DiagnosticError(f"outer SHA-256 mismatch: {source_name}")

    selected_sources: dict[str, bytes] = {}
    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        portable_names = [unicodedata.normalize("NFC", name).casefold() for name in names]
        unique_members = len(names) == len(set(names))
        portable_unique_members = len(portable_names) == len(set(portable_names))
        safe_members = all(safe_zip_member(info) for info in infos)
        if not unique_members or not portable_unique_members:
            raise DiagnosticError(f"duplicate ZIP members: {source_name}")
        if not safe_members:
            raise DiagnosticError(f"unsafe ZIP member: {source_name}")
        if sums_name not in names:
            raise DiagnosticError(f"missing embedded SHA256SUMS: {source_name}")

        sums_data = archive.read(sums_name)
        observed_sums_sha256 = sha256_bytes(sums_data)
        if observed_sums_sha256 != expected_sums_sha256:
            raise DiagnosticError(f"embedded SHA256SUMS hash mismatch: {source_name}")
        declared = parse_sums(sums_data)
        declared_names = {name for name, _ in declared}
        covered_names = set(names) - {sums_name}
        complete_coverage = declared_names == covered_names
        if not complete_coverage:
            raise DiagnosticError(f"embedded SHA256SUMS coverage mismatch: {source_name}")

        entry_results: list[dict[str, Any]] = []
        for name, expected in sorted(declared):
            data = archive.read(name)
            observed = sha256_bytes(data)
            verified = observed == expected
            entry_results.append(
                {
                    "bytes": len(data),
                    "expected_sha256": expected,
                    "observed_sha256": observed,
                    "path": name,
                    "verified": verified,
                }
            )
            if not verified:
                raise DiagnosticError(f"embedded member SHA-256 mismatch: {source_name}")

        for name, expected in FROZEN_SOURCES[source_name].items():
            data = archive.read(name)
            observed = sha256_bytes(data)
            if observed != expected:
                raise DiagnosticError(f"frozen source SHA-256 mismatch: {name}")
            selected_sources[name] = data

    report = {
        "archive_bytes": path.stat().st_size,
        "embedded_ledger": {
            "complete_archive_coverage": complete_coverage,
            "declared_entries": len(declared),
            "entries": entry_results,
            "expected_sha256": expected_sums_sha256,
            "observed_sha256": observed_sums_sha256,
            "path": sums_name,
            "verified_entries": len(entry_results),
        },
        "expected_sha256": expected_archive_sha256,
        "member_count": len(names),
        "observed_sha256": observed_archive_sha256,
        "portable_unique_members": portable_unique_members,
        "safe_members": safe_members,
        "source_name": source_name,
        "unique_members": unique_members,
        "verified": True,
    }
    return report, selected_sources


def frozen_source_report(sources: dict[str, dict[str, bytes]]) -> list[dict[str, Any]]:
    report: list[dict[str, Any]] = []
    for archive_name in sorted(sources):
        for name in sorted(sources[archive_name]):
            data = sources[archive_name][name]
            expected = FROZEN_SOURCES[archive_name][name]
            report.append(
                {
                    "archive": archive_name,
                    "bytes": len(data),
                    "expected_sha256": expected,
                    "observed_sha256": sha256_bytes(data),
                    "path": name,
                    "verified": sha256_bytes(data) == expected,
                }
            )
    return report


def inspect_interface_gap(sources: dict[str, dict[str, bytes]]) -> dict[str, Any]:
    g12_suite = sources[G12_ARCHIVE]["g12_suite.cpp"]
    adapter = sources[G13_ARCHIVE]["g13_g12_adapter.py"]
    campaign = sources[G13_ARCHIVE]["g13_reference_campaign.py"]
    platform = sources[G13_ARCHIVE]["g13_platform.py"]

    checks = {
        "adapter_has_bundle_and_out_only_interface": (
            b'ap.add_argument("--bundle")' in adapter
            and b'ap.add_argument("--out",required=True)' in adapter
            and b"subprocess" not in adapter
            and b"g13_platform" not in adapter
            and b"g13_reference_campaign" not in adapter
        ),
        "campaign_has_no_g12_bundle_or_adapter_hook": (
            b'"--bundle"' not in campaign and b"g13_g12_adapter" not in campaign
        ),
        "campaign_is_hard_wired_to_synthetic_2048x32_problem": (
            b'"make-problem","--out"' in campaign
            and b'"--components","2048","--nodes","32"' in campaign
        ),
        "platform_worker_calls_internal_synthetic_solver_directly": (
            b'def solve_component(seed_hex, component, nodes):' in platform
            and b'out, ranks = solve_component(seed, c, nodes)' in platform
            and b'"ruleset_ref": "engineering-reference-only-not-chess"' in platform
        ),
        "g12_producer_has_output_directory_only_interface": (
            b'int main(int argc,char**argv){string outdir=argc>1?argv[1]:".";'
            in g12_suite
        ),
        "g12_producer_has_no_shard_or_checkpoint_interface": (
            b"shard" not in g12_suite.lower()
            and b"checkpoint" not in g12_suite.lower()
        ),
    }
    if not all(checks.values()):
        raise DiagnosticError("frozen interface-gap inspection did not match exact sources")
    return {
        "checks": checks,
        "conclusion": "NO_EXECUTABLE_G12_THROUGH_G13_ACCEPTANCE_PATH_IN_FROZEN_BUNDLE",
        "g12_producer_interface": "WHOLE_SUITE_OUTPUT_DIRECTORY_ONLY",
        "g13_adapter_scope": "BUNDLE_AND_SELECTED_MEMBER_INTEGRITY_ONLY",
        "g13_campaign_scope": "SYNTHETIC_ENGINEERING_REFERENCE_ONLY",
        "missing_interfaces": [
            "G12 workload hook from the frozen adapter into the G13 worker",
            "G12 semantic shard declaration and execution plan",
            "G12 checkpoint/resume cursor and partial-result protocol",
            "G12 deterministic shard merge into the seven canonical outputs",
        ],
        "status": "BLOCKED",
    }


def run_frozen_adapter(adapter: bytes, g12_path: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="g14-g13-replay-pregate-") as directory:
        temporary = Path(directory)
        adapter_path = temporary / "g13_g12_adapter.py"
        adapter_out = temporary / "adapter_status.json"
        adapter_path.write_bytes(adapter)
        environment = os.environ.copy()
        environment.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
                "PYTHONIOENCODING": "utf-8",
            }
        )
        try:
            process = subprocess.run(
                [
                    sys.executable,
                    str(adapter_path),
                    "--bundle",
                    str(g12_path.resolve()),
                    "--out",
                    str(adapter_out),
                ],
                cwd=temporary,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise DiagnosticError("frozen adapter timed out") from error
        if process.returncode != 0:
            raise DiagnosticError("frozen adapter returned nonzero")
        if process.stderr:
            raise DiagnosticError("frozen adapter wrote to stderr")
        if not adapter_out.is_file():
            raise DiagnosticError("frozen adapter did not write its status ledger")

        output_bytes = adapter_out.read_bytes()
        output = strict_json_loads(output_bytes)
        stdout_object = strict_json_loads(process.stdout)
        if stdout_object != output:
            raise DiagnosticError("frozen adapter stdout/status disagreement")
        if output_bytes != canonical_json_bytes(output):
            raise DiagnosticError("frozen adapter status is not canonical JSON")

    required = {
        "bundle_bytes_retrieved": True,
        "inventory_files_present": ADAPTER_INVENTORY,
        "inventory_mismatches": [],
        "observed_sha256": G12_ARCHIVE_SHA256,
        "required_bundle": G12_ARCHIVE,
        "required_sha256": G12_ARCHIVE_SHA256,
        "schema": "G13.G12.BASELINE.STATUS.v1",
        "semantic_authority": "G10.RULES.v1.0",
        "state_profile": "G12.STATE.SERIAL.v2",
        "status": "READY",
    }
    for key, expected in required.items():
        if output.get(key) != expected:
            raise DiagnosticError(f"unexpected frozen adapter field: {key}")
    if not isinstance(output.get("mandatory_acceptance"), str):
        raise DiagnosticError("frozen adapter omitted mandatory acceptance statement")
    return {
        "adapter_output_sha256": sha256_bytes(output_bytes),
        "adapter_returncode": process.returncode,
        "adapter_status": output["status"],
        "bundle_bytes_retrieved": output["bundle_bytes_retrieved"],
        "diagnostic_interpretation": "INPUT_INTEGRITY_READY_ONLY",
        "inventory_files_present": output["inventory_files_present"],
        "inventory_mismatches": output["inventory_mismatches"],
        "temporary_extraction_removed": not Path(directory).exists(),
        "verified": True,
    }


def base_ledger() -> dict[str, Any]:
    return {
        "claim": {
            "class": "ENGINEERING_TEST",
            "scope": "Inherited archive integrity and frozen-adapter input readiness only",
        },
        "mandatory_acceptance": {
            "claim_class": "NOT_CLAIMED",
            "reason": (
                "The frozen adapter performs input integrity checks only; no G12 workload "
                "was executed through G13 shard, checkpoint, retry, repartition, or "
                "merge machinery."
            ),
            "status": "NOT_PERFORMED",
        },
        "preserved_programme_state": {
            "blocks": ["G15", "G17"],
            "g13_core_engineering": {
                "claim_class": "ENGINEERING_TEST",
                "status": "PASS",
            },
            "g13_roadmap_advance_gate": {
                "reason": "Mandatory exact G12 acceptance replay remains NOT_PERFORMED",
                "status": "HOLD",
            },
        },
        "schema": SCHEMA,
    }


def diagnose(g12_path: Path, g13_path: Path) -> dict[str, Any]:
    ledger = base_ledger()
    g12_report, g12_sources = verify_archive(
        g12_path,
        source_name=G12_ARCHIVE,
        expected_archive_sha256=G12_ARCHIVE_SHA256,
        sums_name=G12_SUMS,
        expected_sums_sha256=G12_SUMS_SHA256,
    )
    g13_report, g13_sources = verify_archive(
        g13_path,
        source_name=G13_ARCHIVE,
        expected_archive_sha256=G13_ARCHIVE_SHA256,
        sums_name=G13_SUMS,
        expected_sums_sha256=G13_SUMS_SHA256,
    )
    sources = {G12_ARCHIVE: g12_sources, G13_ARCHIVE: g13_sources}
    source_report = frozen_source_report(sources)
    gap_report = inspect_interface_gap(sources)
    adapter_report = run_frozen_adapter(
        g13_sources["g13_g12_adapter.py"], g12_path
    )
    fully_verified = (
        g12_report["verified"]
        and g13_report["verified"]
        and all(item["verified"] for item in source_report)
        and adapter_report["verified"]
        and adapter_report["adapter_status"] == "READY"
        and gap_report["status"] == "BLOCKED"
        and ledger["mandatory_acceptance"]["status"] == "NOT_PERFORMED"
        and ledger["preserved_programme_state"]["g13_core_engineering"]["status"]
        == "PASS"
        and ledger["preserved_programme_state"]["g13_roadmap_advance_gate"]["status"]
        == "HOLD"
        and ledger["preserved_programme_state"]["blocks"] == ["G15", "G17"]
    )
    ledger.update(
        {
            "adapter_execution": adapter_report,
            "archives": [g12_report, g13_report],
            "diagnostic": {
                "fully_verified": fully_verified,
                "status": "PASS" if fully_verified else "FAILED",
            },
            "frozen_sources": source_report,
            "interface_gap": gap_report,
        }
    )
    if not fully_verified:
        raise DiagnosticError("diagnostic invariants are not fully verified")
    return ledger


def main(argv: list[str] | None = None) -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Verify the inherited G12/G13 replay pre-gate without claiming acceptance"
    )
    parser.add_argument(
        "--g12-bundle",
        type=Path,
        default=repository_root / "legacy" / "originals" / G12_ARCHIVE,
    )
    parser.add_argument(
        "--g13-bundle",
        type=Path,
        default=repository_root / "legacy" / "originals" / G13_ARCHIVE,
    )
    parser.add_argument("--out", type=Path, required=True)
    arguments = parser.parse_args(argv)

    try:
        ledger = diagnose(arguments.g12_bundle, arguments.g13_bundle)
    except (DiagnosticError, OSError, zipfile.BadZipFile) as error:
        ledger = base_ledger()
        ledger["diagnostic"] = {
            "error": str(error),
            "error_type": type(error).__name__,
            "fully_verified": False,
            "status": "FAILED",
        }
        write_atomic(arguments.out, ledger)
        return 1
    write_atomic(arguments.out, ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
