#!/usr/bin/env python3
"""Independent offline verifier for G14 portable proof-store bundles.

This verifier intentionally uses only the Python standard library and the frozen
G14 contract/acceptance documents.  It does not import the producer, store, or
campaign implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import sys
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable


VERIFIER_ID = "G14.INDEPENDENT.VERIFIER.v1"
DEFAULT_CONTRACT_SHA256 = (
    "d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OBJECT_PATH_RE = re.compile(r"^objects/sha256/([0-9a-f]{2})/([0-9a-f]{62})$")
DRIVE_RE = re.compile(r"^[A-Za-z]:")
REGULAR_0644_EXTERNAL_ATTR = (stat.S_IFREG | 0o644) << 16


class ValidationError(Exception):
    """A deterministic contract violation."""

    def __init__(self, code: str, message: str, **context: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.context = context

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.context:
            result["context"] = self.context
        return result


class StrictJSONError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject_float(value: str) -> None:
    raise StrictJSONError(f"floating-point number is prohibited: {value}")


def _reject_constant(value: str) -> None:
    raise StrictJSONError(f"non-finite number is prohibited: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _check_nfc(value: Any, location: str = "$") -> None:
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise StrictJSONError(f"non-NFC string at {location}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _check_nfc(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _check_nfc(key, f"{location}.<key>")
            _check_nfc(item, f"{location}.{key}")


def parse_json_bytes(data: bytes, *, canonical: bool, label: str) -> Any:
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValidationError(
            "JSON_UTF8", f"{label} is not valid UTF-8", offset=exc.start
        ) from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
        _check_nfc(value)
    except (json.JSONDecodeError, StrictJSONError) as exc:
        raise ValidationError("JSON_INVALID", f"{label}: {exc}") from exc
    if canonical:
        expected = canonical_json_bytes(value)
        if data != expected:
            raise ValidationError(
                "JSON_NONCANONICAL",
                f"{label} is not exact G14.CANONICAL.JSON.v1",
            )
    return value


def canonical_json_bytes(value: Any) -> bytes:
    _check_nfc(value)
    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (text + "\n").encode("utf-8")


def expect_exact_fields(value: Any, fields: Iterable[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("TYPE", f"{location} must be an object")
    expected = set(fields)
    actual = set(value)
    if actual != expected:
        raise ValidationError(
            "FIELDS",
            f"{location} has non-exact fields",
            missing=sorted(expected - actual),
            unknown=sorted(actual - expected),
        )
    return value


def expect_str(value: Any, location: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise ValidationError("TYPE", f"{location} must be a non-empty string")
    if unicodedata.normalize("NFC", value) != value:
        raise ValidationError("NON_NFC", f"{location} must be NFC")
    return value


def expect_bool(value: Any, location: str) -> bool:
    if type(value) is not bool:
        raise ValidationError("TYPE", f"{location} must be a boolean")
    return value


def expect_int(value: Any, location: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise ValidationError("TYPE", f"{location} must be an integer")
    if minimum is not None and value < minimum:
        raise ValidationError("RANGE", f"{location} must be >= {minimum}")
    return value


def expect_list(value: Any, location: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "a non-empty" if nonempty else "a"
        raise ValidationError("TYPE", f"{location} must be {qualifier} list")
    return value


def ensure_safe_posix_path(name: str, location: str) -> None:
    expect_str(name, location)
    if unicodedata.normalize("NFC", name) != name:
        raise ValidationError("PATH_NFC", f"{location} is not NFC")
    if "\\" in name or "\x00" in name:
        raise ValidationError("PATH_UNSAFE", f"{location} contains a forbidden character")
    if name.startswith("/") or DRIVE_RE.match(name):
        raise ValidationError("PATH_UNSAFE", f"{location} is absolute or drive-qualified")
    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValidationError("PATH_UNSAFE", f"{location} has an empty/dot/dot-dot segment")


def ref_key(ref: dict[str, Any]) -> tuple[str, str]:
    return (ref["expected_kind"], ref["digest"])


def digest_ref_key(ref: dict[str, Any]) -> tuple[str, int, str]:
    return (ref["digest"], ref["size"], ref["expected_kind"])


@dataclass
class StoredObject:
    digest: str
    path: str
    data: bytes
    kind: str
    record: dict[str, Any] | None = None
    references: list[tuple[str, dict[str, Any]]] = field(default_factory=list)


class IndependentVerifier:
    def __init__(
        self,
        bundle_path: Path,
        contract_path: Path,
        acceptance_path: Path,
        expected_contract_sha256: str,
    ) -> None:
        self.bundle_path = bundle_path
        self.contract_path = contract_path
        self.acceptance_path = acceptance_path
        self.expected_contract_sha256 = expected_contract_sha256.lower()
        self.contract_bytes = contract_path.read_bytes()
        self.acceptance_bytes = acceptance_path.read_bytes()
        self.contract = parse_json_bytes(
            self.contract_bytes, canonical=False, label="proof-store contract"
        )
        self.acceptance = parse_json_bytes(
            self.acceptance_bytes, canonical=False, label="prospective acceptance"
        )
        self.bundle_bytes = b""
        self.entries: dict[str, bytes] = {}
        self.manifest: dict[str, Any] = {}
        self.objects: dict[str, StoredObject] = {}
        self.inventory_refs: dict[str, dict[str, Any]] = {}
        self.adjacency: dict[str, set[str]] = {}
        self.checks: list[dict[str, Any]] = []
        self.errors: list[dict[str, Any]] = []

    def run(self) -> dict[str, Any]:
        stages: list[tuple[str, Callable[[], dict[str, Any] | None]]] = [
            ("SPEC_BINDING", self._validate_spec_binding),
            ("ZIP_ENVELOPE", self._load_and_validate_zip),
            ("BUNDLE_MANIFEST", self._validate_manifest),
            ("CAS_OBJECTS_AND_RECORDS", self._load_and_validate_objects),
            ("TYPED_CLOSURE_AND_KINDS", self._validate_references_and_closure),
            ("PROOF_DAGS", self._validate_proofs),
            ("LINEAGE_CATALOG_AND_RETENTION", self._validate_lineage_catalog),
            ("RELEASE_AND_CLAIM_BOUNDARIES", self._validate_releases),
            ("G13_LOSSLESS_FIXTURE", self._validate_g13_fixture),
            ("GC_DRY_RUN", self._validate_gc_plans),
        ]
        for check_id, function in stages:
            try:
                details = function() or {}
            except ValidationError as exc:
                self.checks.append(
                    {"id": check_id, "status": "FAIL", "details": exc.as_dict()}
                )
                self.errors.append(exc.as_dict())
                break
            except Exception as exc:  # fail closed on an unexpected verifier condition
                error = ValidationError(
                    "VERIFIER_INTERNAL_ERROR", f"{type(exc).__name__}: {exc}"
                )
                self.checks.append(
                    {"id": check_id, "status": "FAIL", "details": error.as_dict()}
                )
                self.errors.append(error.as_dict())
                break
            else:
                self.checks.append(
                    {"id": check_id, "status": "PASS", "details": details}
                )
        status = "PASS" if not self.errors and len(self.checks) == len(stages) else "FAIL"
        return {
            "schema_version": "1.0.0",
            "verifier_id": VERIFIER_ID,
            "status": status,
            "bundle_name": self.bundle_path.name,
            "bundle_sha256": sha256_bytes(self.bundle_bytes) if self.bundle_bytes else None,
            "contract_sha256": sha256_bytes(self.contract_bytes),
            "acceptance_sha256": sha256_bytes(self.acceptance_bytes),
            "offline": True,
            "producer_code_imported": False,
            "checks": self.checks,
            "errors": self.errors,
            "summary": {
                "checks_passed": sum(item["status"] == "PASS" for item in self.checks),
                "checks_failed": sum(item["status"] == "FAIL" for item in self.checks),
                "objects_verified": len(self.objects),
                "records_verified": sum(obj.record is not None for obj in self.objects.values()),
            },
            "claim_boundary": self.acceptance.get("claim_boundary"),
        }

    def _validate_spec_binding(self) -> dict[str, Any]:
        actual = sha256_bytes(self.contract_bytes)
        if not SHA256_RE.fullmatch(self.expected_contract_sha256):
            raise ValidationError("CONTRACT_DIGEST_FORMAT", "expected contract digest is invalid")
        if actual != self.expected_contract_sha256:
            raise ValidationError(
                "CONTRACT_HASH",
                "local proof-store contract does not match the expected frozen identity",
                expected=self.expected_contract_sha256,
                actual=actual,
            )
        bindings = self.acceptance.get("authority_bindings")
        if not isinstance(bindings, dict):
            raise ValidationError("ACCEPTANCE_SHAPE", "authority_bindings must be an object")
        bound = bindings.get("g14_proof_store_contract_sha256")
        if bound != actual:
            raise ValidationError(
                "ACCEPTANCE_CONTRACT_BINDING",
                "acceptance document does not bind the loaded contract",
                expected=actual,
                actual=bound,
            )
        if self.contract.get("contract_id") != "G14.PROOFSTORE.v1":
            raise ValidationError("CONTRACT_ID", "unexpected contract_id")
        if self.acceptance.get("acceptance_id") != "G14.ACCEPTANCE.v1":
            raise ValidationError("ACCEPTANCE_ID", "unexpected acceptance_id")
        return {"contract_sha256": actual}

    def _load_and_validate_zip(self) -> dict[str, Any]:
        limits = self.acceptance["resource_limits"]
        max_bundle = expect_int(limits["max_bundle_bytes"], "max_bundle_bytes", minimum=1)
        max_entry = expect_int(limits["max_entry_bytes"], "max_entry_bytes", minimum=1)
        max_objects = expect_int(limits["max_object_count"], "max_object_count", minimum=1)
        try:
            self.bundle_bytes = self.bundle_path.read_bytes()
        except OSError as exc:
            raise ValidationError("BUNDLE_READ", f"cannot read bundle: {exc}") from exc
        if len(self.bundle_bytes) > max_bundle:
            raise ValidationError(
                "BUNDLE_SIZE", "bundle exceeds frozen byte limit", size=len(self.bundle_bytes)
            )
        try:
            archive = zipfile.ZipFile(io.BytesIO(self.bundle_bytes), mode="r")
        except (zipfile.BadZipFile, OSError) as exc:
            raise ValidationError("ZIP_INVALID", f"invalid/truncated ZIP: {exc}") from exc
        with archive:
            if archive.comment:
                raise ValidationError("ZIP_COMMENT", "archive comment is prohibited")
            infos = archive.infolist()
            if not infos:
                raise ValidationError("ZIP_EMPTY", "portable bundle is empty")
            if len(infos) - 1 > max_objects:
                raise ValidationError("ZIP_OBJECT_COUNT", "bundle exceeds object-count limit")
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise ValidationError("ZIP_DUPLICATE_PATH", "duplicate ZIP entry name")
            folded = [name.casefold() for name in names]
            if len(folded) != len(set(folded)):
                raise ValidationError("ZIP_CASE_COLLISION", "case-colliding ZIP entry names")
            for name in names:
                ensure_safe_posix_path(name, f"ZIP entry {name!r}")
            if names != sorted(names, key=lambda name: name.encode("utf-8")):
                raise ValidationError("ZIP_ORDER", "entries are not bytewise path ascending")
            declared_total = 0
            for info in infos:
                if info.flag_bits & 0x1:
                    raise ValidationError("ZIP_ENCRYPTED", f"encrypted entry: {info.filename}")
                if info.compress_type != zipfile.ZIP_STORED:
                    raise ValidationError("ZIP_COMPRESSION", f"entry is not ZIP_STORED: {info.filename}")
                if info.compress_size != info.file_size:
                    raise ValidationError("ZIP_STORED_SIZE", f"stored size mismatch: {info.filename}")
                if info.file_size > max_entry:
                    raise ValidationError("ZIP_ENTRY_SIZE", f"entry exceeds limit: {info.filename}")
                declared_total += info.file_size
                if declared_total > max_bundle:
                    raise ValidationError("ZIP_TOTAL_SIZE", "uncompressed total exceeds limit")
                if info.date_time != (1980, 1, 1, 0, 0, 0):
                    raise ValidationError("ZIP_TIMESTAMP", f"non-fixed timestamp: {info.filename}")
                if info.external_attr != REGULAR_0644_EXTERNAL_ATTR:
                    raise ValidationError(
                        "ZIP_ATTRIBUTES", f"non-regular-0644 attributes: {info.filename}"
                    )
                if info.extra or info.comment:
                    raise ValidationError("ZIP_METADATA", f"extra/comment metadata: {info.filename}")
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                    raise ValidationError("ZIP_NONREGULAR", f"non-regular entry: {info.filename}")
            try:
                self.entries = {info.filename: archive.read(info) for info in infos}
            except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
                raise ValidationError("ZIP_PAYLOAD", f"ZIP payload/CRC failure: {exc}") from exc
        manifest_name = self.contract["portable_bundle"]["manifest_name"]
        if manifest_name not in self.entries:
            raise ValidationError("MANIFEST_MISSING", f"missing {manifest_name}")
        return {"entries": len(self.entries), "archive_bytes": len(self.bundle_bytes)}

    def _validate_ref(self, value: Any, location: str) -> dict[str, Any]:
        fields = self.contract["dependency_rules"]["accepted_reference_form"]["fields"]
        ref = expect_exact_fields(value, fields, location)
        if ref["algorithm"] != "sha256":
            raise ValidationError("REF_ALGORITHM", f"{location}.algorithm must be sha256")
        if not isinstance(ref["digest"], str) or not SHA256_RE.fullmatch(ref["digest"]):
            raise ValidationError("REF_DIGEST", f"{location}.digest is invalid")
        expect_int(ref["size"], f"{location}.size", minimum=0)
        expect_str(ref["expected_kind"], f"{location}.expected_kind")
        allowed = {"RAW", *self.contract["object_kinds"].keys()}
        if ref["expected_kind"] not in allowed:
            raise ValidationError(
                "REF_KIND", f"{location}.expected_kind is unknown", kind=ref["expected_kind"]
            )
        return ref

    def _validate_manifest(self) -> dict[str, Any]:
        manifest_name = self.contract["portable_bundle"]["manifest_name"]
        value = parse_json_bytes(
            self.entries[manifest_name], canonical=True, label=manifest_name
        )
        fields = self.contract["nested_shapes"]["bundle_manifest"]["fields"]
        self.manifest = expect_exact_fields(value, fields, "bundle manifest")
        required = self.contract["nested_shapes"]["bundle_manifest"]["required_values"]
        for key, expected in required.items():
            if self.manifest[key] != expected:
                raise ValidationError("MANIFEST_VALUE", f"manifest.{key} has wrong value")
        contract_ref = self._validate_ref(self.manifest["contract"], "manifest.contract")
        if contract_ref["expected_kind"] != "RAW":
            raise ValidationError("MANIFEST_CONTRACT_KIND", "manifest contract must be RAW")
        if contract_ref["digest"] != self.expected_contract_sha256:
            raise ValidationError("MANIFEST_CONTRACT_HASH", "manifest binds the wrong contract")

        roots = expect_list(self.manifest["roots"], "manifest.roots", nonempty=True)
        root_refs = [self._validate_ref(item, f"manifest.roots[{i}]") for i, item in enumerate(roots)]
        if [ref_key(ref) for ref in root_refs] != sorted(ref_key(ref) for ref in root_refs):
            raise ValidationError("MANIFEST_ROOT_ORDER", "manifest roots are not kind/digest sorted")
        if len({digest_ref_key(ref) for ref in root_refs}) != len(root_refs):
            raise ValidationError("MANIFEST_ROOT_DUPLICATE", "duplicate manifest root")
        if not any(ref["expected_kind"] == "RELEASE" for ref in root_refs):
            raise ValidationError("MANIFEST_RELEASE_ROOT", "manifest has no RELEASE root")

        inventory = expect_list(self.manifest["inventory"], "manifest.inventory", nonempty=True)
        inventory_fields = self.contract["nested_shapes"]["bundle_inventory_entry"]["fields"]
        parsed_inventory: list[tuple[str, dict[str, Any]]] = []
        for index, item in enumerate(inventory):
            entry = expect_exact_fields(item, inventory_fields, f"manifest.inventory[{index}]")
            path = expect_str(entry["path"], f"manifest.inventory[{index}].path")
            ensure_safe_posix_path(path, f"manifest.inventory[{index}].path")
            ref = self._validate_ref(entry["ref"], f"manifest.inventory[{index}].ref")
            expected_path = f"objects/sha256/{ref['digest'][:2]}/{ref['digest'][2:]}"
            if path != expected_path:
                raise ValidationError("INVENTORY_PATH", "inventory path does not match digest", path=path)
            parsed_inventory.append((path, ref))
        paths = [path for path, _ in parsed_inventory]
        if paths != sorted(paths):
            raise ValidationError("INVENTORY_ORDER", "inventory is not path sorted")
        if len(paths) != len(set(paths)):
            raise ValidationError("INVENTORY_DUPLICATE", "duplicate inventory path")
        digests = [ref["digest"] for _, ref in parsed_inventory]
        if len(digests) != len(set(digests)):
            raise ValidationError("INVENTORY_DIGEST_DUPLICATE", "duplicate inventory digest")

        limits_fields = self.contract["nested_shapes"]["bundle_limits"]["fields"]
        bundle_limits = expect_exact_fields(self.manifest["limits"], limits_fields, "manifest.limits")
        for key in limits_fields:
            expect_int(bundle_limits[key], f"manifest.limits.{key}", minimum=1)
        frozen = self.acceptance["resource_limits"]
        if bundle_limits["max_entries"] > frozen["max_object_count"]:
            raise ValidationError("MANIFEST_LIMIT", "manifest max_entries weakens frozen limit")
        if bundle_limits["max_entry_bytes"] > frozen["max_entry_bytes"]:
            raise ValidationError("MANIFEST_LIMIT", "manifest max_entry_bytes weakens frozen limit")
        if bundle_limits["max_total_bytes"] > frozen["max_bundle_bytes"]:
            raise ValidationError("MANIFEST_LIMIT", "manifest max_total_bytes weakens frozen limit")
        if len(parsed_inventory) > bundle_limits["max_entries"]:
            raise ValidationError("MANIFEST_LIMIT", "inventory exceeds manifest max_entries")
        if any(ref["size"] > bundle_limits["max_entry_bytes"] for _, ref in parsed_inventory):
            raise ValidationError("MANIFEST_LIMIT", "object exceeds manifest max_entry_bytes")
        if sum(ref["size"] for _, ref in parsed_inventory) > bundle_limits["max_total_bytes"]:
            raise ValidationError("MANIFEST_LIMIT", "objects exceed manifest max_total_bytes")

        actual_object_paths = set(self.entries) - {manifest_name}
        if actual_object_paths != set(paths):
            raise ValidationError(
                "BUNDLE_INVENTORY_MISMATCH",
                "ZIP entries and manifest inventory differ",
                missing=sorted(set(paths) - actual_object_paths),
                extra=sorted(actual_object_paths - set(paths)),
            )
        self.inventory_refs = {ref["digest"]: ref for _, ref in parsed_inventory}
        manifest_refs = [contract_ref, *root_refs]
        for ref in manifest_refs:
            inventory_ref = self.inventory_refs.get(ref["digest"])
            if inventory_ref != ref:
                raise ValidationError("MANIFEST_DANGLING", "manifest root/contract not exactly inventoried")
        return {"inventory_objects": len(parsed_inventory), "roots": len(root_refs)}

    def _record_ref(
        self,
        refs: list[tuple[str, dict[str, Any]]],
        semantic_path: str,
        value: Any,
        location: str,
    ) -> dict[str, Any]:
        ref = self._validate_ref(value, location)
        allowed = self.contract["reference_target_kinds"].get(semantic_path)
        if allowed is None:
            raise ValidationError("CONTRACT_REFERENCE_PATH", f"no kind rule for {semantic_path}")
        if ref["expected_kind"] not in allowed:
            raise ValidationError(
                "REFERENCE_ROLE_KIND",
                f"{location} has a kind forbidden for its role",
                actual=ref["expected_kind"],
                allowed=allowed,
            )
        refs.append((semantic_path, ref))
        return ref

    def _validate_digest_claims(self, value: Any, location: str) -> None:
        claims = expect_list(value, location)
        shape = self.contract["nested_shapes"]["digest_claim"]
        keys: list[tuple[str, str]] = []
        for index, item in enumerate(claims):
            claim = expect_exact_fields(item, shape["fields"], f"{location}[{index}]")
            if claim["algorithm"] != "sha256" or claim["resolution_status"] != "UNRESOLVED_BYTES":
                raise ValidationError("DIGEST_CLAIM_VALUE", f"{location}[{index}] has invalid fixed value")
            if not isinstance(claim["digest"], str) or not SHA256_RE.fullmatch(claim["digest"]):
                raise ValidationError("DIGEST_CLAIM_HASH", f"{location}[{index}].digest is invalid")
            expect_str(claim["label"], f"{location}[{index}].label")
            keys.append((claim["label"], claim["digest"]))
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            raise ValidationError("DIGEST_CLAIM_ORDER", f"{location} is unsorted or duplicated")

    def _validate_ref_array(
        self,
        value: Any,
        refs: list[tuple[str, dict[str, Any]]],
        semantic_path: str,
        location: str,
        *,
        nonempty: bool = False,
    ) -> list[dict[str, Any]]:
        items = expect_list(value, location, nonempty=nonempty)
        parsed = [
            self._record_ref(refs, semantic_path, item, f"{location}[{index}]")
            for index, item in enumerate(items)
        ]
        keys = [digest_ref_key(ref) for ref in parsed]
        if len(keys) != len(set(keys)):
            raise ValidationError("REFERENCE_DUPLICATE", f"{location} contains duplicate refs")
        return parsed

    def _validate_record_shape(self, record: dict[str, Any], digest: str) -> list[tuple[str, dict[str, Any]]]:
        kind = record.get("kind")
        if kind not in self.contract["object_kinds"]:
            raise ValidationError("RECORD_KIND", "unknown record kind", digest=digest, kind=kind)
        kind_spec = self.contract["object_kinds"][kind]
        required = set(kind_spec["required"])
        optional = set(kind_spec["optional"])
        actual = set(record)
        if not required <= actual or not actual <= required | optional:
            raise ValidationError(
                "RECORD_FIELDS",
                f"{kind} record has non-exact fields",
                digest=digest,
                missing=sorted(required - actual),
                unknown=sorted(actual - required - optional),
            )
        for prohibited in kind_spec.get("prohibited", []):
            if prohibited in record:
                raise ValidationError("RECORD_PROHIBITED_FIELD", f"{kind}.{prohibited} is prohibited")
        if record["schema_version"] != self.contract["record_schema_version"]:
            raise ValidationError("RECORD_SCHEMA", f"{kind} has wrong schema_version")
        for id_field in self.contract["record_field_semantics"]["human_id_fields"]:
            if id_field in record:
                expect_str(record[id_field], f"{kind}.{id_field}")
                if record[id_field] in {digest, f"sha256:{digest}"}:
                    raise ValidationError("HUMAN_ID_CAS_ALIAS", f"{kind}.{id_field} aliases its CAS ID")

        refs: list[tuple[str, dict[str, Any]]] = []
        if kind == "MODEL":
            for field_name in ("rules_profile", "state_profile", "semantic_profile", "serialization_profile", "domain"):
                expect_str(record[field_name], f"MODEL.{field_name}")
            self._validate_ref_array(
                record["authority_context"], refs, "MODEL.authority_context[]", "MODEL.authority_context", nonempty=True
            )
        elif kind == "ARENA":
            self._record_ref(refs, "ARENA.model", record["model"], "ARENA.model")
            if not isinstance(record["declaration"], dict) or not record["declaration"]:
                raise ValidationError("ARENA_DECLARATION", "ARENA.declaration must be a non-empty object")
            expect_str(record["reachability"], "ARENA.reachability")
            if "digest_claims" in record:
                self._validate_digest_claims(record["digest_claims"], "ARENA.digest_claims")
        elif kind == "SOURCE_SET":
            self._validate_ref_array(record["sources"], refs, "SOURCE_SET.sources[]", "SOURCE_SET.sources", nonempty=True)
        elif kind == "SOLUTION_CORE":
            for field_name, path in (
                ("model", "SOLUTION_CORE.model"),
                ("arena", "SOLUTION_CORE.arena"),
                ("source_set", "SOLUTION_CORE.source_set"),
                ("truth", "SOLUTION_CORE.truth"),
                ("certificate", "SOLUTION_CORE.certificate"),
                ("certificate_contract", "SOLUTION_CORE.certificate_contract"),
            ):
                self._record_ref(refs, path, record[field_name], f"SOLUTION_CORE.{field_name}")
            dependencies = expect_list(record["dependencies"], "SOLUTION_CORE.dependencies")
            shape = self.contract["nested_shapes"]["dependency_edge"]
            keys: list[tuple[str, str]] = []
            for index, item in enumerate(dependencies):
                edge = expect_exact_fields(item, shape["fields"], f"SOLUTION_CORE.dependencies[{index}]")
                role = expect_str(edge["role"], f"SOLUTION_CORE.dependencies[{index}].role")
                target = self._record_ref(
                    refs,
                    "SOLUTION_CORE.dependencies[].target",
                    edge["target"],
                    f"SOLUTION_CORE.dependencies[{index}].target",
                )
                self._record_ref(
                    refs,
                    "SOLUTION_CORE.dependencies[].expected_model",
                    edge["expected_model"],
                    f"SOLUTION_CORE.dependencies[{index}].expected_model",
                )
                if edge["allow_superseded"] is not False:
                    raise ValidationError("DEPENDENCY_SUPERSEDED", "allow_superseded must be false")
                keys.append((role, target["digest"]))
            if keys != sorted(keys) or len(keys) != len(set(keys)):
                raise ValidationError("DEPENDENCY_ORDER", "dependencies are unsorted or duplicated")
            for field_name in ("claim_class", "domain", "reachability"):
                expect_str(record[field_name], f"SOLUTION_CORE.{field_name}")
        elif kind == "AUTHORITY":
            expect_str(record["authority_role"], "AUTHORITY.authority_role")
            self._record_ref(refs, "AUTHORITY.content", record["content"], "AUTHORITY.content")
            if "notes" in record:
                expect_str(record["notes"], "AUTHORITY.notes", nonempty=False)
        elif kind == "ATTESTATION":
            for field_name, path in (
                ("solution", "ATTESTATION.solution"),
                ("compute_contract", "ATTESTATION.compute_contract"),
                ("source_set", "ATTESTATION.source_set"),
                ("execution_plan", "ATTESTATION.execution_plan"),
                ("merge_evidence", "ATTESTATION.merge_evidence"),
                ("verification_evidence", "ATTESTATION.verification_evidence"),
            ):
                self._record_ref(refs, path, record[field_name], f"ATTESTATION.{field_name}")
            mappings = expect_list(record["source_mapping"], "ATTESTATION.source_mapping", nonempty=True)
            shape = self.contract["nested_shapes"]["source_mapping_entry"]
            map_keys: list[str] = []
            for index, item in enumerate(mappings):
                mapping = expect_exact_fields(item, shape["fields"], f"ATTESTATION.source_mapping[{index}]")
                source_field = expect_str(mapping["source_field"], f"ATTESTATION.source_mapping[{index}].source_field")
                expect_str(mapping["target_field"], f"ATTESTATION.source_mapping[{index}].target_field")
                if mapping["treatment"] not in shape["treatment_enum"]:
                    raise ValidationError("SOURCE_MAPPING_TREATMENT", "invalid source-mapping treatment")
                if mapping["value_state"] not in shape["value_state_enum"]:
                    raise ValidationError("SOURCE_MAPPING_STATE", "invalid source-mapping value_state")
                map_keys.append(source_field)
            if map_keys != sorted(map_keys) or len(map_keys) != len(set(map_keys)):
                raise ValidationError("SOURCE_MAPPING_ORDER", "source mapping is unsorted or duplicated")
            gate_shape = self.contract["nested_shapes"]["attestation_gate_status"]
            gate = expect_exact_fields(record["gate_status"], gate_shape["fields"], "ATTESTATION.gate_status")
            if gate != gate_shape["required_values"]:
                raise ValidationError("GATE_STATUS", "attestation gate status rewrites frozen history")
            if "checkpoint_refs" in record:
                self._validate_ref_array(
                    record["checkpoint_refs"], refs, "ATTESTATION.checkpoint_refs[]", "ATTESTATION.checkpoint_refs"
                )
            if "digest_claims" in record:
                self._validate_digest_claims(record["digest_claims"], "ATTESTATION.digest_claims")
        elif kind == "OCCURRENCE":
            self._record_ref(refs, "OCCURRENCE.content", record["content"], "OCCURRENCE.content")
            self._record_ref(
                refs, "OCCURRENCE.source_container", record["source_container"], "OCCURRENCE.source_container"
            )
            ensure_safe_posix_path(expect_str(record["member_path"], "OCCURRENCE.member_path"), "OCCURRENCE.member_path")
            for field_name in ("programme", "historical_availability", "current_availability"):
                expect_str(record[field_name], f"OCCURRENCE.{field_name}")
        elif kind == "LINEAGE_EVENT":
            event_type = expect_str(record["event_type"], "LINEAGE_EVENT.event_type")
            if event_type not in self.contract["lineage_and_supersession"]["event_types"]:
                raise ValidationError("LINEAGE_EVENT_TYPE", "unknown lineage event type")
            self._record_ref(refs, "LINEAGE_EVENT.subject", record["subject"], "LINEAGE_EVENT.subject")
            if "replacement" in record:
                self._record_ref(
                    refs, "LINEAGE_EVENT.replacement", record["replacement"], "LINEAGE_EVENT.replacement"
                )
            elif event_type == "SUPERSEDES":
                raise ValidationError("SUPERSESSION_REPLACEMENT", "SUPERSEDES requires replacement")
            self._record_ref(refs, "LINEAGE_EVENT.authority", record["authority"], "LINEAGE_EVENT.authority")
            self._validate_ref_array(record["evidence"], refs, "LINEAGE_EVENT.evidence[]", "LINEAGE_EVENT.evidence")
            for field_name in ("scope", "status"):
                expect_str(record[field_name], f"LINEAGE_EVENT.{field_name}")
            token = self.contract["lineage_and_supersession"]["historical_effect_token"]
            if record["historical_effect"] != token:
                raise ValidationError("LINEAGE_RETROACTIVE", "lineage historical_effect is not NON_RETROACTIVE")
        elif kind == "CATALOG":
            entries = expect_list(record["entries"], "CATALOG.entries", nonempty=True)
            shape = self.contract["nested_shapes"]["catalog_entry"]
            names: list[str] = []
            for index, item in enumerate(entries):
                entry = expect_exact_fields(item, shape["fields"], f"CATALOG.entries[{index}]")
                name = expect_str(entry["logical_name"], f"CATALOG.entries[{index}].logical_name")
                self._record_ref(
                    refs,
                    "CATALOG.entries[].active_target",
                    entry["active_target"],
                    f"CATALOG.entries[{index}].active_target",
                )
                if entry["status"] != "ACTIVE":
                    raise ValidationError("CATALOG_STATUS", "catalog entry status must be ACTIVE")
                names.append(name)
            if names != sorted(names) or len(names) != len(set(names)):
                raise ValidationError("CATALOG_ORDER", "catalog entries are unsorted or duplicated")
            self._validate_ref_array(
                record["lineage_events"], refs, "CATALOG.lineage_events[]", "CATALOG.lineage_events"
            )
        elif kind == "PROOF":
            self._record_ref(refs, "PROOF.model", record["model"], "PROOF.model")
            nodes = expect_list(record["nodes"], "PROOF.nodes", nonempty=True)
            shape = self.contract["nested_shapes"]["proof_node"]
            node_ids: list[str] = []
            for index, item in enumerate(nodes):
                node = expect_exact_fields(item, shape["fields"], f"PROOF.nodes[{index}]")
                node_id = expect_str(node["node_id"], f"PROOF.nodes[{index}].node_id")
                depends = expect_list(node["depends_on"], f"PROOF.nodes[{index}].depends_on")
                for dep_index, dependency in enumerate(depends):
                    expect_str(dependency, f"PROOF.nodes[{index}].depends_on[{dep_index}]")
                if depends != sorted(depends) or len(depends) != len(set(depends)):
                    raise ValidationError("PROOF_DEPENDENCY_ORDER", "proof node dependencies are unsorted/duplicated")
                self._record_ref(
                    refs, "PROOF.nodes[].solution", node["solution"], f"PROOF.nodes[{index}].solution"
                )
                node_ids.append(node_id)
            if node_ids != sorted(node_ids) or len(node_ids) != len(set(node_ids)):
                raise ValidationError("PROOF_NODE_ORDER", "proof nodes are unsorted or duplicated")
            roots = expect_list(record["roots"], "PROOF.roots", nonempty=True)
            for index, root in enumerate(roots):
                expect_str(root, f"PROOF.roots[{index}]")
            if roots != sorted(roots) or len(roots) != len(set(roots)):
                raise ValidationError("PROOF_ROOT_ORDER", "proof roots are unsorted or duplicated")
            for field_name in ("claim_class", "domain"):
                expect_str(record[field_name], f"PROOF.{field_name}")
        elif kind == "RELEASE":
            self._record_ref(refs, "RELEASE.catalog", record["catalog"], "RELEASE.catalog")
            for field_name, path, nonempty in (
                ("roots", "RELEASE.roots[]", True),
                ("attestations", "RELEASE.attestations[]", True),
                ("lineage_events", "RELEASE.lineage_events[]", True),
                ("occurrences", "RELEASE.occurrences[]", True),
                ("authorities", "RELEASE.authorities[]", True),
            ):
                self._validate_ref_array(record[field_name], refs, path, f"RELEASE.{field_name}", nonempty=nonempty)
            exceptions = expect_list(record["open_exceptions"], "RELEASE.open_exceptions", nonempty=True)
            exception_shape = self.contract["nested_shapes"]["open_exception"]
            exception_ids: list[str] = []
            for index, item in enumerate(exceptions):
                exception = expect_exact_fields(item, exception_shape["fields"], f"RELEASE.open_exceptions[{index}]")
                for key, expected in exception_shape["required_values"].items():
                    if exception[key] != expected:
                        raise ValidationError("OPEN_EXCEPTION", f"open exception {key} has wrong value")
                blocks = expect_list(exception["blocks"], f"RELEASE.open_exceptions[{index}].blocks", nonempty=True)
                for block_index, block in enumerate(blocks):
                    expect_str(block, f"RELEASE.open_exceptions[{index}].blocks[{block_index}]")
                if blocks != sorted(blocks) or len(blocks) != len(set(blocks)):
                    raise ValidationError("OPEN_EXCEPTION_BLOCKS", "open-exception blocks are unsorted/duplicated")
                if set(blocks) != {"G15", "G17"}:
                    raise ValidationError("OPEN_EXCEPTION_BLOCKS", "open exception must retain G15 and G17 blocks")
                exception_ids.append(exception["exception_id"])
            if exception_ids != sorted(exception_ids) or len(exception_ids) != len(set(exception_ids)):
                raise ValidationError("OPEN_EXCEPTION_ORDER", "open exceptions are unsorted/duplicated")
            if len(exceptions) != 1:
                raise ValidationError("OPEN_EXCEPTION_COUNT", "exactly one frozen open exception is required")
            claim_shape = self.contract["nested_shapes"]["release_claim_boundary"]
            boundary = expect_exact_fields(record["claim_boundary"], claim_shape["fields"], "RELEASE.claim_boundary")
            if boundary != claim_shape["required_values"]:
                raise ValidationError("CLAIM_PROMOTION", "release claim boundary promotes the result")
            retention_token = self.contract["garbage_and_retention"]["release_retention_policy_token"]
            if record["retention_policy"] != retention_token:
                raise ValidationError("RETENTION_POLICY", "release has wrong retention policy token")
        elif kind == "GC_PLAN":
            self._record_ref(refs, "GC_PLAN.release", record["release"], "GC_PLAN.release")
            self._validate_ref_array(
                record["protected_objects"], refs, "GC_PLAN.protected_objects[]", "GC_PLAN.protected_objects", nonempty=True
            )
            claims = expect_list(record["candidate_digest_claims"], "GC_PLAN.candidate_digest_claims")
            shape = self.contract["nested_shapes"]["gc_candidate_digest_claim"]
            keys: list[tuple[str, str]] = []
            for index, item in enumerate(claims):
                claim = expect_exact_fields(item, shape["fields"], f"GC_PLAN.candidate_digest_claims[{index}]")
                if claim["algorithm"] != "sha256":
                    raise ValidationError("GC_CLAIM_ALGORITHM", "GC candidate algorithm must be sha256")
                if not isinstance(claim["digest"], str) or not SHA256_RE.fullmatch(claim["digest"]):
                    raise ValidationError("GC_CLAIM_DIGEST", "GC candidate digest is invalid")
                for field_name in ("label", "reason"):
                    expect_str(claim[field_name], f"GC_PLAN.candidate_digest_claims[{index}].{field_name}")
                keys.append((claim["label"], claim["digest"]))
            if keys != sorted(keys) or len(keys) != len(set(keys)):
                raise ValidationError("GC_CLAIM_ORDER", "GC candidates are unsorted/duplicated")
            if expect_bool(record["deletion_performed"], "GC_PLAN.deletion_performed"):
                raise ValidationError("GC_DELETION", "GC plan performed deletion")
            if record["policy"] != self.contract["garbage_and_retention"]["gc_plan_policy_token"]:
                raise ValidationError("GC_POLICY", "GC plan is not DRY_RUN_ONLY")
        else:  # pragma: no cover - all contract kinds are exhausted above
            raise ValidationError("RECORD_KIND_UNHANDLED", f"unhandled record kind {kind}")
        return refs

    def _load_and_validate_objects(self) -> dict[str, Any]:
        manifest_name = self.contract["portable_bundle"]["manifest_name"]
        inventory_by_path = {
            item["path"]: item["ref"] for item in self.manifest["inventory"]
        }
        for path, ref in inventory_by_path.items():
            data = self.entries[path]
            actual_digest = sha256_bytes(data)
            if actual_digest != ref["digest"]:
                raise ValidationError(
                    "OBJECT_HASH", "object bytes do not match address", path=path, actual=actual_digest
                )
            if len(data) != ref["size"]:
                raise ValidationError("OBJECT_SIZE", "object size does not match inventory", path=path)
            match = OBJECT_PATH_RE.fullmatch(path)
            if match is None or "".join(match.groups()) != actual_digest:
                raise ValidationError("OBJECT_PATH", "object path does not encode its digest", path=path)
            kind = ref["expected_kind"]
            record: dict[str, Any] | None = None
            refs: list[tuple[str, dict[str, Any]]] = []
            if kind != "RAW":
                parsed = parse_json_bytes(data, canonical=True, label=path)
                if not isinstance(parsed, dict):
                    raise ValidationError("RECORD_TYPE", "record object must decode to a JSON object", path=path)
                record = parsed
                if record.get("kind") != kind:
                    raise ValidationError("RECORD_KIND_MISMATCH", "inventory kind differs from record kind", path=path)
                refs = self._validate_record_shape(record, actual_digest)
            self.objects[actual_digest] = StoredObject(
                digest=actual_digest,
                path=path,
                data=data,
                kind=kind,
                record=record,
                references=refs,
            )
        contract_obj = self.objects.get(self.expected_contract_sha256)
        if contract_obj is None or contract_obj.kind != "RAW" or contract_obj.data != self.contract_bytes:
            raise ValidationError("CONTRACT_OBJECT", "bundle does not contain exact contract bytes as RAW")
        if manifest_name in {obj.path for obj in self.objects.values()}:
            raise ValidationError("MANIFEST_IN_CAS", "manifest must not masquerade as a CAS object")
        return {
            "raw_objects": sum(obj.kind == "RAW" for obj in self.objects.values()),
            "record_objects": sum(obj.kind != "RAW" for obj in self.objects.values()),
        }

    def _resolve_ref(self, ref: dict[str, Any], location: str) -> StoredObject:
        target = self.objects.get(ref["digest"])
        if target is None:
            raise ValidationError("DANGLING_REFERENCE", f"missing object for {location}", digest=ref["digest"])
        if len(target.data) != ref["size"]:
            raise ValidationError("REFERENCE_SIZE", f"size mismatch for {location}")
        if target.kind != ref["expected_kind"]:
            raise ValidationError(
                "REFERENCE_KIND", f"kind mismatch for {location}", expected=ref["expected_kind"], actual=target.kind
            )
        return target

    def _reachable(self, starts: Iterable[str]) -> set[str]:
        seen: set[str] = set()
        stack = list(starts)
        while stack:
            digest = stack.pop()
            if digest in seen:
                continue
            seen.add(digest)
            stack.extend(self.adjacency.get(digest, ()))
        return seen

    def _assert_acyclic(self, adjacency: dict[str, set[str]], code: str) -> None:
        white, gray, black = 0, 1, 2
        state: dict[str, int] = {}

        def visit(node: str, trail: list[str]) -> None:
            marker = state.get(node, white)
            if marker == gray:
                raise ValidationError(code, "cycle detected", cycle=trail + [node])
            if marker == black:
                return
            state[node] = gray
            for target in sorted(adjacency.get(node, ())):
                visit(target, trail + [node])
            state[node] = black

        for node in sorted(adjacency):
            visit(node, [])

    def _validate_references_and_closure(self) -> dict[str, Any]:
        self.adjacency = {digest: set() for digest in self.objects}
        edge_count = 0
        for digest, obj in self.objects.items():
            for semantic_path, ref in obj.references:
                target = self._resolve_ref(ref, f"{obj.kind}:{digest}:{semantic_path}")
                self.adjacency[digest].add(target.digest)
                edge_count += 1
            if obj.record:
                for field_name in ("digest_claims",):
                    for claim in obj.record.get(field_name, []):
                        if claim["digest"] in self.objects:
                            raise ValidationError(
                                "RESOLVED_DIGEST_CLAIM",
                                "UNRESOLVED_BYTES digest claim resolves to a bundled object",
                                digest=claim["digest"],
                            )
        root_digests = [self.manifest["contract"]["digest"]]
        root_digests.extend(ref["digest"] for ref in self.manifest["roots"])
        for index, ref in enumerate([self.manifest["contract"], *self.manifest["roots"]]):
            self._resolve_ref(ref, f"manifest reference {index}")
        reachable = self._reachable(root_digests)
        if reachable != set(self.objects):
            raise ValidationError(
                "UNREACHABLE_INVENTORY_OBJECT",
                "inventory contains objects outside exact root closure",
                unreachable=sorted(set(self.objects) - reachable),
            )
        self._assert_acyclic(self.adjacency, "TYPED_GRAPH_CYCLE")
        bindings = self.acceptance["authority_bindings"]
        for name, digest in sorted(bindings.items()):
            target = self.objects.get(digest)
            if target is None or target.kind != "RAW":
                raise ValidationError("AUTHORITY_BINDING_MISSING", f"missing exact RAW authority {name}")
        return {"typed_edges": edge_count, "closure_objects": len(reachable)}

    def _validate_proofs(self) -> dict[str, Any]:
        proofs = [obj for obj in self.objects.values() if obj.kind == "PROOF"]
        if not proofs:
            raise ValidationError("PROOF_MISSING", "bundle has no PROOF record")
        diamond_found = False
        for proof_obj in proofs:
            proof = proof_obj.record
            assert proof is not None
            nodes = proof["nodes"]
            by_id = {node["node_id"]: node for node in nodes}
            if any(root not in by_id for root in proof["roots"]):
                raise ValidationError("PROOF_ROOT_UNKNOWN", "proof root names an unknown node")
            solution_to_node: dict[str, str] = {}
            adjacency: dict[str, set[str]] = {}
            for node in nodes:
                solution_digest = node["solution"]["digest"]
                if solution_digest in solution_to_node:
                    raise ValidationError("PROOF_SOLUTION_DUPLICATE", "two proof nodes use one solution core")
                solution_to_node[solution_digest] = node["node_id"]
                solution = self.objects[solution_digest].record
                assert solution is not None
                if solution["model"]["digest"] != proof["model"]["digest"]:
                    raise ValidationError("PROOF_MODEL", "proof node solution uses a different model")
            for node in nodes:
                solution = self.objects[node["solution"]["digest"]].record
                assert solution is not None
                expected_dependencies: set[str] = set()
                for edge in solution["dependencies"]:
                    target_digest = edge["target"]["digest"]
                    target_node = solution_to_node.get(target_digest)
                    if target_node is None:
                        raise ValidationError("PROOF_NODE_CLOSURE", "solution dependency is absent from proof nodes")
                    expected_dependencies.add(target_node)
                    target_solution = self.objects[target_digest].record
                    assert target_solution is not None
                    if edge["expected_model"]["digest"] != target_solution["model"]["digest"]:
                        raise ValidationError("DEPENDENCY_MODEL", "dependency expected_model does not match target")
                if expected_dependencies != set(node["depends_on"]):
                    raise ValidationError("PROOF_EDGE_MISMATCH", "proof depends_on disagrees with solution dependencies")
                if node["node_id"] in expected_dependencies:
                    raise ValidationError("PROOF_SELF_CYCLE", "proof node depends on itself")
                adjacency[node["node_id"]] = expected_dependencies
            self._assert_acyclic(adjacency, "PROOF_DAG_CYCLE")
            for parent, children in adjacency.items():
                if len(children) < 2:
                    continue
                ordered = sorted(children)
                for left_index, left in enumerate(ordered):
                    for right in ordered[left_index + 1 :]:
                        if adjacency.get(left, set()) & adjacency.get(right, set()):
                            diamond_found = True
        if not diamond_found:
            raise ValidationError("DIAMOND_MISSING", "shared-dependency diamond fixture is absent")
        return {"proofs": len(proofs), "shared_dependency_diamond": True}

    def _validate_lineage_catalog(self) -> dict[str, Any]:
        events = {obj.digest: obj for obj in self.objects.values() if obj.kind == "LINEAGE_EVENT"}
        catalogs = [obj for obj in self.objects.values() if obj.kind == "CATALOG"]
        if not events or not catalogs:
            raise ValidationError("LINEAGE_CATALOG_MISSING", "lineage events and catalogs are required")
        supersession: dict[str, str] = {}
        superseded: set[str] = set()
        event_types: set[str] = set()
        g12_bundle_digest = self.acceptance["authority_bindings"]["g12_recovered_bundle_sha256"]
        recovery_found = False
        for event_obj in events.values():
            event = event_obj.record
            assert event is not None
            event_type = event["event_type"]
            event_types.add(event_type)
            subject = event["subject"]["digest"]
            if event_type == "SUPERSEDES":
                replacement = event["replacement"]["digest"]
                if subject == replacement:
                    raise ValidationError("SUPERSESSION_SELF", "supersession subject equals replacement")
                if self.objects[subject].kind != "SOLUTION_CORE":
                    raise ValidationError("SUPERSESSION_SUBJECT_KIND", "SUPERSEDES subject must be SOLUTION_CORE")
                previous = supersession.get(subject)
                if previous is not None and previous != replacement:
                    raise ValidationError(
                        "SUPERSESSION_CONFLICT",
                        "one supersession subject has conflicting replacements",
                        subject=subject,
                    )
                supersession[subject] = replacement
                superseded.add(subject)
            elif "replacement" in event:
                raise ValidationError("LINEAGE_REPLACEMENT", "non-SUPERSEDES event must not have replacement")
            if event_type == "BYTES_RECOVERED" and subject == g12_bundle_digest:
                recovery_found = True
        self._assert_acyclic(
            {subject: {replacement} for subject, replacement in supersession.items()},
            "SUPERSESSION_CYCLE",
        )
        if "SUPERSEDES" not in event_types:
            raise ValidationError("SUPERSESSION_FIXTURE", "no supersession fixture is present")
        if not recovery_found:
            raise ValidationError("RECOVERY_EVENT", "exact G12 byte-recovery event is absent")

        for catalog_obj in catalogs:
            catalog = catalog_obj.record
            assert catalog is not None
            catalog_event_digests = {ref["digest"] for ref in catalog["lineage_events"]}
            if not catalog_event_digests <= set(events):
                raise ValidationError("CATALOG_EVENT", "catalog references non-lineage event")
            snapshot_inactive = {
                events[event_digest].record["subject"]["digest"]
                for event_digest in catalog_event_digests
                if events[event_digest].record["event_type"] in {"SUPERSEDES", "WITHDRAWN"}
            }
            active_pending = [
                entry["active_target"]["digest"] for entry in catalog["entries"]
            ]
            active_graph: set[str] = set()
            while active_pending:
                active_digest = active_pending.pop()
                if active_digest in active_graph:
                    continue
                active_graph.add(active_digest)
                active_object = self.objects[active_digest]
                active_record = active_object.record
                assert active_record is not None
                if active_object.kind == "PROOF":
                    active_pending.extend(
                        node["solution"]["digest"] for node in active_record["nodes"]
                    )
                elif active_object.kind == "SOLUTION_CORE":
                    active_pending.extend(
                        edge["target"]["digest"] for edge in active_record["dependencies"]
                    )
                else:  # target-kind validation makes this fail-closed branch defensive
                    raise ValidationError(
                        "CATALOG_ACTIVE_KIND",
                        "catalog active graph contains an invalid object kind",
                        kind=active_object.kind,
                    )
            inactive_active = sorted(active_graph & snapshot_inactive)
            if inactive_active:
                raise ValidationError(
                    "CATALOG_INACTIVE_ACTIVE",
                    "pinned catalog active graph reuses a superseded or withdrawn solution",
                    digests=inactive_active,
                )
        return {
            "lineage_events": len(events),
            "catalogs": len(catalogs),
            "superseded_retained": len(superseded),
        }

    def _solution_closure_for_release(self, release: dict[str, Any]) -> set[str]:
        solutions: set[str] = set()
        stack = [ref["digest"] for ref in release["roots"]]
        while stack:
            digest = stack.pop()
            obj = self.objects[digest]
            if obj.kind == "SOLUTION_CORE":
                if digest in solutions:
                    continue
                solutions.add(digest)
                assert obj.record is not None
                stack.extend(edge["target"]["digest"] for edge in obj.record["dependencies"])
            elif obj.kind == "PROOF":
                assert obj.record is not None
                stack.extend(node["solution"]["digest"] for node in obj.record["nodes"])
        return solutions

    def _validate_releases(self) -> dict[str, Any]:
        releases = [obj for obj in self.objects.values() if obj.kind == "RELEASE"]
        if not releases:
            raise ValidationError("RELEASE_MISSING", "bundle has no RELEASE record")
        manifest_release_roots = {
            ref["digest"] for ref in self.manifest["roots"] if ref["expected_kind"] == "RELEASE"
        }
        if manifest_release_roots != {obj.digest for obj in releases}:
            raise ValidationError("RELEASE_ROOT_SET", "all and only RELEASE records must be manifest release roots")
        for release_obj in releases:
            release = release_obj.record
            assert release is not None
            catalog = self.objects[release["catalog"]["digest"]].record
            assert catalog is not None
            active_targets = {entry["active_target"]["digest"] for entry in catalog["entries"]}
            release_roots = {ref["digest"] for ref in release["roots"]}
            if not release_roots <= active_targets:
                raise ValidationError("RELEASE_NOT_CATALOG_PINNED", "release root is not active in pinned catalog")
            release_events = {ref["digest"] for ref in release["lineage_events"]}
            catalog_events = {ref["digest"] for ref in catalog["lineage_events"]}
            if release_events != catalog_events:
                raise ValidationError("RELEASE_CATALOG_LINEAGE", "release/catalog lineage snapshots differ")
            solutions = self._solution_closure_for_release(release)
            for attestation_ref in release["attestations"]:
                attestation = self.objects[attestation_ref["digest"]].record
                assert attestation is not None
                if attestation["solution"]["digest"] not in solutions:
                    raise ValidationError("ATTESTATION_ORPHAN", "release attestation does not describe a released solution")
            if release["claim_boundary"] != self.contract["nested_shapes"]["release_claim_boundary"]["required_values"]:
                raise ValidationError("CLAIM_PROMOTION", "release claim boundary changed")
        return {"releases": len(releases), "open_exception_preserved": True}

    @staticmethod
    def _contains_literal(value: Any, needle: str) -> bool:
        if value == needle:
            return True
        if isinstance(value, list):
            return any(IndependentVerifier._contains_literal(item, needle) for item in value)
        if isinstance(value, dict):
            return any(
                IndependentVerifier._contains_literal(key, needle)
                or IndependentVerifier._contains_literal(item, needle)
                for key, item in value.items()
            )
        return False

    def _authority_content_digest(self, ref: dict[str, Any]) -> str:
        authority = self.objects[ref["digest"]].record
        assert authority is not None and authority["kind"] == "AUTHORITY"
        return authority["content"]["digest"]

    def _validate_g13_fixture(self) -> dict[str, Any]:
        fixture = self.acceptance["fixture_invariants"]
        models = [
            obj
            for obj in self.objects.values()
            if obj.kind == "MODEL" and obj.record["semantic_profile"] == fixture["g13_actual_model"]
        ]
        if len(models) != 1:
            raise ValidationError("G13_MODEL_COUNT", "expected exactly one G13 engineering model")
        model_obj = models[0]
        model = model_obj.record
        assert model is not None
        if model["rules_profile"] != "engineering-reference-only-not-chess":
            raise ValidationError("G13_RULES_PROMOTION", "G13 engineering model was relabelled as chess")
        if model["semantic_profile"] in fixture["inherited_authority_context"]:
            raise ValidationError("G13_MODEL_PROMOTION", "authority context collapsed into actual model")
        authority_ids = {
            self.objects[ref["digest"]].record["authority_id"] for ref in model["authority_context"]
        }
        if authority_ids != set(fixture["inherited_authority_context"]):
            raise ValidationError("G13_AUTHORITY_CONTEXT", "G10/G12 authority context is not preserved exactly")
        expected_authority_content = {
            "G10.RULES.v1.0": self.acceptance["authority_bindings"]["g10_handoff_sha256"],
            "G12.STATE.SERIAL.v2": self.acceptance["authority_bindings"]["g12_handoff_sha256"],
        }
        for authority_ref in model["authority_context"]:
            authority = self.objects[authority_ref["digest"]].record
            assert authority is not None
            expected_content = expected_authority_content[authority["authority_id"]]
            if authority["content"]["digest"] != expected_content:
                raise ValidationError(
                    "G10_G12_IDENTITY_ALIAS",
                    "active contract ID is not bound to its distinct controlling handoff",
                    authority_id=authority["authority_id"],
                )

        solutions = [
            obj
            for obj in self.objects.values()
            if obj.kind == "SOLUTION_CORE" and obj.record["model"]["digest"] == model_obj.digest
        ]
        if len(solutions) != fixture["g13_solution_core_count"]:
            raise ValidationError("G13_SOLUTION_COUNT", "G13 solution-core count is not frozen value")
        solution_obj = solutions[0]
        solution = solution_obj.record
        assert solution is not None
        if solution["claim_class"] != fixture["g13_claim_class"]:
            raise ValidationError("G13_CLAIM_PROMOTION", "G13 solution claim class was promoted")
        if solution["truth"]["digest"] != fixture["g13_truth_sha256"]:
            raise ValidationError("G13_TRUTH_ROLE", "G13 truth hash is missing or role-swapped")
        if solution["certificate"]["digest"] != fixture["g13_certificate_sha256"]:
            raise ValidationError("G13_CERTIFICATE_ROLE", "G13 certificate hash is missing or role-swapped")
        arena = self.objects[solution["arena"]["digest"]].record
        assert arena is not None
        if arena["model"]["digest"] != model_obj.digest:
            raise ValidationError("G13_ARENA_MODEL", "G13 arena points to another model")
        if not self._contains_literal(arena["declaration"], fixture["g13_problem_sha256"]):
            raise ValidationError("G13_PROBLEM_ID", "G13 arena does not bind exact problem hash")
        source_set = self.objects[solution["source_set"]["digest"]].record
        assert source_set is not None
        if fixture["g13_producer_sha256"] not in {ref["digest"] for ref in source_set["sources"]}:
            raise ValidationError("G13_PRODUCER_SOURCE", "G13 producer source hash is absent")

        attestations = [
            obj
            for obj in self.objects.values()
            if obj.kind == "ATTESTATION" and obj.record["solution"]["digest"] == solution_obj.digest
        ]
        if len(attestations) != fixture["g13_plan_count"]:
            raise ValidationError("G13_ATTESTATION_COUNT", "expected one attestation per frozen G13 plan")
        plan_digests = {obj.record["execution_plan"]["digest"] for obj in attestations}
        if len(plan_digests) != fixture["g13_plan_count"]:
            raise ValidationError("G13_PLAN_IDENTITY", "G13 execution plans are not five distinct provenance objects")

        compute_digest = fixture["g13_compute_contract_sha256"]
        compute_raw = self.objects.get(compute_digest)
        if compute_raw is None or compute_raw.kind != "RAW":
            raise ValidationError("G13_COMPUTE_CONTRACT", "exact G13 compute contract RAW object is absent")
        try:
            compute_json = parse_json_bytes(compute_raw.data, canonical=False, label="G13 compute contract")
            lossless_fields = compute_json["g14_projection"]["lossless_fields"]
        except (KeyError, TypeError) as exc:
            raise ValidationError("G13_COMPUTE_PROJECTION", "compute contract lacks lossless_fields") from exc
        if not isinstance(lossless_fields, list) or not all(isinstance(item, str) for item in lossless_fields):
            raise ValidationError("G13_COMPUTE_PROJECTION", "lossless_fields is malformed")
        expected_source_fields = sorted(lossless_fields)
        expected_targets = {
            "semantic rules version": "model.rules_profile",
            "state serialization version": "model.serialization_profile",
            "problem/arena manifest hash": "solution.arena",
            "producer/source hash": "solution.source_set",
            "execution plan hash (execution provenance only)": "attestation.execution_plan",
            "truth hash": "solution.truth",
            "certificate hash": "solution.certificate",
            "dependency object hashes": "solution.dependencies",
            "supersession/provenance status": "attestation.gate_status",
        }
        if set(expected_source_fields) != set(expected_targets):
            raise ValidationError(
                "G13_COMPUTE_PROJECTION_CONTRACT",
                "frozen G13 lossless_fields no longer match the governed projection map",
            )
        for attestation_obj in attestations:
            attestation = attestation_obj.record
            assert attestation is not None
            if self._authority_content_digest(attestation["compute_contract"]) != compute_digest:
                raise ValidationError("G13_COMPUTE_AUTHORITY", "attestation points to wrong compute contract")
            actual_source_fields = [item["source_field"] for item in attestation["source_mapping"]]
            if actual_source_fields != expected_source_fields:
                raise ValidationError(
                    "G13_LOSSY_PROJECTION",
                    "source mapping does not cover exact G13 lossless_fields",
                    expected=expected_source_fields,
                    actual=actual_source_fields,
                )
            for mapping in attestation["source_mapping"]:
                label = mapping["source_field"]
                if mapping["target_field"] != expected_targets[label]:
                    raise ValidationError(
                        "G13_PROJECTION_TARGET",
                        f"lossy target mapping for {label}",
                        expected=expected_targets[label],
                        actual=mapping["target_field"],
                    )
                if "dependency object hashes" in label:
                    if (
                        mapping["treatment"] != "LITERAL"
                        or mapping["value_state"] != "PRESENT_EMPTY"
                    ):
                        raise ValidationError(
                            "G13_DEPENDENCY_PROJECTION",
                            "the declared empty dependency-hash list is not preserved exactly",
                        )
                elif "execution plan hash" in label or "hash" in label:
                    if mapping["treatment"] != "OBJECT_REF" or mapping["value_state"] != "PRESENT_VALUE":
                        raise ValidationError("G13_OBJECT_PROJECTION", f"lossy object mapping for {label}")
                else:
                    if mapping["treatment"] != "LITERAL" or mapping["value_state"] != "PRESENT_VALUE":
                        raise ValidationError("G13_LITERAL_PROJECTION", f"lossy literal mapping for {label}")
            if attestation["gate_status"]["mandatory_replay_status"] != fixture["replay_status"]:
                raise ValidationError("G13_REPLAY_STATUS", "recovered bytes were promoted to replay performed")
        return {
            "g13_solution_cores": len(solutions),
            "g13_attestations": len(attestations),
            "distinct_execution_plans": len(plan_digests),
            "actual_model": model["semantic_profile"],
        }

    def _validate_gc_plans(self) -> dict[str, Any]:
        plans = [obj for obj in self.objects.values() if obj.kind == "GC_PLAN"]
        if len(plans) != 1:
            raise ValidationError("GC_PLAN_COUNT", "exactly one frozen dry-run GC plan is required")
        if not any(ref["digest"] == plans[0].digest for ref in self.manifest["roots"]):
            raise ValidationError("GC_PLAN_ROOT", "GC plan must be a manifest root")
        plan = plans[0].record
        assert plan is not None
        release_digest = plan["release"]["digest"]
        protected_expected = self._reachable([release_digest])
        protected_actual = {ref["digest"] for ref in plan["protected_objects"]}
        if protected_actual != protected_expected:
            raise ValidationError(
                "GC_PROTECTED_CLOSURE",
                "GC protected_objects is not the complete admitted release closure",
                missing=sorted(protected_expected - protected_actual),
                extra=sorted(protected_actual - protected_expected),
            )
        for claim in plan["candidate_digest_claims"]:
            if claim["digest"] in protected_expected or claim["digest"] in self.objects:
                raise ValidationError("GC_PROTECTED_CANDIDATE", "GC candidate is admitted/present/protected")
        return {
            "plans": 1,
            "deletion_performed": False,
            "protected_objects": len(protected_actual),
        }


def build_parser() -> argparse.ArgumentParser:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="G14 portable ZIP bundle")
    parser.add_argument("--ledger", type=Path, help="write deterministic JSON ledger")
    parser.add_argument(
        "--contract",
        type=Path,
        default=script_dir / "G14_Proof_Store_Contract_v1.json",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--acceptance",
        type=Path,
        default=script_dir / "G14_Prospective_Acceptance_v1.json",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--expected-contract-sha256",
        default=DEFAULT_CONTRACT_SHA256,
        help="expected frozen contract SHA-256",
    )
    return parser


def write_ledger(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        verifier = IndependentVerifier(
            bundle_path=args.bundle,
            contract_path=args.contract,
            acceptance_path=args.acceptance,
            expected_contract_sha256=args.expected_contract_sha256,
        )
        ledger = verifier.run()
    except (OSError, ValidationError, StrictJSONError) as exc:
        if isinstance(exc, ValidationError):
            error = exc.as_dict()
        else:
            error = {"code": "VERIFIER_STARTUP", "message": f"{type(exc).__name__}: {exc}"}
        ledger = {
            "schema_version": "1.0.0",
            "verifier_id": VERIFIER_ID,
            "status": "FAIL",
            "bundle_name": args.bundle.name,
            "bundle_sha256": None,
            "contract_sha256": None,
            "acceptance_sha256": None,
            "offline": True,
            "producer_code_imported": False,
            "checks": [],
            "errors": [error],
            "summary": {
                "checks_passed": 0,
                "checks_failed": 1,
                "objects_verified": 0,
                "records_verified": 0,
            },
            "claim_boundary": None,
        }
    output = canonical_json_bytes(ledger)
    if args.ledger is not None:
        write_ledger(args.ledger, output)
    sys.stdout.buffer.write(output)
    return 0 if ledger["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
