"""Prospectively frozen G14 proof-store campaign and hostile test harness."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import warnings
import zipfile
from pathlib import Path
from typing import Any, Callable

from g14_proof_store import (
    FIXED_ZIP_TIME,
    G13_CERTIFICATE_SHA256,
    G13_LOSSLESS_FIELDS,
    G13_PROBLEM_SHA256,
    G13_TRUTH_SHA256,
    ProofStore,
    StoreError,
    _zip_info,
    canonical_json_bytes,
    export_bundle,
    import_bundle,
    inspect_bundle,
    make_ref,
    object_relpath,
    ref_key,
    sha256_hex,
    strict_json_loads,
    validate_record_shape,
)


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CONTRACT = HERE / "G14_Proof_Store_Contract_v1.json"
ACCEPTANCE = HERE / "G14_Prospective_Acceptance_v1.json"
INDEPENDENT_VERIFIER = HERE / "g14_independent_verifier.py"
G10_BUNDLE = REPO / "legacy" / "originals" / "G10_Semantics_Contract_Bundle.zip"
G12_BUNDLE = REPO / "legacy" / "originals" / "G12_Final_Rules_Reference_Bundle.zip"
G13_BUNDLE = REPO / "legacy" / "originals" / "G13_Distributed_Compute_Bundle.zip"
G10_HANDOFF = REPO / "handoffs" / "originals" / "G10_Technical_Handoff.docx"
G12_HANDOFF = REPO / "handoffs" / "originals" / "G12_Technical_Handoff.docx"
G13_HANDOFF = REPO / "handoffs" / "originals" / "G13_Technical_Handoff.docx"
ROADMAP = REPO / "roadmap" / "originals" / "G9_G10_Onwards_Long_Range_Plan.docx"

EXPECTED = {
    "acceptance": "3bc06d60462044169cd396433ee174bf1d2a365f850de14bb51d83aa46fedcd5",
    "contract": "d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825",
    "g10_bundle": "a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793",
    "g10_handoff": "41267d308be04d79f078fbc3f41aa47add8d0a085bfe7b9cad1587edca7787be",
    "g12_bundle": "7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c",
    "g12_handoff": "958367f224467efc439217ac7a546249915e7a596717e8ad0c2131349e50eff3",
    "g13_bundle": "584a22452cdbc6b296e229d69bb1b1b01672ab0c840816dd5614aacda58ec3a5",
    "g13_compute": "030930d52931d8d9346d1feace8756a5edaf1a43495ed3b7a8991bb9146a8dc8",
    "g13_handoff": "34cc4caea8fdf9902bd04f14701660f5942c6f12ef3901d50164523330302194",
    "g13_platform": "251989338b314ab3804b4fdf8f7a1fd7a90bcbd1e3a576708ea16588dc1feb00",
    "roadmap": "2ccb06fad1d9cbe42631e40861f8982bffdeefe8c981ecda5b7c2f470fdd77b9",
    "verifier": "887eca1987c4c1c2f60147486a5e94313f38b61b9a35c52bf011411d0718d128",
}

PLAN_NAMES = [
    "campaign/A_baseline_4/plan.json",
    "campaign/B_kill_restart_4/plan.json",
    "campaign/C_repartition_7/plan.json",
    "campaign/D_repartition_retry_11/plan.json",
    "campaign/E_fresh_13/plan.json",
]


def file_bytes(path: Path, expected: str | None = None) -> bytes:
    data = path.read_bytes()
    observed = sha256_hex(data)
    if expected is not None and observed != expected:
        raise StoreError(f"authority hash mismatch for {path}: {observed}")
    return data


def zip_members(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise StoreError(f"duplicate member in {path}")
        for name in names:
            if name.startswith("/") or "\\" in name or ".." in Path(name).parts:
                raise StoreError(f"unsafe member in {path}: {name}")
        return {name: archive.read(name) for name in names}


def put_raw(store: ProofStore, data: bytes, expected: str | None = None) -> dict[str, Any]:
    return store.put_bytes(data, expected_digest=expected)


def sorted_refs(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(values, key=ref_key)


def authority(
    store: ProofStore,
    authority_id: str,
    role: str,
    data: bytes,
    notes: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = put_raw(store, data)
    record: dict[str, Any] = {
        "authority_id": authority_id,
        "authority_role": role,
        "content": raw,
        "kind": "AUTHORITY",
        "schema_version": "G14.OBJECT.v1",
    }
    if notes is not None:
        record["notes"] = notes
    return store.put_record(record), record


def source_mapping() -> list[dict[str, str]]:
    target = {
        "certificate hash": "solution.certificate",
        "dependency object hashes": "solution.dependencies",
        "execution plan hash (execution provenance only)": "attestation.execution_plan",
        "problem/arena manifest hash": "solution.arena",
        "producer/source hash": "solution.source_set",
        "semantic rules version": "model.rules_profile",
        "state serialization version": "model.serialization_profile",
        "supersession/provenance status": "attestation.gate_status",
        "truth hash": "solution.truth",
    }
    treatment = {
        "dependency object hashes": "LITERAL",
        "semantic rules version": "LITERAL",
        "state serialization version": "LITERAL",
        "supersession/provenance status": "LITERAL",
    }
    return [
        {
            "source_field": field,
            "target_field": target[field],
            "treatment": treatment.get(field, "OBJECT_REF"),
            "value_state": "PRESENT_EMPTY" if field == "dependency object hashes" else "PRESENT_VALUE",
        }
        for field in sorted(G13_LOSSLESS_FIELDS)
    ]


def build_fixture(store_root: Path) -> dict[str, Any]:
    store = ProofStore(store_root)
    acceptance = json.loads(file_bytes(ACCEPTANCE, EXPECTED["acceptance"]).decode("utf-8"))
    contract_data = file_bytes(CONTRACT, EXPECTED["contract"])
    if acceptance["authority_bindings"]["g14_proof_store_contract_sha256"] != EXPECTED["contract"]:
        raise StoreError("prospective acceptance does not bind the executed contract")

    g10_bundle_data = file_bytes(G10_BUNDLE, EXPECTED["g10_bundle"])
    g12_bundle_data = file_bytes(G12_BUNDLE, EXPECTED["g12_bundle"])
    g13_bundle_data = file_bytes(G13_BUNDLE, EXPECTED["g13_bundle"])
    members = zip_members(G13_BUNDLE)
    required_members = {
        "G13_Compute_Contract_v1.json": EXPECTED["g13_compute"],
        "g13_platform.py": EXPECTED["g13_platform"],
        "campaign/problem.json": G13_PROBLEM_SHA256,
        "campaign/A_baseline_4/merged/truth.bin": G13_TRUTH_SHA256,
        "campaign/A_baseline_4/merged/certificate.bin": G13_CERTIFICATE_SHA256,
    }
    for name, digest in required_members.items():
        if name not in members or sha256_hex(members[name]) != digest:
            raise StoreError(f"G13 fixture member hash mismatch: {name}")

    raw: dict[str, dict[str, Any]] = {}
    raw["contract"] = put_raw(store, contract_data, EXPECTED["contract"])
    raw["acceptance"] = put_raw(store, file_bytes(ACCEPTANCE))
    raw["roadmap"] = put_raw(store, file_bytes(ROADMAP, EXPECTED["roadmap"]), EXPECTED["roadmap"])
    raw["g10_bundle"] = put_raw(store, g10_bundle_data, EXPECTED["g10_bundle"])
    raw["g12_bundle"] = put_raw(store, g12_bundle_data, EXPECTED["g12_bundle"])
    raw["g13_bundle"] = put_raw(store, g13_bundle_data, EXPECTED["g13_bundle"])
    raw["g10_handoff"] = put_raw(store, file_bytes(G10_HANDOFF, EXPECTED["g10_handoff"]), EXPECTED["g10_handoff"])
    raw["g12_handoff"] = put_raw(store, file_bytes(G12_HANDOFF, EXPECTED["g12_handoff"]), EXPECTED["g12_handoff"])
    raw["g13_handoff"] = put_raw(store, file_bytes(G13_HANDOFF, EXPECTED["g13_handoff"]), EXPECTED["g13_handoff"])
    for name in [
        "G13_Compute_Contract_v1.json",
        "G13_Reference_Campaign_Ledger.json",
        "G13_Fresh_Reproduction.json",
        "G13_Reference_Verification_Ledger.json",
        "G13_G12_Baseline_Status.json",
        "campaign/problem.json",
        "campaign/A_baseline_4/merged/truth.bin",
        "campaign/A_baseline_4/merged/certificate.bin",
        "campaign/A_baseline_4/merged/merge_manifest.json",
        "campaign/B_kill_restart_4/controlled_kill_checkpoint.json",
        "g13_platform.py",
        "g13_reference_campaign.py",
        "g13_reference_verifier.py",
    ] + PLAN_NAMES:
        raw[name] = put_raw(store, members[name])
    raw["g14_store_source"] = put_raw(store, file_bytes(HERE / "g14_proof_store.py"))
    raw["g14_campaign_source"] = put_raw(store, file_bytes(Path(__file__)))
    raw["g14_verifier_source"] = put_raw(store, file_bytes(INDEPENDENT_VERIFIER, EXPECTED["verifier"]))

    authorities: dict[str, dict[str, Any]] = {}
    authority_records: dict[str, dict[str, Any]] = {}
    for key, identifier, role, data, notes in [
        ("roadmap", "G9-G42.PERMANENT.ROADMAP", "PERMANENT_STRATEGIC_AUTHORITY", file_bytes(ROADMAP), "Permanent strategic authority; not an executable semantics contract."),
        ("g10", "G10.RULES.v1.0", "RULES", file_bytes(G10_HANDOFF), "Semantic chess-rules authority."),
        ("g12", "G12.STATE.SERIAL.v2", "STATE_SERIALIZATION", file_bytes(G12_HANDOFF), "Distinct forward state profile; not an alias of G10 bytes."),
        ("g13", "G13.COMPUTE.CONTRACT.v1", "COMPUTE", members["G13_Compute_Contract_v1.json"], "Execution provenance is separate from proof identity."),
        ("g13_handoff", "G13.FROZEN.TECHNICAL.HANDOFF", "PREDECESSOR_HANDOFF", file_bytes(G13_HANDOFF), "Frozen predecessor authority; distinct from its embedded compute contract."),
        ("g14", "G14.PROOFSTORE.v1", "PROOF_STORE", contract_data, "G14 proof-store and portable dependency contract."),
    ]:
        authorities[key], authority_records[key] = authority(store, identifier, role, data, notes)

    g13_model_record = {
        "authority_context": sorted_refs([authorities["g10"], authorities["g12"]]),
        "domain": "65,536-state deterministic synthetic exact-game engineering graph; not chess",
        "kind": "MODEL",
        "model_id": "G13.ENGINEERING.REFERENCE.MODEL.v1",
        "rules_profile": "engineering-reference-only-not-chess",
        "schema_version": "G14.OBJECT.v1",
        "semantic_profile": "G13.TEST.SEMANTICS.v1",
        "serialization_profile": "component:u32,node:u16,outcome:u8,rank:u16",
        "state_profile": "G13.TEST.COMPONENT.STATE.v1",
    }
    g13_model = store.put_record(g13_model_record)
    problem_object = strict_json_loads(members["campaign/problem.json"])
    if sha256_hex(canonical_json_bytes(problem_object)) != G13_PROBLEM_SHA256:
        raise StoreError("G13 problem declaration is not reproducible under canonical JSON")
    g13_arena_record = {
        "arena_id": "G13 deterministic exact-game engineering reference",
        "declaration": {"problem_manifest": problem_object, "problem_sha256": G13_PROBLEM_SHA256},
        "digest_claims": [],
        "kind": "ARENA",
        "model": g13_model,
        "reachability": "SYNTHETIC",
        "schema_version": "G14.OBJECT.v1",
    }
    g13_arena = store.put_record(g13_arena_record)
    g13_sources_record = {
        "kind": "SOURCE_SET",
        "schema_version": "G14.OBJECT.v1",
        "source_set_id": "G13.ENGINEERING.REFERENCE.SOURCES.v1",
        "sources": sorted_refs([
            raw["campaign/problem.json"], raw["g13_platform.py"], raw["g13_reference_campaign.py"], raw["g13_reference_verifier.py"]
        ]),
    }
    g13_sources = store.put_record(g13_sources_record)
    g13_solution_record = {
        "arena": g13_arena,
        "certificate": raw["campaign/A_baseline_4/merged/certificate.bin"],
        "certificate_contract": authorities["g13"],
        "claim_class": "ENGINEERING_TEST",
        "dependencies": [],
        "domain": "G13 synthetic 2,048-component by 32-node reference workload",
        "kind": "SOLUTION_CORE",
        "model": g13_model,
        "reachability": "SYNTHETIC",
        "schema_version": "G14.OBJECT.v1",
        "solution_label": "G13 engineering reference exact finite result; not chess truth",
        "source_set": g13_sources,
        "truth": raw["campaign/A_baseline_4/merged/truth.bin"],
    }
    g13_solution = store.put_record(g13_solution_record)

    merge_manifest = strict_json_loads(members["campaign/A_baseline_4/merged/merge_manifest.json"])
    shard_claims = [
        {
            "algorithm": "sha256",
            "digest": digest,
            "label": f"shard_result_sha256[{index:03d}]",
            "resolution_status": "UNRESOLVED_BYTES",
        }
        for index, digest in enumerate(merge_manifest["shard_result_sha256"])
    ]
    attestations: list[dict[str, Any]] = []
    attestation_records: list[dict[str, Any]] = []
    for plan_name in PLAN_NAMES:
        scenario = plan_name.split("/")[1]
        if scenario == "A_baseline_4":
            merge_evidence = raw["campaign/A_baseline_4/merged/merge_manifest.json"]
        elif scenario == "E_fresh_13":
            merge_evidence = raw["G13_Fresh_Reproduction.json"]
        else:
            merge_evidence = raw["G13_Reference_Campaign_Ledger.json"]
        record = {
            "attestation_id": f"G13.{scenario}",
            "checkpoint_refs": [raw["campaign/B_kill_restart_4/controlled_kill_checkpoint.json"]] if scenario == "B_kill_restart_4" else [],
            "compute_contract": authorities["g13"],
            "digest_claims": shard_claims if scenario == "A_baseline_4" else [],
            "execution_plan": raw[plan_name],
            "gate_status": {
                "core_result": "PASS",
                "frozen_input_status": "BLOCKED_INPUT_UNAVAILABLE",
                "mandatory_replay_status": "NOT_PERFORMED",
                "roadmap_gate": "HOLD",
            },
            "kind": "ATTESTATION",
            "merge_evidence": merge_evidence,
            "schema_version": "G14.OBJECT.v1",
            "solution": g13_solution,
            "source_mapping": source_mapping(),
            "source_set": g13_sources,
            "verification_evidence": raw["G13_Reference_Verification_Ledger.json"],
        }
        attestation_records.append(record)
        attestations.append(store.put_record(record))

    synthetic_model_record = {
        "authority_context": [authorities["g14"]],
        "domain": "G14 proof-store dependency and supersession controls; not chess",
        "kind": "MODEL",
        "model_id": "G14.SYNTHETIC.STORE.MODEL.v1",
        "rules_profile": "engineering-reference-only-not-chess",
        "schema_version": "G14.OBJECT.v1",
        "semantic_profile": "G14.SYNTHETIC.STORE.SEMANTICS.v1",
        "serialization_profile": "G14.SYNTHETIC.BYTES.v1",
        "state_profile": "G14.SYNTHETIC.STATE.v1",
    }
    synthetic_model = store.put_record(synthetic_model_record)
    synthetic_arena_record = {
        "arena_id": "G14 shared-dependency diamond and supersession control",
        "declaration": {"cohort": "prospectively-frozen", "nodes": ["base", "left", "right", "top", "old", "new"]},
        "digest_claims": [],
        "kind": "ARENA",
        "model": synthetic_model,
        "reachability": "SYNTHETIC",
        "schema_version": "G14.OBJECT.v1",
    }
    synthetic_arena = store.put_record(synthetic_arena_record)
    synthetic_sources_record = {
        "kind": "SOURCE_SET",
        "schema_version": "G14.OBJECT.v1",
        "source_set_id": "G14.REFERENCE.IMPLEMENTATION.SOURCES.v1",
        "sources": sorted_refs([
            raw["contract"],
            raw["g14_campaign_source"],
            raw["g14_store_source"],
            raw["g14_verifier_source"],
        ]),
    }
    synthetic_sources = store.put_record(synthetic_sources_record)

    solution_records: dict[str, dict[str, Any]] = {"g13": g13_solution_record}
    solutions: dict[str, dict[str, Any]] = {"g13": g13_solution}

    def synthetic_solution(label: str, dependencies: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
        truth = put_raw(store, f"G14 synthetic truth {label}\n".encode("utf-8"))
        certificate = put_raw(store, f"G14 synthetic certificate {label}\n".encode("utf-8"))
        edges = sorted(
            [
                {
                    "allow_superseded": False,
                    "expected_model": synthetic_model,
                    "role": role,
                    "target": target,
                }
                for role, target in dependencies
            ],
            key=lambda item: (item["role"], item["target"]["digest"]),
        )
        record = {
            "arena": synthetic_arena,
            "certificate": certificate,
            "certificate_contract": authorities["g14"],
            "claim_class": "ENGINEERING_TEST",
            "dependencies": edges,
            "domain": f"G14 synthetic control {label}",
            "kind": "SOLUTION_CORE",
            "model": synthetic_model,
            "reachability": "SYNTHETIC",
            "schema_version": "G14.OBJECT.v1",
            "solution_label": label,
            "source_set": synthetic_sources,
            "truth": truth,
        }
        ref = store.put_record(record)
        solution_records[label] = record
        solutions[label] = ref
        return ref

    base = synthetic_solution("diamond-base", [])
    left = synthetic_solution("diamond-left", [("shared-base", base)])
    right = synthetic_solution("diamond-right", [("shared-base", base)])
    top = synthetic_solution("diamond-top", [("left-branch", left), ("right-branch", right)])
    old = synthetic_solution("supersession-old", [])
    new = synthetic_solution("supersession-new", [])

    proof_record = {
        "claim_class": "ENGINEERING_TEST",
        "domain": "G14 shared-dependency diamond",
        "kind": "PROOF",
        "model": synthetic_model,
        "nodes": [
            {"depends_on": [], "node_id": "n0-base", "solution": base},
            {"depends_on": ["n0-base"], "node_id": "n1-left", "solution": left},
            {"depends_on": ["n0-base"], "node_id": "n2-right", "solution": right},
            {"depends_on": ["n1-left", "n2-right"], "node_id": "n3-top", "solution": top},
        ],
        "proof_id": "G14.DIAMOND.PROOF.v1",
        "roots": ["n3-top"],
        "schema_version": "G14.OBJECT.v1",
    }
    proof = store.put_record(proof_record)

    supersession_record = {
        "authority": authorities["g14"],
        "event_id": "G14.SYNTHETIC.SUPERSESSION.v1",
        "event_type": "SUPERSEDES",
        "evidence": [raw["acceptance"]],
        "historical_effect": "NON_RETROACTIVE",
        "kind": "LINEAGE_EVENT",
        "replacement": new,
        "schema_version": "G14.OBJECT.v1",
        "scope": "synthetic supersession-control logical object only",
        "status": "ACCEPTED_EVENT",
        "subject": old,
    }
    supersession = store.put_record(supersession_record)
    recovery_g10_record = {
        "authority": authorities["g14"],
        "event_id": "G14.G10.BYTES.RECOVERED.PRESERVED.v1",
        "event_type": "BYTES_RECOVERED",
        "evidence": [raw["g10_bundle"]],
        "historical_effect": "NON_RETROACTIVE",
        "kind": "LINEAGE_EVENT",
        "schema_version": "G14.OBJECT.v1",
        "scope": "G10 bundle availability only; historical G11 HOLD and pending replay remain unchanged",
        "status": "ACCEPTED_EVENT",
        "subject": raw["g10_bundle"],
    }
    recovery_g10 = store.put_record(recovery_g10_record)
    recovery_record = {
        "authority": authorities["g14"],
        "event_id": "G14.G12.BYTES.RECOVERED.PRESERVED.v1",
        "event_type": "BYTES_RECOVERED",
        "evidence": [raw["g12_bundle"]],
        "historical_effect": "NON_RETROACTIVE",
        "kind": "LINEAGE_EVENT",
        "schema_version": "G14.OBJECT.v1",
        "scope": "G12 bundle availability only; not G13 acceptance replay",
        "status": "ACCEPTED_EVENT",
        "subject": raw["g12_bundle"],
    }
    recovery = store.put_record(recovery_record)

    occurrences: list[dict[str, Any]] = []
    occurrence_records: list[dict[str, Any]] = []
    for index, (name, content, container, historical, current, programme) in enumerate([
        ("campaign/problem.json", raw["campaign/problem.json"], raw["g13_bundle"], "PRESENT", "PRESENT", "G13"),
        ("campaign/A_baseline_4/merged/truth.bin", raw["campaign/A_baseline_4/merged/truth.bin"], raw["g13_bundle"], "PRESENT", "PRESENT", "G13"),
        ("campaign/A_baseline_4/merged/certificate.bin", raw["campaign/A_baseline_4/merged/certificate.bin"], raw["g13_bundle"], "PRESENT", "PRESENT", "G13"),
    ]):
        record = {
            "content": content,
            "current_availability": current,
            "historical_availability": historical,
            "kind": "OCCURRENCE",
            "member_path": name,
            "occurrence_id": f"G14.OCCURRENCE.{index:02d}",
            "programme": programme,
            "schema_version": "G14.OBJECT.v1",
            "source_container": container,
        }
        occurrence_records.append(record)
        occurrences.append(store.put_record(record))

    catalog_record = {
        "catalog_id": "G14.REFERENCE.CATALOG.v1",
        "entries": [
            {"active_target": g13_solution, "logical_name": "g13-engineering-reference", "status": "ACTIVE"},
            {"active_target": new, "logical_name": "supersession-control", "status": "ACTIVE"},
            {"active_target": proof, "logical_name": "synthetic-diamond", "status": "ACTIVE"},
        ],
        "kind": "CATALOG",
        "lineage_events": sorted_refs([recovery_g10, recovery, supersession]),
        "schema_version": "G14.OBJECT.v1",
    }
    catalog = store.put_record(catalog_record)
    release_record = {
        "attestations": sorted_refs(attestations),
        "authorities": sorted_refs(list(authorities.values())),
        "catalog": catalog,
        "claim_boundary": {
            "claim_class": "ENGINEERING_TEST",
            "initial_position_reachability_claimed": False,
            "new_chess_truth_claimed": False,
        },
        "kind": "RELEASE",
        "lineage_events": sorted_refs([recovery_g10, recovery, supersession]),
        "occurrences": sorted_refs(occurrences),
        "open_exceptions": [
            {
                "blocks": ["G15", "G17"],
                "bytes_status": "RECOVERED_EXACT_BYTES",
                "exception_id": "G13_MANDATORY_G12_REPLAY_OPEN",
                "replay_status": "NOT_PERFORMED",
                "status": "OPEN",
            }
        ],
        "release_id": "G14.REFERENCE.RELEASE.v1",
        "retention_policy": "RETAIN_ALL_ADMITTED_CLOSURE",
        "roots": sorted_refs([g13_solution, proof]),
        "schema_version": "G14.OBJECT.v1",
    }
    release = store.put_record(release_record)
    release_closure = store.resolve_closure([release])
    protected = sorted_refs([item[0] for item in release_closure.values()])
    orphan = put_raw(store, b"G14 rejected staging orphan; dry-run candidate only\n")
    gc_record = {
        "candidate_digest_claims": [
            {
                "algorithm": "sha256",
                "digest": orphan["digest"],
                "label": "rejected-staging-orphan",
                "reason": "unreachable from every admitted release in this frozen fixture",
            }
        ],
        "deletion_performed": False,
        "kind": "GC_PLAN",
        "plan_id": "G14.REFERENCE.GC.DRYRUN.v1",
        "policy": "DRY_RUN_ONLY",
        "protected_objects": protected,
        "release": release,
        "schema_version": "G14.OBJECT.v1",
    }
    gc_plan = store.put_record(gc_record)
    roots = sorted_refs([release, gc_plan])
    full_closure = store.resolve_closure(roots)

    return {
        "attestation_records": attestation_records,
        "attestations": sorted_refs(attestations),
        "authorities": authorities,
        "authority_records": authority_records,
        "catalog": catalog,
        "catalog_record": catalog_record,
        "contract_ref": raw["contract"],
        "full_closure": full_closure,
        "g13_arena": g13_arena,
        "g13_arena_record": g13_arena_record,
        "g13_model": g13_model,
        "g13_model_record": g13_model_record,
        "g13_solution": g13_solution,
        "gc_plan": gc_plan,
        "gc_record": gc_record,
        "identities": {
            "attestations": [ref["digest"] for ref in sorted_refs(attestations)],
            "catalog": catalog["digest"],
            "g13_solution_core": g13_solution["digest"],
            "gc_plan": gc_plan["digest"],
            "proof": proof["digest"],
            "release": release["digest"],
            "synthetic_model": synthetic_model["digest"],
        },
        "lineage": {"g10_recovery": recovery_g10, "recovery": recovery, "supersession": supersession},
        "lineage_records": {
            "g10_recovery": recovery_g10_record,
            "recovery": recovery_record,
            "supersession": supersession_record,
        },
        "old": old,
        "new": new,
        "proof": proof,
        "proof_record": proof_record,
        "raw": raw,
        "release": release,
        "release_record": release_record,
        "roots": roots,
        "solution_records": solution_records,
        "solutions": solutions,
        "store": store,
        "synthetic_model": synthetic_model,
    }


def write_zip_payloads(path: Path, payloads: list[tuple[str, bytes]]) -> None:
    with zipfile.ZipFile(path, "w", allowZip64=False) as archive:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            for name, data in payloads:
                archive.writestr(_zip_info(name), data)


def bundle_payloads(path: Path) -> list[tuple[str, bytes]]:
    with zipfile.ZipFile(path, "r") as archive:
        return [(info.filename, archive.read(info)) for info in archive.infolist()]


def expect_reject(case_id: str, mutation: str, action: Callable[[], None]) -> dict[str, Any]:
    try:
        action()
    except (StoreError, zipfile.BadZipFile, EOFError, UnicodeError) as error:
        return {
            "expected": "REJECT",
            "id": case_id,
            "mutation": mutation,
            "observed": "REJECT",
            "reason": f"{type(error).__name__}: {error}",
            "result": "PASS",
        }
    return {
        "expected": "REJECT",
        "id": case_id,
        "mutation": mutation,
        "observed": "ACCEPT",
        "reason": "mutation was not rejected",
        "result": "FAIL",
    }


def run_hostile_campaign(fixture: dict[str, Any], accepted_bundle: Path, temporary: Path) -> list[dict[str, Any]]:
    temporary.mkdir(parents=True, exist_ok=True)
    store: ProofStore = fixture["store"]
    cases: list[dict[str, Any]] = []

    def add(case_id: str, mutation: str, action: Callable[[], None]) -> None:
        cases.append(expect_reject(case_id, mutation, action))

    def corrupted_store(ref: dict[str, Any], mutate: Callable[[bytes], bytes], name: str) -> None:
        root = temporary / name
        target_store = ProofStore(root)
        data = store.read(ref)
        path = root / object_relpath(ref["digest"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(mutate(data))
        target_store.read(ref)

    add("H01", "BIT_FLIP_OBJECT_UNDER_OLD_ADDRESS", lambda: corrupted_store(fixture["g13_solution"], lambda data: bytes([data[0] ^ 1]) + data[1:], "h01"))
    add("H02", "WRONG_DECLARED_OBJECT_LENGTH", lambda: store.read({**fixture["g13_solution"], "size": fixture["g13_solution"]["size"] + 1}))

    def h03() -> None:
        target = ProofStore(temporary / "h03")
        ref = target.put_bytes(b"collision-control-A")
        path = target.root / object_relpath(ref["digest"])
        path.write_bytes(b"collision-control-B")
        target.put_bytes(b"collision-control-A")

    add("H03", "SAME_ADDRESS_DIFFERENT_BYTES_COLLISION_SIMULATION", h03)
    add("H04", "NONCANONICAL_JSON", lambda: strict_json_loads(b'{"b":1, "a":2}\n'))
    add("H05", "DUPLICATE_JSON_KEY", lambda: strict_json_loads(b'{"a":1,"a":2}\n'))

    def mutate_record(record: dict[str, Any], operation: Callable[[dict[str, Any]], None]) -> None:
        value = copy.deepcopy(record)
        operation(value)
        validate_record_shape(value)

    add("H06", "UNKNOWN_RECORD_FIELD", lambda: mutate_record(fixture["release_record"], lambda value: value.__setitem__("unknown", True)))
    add("H07", "UNSORTED_OR_DUPLICATE_DEPENDENCIES", lambda: mutate_record(fixture["solution_records"]["diamond-top"], lambda value: value["dependencies"].reverse()))

    def h08() -> None:
        value = copy.deepcopy(fixture["solution_records"]["diamond-top"])
        value["dependencies"][0]["target"] = {"algorithm": "sha256", "digest": "0" * 64, "expected_kind": "SOLUTION_CORE", "size": 1}
        ref = store.put_record(value)
        store.resolve_closure([ref])

    add("H08", "MISSING_DEPENDENCY_LEAF", h08)
    add("H09", "WRONG_KIND_DEPENDENCY_TARGET", lambda: mutate_record(fixture["solution_records"]["diamond-top"], lambda value: value["dependencies"][0]["target"].__setitem__("expected_kind", "RAW")))
    add("H10", "CYCLIC_INTERNAL_PROOF_GRAPH", lambda: mutate_record(fixture["proof_record"], lambda value: value["nodes"][0]["depends_on"].append("n3-top")))
    add("H11", "MUTABLE_LOGICAL_ALIAS_AS_DEPENDENCY", lambda: mutate_record(fixture["solution_records"]["diamond-top"], lambda value: value["dependencies"][0].__setitem__("target", "KQK_latest")))
    add("H12", "CHANGED_RULES_WITH_UNCHANGED_SOLUTION_ID", lambda: corrupted_store(fixture["g13_model"], lambda data: data.replace(b"engineering-reference-only-not-chess", b"G10.RULES.v1.0________________"), "h12"))
    add("H13", "CHANGED_STATE_PROFILE_WITH_UNCHANGED_SOLUTION_ID", lambda: corrupted_store(fixture["g13_model"], lambda data: data.replace(b"G13.TEST.COMPONENT.STATE.v1", b"G12.STATE.SERIAL.v2_______"), "h13"))

    def resolve_mutated_solution(operation: Callable[[dict[str, Any]], None], suffix: str) -> None:
        value = copy.deepcopy(fixture["solution_records"]["g13"])
        operation(value)
        ref = store.put_record(value)
        store.resolve_closure([ref])

    add("H14", "TRUTH_AND_CERTIFICATE_ROLE_SWAP", lambda: resolve_mutated_solution(lambda value: (value.__setitem__("truth", value["certificate"]), value.__setitem__("certificate", fixture["solution_records"]["g13"]["truth"])), "h14"))
    add("H15", "G13_PLAN_HASH_INSERTED_IN_SOLUTION_CORE", lambda: mutate_record(fixture["solution_records"]["g13"], lambda value: value.__setitem__("execution_plan", fixture["raw"][PLAN_NAMES[0]])))
    add("H16", "CHANGED_PROBLEM_HASH_WITH_UNCHANGED_SOLUTION_CORE", lambda: corrupted_store(fixture["g13_arena"], lambda data: data.replace(G13_PROBLEM_SHA256.encode(), ("f" * 64).encode()), "h16"))
    add("H17", "G13_ENGINEERING_FIXTURE_PROMOTED_TO_G10_CHESS_EXACT", lambda: resolve_mutated_solution(lambda value: value.__setitem__("claim_class", "EXACT"), "h17"))
    add("H18", "LOSSY_G13_FIELD_PROJECTION", lambda: mutate_record(fixture["attestation_records"][0], lambda value: value["source_mapping"].pop()))

    def h19() -> None:
        value = copy.deepcopy(fixture["authority_records"]["g12"])
        value["content"] = fixture["raw"]["g10_handoff"]
        ref = store.put_record(value)
        store.resolve_closure([ref])

    add("H19", "G12_V2_ALIASED_TO_G10_IDENTITY", h19)
    add("H20", "RECOVERED_BYTES_MARKED_AS_REPLAY_PERFORMED", lambda: mutate_record(fixture["release_record"], lambda value: value["open_exceptions"][0].__setitem__("replay_status", "PERFORMED")))
    add("H21", "SUPERSESSION_SELF_OR_CYCLE", lambda: mutate_record(fixture["lineage_records"]["supersession"], lambda value: value.__setitem__("replacement", value["subject"])))

    def h22() -> None:
        value = copy.deepcopy(fixture["solution_records"]["diamond-left"])
        value["dependencies"] = [{
            "allow_superseded": False,
            "expected_model": fixture["synthetic_model"],
            "role": "old-default-reuse",
            "target": fixture["old"],
        }]
        ref = store.put_record(value)
        catalog_value = copy.deepcopy(fixture["catalog_record"])
        for entry in catalog_value["entries"]:
            if entry["logical_name"] == "synthetic-diamond":
                entry["active_target"] = ref
        catalog_ref = store.put_record(catalog_value)
        release_value = copy.deepcopy(fixture["release_record"])
        release_value["catalog"] = catalog_ref
        release_value["roots"] = sorted_refs([fixture["g13_solution"], ref])
        release_ref = store.put_record(release_value)
        store.resolve_closure([release_ref])

    add("H22", "SUPERSEDED_DEPENDENCY_REUSED_BY_DEFAULT", h22)

    def h23() -> None:
        value = copy.deepcopy(fixture["gc_record"])
        protected = value["protected_objects"][0]
        value["protected_objects"] = [
            ref for ref in value["protected_objects"] if ref["digest"] != protected["digest"]
        ]
        value["candidate_digest_claims"] = [{
            "algorithm": "sha256",
            "digest": protected["digest"],
            "label": "shared-release-object",
            "reason": "hostile attempted deletion",
        }]
        ref = store.put_record(value)
        store.resolve_closure([ref])

    add("H23", "GC_SHARED_OR_SUPERSEDED_RELEASE_OBJECT", h23)

    base_payloads = bundle_payloads(accepted_bundle)
    missing_bundle = temporary / "h24.zip"
    first_object = next(name for name, _ in base_payloads if name.startswith("objects/"))
    write_zip_payloads(missing_bundle, [(name, data) for name, data in base_payloads if name != first_object])
    add("H24", "PORTABLE_BUNDLE_MISSING_OBJECT", lambda: inspect_bundle(missing_bundle))
    extra_bundle = temporary / "h25.zip"
    write_zip_payloads(extra_bundle, base_payloads + [("unlisted-extra.bin", b"x")])
    add("H25", "PORTABLE_BUNDLE_EXTRA_OBJECT", lambda: inspect_bundle(extra_bundle))
    duplicate_bundle = temporary / "h26.zip"
    write_zip_payloads(duplicate_bundle, base_payloads + [base_payloads[1]])
    add("H26", "PORTABLE_BUNDLE_DUPLICATE_OR_CASE_COLLIDING_NAME", lambda: inspect_bundle(duplicate_bundle))
    unsafe_bundle = temporary / "h27.zip"
    write_zip_payloads(unsafe_bundle, base_payloads + [("../escape", b"x")])
    add("H27", "PORTABLE_BUNDLE_UNSAFE_PATH", lambda: inspect_bundle(unsafe_bundle))

    tampered_bundle = temporary / "h28.zip"
    tampered_payloads = list(base_payloads)
    manifest = strict_json_loads(tampered_payloads[0][1])
    manifest["inventory"][0]["ref"]["size"] += 1
    tampered_payloads[0] = ("bundle_manifest.json", canonical_json_bytes(manifest))
    write_zip_payloads(tampered_bundle, tampered_payloads)
    add("H28", "PORTABLE_BUNDLE_INVENTORY_HASH_OR_SIZE_TAMPER", lambda: inspect_bundle(tampered_bundle))
    truncated_bundle = temporary / "h29.zip"
    truncated_bundle.write_bytes(accepted_bundle.read_bytes()[: len(accepted_bundle.read_bytes()) // 2])
    add("H29", "PORTABLE_BUNDLE_TRUNCATION", lambda: inspect_bundle(truncated_bundle))

    def h30() -> None:
        target = temporary / "h30-published-store"
        try:
            import_bundle(missing_bundle, target)
        except (StoreError, zipfile.BadZipFile) as error:
            if target.exists():
                raise AssertionError("failed import published a partial root")
            raise StoreError(f"failed import remained unpublished: {error}") from error

    add("H30", "FAILED_IMPORT_PUBLISHES_PARTIAL_ROOT", h30)
    return cases


def run_g13_independent_replay(fixture: dict[str, Any], imported: ProofStore, temporary: Path) -> dict[str, Any]:
    temporary.mkdir(parents=True, exist_ok=True)
    problem = temporary / "problem.json"
    truth = temporary / "truth.bin"
    certificate = temporary / "certificate.bin"
    verifier = temporary / "g13_reference_verifier.py"
    out = temporary / "g13_replay.json"
    problem.write_bytes(imported.read(fixture["raw"]["campaign/problem.json"]))
    truth.write_bytes(imported.read(fixture["raw"]["campaign/A_baseline_4/merged/truth.bin"]))
    certificate.write_bytes(imported.read(fixture["raw"]["campaign/A_baseline_4/merged/certificate.bin"]))
    verifier.write_bytes(imported.read(fixture["raw"]["g13_reference_verifier.py"]))
    command = [
        sys.executable,
        str(verifier),
        "--problem", str(problem),
        "--truth", str(truth),
        "--certificate", str(certificate),
        "--out", str(out),
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=120)
    if result.returncode != 0:
        raise StoreError(f"independent G13 replay failed: {result.stderr or result.stdout}")
    ledger = json.loads(out.read_text(encoding="utf-8"))
    if not ledger.get("pass") or ledger.get("states_checked") != 65536:
        raise StoreError("independent G13 replay ledger does not pass frozen domain")
    return {
        "bellman_or_index_mismatches": ledger["bellman_or_index_mismatches"],
        "claim_class": ledger["claim_class"],
        "command": "python g13_reference_verifier.py --problem <portable> --truth <portable> --certificate <portable> --out <ledger>",
        "exit_code": result.returncode,
        "states_checked": ledger["states_checked"],
        "truth_certificate_mismatches": ledger["truth_certificate_mismatches"],
    }


def run_independent_verifier(verifier: Path, bundle: Path, ledger: Path) -> dict[str, Any]:
    if verifier.resolve() != INDEPENDENT_VERIFIER.resolve():
        raise StoreError("independent verifier path is not the frozen G14 verifier")
    file_bytes(verifier, EXPECTED["verifier"])
    if ledger.exists():
        raise StoreError("independent verifier ledger staging path already exists")
    command = [
        sys.executable,
        str(verifier),
        str(bundle),
        "--ledger",
        str(ledger),
        "--expected-contract-sha256",
        EXPECTED["contract"],
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=120)
    if result.returncode != 0:
        raise StoreError(f"independent G14 verifier failed: {result.stderr or result.stdout}")
    value = strict_json_loads(ledger.read_bytes())
    expected_check_ids = [
        "SPEC_BINDING",
        "ZIP_ENVELOPE",
        "BUNDLE_MANIFEST",
        "CAS_OBJECTS_AND_RECORDS",
        "TYPED_CLOSURE_AND_KINDS",
        "PROOF_DAGS",
        "LINEAGE_CATALOG_AND_RETENTION",
        "RELEASE_AND_CLAIM_BOUNDARIES",
        "G13_LOSSLESS_FIXTURE",
        "GC_DRY_RUN",
    ]
    if (
        value.get("schema_version") != "1.0.0"
        or value.get("verifier_id") != "G14.INDEPENDENT.VERIFIER.v1"
        or value.get("status") != "PASS"
        or value.get("bundle_sha256") != sha256_hex(bundle.read_bytes())
        or value.get("contract_sha256") != EXPECTED["contract"]
        or value.get("acceptance_sha256") != EXPECTED["acceptance"]
        or value.get("offline") is not True
        or value.get("producer_code_imported") is not False
        or value.get("errors") != []
        or [item.get("id") for item in value.get("checks", [])] != expected_check_ids
        or any(item.get("status") != "PASS" for item in value.get("checks", []))
        or value.get("summary", {}).get("checks_passed") != len(expected_check_ids)
        or value.get("summary", {}).get("checks_failed") != 0
    ):
        raise StoreError("independent G14 verifier ledger is incomplete, unbound, or not PASS")
    return value


def run_campaign(output_dir: Path, work_parent: Path, verifier: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    campaign_started = time.monotonic()
    acceptance = json.loads(file_bytes(ACCEPTANCE, EXPECTED["acceptance"]).decode("utf-8"))
    campaign_limit = acceptance["resource_limits"]["max_campaign_seconds"]
    if campaign_limit != 300 or acceptance["resource_limits"]["network_required_for_replay"] is not False:
        raise StoreError("prospectively frozen campaign resource policy changed")
    output_dir.mkdir(parents=True, exist_ok=True)
    work_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="g14-campaign-", dir=work_parent) as name:
        work = Path(name)
        fixture_a = build_fixture(work / "store-a")
        fixture_b = build_fixture(work / "store-b")
        if fixture_a["identities"] != fixture_b["identities"] or fixture_a["roots"] != fixture_b["roots"]:
            raise StoreError("fresh-store fixture identities differ")
        # Idempotent duplicate insertion must compare exact bytes and retain identity.
        duplicate = fixture_a["store"].put_bytes(CONTRACT.read_bytes())
        if duplicate != fixture_a["contract_ref"]:
            raise StoreError("idempotent duplicate insert changed identity")

        bundle_a = work / "bundle-a.zip"
        bundle_b = work / "bundle-b.zip"
        export_bundle(fixture_a["store"], bundle_a, fixture_a["roots"], fixture_a["contract_ref"])
        export_bundle(fixture_b["store"], bundle_b, fixture_b["roots"], fixture_b["contract_ref"])
        if bundle_a.read_bytes() != bundle_b.read_bytes():
            raise StoreError("two fresh exports are not byte-identical")
        accepted_bundle = work / "G14_Portable_Proof_Store_Bundle.zip"
        os.replace(bundle_a, accepted_bundle)

        manifest_one = import_bundle(accepted_bundle, work / "import-one")
        manifest_two = import_bundle(accepted_bundle, work / "import-two")
        imported_one = ProofStore(work / "import-one")
        imported_two = ProofStore(work / "import-two")
        closure_one = imported_one.resolve_closure(manifest_one["roots"])
        closure_two = imported_two.resolve_closure(manifest_two["roots"])
        if set(closure_one) != set(closure_two):
            raise StoreError("offline imports resolve different closures")
        reexport_one = work / "reexport-one.zip"
        reexport_two = work / "reexport-two.zip"
        export_bundle(imported_one, reexport_one, manifest_one["roots"], manifest_one["contract"])
        export_bundle(imported_two, reexport_two, manifest_two["roots"], manifest_two["contract"])
        if reexport_one.read_bytes() != accepted_bundle.read_bytes() or reexport_two.read_bytes() != accepted_bundle.read_bytes():
            raise StoreError("offline import/re-export changed portable bytes")

        g13_replay = run_g13_independent_replay(fixture_a, imported_one, work / "g13-replay")
        independent_ledger_path = work / "G14_Independent_Verification_Ledger.json"
        independent = run_independent_verifier(verifier, accepted_bundle, independent_ledger_path)
        hostiles = run_hostile_campaign(fixture_a, accepted_bundle, work / "hostiles")
        if any(item["result"] != "PASS" for item in hostiles):
            failed = [item["id"] for item in hostiles if item["result"] != "PASS"]
            raise StoreError(f"hostile campaign accepted mutations: {failed}")

        release_closure = fixture_a["store"].resolve_closure([fixture_a["release"]])
        old_bytes = fixture_a["store"].read(fixture_a["old"])
        if not old_bytes or fixture_a["old"]["digest"] not in release_closure:
            raise StoreError("superseded subject was not retained in release closure")
        if fixture_a["authorities"]["g10"]["digest"] == fixture_a["authorities"]["g12"]["digest"]:
            raise StoreError("G10 and G12 authority identities were aliased")
        if len({ref["digest"] for ref in fixture_a["attestations"]}) != 5:
            raise StoreError("G13 five-plan projection did not produce five attestations")
        if {record["solution"]["digest"] for record in fixture_a["attestation_records"]} != {fixture_a["g13_solution"]["digest"]}:
            raise StoreError("execution topology contaminated solution-core identity")

        positives = [
            ("P01", "AUTHORITY_AND_ARCHIVE_HASH_GATE", "All frozen outer and selected inner identities matched."),
            ("P02", "RAW_CAS_ROUND_TRIP_AND_IDEMPOTENT_DUPLICATE_INSERT", "Exact duplicate insertion retained one content ID after byte comparison."),
            ("P03", "SHARED_DEPENDENCY_DIAMOND_FULL_TYPED_CLOSURE", "Diamond closure resolved with one shared base object."),
            ("P04", "LOSSLESS_G13_FIVE_PLAN_PROJECTION", "All nine G13 projection fields were retained in each attestation."),
            ("P05", "ONE_G13_SOLUTION_CORE_FIVE_DISTINCT_ATTESTATIONS", "Five plan attestations point to one topology-independent solution core."),
            ("P06", "G10_AND_G12_IDENTITIES_REMAIN_DISTINCT", "G10 rules and G12 v2 state authorities have distinct content IDs."),
            ("P07", "SUPERSESSION_RETENTION_AND_ACTIVE_RESOLUTION", "Catalog resolves replacement; old immutable subject remains in closure."),
            ("P08", "GC_DRY_RUN_WITH_ZERO_DELETIONS", "Only an unreachable staging orphan was listed; deletion_performed=false."),
            ("P09", "TWO_EMPTY_STORE_EXPORTS_BYTE_IDENTICAL", "Independent builds emitted byte-identical ZIP_STORED bundles."),
            ("P10", "TWO_OFFLINE_EMPTY_STORE_IMPORTS_RESOLVE_FULL_RELEASE", f"Both imports resolved {len(closure_one)} typed objects."),
            ("P11", "STRUCTURALLY_SEPARATE_VERIFIER_RECOMPUTES_ALL_HASHES_AND_GRAPH_OBLIGATIONS", f"Independent verifier passed {independent['summary']['checks_passed']} checks."),
            ("P12", "REEXPORT_AFTER_IMPORT_BYTE_IDENTICAL", "Both offline imports re-exported exact accepted bundle bytes."),
            ("P13", "OPEN_G13_G12_REPLAY_EXCEPTION_PRESERVED_NONRETROACTIVELY", "Recovered bytes remain NOT_PERFORMED; G15/G17 remain blocked."),
            ("P14", "PORTABLE_RELEASE_REPRODUCES_EXACT_DECLARED_ENGINEERING_MODEL", f"Fresh G13 verifier replayed {g13_replay['states_checked']} synthetic states with zero mismatch."),
        ]
        campaign = {
            "bundle": {
                "bytes": accepted_bundle.stat().st_size,
                "object_count": len(inspect_bundle(accepted_bundle)[1]),
                "sha256": sha256_hex(accepted_bundle.read_bytes()),
            },
            "claim_class": "ENGINEERING_TEST",
            "g13_independent_replay": g13_replay,
            "identities": fixture_a["identities"],
            "positive_checks": [
                {"expected": "PASS", "id": identifier, "result": "PASS", "summary": summary, "test": test}
                for identifier, test, summary in positives
            ],
            "programme": "G14",
            "resource_gate": {
                "max_campaign_seconds": campaign_limit,
                "network_used": False,
                "within_limit": True,
            },
            "result": "PASS",
            "run_id": "G14-a01-d02c7f5da9fe",
            "schema_version": "1.0.0",
            "summary": "14/14 positive checks passed; proof-store evidence is engineering/preservation, not chess truth.",
        }
        hostile_ledger = {
            "cases": hostiles,
            "claim_class": "ENGINEERING_TEST",
            "rejected": sum(item["observed"] == "REJECT" for item in hostiles),
            "result": "PASS",
            "schema_version": "1.0.0",
            "summary": "30/30 prospectively frozen hostile mutations rejected.",
            "total": len(hostiles),
        }
        expected_positives = [(item["id"], item["test"]) for item in acceptance["positive_checks"]]
        observed_positives = [(item["id"], item["test"]) for item in campaign["positive_checks"]]
        expected_hostiles = [(item["id"], item["mutation"]) for item in acceptance["hostile_cases"]]
        observed_hostiles = [(item["id"], item["mutation"]) for item in hostile_ledger["cases"]]
        if expected_positives != observed_positives or len(observed_positives) != 14:
            raise StoreError("executed positive checks differ from prospectively frozen acceptance")
        if expected_hostiles != observed_hostiles or len(observed_hostiles) != 30:
            raise StoreError("executed hostile cases differ from prospectively frozen acceptance")
        if time.monotonic() - campaign_started > campaign_limit:
            raise StoreError("campaign exceeded prospectively frozen 300-second resource limit")

        staged_campaign = work / "G14_Reference_Campaign_Ledger.json"
        staged_hostile = work / "G14_Hostile_Mutation_Ledger.json"
        staged_campaign.write_bytes(canonical_json_bytes(campaign))
        staged_hostile.write_bytes(canonical_json_bytes(hostile_ledger))
        for source, target_name in [
            (staged_campaign, "G14_Reference_Campaign_Ledger.json"),
            (staged_hostile, "G14_Hostile_Mutation_Ledger.json"),
            (independent_ledger_path, "G14_Independent_Verification_Ledger.json"),
            (accepted_bundle, "G14_Portable_Proof_Store_Bundle.zip"),
        ]:
            os.replace(source, output_dir / target_name)
        return campaign, hostile_ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    parser.add_argument("--work-parent", type=Path, required=True)
    parser.add_argument("--verifier", type=Path, default=HERE / "g14_independent_verifier.py")
    args = parser.parse_args()
    try:
        campaign, hostile = run_campaign(args.output_dir.resolve(), args.work_parent.resolve(), args.verifier.resolve())
        print(json.dumps({
            "bundle": campaign["bundle"],
            "hostile_rejections": hostile["rejected"],
            "positive_checks": len(campaign["positive_checks"]),
            "result": "PASS",
        }, indent=2, sort_keys=True))
        return 0
    except Exception as error:
        print(json.dumps({"error": f"{type(error).__name__}: {error}", "result": "FAIL"}, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
