"""G14 append-only proof store reference implementation.

This module is deliberately standard-library only.  It implements the producer-side
store, deterministic portable bundle writer and atomic importer for
G14.PROOFSTORE.v1.  The structurally separate verifier does not import this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import unicodedata
import zipfile
from collections.abc import Iterable, Iterator
from pathlib import Path, PurePosixPath
from typing import Any


RECORD_SCHEMA = "G14.OBJECT.v1"
BUNDLE_FORMAT = "G14.PORTABLE.BUNDLE.v1"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
CLAIM_CLASSES = {
    "EXACT",
    "FORMALLY_PROVED",
    "INDEPENDENTLY_REPLAYED",
    "EMPIRICAL",
    "ENGINEERING_TEST",
    "CONDITIONAL",
    "SUPERSEDED",
    "FAILED",
    "BLOCKED",
    "NOT_CLAIMED",
}
RECORD_KINDS = {
    "ARENA",
    "ATTESTATION",
    "AUTHORITY",
    "CATALOG",
    "GC_PLAN",
    "LINEAGE_EVENT",
    "MODEL",
    "OCCURRENCE",
    "PROOF",
    "RELEASE",
    "SOLUTION_CORE",
    "SOURCE_SET",
}
ALL_KINDS = RECORD_KINDS | {"RAW"}
MAX_BUNDLE_ENTRIES = 4096
MAX_ENTRY_BYTES = 8 * 1024 * 1024
MAX_BUNDLE_BYTES = 16 * 1024 * 1024
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
FIXED_ZIP_EXTERNAL_ATTR = (stat.S_IFREG | 0o644) << 16
G14_CONTRACT_SHA256 = "d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825"
G13_TRUTH_SHA256 = "00dde19eddcdf236cad2ce5fbfe115c1951d84b52e7224d230095c904bd03d85"
G13_CERTIFICATE_SHA256 = "5594391149c4464d63811741d90969d1bbe5bbc43a20c39a2e47eb30eb687da7"
G13_PROBLEM_SHA256 = "08f4960faf6b2d5e4d0a93c620373566226dea436318a6da3b5e2022656c9a0d"
G13_COMPUTE_SHA256 = "030930d52931d8d9346d1feace8756a5edaf1a43495ed3b7a8991bb9146a8dc8"
G13_PLATFORM_SHA256 = "251989338b314ab3804b4fdf8f7a1fd7a90bcbd1e3a576708ea16588dc1feb00"
G13_LOSSLESS_FIELDS = {
    "certificate hash",
    "dependency object hashes",
    "execution plan hash (execution provenance only)",
    "problem/arena manifest hash",
    "producer/source hash",
    "semantic rules version",
    "state serialization version",
    "supersession/provenance status",
    "truth hash",
}
G13_SOURCE_MAPPING_POLICY = {
    "certificate hash": ("solution.certificate", "OBJECT_REF", "PRESENT_VALUE"),
    "dependency object hashes": ("solution.dependencies", "LITERAL", "PRESENT_EMPTY"),
    "execution plan hash (execution provenance only)": (
        "attestation.execution_plan",
        "OBJECT_REF",
        "PRESENT_VALUE",
    ),
    "problem/arena manifest hash": ("solution.arena", "OBJECT_REF", "PRESENT_VALUE"),
    "producer/source hash": ("solution.source_set", "OBJECT_REF", "PRESENT_VALUE"),
    "semantic rules version": ("model.rules_profile", "LITERAL", "PRESENT_VALUE"),
    "state serialization version": ("model.serialization_profile", "LITERAL", "PRESENT_VALUE"),
    "supersession/provenance status": ("attestation.gate_status", "LITERAL", "PRESENT_VALUE"),
    "truth hash": ("solution.truth", "OBJECT_REF", "PRESENT_VALUE"),
}
AUTHORITY_CONTENT_SHA256 = {
    "G10.RULES.v1.0": "41267d308be04d79f078fbc3f41aa47add8d0a085bfe7b9cad1587edca7787be",
    "G12.STATE.SERIAL.v2": "958367f224467efc439217ac7a546249915e7a596717e8ad0c2131349e50eff3",
    "G13.COMPUTE.CONTRACT.v1": "030930d52931d8d9346d1feace8756a5edaf1a43495ed3b7a8991bb9146a8dc8",
}


class StoreError(ValueError):
    """Fail-closed proof-store error."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _check_canonical_value(value: Any, location: str = "$") -> None:
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float):
        raise StoreError(f"{location}: floats are prohibited")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise StoreError(f"{location}: string is not NFC")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _check_canonical_value(item, f"{location}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise StoreError(f"{location}: object key is not a string")
            if unicodedata.normalize("NFC", key) != key:
                raise StoreError(f"{location}: key is not NFC")
            _check_canonical_value(item, f"{location}.{key}")
        return
    raise StoreError(f"{location}: unsupported JSON type {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Return G14.CANONICAL.JSON.v1 bytes (including exactly one LF)."""

    _check_canonical_value(value)
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return encoded + b"\n"


def _reject_float(_: str) -> Any:
    raise StoreError("floats are prohibited")


def _reject_constant(value: str) -> Any:
    raise StoreError(f"non-finite JSON constant is prohibited: {value}")


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StoreError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_loads(data: bytes) -> Any:
    """Parse and require byte-for-byte canonical G14 JSON."""

    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise StoreError("canonical JSON must end in exactly one LF")
    if b"\r" in data:
        raise StoreError("canonical JSON must not contain CR bytes")
    try:
        text = data.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_unique_pairs,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise StoreError(f"invalid canonical JSON: {error}") from error
    if canonical_json_bytes(value) != data:
        raise StoreError("JSON bytes are not canonical")
    return value


def object_relpath(digest: str) -> str:
    if not HASH_RE.fullmatch(digest):
        raise StoreError(f"invalid sha256 digest: {digest!r}")
    return f"objects/sha256/{digest[:2]}/{digest[2:]}"


def make_ref(data: bytes, expected_kind: str) -> dict[str, Any]:
    if expected_kind not in ALL_KINDS:
        raise StoreError(f"unknown expected kind: {expected_kind}")
    return {
        "algorithm": "sha256",
        "digest": sha256_hex(data),
        "expected_kind": expected_kind,
        "size": len(data),
    }


def validate_ref(value: Any, allowed_kinds: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise StoreError("object reference is not an object")
    if set(value) != {"algorithm", "digest", "expected_kind", "size"}:
        raise StoreError("object reference fields are not exact")
    if value.get("algorithm") != "sha256":
        raise StoreError("object reference algorithm is not sha256")
    digest = value.get("digest")
    if not isinstance(digest, str) or not HASH_RE.fullmatch(digest):
        raise StoreError("object reference digest is not lowercase SHA-256")
    kind = value.get("expected_kind")
    if kind not in ALL_KINDS:
        raise StoreError(f"object reference has unknown kind: {kind!r}")
    if allowed_kinds is not None and kind not in allowed_kinds:
        raise StoreError(f"object reference kind {kind} is not in {sorted(allowed_kinds)}")
    size = value.get("size")
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise StoreError("object reference size is invalid")
    return value


def ref_key(value: dict[str, Any]) -> tuple[str, str]:
    return str(value["expected_kind"]), str(value["digest"])


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StoreError(f"{label} must be a non-empty string")
    return value


def _require_sorted_unique(
    values: Any,
    label: str,
    key,
) -> list[Any]:
    if not isinstance(values, list):
        raise StoreError(f"{label} must be an array")
    try:
        keys = [key(value) for value in values]
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise StoreError(f"{label} contains a malformed entry") from error
    if keys != sorted(keys):
        raise StoreError(f"{label} is not in canonical order")
    if len(keys) != len(set(keys)):
        raise StoreError(f"{label} contains duplicates")
    return values


def validate_digest_claim(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != {
        "algorithm",
        "digest",
        "label",
        "resolution_status",
    }:
        raise StoreError("digest claim fields are not exact")
    if value["algorithm"] != "sha256" or value["resolution_status"] != "UNRESOLVED_BYTES":
        raise StoreError("digest claim policy is invalid")
    if not isinstance(value["digest"], str) or not HASH_RE.fullmatch(value["digest"]):
        raise StoreError("digest claim hash is invalid")
    _require_string(value["label"], "digest claim label")


def _validate_source_mapping(value: Any) -> None:
    allowed = {"DIGEST_CLAIM", "LITERAL", "OBJECT_REF"}
    states = {"ABSENT", "PRESENT_EMPTY", "PRESENT_NULL", "PRESENT_VALUE"}
    entries = _require_sorted_unique(value, "source_mapping", lambda item: item.get("source_field", "") if isinstance(item, dict) else "")
    for item in entries:
        if not isinstance(item, dict) or set(item) != {
            "source_field",
            "target_field",
            "treatment",
            "value_state",
        }:
            raise StoreError("source mapping entry fields are not exact")
        _require_string(item["source_field"], "source mapping source_field")
        _require_string(item["target_field"], "source mapping target_field")
        if item["treatment"] not in allowed or item["value_state"] not in states:
            raise StoreError("source mapping enum is invalid")
    if {item["source_field"] for item in entries} != G13_LOSSLESS_FIELDS:
        raise StoreError("source mapping is not the complete frozen G13 lossless projection")
    for item in entries:
        expected_target, expected_treatment, expected_state = G13_SOURCE_MAPPING_POLICY[item["source_field"]]
        if (
            item["target_field"] != expected_target
            or item["treatment"] != expected_treatment
            or item["value_state"] != expected_state
        ):
            raise StoreError(f"source mapping policy mismatch for {item['source_field']}")


def _validate_proof_nodes(record: dict[str, Any]) -> None:
    nodes = _require_sorted_unique(
        record["nodes"], "proof nodes", lambda item: item.get("node_id", "") if isinstance(item, dict) else ""
    )
    identifiers: set[str] = set()
    graph: dict[str, list[str]] = {}
    for node in nodes:
        if not isinstance(node, dict) or set(node) != {"depends_on", "node_id", "solution"}:
            raise StoreError("proof node fields are not exact")
        node_id = _require_string(node["node_id"], "proof node id")
        identifiers.add(node_id)
        dependencies = _require_sorted_unique(node["depends_on"], f"proof node {node_id} dependencies", lambda item: item)
        if any(not isinstance(item, str) or not item for item in dependencies):
            raise StoreError("proof node dependency is not a node id")
        validate_ref(node["solution"], {"SOLUTION_CORE"})
        graph[node_id] = dependencies
    for node_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in identifiers:
                raise StoreError(f"proof node {node_id} has missing local dependency {dependency}")
    roots = _require_sorted_unique(record["roots"], "proof roots", lambda item: item)
    if not roots or any(root not in identifiers for root in roots):
        raise StoreError("proof roots are empty or unresolved")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise StoreError("cyclic internal proof graph")
        if node_id in visited:
            return
        visiting.add(node_id)
        for dependency in graph[node_id]:
            visit(dependency)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in sorted(graph):
        visit(node_id)


def _validate_open_exceptions(value: Any) -> None:
    entries = _require_sorted_unique(
        value,
        "open exceptions",
        lambda item: item.get("exception_id", "") if isinstance(item, dict) else "",
    )
    if len(entries) != 1:
        raise StoreError("exactly one frozen G13/G12 open exception is required")
    for item in entries:
        if not isinstance(item, dict) or set(item) != {
            "blocks",
            "bytes_status",
            "exception_id",
            "replay_status",
            "status",
        }:
            raise StoreError("open exception fields are not exact")
        if item != {
            "blocks": ["G15", "G17"],
            "bytes_status": "RECOVERED_EXACT_BYTES",
            "exception_id": "G13_MANDATORY_G12_REPLAY_OPEN",
            "replay_status": "NOT_PERFORMED",
            "status": "OPEN",
        }:
            raise StoreError("G13/G12 open exception was weakened or changed")


def validate_record_shape(record: Any) -> dict[str, Any]:
    """Validate the exact producer record vocabulary, without resolving refs."""

    if not isinstance(record, dict):
        raise StoreError("record root is not an object")
    if record.get("schema_version") != RECORD_SCHEMA:
        raise StoreError("record schema_version mismatch")
    kind = record.get("kind")
    if kind not in RECORD_KINDS:
        raise StoreError(f"unknown record kind: {kind!r}")

    required: dict[str, set[str]] = {
        "ARENA": {"arena_id", "declaration", "kind", "model", "reachability", "schema_version"},
        "ATTESTATION": {
            "attestation_id", "compute_contract", "execution_plan", "gate_status", "kind",
            "merge_evidence", "schema_version", "solution", "source_mapping", "source_set",
            "verification_evidence",
        },
        "AUTHORITY": {"authority_id", "authority_role", "content", "kind", "schema_version"},
        "CATALOG": {"catalog_id", "entries", "kind", "lineage_events", "schema_version"},
        "GC_PLAN": {
            "candidate_digest_claims", "deletion_performed", "kind", "plan_id", "policy",
            "protected_objects", "release", "schema_version",
        },
        "LINEAGE_EVENT": {
            "authority", "event_id", "event_type", "evidence", "historical_effect", "kind",
            "schema_version", "scope", "status", "subject",
        },
        "MODEL": {
            "authority_context", "domain", "kind", "model_id", "rules_profile", "schema_version",
            "semantic_profile", "serialization_profile", "state_profile",
        },
        "OCCURRENCE": {
            "content", "current_availability", "historical_availability", "kind", "member_path",
            "occurrence_id", "programme", "schema_version", "source_container",
        },
        "PROOF": {"claim_class", "domain", "kind", "model", "nodes", "proof_id", "roots", "schema_version"},
        "RELEASE": {
            "attestations", "authorities", "catalog", "claim_boundary", "kind", "lineage_events",
            "occurrences", "open_exceptions", "release_id", "retention_policy", "roots", "schema_version",
        },
        "SOLUTION_CORE": {
            "arena", "certificate", "certificate_contract", "claim_class", "dependencies", "domain",
            "kind", "model", "reachability", "schema_version", "solution_label", "source_set", "truth",
        },
        "SOURCE_SET": {"kind", "schema_version", "source_set_id", "sources"},
    }
    optional: dict[str, set[str]] = {
        "ARENA": {"digest_claims"},
        "ATTESTATION": {"checkpoint_refs", "digest_claims"},
        "AUTHORITY": {"notes"},
        "LINEAGE_EVENT": {"replacement"},
    }
    allowed = required[kind] | optional.get(kind, set())
    missing = required[kind] - set(record)
    extra = set(record) - allowed
    if missing or extra:
        raise StoreError(f"{kind} record fields differ: missing={sorted(missing)} extra={sorted(extra)}")

    if kind == "AUTHORITY":
        _require_string(record["authority_id"], "authority_id")
        _require_string(record["authority_role"], "authority_role")
        validate_ref(record["content"], {"RAW"})
        if "notes" in record:
            _require_string(record["notes"], "authority notes")
    elif kind == "MODEL":
        for field in ("model_id", "rules_profile", "state_profile", "semantic_profile", "serialization_profile", "domain"):
            _require_string(record[field], field)
        refs = _require_sorted_unique(record["authority_context"], "authority_context", ref_key)
        for ref in refs:
            validate_ref(ref, {"AUTHORITY"})
    elif kind == "ARENA":
        _require_string(record["arena_id"], "arena_id")
        validate_ref(record["model"], {"MODEL"})
        if not isinstance(record["declaration"], dict) or not record["declaration"]:
            raise StoreError("arena declaration must be a non-empty object")
        if record["reachability"] not in {"ARENA_ADMISSIBLE", "START_REACHABLE", "REACHABLE_ENTRY_CERTIFIED", "SYNTHETIC"}:
            raise StoreError("arena reachability is invalid")
        claims = record.get("digest_claims", [])
        _require_sorted_unique(claims, "arena digest claims", lambda item: (item.get("label", ""), item.get("digest", "")) if isinstance(item, dict) else ("", ""))
        for claim in claims:
            validate_digest_claim(claim)
    elif kind == "SOURCE_SET":
        _require_string(record["source_set_id"], "source_set_id")
        refs = _require_sorted_unique(record["sources"], "source refs", ref_key)
        if not refs:
            raise StoreError("source set must not be empty")
        for ref in refs:
            validate_ref(ref, {"RAW"})
    elif kind == "SOLUTION_CORE":
        _require_string(record["solution_label"], "solution_label")
        validate_ref(record["model"], {"MODEL"})
        validate_ref(record["arena"], {"ARENA"})
        validate_ref(record["source_set"], {"SOURCE_SET"})
        validate_ref(record["truth"], {"RAW"})
        validate_ref(record["certificate"], {"RAW"})
        validate_ref(record["certificate_contract"], {"AUTHORITY"})
        if record["claim_class"] not in CLAIM_CLASSES:
            raise StoreError("solution claim class is invalid")
        _require_string(record["domain"], "solution domain")
        if record["reachability"] not in {"ARENA_ADMISSIBLE", "START_REACHABLE", "REACHABLE_ENTRY_CERTIFIED", "SYNTHETIC"}:
            raise StoreError("solution reachability is invalid")
        dependencies = _require_sorted_unique(
            record["dependencies"],
            "solution dependencies",
            lambda item: (item.get("role", ""), item.get("target", {}).get("digest", "")) if isinstance(item, dict) else ("", ""),
        )
        for edge in dependencies:
            if not isinstance(edge, dict) or set(edge) != {"allow_superseded", "expected_model", "role", "target"}:
                raise StoreError("dependency edge fields are not exact")
            if edge["allow_superseded"] is not False:
                raise StoreError("admitted dependencies may not allow superseded targets")
            _require_string(edge["role"], "dependency role")
            validate_ref(edge["target"], {"SOLUTION_CORE"})
            validate_ref(edge["expected_model"], {"MODEL"})
    elif kind == "ATTESTATION":
        _require_string(record["attestation_id"], "attestation_id")
        validate_ref(record["solution"], {"SOLUTION_CORE"})
        validate_ref(record["compute_contract"], {"AUTHORITY"})
        validate_ref(record["source_set"], {"SOURCE_SET"})
        for field in ("execution_plan", "merge_evidence", "verification_evidence"):
            validate_ref(record[field], {"RAW"})
        checkpoints = _require_sorted_unique(record.get("checkpoint_refs", []), "checkpoint refs", ref_key)
        for ref in checkpoints:
            validate_ref(ref, {"RAW"})
        claims = _require_sorted_unique(
            record.get("digest_claims", []),
            "attestation digest claims",
            lambda item: (item.get("label", ""), item.get("digest", "")) if isinstance(item, dict) else ("", ""),
        )
        for claim in claims:
            validate_digest_claim(claim)
        _validate_source_mapping(record["source_mapping"])
        if record["gate_status"] != {
            "core_result": "PASS",
            "frozen_input_status": "BLOCKED_INPUT_UNAVAILABLE",
            "mandatory_replay_status": "NOT_PERFORMED",
            "roadmap_gate": "HOLD",
        }:
            raise StoreError("attestation gate status rewrites frozen G13 state")
    elif kind == "OCCURRENCE":
        _require_string(record["occurrence_id"], "occurrence_id")
        validate_ref(record["content"], {"RAW"})
        validate_ref(record["source_container"], {"RAW"})
        _safe_zip_path(_require_string(record["member_path"], "member_path"))
        if record["programme"] not in {f"G{value}" for value in range(1, 43)}:
            raise StoreError("occurrence programme is invalid")
        allowed = {"AVAILABLE", "PRESENT", "UNAVAILABLE", "RECOVERED_EXACT_BYTES"}
        if record["historical_availability"] not in allowed or record["current_availability"] not in allowed:
            raise StoreError("occurrence availability is invalid")
    elif kind == "LINEAGE_EVENT":
        _require_string(record["event_id"], "event_id")
        if record["event_type"] not in {"SUPERSEDES", "BYTES_RECOVERED", "REPLAY_STATUS_CHANGED", "WITHDRAWN"}:
            raise StoreError("lineage event type is invalid")
        _require_string(record["scope"], "lineage scope")
        validate_ref(record["subject"], {"RAW", "SOLUTION_CORE"})
        validate_ref(record["authority"], {"AUTHORITY"})
        evidence = _require_sorted_unique(record["evidence"], "lineage evidence", ref_key)
        for ref in evidence:
            validate_ref(ref, {"RAW"})
        if record["status"] != "ACCEPTED_EVENT" or record["historical_effect"] != "NON_RETROACTIVE":
            raise StoreError("lineage event is not append-only/non-retroactive")
        replacement = record.get("replacement")
        if record["event_type"] == "SUPERSEDES":
            validate_ref(replacement, {"SOLUTION_CORE"})
            if replacement["digest"] == record["subject"]["digest"]:
                raise StoreError("self-supersession is prohibited")
        elif replacement is not None:
            raise StoreError("replacement is only valid for SUPERSEDES")
    elif kind == "PROOF":
        _require_string(record["proof_id"], "proof_id")
        validate_ref(record["model"], {"MODEL"})
        if record["claim_class"] not in CLAIM_CLASSES:
            raise StoreError("proof claim class is invalid")
        _require_string(record["domain"], "proof domain")
        _validate_proof_nodes(record)
    elif kind == "CATALOG":
        _require_string(record["catalog_id"], "catalog_id")
        entries = _require_sorted_unique(
            record["entries"], "catalog entries", lambda item: item.get("logical_name", "") if isinstance(item, dict) else ""
        )
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {"active_target", "logical_name", "status"}:
                raise StoreError("catalog entry fields are not exact")
            _require_string(entry["logical_name"], "catalog logical_name")
            validate_ref(entry["active_target"], {"PROOF", "SOLUTION_CORE"})
            if entry["status"] != "ACTIVE":
                raise StoreError("catalog status is not ACTIVE")
        events = _require_sorted_unique(record["lineage_events"], "catalog lineage events", ref_key)
        for ref in events:
            validate_ref(ref, {"LINEAGE_EVENT"})
    elif kind == "RELEASE":
        _require_string(record["release_id"], "release_id")
        validate_ref(record["catalog"], {"CATALOG"})
        for field, kinds in (
            ("roots", {"PROOF", "SOLUTION_CORE"}),
            ("attestations", {"ATTESTATION"}),
            ("lineage_events", {"LINEAGE_EVENT"}),
            ("occurrences", {"OCCURRENCE"}),
            ("authorities", {"AUTHORITY"}),
        ):
            refs = _require_sorted_unique(record[field], f"release {field}", ref_key)
            for ref in refs:
                validate_ref(ref, kinds)
        if not record["roots"]:
            raise StoreError("release has no roots")
        _validate_open_exceptions(record["open_exceptions"])
        if record["claim_boundary"] != {
            "claim_class": "ENGINEERING_TEST",
            "initial_position_reachability_claimed": False,
            "new_chess_truth_claimed": False,
        }:
            raise StoreError("release claim boundary is invalid")
        if record["retention_policy"] != "RETAIN_ALL_ADMITTED_CLOSURE":
            raise StoreError("release retention policy is invalid")
    elif kind == "GC_PLAN":
        _require_string(record["plan_id"], "plan_id")
        validate_ref(record["release"], {"RELEASE"})
        protected = _require_sorted_unique(record["protected_objects"], "protected objects", ref_key)
        for ref in protected:
            validate_ref(ref)
        candidates = _require_sorted_unique(
            record["candidate_digest_claims"],
            "GC candidate claims",
            lambda item: (item.get("label", ""), item.get("digest", "")) if isinstance(item, dict) else ("", ""),
        )
        for candidate in candidates:
            if not isinstance(candidate, dict) or set(candidate) != {"algorithm", "digest", "label", "reason"}:
                raise StoreError("GC candidate claim fields are not exact")
            if candidate["algorithm"] != "sha256" or not HASH_RE.fullmatch(str(candidate["digest"])):
                raise StoreError("GC candidate digest is invalid")
            _require_string(candidate["label"], "GC candidate label")
            _require_string(candidate["reason"], "GC candidate reason")
        if record["deletion_performed"] is not False or record["policy"] != "DRY_RUN_ONLY":
            raise StoreError("G14 reference GC must be dry-run with no deletion")
    return record


def record_refs(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only normative typed object edges, never digest claims."""

    kind = record["kind"]
    refs: list[dict[str, Any]] = []
    if kind == "AUTHORITY":
        refs.append(record["content"])
    elif kind == "MODEL":
        refs.extend(record["authority_context"])
    elif kind == "ARENA":
        refs.append(record["model"])
    elif kind == "SOURCE_SET":
        refs.extend(record["sources"])
    elif kind == "SOLUTION_CORE":
        refs.extend([record["model"], record["arena"], record["source_set"], record["truth"], record["certificate"], record["certificate_contract"]])
        for edge in record["dependencies"]:
            refs.extend([edge["target"], edge["expected_model"]])
    elif kind == "ATTESTATION":
        refs.extend([
            record["solution"], record["compute_contract"], record["source_set"], record["execution_plan"],
            record["merge_evidence"], record["verification_evidence"],
        ])
        refs.extend(record.get("checkpoint_refs", []))
    elif kind == "OCCURRENCE":
        refs.extend([record["content"], record["source_container"]])
    elif kind == "LINEAGE_EVENT":
        refs.extend([record["subject"], record["authority"], *record["evidence"]])
        if "replacement" in record:
            refs.append(record["replacement"])
    elif kind == "PROOF":
        refs.append(record["model"])
        refs.extend(node["solution"] for node in record["nodes"])
    elif kind == "CATALOG":
        refs.extend(entry["active_target"] for entry in record["entries"])
        refs.extend(record["lineage_events"])
    elif kind == "RELEASE":
        refs.append(record["catalog"])
        for field in ("roots", "attestations", "lineage_events", "occurrences", "authorities"):
            refs.extend(record[field])
    elif kind == "GC_PLAN":
        refs.append(record["release"])
        refs.extend(record["protected_objects"])
    return refs


def _safe_zip_path(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name:
        raise StoreError(f"unsafe bundle path: {name!r}")
    if re.match(r"^[A-Za-z]:", name):
        raise StoreError(f"drive-qualified bundle path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise StoreError(f"unsafe bundle path: {name!r}")
    normalized = path.as_posix()
    if normalized != name:
        raise StoreError(f"noncanonical bundle path: {name!r}")
    return normalized


class ProofStore:
    def __init__(self, root: Path | str):
        self.root = Path(root)

    def _path(self, digest: str) -> Path:
        return self.root / object_relpath(digest)

    def put_bytes(self, data: bytes, expected_digest: str | None = None) -> dict[str, Any]:
        digest = sha256_hex(data)
        if expected_digest is not None and digest != expected_digest:
            raise StoreError(f"payload digest mismatch: expected {expected_digest}, got {digest}")
        path = self._path(digest)
        if path.exists():
            existing = path.read_bytes()
            if existing != data:
                raise StoreError("same-address/different-byte collision or corruption")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            handle, temporary_name = tempfile.mkstemp(prefix=".g14-object-", dir=path.parent)
            try:
                with os.fdopen(handle, "wb") as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                try:
                    # A hard-link publish is an atomic no-clobber create on the same
                    # filesystem.  Unlike os.replace, it cannot overwrite a concurrent
                    # same-address publication before its bytes are compared.
                    os.link(temporary_name, path)
                except FileExistsError:
                    existing = path.read_bytes()
                    if existing != data:
                        raise StoreError("same-address/different-byte collision or corruption")
            finally:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
        return make_ref(data, "RAW")

    def put_record(self, record: dict[str, Any]) -> dict[str, Any]:
        validate_record_shape(record)
        data = canonical_json_bytes(record)
        raw_ref = self.put_bytes(data)
        raw_ref["expected_kind"] = record["kind"]
        return raw_ref

    def read(self, ref: dict[str, Any]) -> bytes:
        validate_ref(ref)
        path = self._path(ref["digest"])
        if not path.is_file():
            raise StoreError(f"missing object: {ref['digest']}")
        data = path.read_bytes()
        if len(data) != ref["size"]:
            raise StoreError(f"object size mismatch: {ref['digest']}")
        if sha256_hex(data) != ref["digest"]:
            raise StoreError(f"object hash mismatch: {ref['digest']}")
        if ref["expected_kind"] != "RAW":
            record = strict_json_loads(data)
            validate_record_shape(record)
            if record["kind"] != ref["expected_kind"]:
                raise StoreError(f"record kind mismatch for {ref['digest']}")
        return data

    def read_record(self, ref: dict[str, Any]) -> dict[str, Any]:
        if ref.get("expected_kind") == "RAW":
            raise StoreError("raw object is not a record")
        value = strict_json_loads(self.read(ref))
        return validate_record_shape(value)

    def resolve_closure(self, roots: Iterable[dict[str, Any]]) -> dict[str, tuple[dict[str, Any], bytes]]:
        root_refs = [dict(validate_ref(ref)) for ref in roots]
        pending = list(root_refs)
        resolved: dict[str, tuple[dict[str, Any], bytes]] = {}
        while pending:
            ref = validate_ref(pending.pop())
            digest = ref["digest"]
            if digest in resolved:
                previous_ref = resolved[digest][0]
                if previous_ref["size"] != ref["size"] or previous_ref["expected_kind"] != ref["expected_kind"]:
                    raise StoreError(f"conflicting typed references for {digest}")
                continue
            data = self.read(ref)
            resolved[digest] = (dict(ref), data)
            if ref["expected_kind"] != "RAW":
                pending.extend(record_refs(strict_json_loads(data)))
        self._validate_semantics(resolved, root_refs)
        return resolved

    def _validate_semantics(
        self,
        resolved: dict[str, tuple[dict[str, Any], bytes]],
        roots: list[dict[str, Any]],
    ) -> None:
        records: dict[str, dict[str, Any]] = {}
        for digest, (ref, data) in resolved.items():
            if ref["expected_kind"] != "RAW":
                records[digest] = strict_json_loads(data)

        def reachable_from(start_digest: str) -> set[str]:
            pending = [start_digest]
            reachable: set[str] = set()
            while pending:
                current = pending.pop()
                if current in reachable:
                    continue
                if current not in resolved:
                    raise StoreError(f"semantic closure is missing {current}")
                reachable.add(current)
                record = records.get(current)
                if record is not None:
                    pending.extend(ref["digest"] for ref in record_refs(record))
            return reachable

        supersedes: dict[str, str] = {}
        for digest, record in records.items():
            if record["kind"] == "LINEAGE_EVENT" and record["event_type"] == "SUPERSEDES":
                subject = record["subject"]["digest"]
                replacement = record["replacement"]["digest"]
                if subject in supersedes and supersedes[subject] != replacement:
                    raise StoreError("conflicting supersession events")
                supersedes[subject] = replacement
        for start in sorted(supersedes):
            seen: set[str] = set()
            current = start
            while current in supersedes:
                if current in seen:
                    raise StoreError("cyclic supersession graph")
                seen.add(current)
                current = supersedes[current]

        for digest, record in records.items():
            if record["kind"] == "AUTHORITY" and record["authority_id"] in AUTHORITY_CONTENT_SHA256:
                expected = AUTHORITY_CONTENT_SHA256[record["authority_id"]]
                if record["content"]["digest"] != expected:
                    raise StoreError(f"authority {record['authority_id']} is aliased or has wrong bytes")
            if record["kind"] == "SOLUTION_CORE":
                for edge in record["dependencies"]:
                    target_digest = edge["target"]["digest"]
                    target = records.get(target_digest)
                    if target is None or target.get("kind") != "SOLUTION_CORE":
                        raise StoreError("solution dependency does not resolve to SOLUTION_CORE")
                    if target["model"] != edge["expected_model"]:
                        raise StoreError("dependency expected_model does not match target model")
                model = records.get(record["model"]["digest"])
                arena = records.get(record["arena"]["digest"])
                if model is None or arena is None or arena.get("model") != record["model"]:
                    raise StoreError("solution model/arena binding mismatch")
                if arena.get("reachability") != record["reachability"]:
                    raise StoreError("solution reachability differs from its arena declaration")
                if model.get("semantic_profile") == "G13.TEST.SEMANTICS.v1":
                    if record["claim_class"] != "ENGINEERING_TEST":
                        raise StoreError("G13 engineering fixture claim promotion")
                    if model.get("rules_profile") != "engineering-reference-only-not-chess":
                        raise StoreError("G13 engineering fixture relabelled as chess semantics")
                    if (
                        model.get("serialization_profile")
                        != "component:u32,node:u16,outcome:u8,rank:u16"
                        or model.get("state_profile") != "G13.TEST.COMPONENT.STATE.v1"
                    ):
                        raise StoreError("G13 engineering fixture state/serialization profile changed")
                    authority_ids = {
                        records[ref["digest"]]["authority_id"]
                        for ref in model["authority_context"]
                    }
                    if authority_ids != {"G10.RULES.v1.0", "G12.STATE.SERIAL.v2"}:
                        raise StoreError("G13 actual model collapsed or contaminated its inherited authority context")
                    if record["truth"]["digest"] != G13_TRUTH_SHA256 or record["certificate"]["digest"] != G13_CERTIFICATE_SHA256:
                        raise StoreError("G13 engineering truth/certificate roles or hashes changed")
                    if arena.get("declaration", {}).get("problem_sha256") != G13_PROBLEM_SHA256:
                        raise StoreError("G13 semantic problem identity changed")
                    source_set = records.get(record["source_set"]["digest"])
                    if source_set is None or G13_PLATFORM_SHA256 not in {
                        ref["digest"] for ref in source_set.get("sources", [])
                    }:
                        raise StoreError("G13 producer/source hash is absent from its source set")
                    certificate_contract = records.get(record["certificate_contract"]["digest"])
                    if (
                        certificate_contract is None
                        or certificate_contract.get("authority_id") != "G13.COMPUTE.CONTRACT.v1"
                        or certificate_contract.get("content", {}).get("digest") != G13_COMPUTE_SHA256
                    ):
                        raise StoreError("G13 solution is not bound to the exact compute/certificate contract")
            elif record["kind"] == "PROOF":
                solution_to_node: dict[str, str] = {}
                for node in record["nodes"]:
                    solution = records.get(node["solution"]["digest"])
                    if solution is None or solution.get("model") != record["model"]:
                        raise StoreError("proof node solution/model mismatch")
                    if node["solution"]["digest"] in solution_to_node:
                        raise StoreError("proof assigns one solution core to multiple local nodes")
                    solution_to_node[node["solution"]["digest"]] = node["node_id"]
                for node in record["nodes"]:
                    solution = records[node["solution"]["digest"]]
                    expected_dependencies: set[str] = set()
                    for edge in solution["dependencies"]:
                        target_node = solution_to_node.get(edge["target"]["digest"])
                        if target_node is None:
                            raise StoreError("solution dependency is absent from proof nodes")
                        expected_dependencies.add(target_node)
                    if expected_dependencies != set(node["depends_on"]):
                        raise StoreError("proof local edges disagree with solution-core dependencies")
            elif record["kind"] == "CATALOG":
                snapshot_inactive = {
                    records[ref["digest"]]["subject"]["digest"]
                    for ref in record["lineage_events"]
                    if records[ref["digest"]]["event_type"] in {"SUPERSEDES", "WITHDRAWN"}
                }
                for entry in record["entries"]:
                    if entry["active_target"]["digest"] in snapshot_inactive:
                        raise StoreError("catalog active target is superseded or withdrawn")
            elif record["kind"] == "ATTESTATION":
                solution = records.get(record["solution"]["digest"])
                if solution is None:
                    raise StoreError("attestation solution is missing")
                if record["source_set"] != solution.get("source_set"):
                    raise StoreError("attestation source set differs from solution source set")
            elif record["kind"] == "RELEASE":
                catalog = records.get(record["catalog"]["digest"])
                if catalog is None or catalog.get("kind") != "CATALOG":
                    raise StoreError("release catalog is unresolved")
                catalog_events = {ref["digest"] for ref in catalog["lineage_events"]}
                release_events = {ref["digest"] for ref in record["lineage_events"]}
                if catalog_events != release_events:
                    raise StoreError("release and pinned catalog have different lineage snapshots")
                active_targets = {entry["active_target"]["digest"] for entry in catalog["entries"]}
                if {ref["digest"] for ref in record["roots"]} - active_targets:
                    raise StoreError("release root is not active in its pinned catalog")
                snapshot_inactive = {
                    records[event_digest]["subject"]["digest"]
                    for event_digest in release_events
                    if records[event_digest]["event_type"] in {"SUPERSEDES", "WITHDRAWN"}
                }
                active_pending = list(active_targets)
                active_graph: set[str] = set()
                active_solutions: set[str] = set()
                while active_pending:
                    active_digest = active_pending.pop()
                    if active_digest in active_graph:
                        continue
                    active_graph.add(active_digest)
                    active_record = records.get(active_digest)
                    if active_record is None:
                        raise StoreError("catalog active target is unresolved")
                    if active_record["kind"] == "PROOF":
                        active_pending.extend(node["solution"]["digest"] for node in active_record["nodes"])
                    elif active_record["kind"] == "SOLUTION_CORE":
                        active_solutions.add(active_digest)
                        active_pending.extend(edge["target"]["digest"] for edge in active_record["dependencies"])
                    else:
                        raise StoreError("catalog active target graph has an invalid kind")
                if active_graph & snapshot_inactive:
                    raise StoreError("pinned active catalog graph reuses a superseded or withdrawn solution")
                for attestation_ref in record["attestations"]:
                    attestation = records[attestation_ref["digest"]]
                    if attestation["solution"]["digest"] not in active_solutions:
                        raise StoreError("release attestation does not describe an active released solution")
            elif record["kind"] == "GC_PLAN":
                protected = {ref["digest"] for ref in record["protected_objects"]}
                candidates = {item["digest"] for item in record["candidate_digest_claims"]}
                release_closure = reachable_from(record["release"]["digest"])
                if protected != release_closure:
                    raise StoreError("GC protected_objects is not the complete admitted release closure")
                if candidates & set(resolved):
                    raise StoreError("GC plan targets an admitted, retained, or otherwise resolved object")

        if not any(records.get(ref["digest"], {}).get("kind") == "RELEASE" for ref in roots):
            if not any(records.get(ref["digest"], {}).get("kind") == "GC_PLAN" for ref in roots):
                raise StoreError("closure has neither RELEASE nor GC_PLAN root")

    def iter_objects(self) -> Iterator[tuple[str, bytes]]:
        base = self.root / "objects" / "sha256"
        if not base.is_dir():
            return
        for path in sorted(base.rglob("*")):
            if path.is_file():
                digest = path.parent.name + path.name
                if HASH_RE.fullmatch(digest):
                    yield digest, path.read_bytes()


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = FIXED_ZIP_EXTERNAL_ATTR
    info.internal_attr = 0
    info.extra = b""
    info.comment = b""
    return info


def export_bundle(
    store: ProofStore,
    output: Path | str,
    roots: list[dict[str, Any]],
    contract_ref: dict[str, Any],
) -> dict[str, Any]:
    validate_ref(contract_ref, {"RAW"})
    if contract_ref["digest"] != G14_CONTRACT_SHA256:
        raise StoreError("portable bundle is not bound to the frozen G14 contract")
    root_refs = [dict(validate_ref(ref, {"GC_PLAN", "RELEASE"})) for ref in roots]
    if not root_refs:
        raise StoreError("portable bundle has no roots")
    if len({ref["digest"] for ref in root_refs}) != len(root_refs):
        raise StoreError("portable bundle roots contain a duplicate digest")
    root_refs.sort(key=ref_key)
    closure = store.resolve_closure(root_refs)
    contract_data = store.read(contract_ref)
    closure[contract_ref["digest"]] = (dict(contract_ref), contract_data)
    inventory = []
    for digest in sorted(closure):
        ref, _ = closure[digest]
        inventory.append({"path": object_relpath(digest), "ref": ref})
    manifest = {
        "contract": contract_ref,
        "format": BUNDLE_FORMAT,
        "inventory": inventory,
        "limits": {
            "max_entries": MAX_BUNDLE_ENTRIES,
            "max_entry_bytes": MAX_ENTRY_BYTES,
            "max_total_bytes": MAX_BUNDLE_BYTES,
        },
        "roots": root_refs,
        "schema_version": "1.0.0",
    }
    manifest_bytes = canonical_json_bytes(manifest)
    total = len(manifest_bytes) + sum(len(data) for _, data in closure.values())
    if len(inventory) + 1 > MAX_BUNDLE_ENTRIES or total > MAX_BUNDLE_BYTES:
        raise StoreError("portable bundle exceeds frozen limits")
    if any(len(data) > MAX_ENTRY_BYTES for _, data in closure.values()):
        raise StoreError("portable bundle entry exceeds frozen limit")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=".g14-bundle-", suffix=".zip", dir=output.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(temporary_name, "w", allowZip64=False) as archive:
            archive.writestr(_zip_info("bundle_manifest.json"), manifest_bytes)
            for item in inventory:
                digest = item["ref"]["digest"]
                archive.writestr(_zip_info(item["path"]), closure[digest][1])
        # The exact temporary bytes must pass the same full offline inspection used
        # by importers before the destination name is atomically published.
        inspect_bundle(temporary_name)
        os.replace(temporary_name, output)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)
    return manifest


def inspect_bundle(path: Path | str) -> tuple[dict[str, Any], dict[str, bytes]]:
    path = Path(path)
    if path.stat().st_size > MAX_BUNDLE_BYTES:
        raise StoreError("bundle file exceeds frozen size limit")
    with zipfile.ZipFile(path, "r") as archive:
        if archive.comment != b"":
            raise StoreError("bundle archive comment is not deterministic")
        infos = archive.infolist()
        if not infos or len(infos) > MAX_BUNDLE_ENTRIES:
            raise StoreError("bundle entry count is invalid")
        names = [info.filename for info in infos]
        for name in names:
            _safe_zip_path(name)
        if len(names) != len(set(names)):
            raise StoreError("duplicate bundle member name")
        folded = [name.casefold() for name in names]
        if len(folded) != len(set(folded)):
            raise StoreError("case-colliding bundle member names")
        if names != sorted(names):
            raise StoreError("bundle members are not canonically ordered")
        if "bundle_manifest.json" not in names:
            raise StoreError("bundle manifest is absent")
        total = 0
        payloads: dict[str, bytes] = {}
        for info in infos:
            mode = (info.external_attr >> 16) & 0xFFFF
            if info.date_time != FIXED_ZIP_TIME or info.compress_type != zipfile.ZIP_STORED:
                raise StoreError("bundle member metadata is not deterministic")
            if (
                info.create_system != 3
                or info.external_attr != FIXED_ZIP_EXTERNAL_ATTR
                or mode != (stat.S_IFREG | 0o644)
                or info.internal_attr != 0
                or info.extra != b""
                or info.comment != b""
                or info.flag_bits != 0
            ):
                raise StoreError("bundle member metadata differs from the fixed regular-file 0644 profile")
            if info.file_size > MAX_ENTRY_BYTES or info.compress_size != info.file_size:
                raise StoreError("bundle member violates size/storage policy")
            total += info.file_size
            if total > MAX_BUNDLE_BYTES:
                raise StoreError("bundle expanded bytes exceed limit")
            payloads[info.filename] = archive.read(info)
    manifest = strict_json_loads(payloads["bundle_manifest.json"])
    if not isinstance(manifest, dict) or set(manifest) != {"contract", "format", "inventory", "limits", "roots", "schema_version"}:
        raise StoreError("bundle manifest fields are not exact")
    if manifest["schema_version"] != "1.0.0" or manifest["format"] != BUNDLE_FORMAT:
        raise StoreError("bundle manifest version/format mismatch")
    validate_ref(manifest["contract"], {"RAW"})
    if manifest["contract"]["digest"] != G14_CONTRACT_SHA256:
        raise StoreError("bundle manifest is not bound to the frozen G14 contract")
    if manifest["limits"] != {
        "max_entries": MAX_BUNDLE_ENTRIES,
        "max_entry_bytes": MAX_ENTRY_BYTES,
        "max_total_bytes": MAX_BUNDLE_BYTES,
    }:
        raise StoreError("bundle manifest limits differ from contract")
    roots = _require_sorted_unique(manifest["roots"], "bundle roots", ref_key)
    if not roots:
        raise StoreError("bundle roots are empty")
    for ref in roots:
        validate_ref(ref, {"GC_PLAN", "RELEASE"})
    inventory = _require_sorted_unique(
        manifest["inventory"], "bundle inventory", lambda item: item.get("path", "") if isinstance(item, dict) else ""
    )
    expected_names = {"bundle_manifest.json"}
    objects: dict[str, bytes] = {}
    inventory_refs: dict[str, dict[str, Any]] = {}
    inventory_digests: set[str] = set()
    for item in inventory:
        if not isinstance(item, dict) or set(item) != {"path", "ref"}:
            raise StoreError("bundle inventory entry fields are not exact")
        ref = validate_ref(item["ref"])
        expected_path = object_relpath(ref["digest"])
        if item["path"] != expected_path:
            raise StoreError("bundle inventory path does not match digest")
        if ref["digest"] in inventory_digests:
            raise StoreError("bundle inventory repeats a digest")
        inventory_digests.add(ref["digest"])
        inventory_refs[ref["digest"]] = dict(ref)
        expected_names.add(expected_path)
        data = payloads.get(expected_path)
        if data is None:
            raise StoreError("bundle inventory object is missing")
        if len(data) != ref["size"] or sha256_hex(data) != ref["digest"]:
            raise StoreError("bundle inventory object hash/size mismatch")
        if ref["expected_kind"] != "RAW":
            record = strict_json_loads(data)
            validate_record_shape(record)
            if record["kind"] != ref["expected_kind"]:
                raise StoreError("bundle inventory record kind mismatch")
        objects[ref["digest"]] = data
    if set(payloads) != expected_names:
        raise StoreError("bundle contains missing or unlisted entries")
    if manifest["contract"]["digest"] not in objects:
        raise StoreError("bundle contract object is not inventoried")
    if inventory_refs[manifest["contract"]["digest"]] != manifest["contract"]:
        raise StoreError("bundle contract reference differs from its inventory reference")

    # Resolve the exact typed closure without writing to disk.  Every inventory
    # object must be reachable from a declared root, except the separately pinned
    # contract object.  This makes inspect-bundle and import-bundle equally strict.
    pending = [dict(ref) for ref in roots]
    reachable: set[str] = set()
    while pending:
        ref = pending.pop()
        digest = ref["digest"]
        declared = inventory_refs.get(digest)
        if declared is None:
            raise StoreError(f"bundle root/dependency is missing from inventory: {digest}")
        if declared != ref:
            raise StoreError(f"bundle typed reference conflicts with inventory: {digest}")
        if digest in reachable:
            continue
        reachable.add(digest)
        if ref["expected_kind"] != "RAW":
            pending.extend(record_refs(strict_json_loads(objects[digest])))
    admitted = reachable | {manifest["contract"]["digest"]}
    if inventory_digests != admitted:
        missing = sorted(admitted - inventory_digests)
        extra = sorted(inventory_digests - admitted)
        raise StoreError(f"bundle inventory is not the exact rooted closure: missing={missing} extra={extra}")

    resolved = {
        digest: (inventory_refs[digest], objects[digest])
        for digest in admitted
    }
    ProofStore(Path("."))._validate_semantics(resolved, roots)
    return manifest, objects


def import_bundle(path: Path | str, target: Path | str) -> dict[str, Any]:
    """Validate completely, then publish a new store atomically."""

    manifest, objects = inspect_bundle(path)
    target = Path(target)
    if target.exists():
        raise StoreError("atomic import target already exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".g14-import-", dir=target.parent))
    try:
        store = ProofStore(staging)
        inventory_by_digest = {item["ref"]["digest"]: item["ref"] for item in manifest["inventory"]}
        for digest in sorted(objects):
            store.put_bytes(objects[digest], expected_digest=digest)
        store.resolve_closure(manifest["roots"])
        # Check the manifest's declared kind survives the raw staging insert.
        for digest, ref in inventory_by_digest.items():
            store.read(ref)
        os.replace(staging, target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return manifest


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect-bundle")
    inspect_parser.add_argument("bundle", type=Path)
    import_parser = subparsers.add_parser("import-bundle")
    import_parser.add_argument("bundle", type=Path)
    import_parser.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inspect-bundle":
            manifest, objects = inspect_bundle(args.bundle)
            result = {"result": "PASS", "objects": len(objects), "roots": manifest["roots"]}
        else:
            manifest = import_bundle(args.bundle, args.target)
            result = {"result": "PASS", "target": str(args.target), "roots": manifest["roots"]}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, StoreError, zipfile.BadZipFile) as error:
        print(json.dumps({"result": "FAIL", "error": str(error)}, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(_main())
