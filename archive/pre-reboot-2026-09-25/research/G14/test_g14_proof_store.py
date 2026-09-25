"""Regression tests for G14 proof-store defects found during hostile review.

These tests deliberately import the producer-side implementation.  They complement,
but do not replace, the structurally separate offline verifier.
"""

from __future__ import annotations

import copy
import hashlib
import json
import stat
import tempfile
import unittest
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from g14_proof_store import (
    FIXED_ZIP_TIME,
    G13_TRUTH_SHA256,
    ProofStore,
    StoreError,
    _zip_info,
    canonical_json_bytes,
    export_bundle,
    inspect_bundle,
    make_ref,
    object_relpath,
)
from g14_reference_campaign import (
    ACCEPTANCE,
    EXPECTED,
    HERE,
    build_fixture,
    run_independent_verifier,
    sorted_refs,
)


FINAL_BUNDLE = HERE / "G14_Portable_Proof_Store_Bundle.zip"
FRESH_REPRODUCTION_SHA256 = "4ba70905efb88ad35d2d3c7cfdf70fde9eb3a8b3bbcec90eebf660809eb81c10"


class G14RegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(prefix="g14-regression-")
        cls.root = Path(cls.temporary.name)
        cls.fixture = build_fixture(cls.root / "fixture-store")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def assert_store_rejects(self, action, pattern: str) -> None:
        with self.assertRaisesRegex(StoreError, pattern):
            action()

    def bundle_payloads(self) -> tuple[dict, dict[str, bytes]]:
        with zipfile.ZipFile(FINAL_BUNDLE, "r") as archive:
            payloads = {info.filename: archive.read(info) for info in archive.infolist()}
        return json.loads(payloads["bundle_manifest.json"]), payloads

    def write_bundle(
        self,
        name: str,
        manifest: dict,
        payloads: dict[str, bytes],
        *,
        mode_name: str | None = None,
        member_comment_name: str | None = None,
        archive_comment: bytes = b"",
    ) -> Path:
        target = self.root / name
        payloads = dict(payloads)
        payloads["bundle_manifest.json"] = canonical_json_bytes(manifest)
        with zipfile.ZipFile(target, "w", allowZip64=False) as archive:
            archive.comment = archive_comment
            for entry_name in sorted(payloads):
                info = _zip_info(entry_name)
                if entry_name == mode_name:
                    info.external_attr = (stat.S_IFREG | 0o600) << 16
                if entry_name == member_comment_name:
                    info.comment = b"not-deterministic"
                archive.writestr(info, payloads[entry_name])
        return target

    def test_acceptance_bytes_are_hash_bound(self) -> None:
        self.assertEqual(hashlib.sha256(ACCEPTANCE.read_bytes()).hexdigest(), EXPECTED["acceptance"])

    def test_empty_open_exception_is_rejected(self) -> None:
        record = copy.deepcopy(self.fixture["release_record"])
        record["open_exceptions"] = []
        self.assert_store_rejects(
            lambda: self.fixture["store"].put_record(record),
            "exactly one frozen G13/G12 open exception",
        )

    def test_wrong_g13_projection_target_is_rejected(self) -> None:
        record = copy.deepcopy(self.fixture["attestation_records"][0])
        record["source_mapping"][0]["target_field"] = "arbitrary.mutable.alias"
        self.assert_store_rejects(
            lambda: self.fixture["store"].put_record(record),
            "source mapping policy mismatch",
        )

    def test_synthetic_reachability_promotion_is_rejected(self) -> None:
        record = copy.deepcopy(self.fixture["solution_records"]["g13"])
        record["reachability"] = "START_REACHABLE"
        ref = self.fixture["store"].put_record(record)
        self.assert_store_rejects(
            lambda: self.fixture["store"].resolve_closure([ref]),
            "reachability differs",
        )

    def test_gc_protection_must_equal_release_closure(self) -> None:
        record = copy.deepcopy(self.fixture["gc_record"])
        record["protected_objects"] = record["protected_objects"][1:]
        ref = self.fixture["store"].put_record(record)
        self.assert_store_rejects(
            lambda: self.fixture["store"].resolve_closure([ref]),
            "complete admitted release closure",
        )

    def test_generator_roots_preserve_semantic_validation(self) -> None:
        roots = (ref for ref in self.fixture["roots"])
        closure = self.fixture["store"].resolve_closure(roots)
        self.assertIn(self.fixture["release"]["digest"], closure)
        self.assertIn(self.fixture["gc_plan"]["digest"], closure)

    def test_duplicate_roots_are_rejected_before_export(self) -> None:
        self.assert_store_rejects(
            lambda: export_bundle(
                self.fixture["store"],
                self.root / "duplicate-roots.zip",
                [self.fixture["release"], self.fixture["release"]],
                self.fixture["contract_ref"],
            ),
            "duplicate digest",
        )

    def test_proof_local_edges_must_match_solution_dependencies(self) -> None:
        proof = copy.deepcopy(self.fixture["proof_record"])
        proof["nodes"][-1]["depends_on"] = ["n1-left"]
        proof_ref = self.fixture["store"].put_record(proof)
        self.assert_store_rejects(
            lambda: self.fixture["store"].resolve_closure([proof_ref]),
            "local edges disagree",
        )

    def test_withdrawn_solution_cannot_remain_catalog_active(self) -> None:
        event = {
            "authority": self.fixture["authorities"]["g14"],
            "event_id": "G14.TEST.WITHDRAWAL.v1",
            "event_type": "WITHDRAWN",
            "evidence": [self.fixture["raw"]["acceptance"]],
            "historical_effect": "NON_RETROACTIVE",
            "kind": "LINEAGE_EVENT",
            "schema_version": "G14.OBJECT.v1",
            "scope": "hostile withdrawal control",
            "status": "ACCEPTED_EVENT",
            "subject": self.fixture["new"],
        }
        event_ref = self.fixture["store"].put_record(event)
        catalog = copy.deepcopy(self.fixture["catalog_record"])
        catalog["lineage_events"] = sorted_refs(catalog["lineage_events"] + [event_ref])
        catalog_ref = self.fixture["store"].put_record(catalog)
        release = copy.deepcopy(self.fixture["release_record"])
        release["catalog"] = catalog_ref
        release["lineage_events"] = list(catalog["lineage_events"])
        release_ref = self.fixture["store"].put_record(release)
        self.assert_store_rejects(
            lambda: self.fixture["store"].resolve_closure([release_ref]),
            "superseded or withdrawn",
        )

    def test_old_catalog_snapshot_survives_later_nonretroactive_event(self) -> None:
        supersession_digest = self.fixture["lineage"]["supersession"]["digest"]
        historical_events = [
            ref
            for ref in self.fixture["catalog_record"]["lineage_events"]
            if ref["digest"] != supersession_digest
        ]
        catalog = copy.deepcopy(self.fixture["catalog_record"])
        catalog["lineage_events"] = historical_events
        for entry in catalog["entries"]:
            if entry["logical_name"] == "supersession-control":
                entry["active_target"] = self.fixture["old"]
        catalog_ref = self.fixture["store"].put_record(catalog)
        release = copy.deepcopy(self.fixture["release_record"])
        release["catalog"] = catalog_ref
        release["lineage_events"] = historical_events
        release["roots"] = sorted_refs([
            self.fixture["g13_solution"],
            self.fixture["old"],
            self.fixture["proof"],
        ])
        release_ref = self.fixture["store"].put_record(release)
        closure = self.fixture["store"].resolve_closure([release_ref, self.fixture["release"]])
        self.assertIn(release_ref["digest"], closure)
        self.assertIn(self.fixture["release"]["digest"], closure)

    def test_bundle_missing_declared_root_is_rejected_by_inspector(self) -> None:
        manifest, payloads = self.bundle_payloads()
        root = manifest["roots"][0]
        root_path = object_relpath(root["digest"])
        manifest["inventory"] = [item for item in manifest["inventory"] if item["path"] != root_path]
        payloads.pop(root_path)
        bundle = self.write_bundle("missing-root.zip", manifest, payloads)
        self.assert_store_rejects(lambda: inspect_bundle(bundle), "root/dependency is missing")

    def test_canonically_inventoried_unreachable_extra_is_rejected(self) -> None:
        manifest, payloads = self.bundle_payloads()
        data = b"canonically inventoried but unreachable\n"
        ref = make_ref(data, "RAW")
        path = object_relpath(ref["digest"])
        manifest["inventory"].append({"path": path, "ref": ref})
        manifest["inventory"].sort(key=lambda item: item["path"])
        payloads[path] = data
        bundle = self.write_bundle("unreachable-extra.zip", manifest, payloads)
        self.assert_store_rejects(lambda: inspect_bundle(bundle), "exact rooted closure")

    def test_wrong_contract_reference_is_rejected(self) -> None:
        manifest, payloads = self.bundle_payloads()
        truth_ref = next(
            item["ref"] for item in manifest["inventory"] if item["ref"]["digest"] == G13_TRUTH_SHA256
        )
        manifest["contract"] = truth_ref
        bundle = self.write_bundle("wrong-contract.zip", manifest, payloads)
        self.assert_store_rejects(lambda: inspect_bundle(bundle), "frozen G14 contract")

    def test_noncanonical_zip_metadata_is_rejected(self) -> None:
        manifest, payloads = self.bundle_payloads()
        object_name = next(name for name in payloads if name.startswith("objects/"))
        mutations = [
            ("mode-0600.zip", {"mode_name": object_name}),
            ("member-comment.zip", {"member_comment_name": object_name}),
            ("archive-comment.zip", {"archive_comment": b"not-deterministic"}),
        ]
        for name, options in mutations:
            with self.subTest(name=name):
                bundle = self.write_bundle(name, manifest, payloads, **options)
                self.assert_store_rejects(lambda bundle=bundle: inspect_bundle(bundle), "not deterministic|0644")

    def test_fresh_reproduction_and_frozen_context_are_reachable(self) -> None:
        manifest, objects = inspect_bundle(FINAL_BUNDLE)
        inventory = {item["ref"]["digest"]: item["ref"] for item in manifest["inventory"]}
        self.assertIn(FRESH_REPRODUCTION_SHA256, inventory)
        records = []
        for item in manifest["inventory"]:
            if item["ref"]["expected_kind"] != "RAW":
                records.append(json.loads(objects[item["ref"]["digest"]]))
        attestations = [record for record in records if record["kind"] == "ATTESTATION"]
        self.assertIn(FRESH_REPRODUCTION_SHA256, {record["merge_evidence"]["digest"] for record in attestations})
        g13_model = next(
            record
            for record in records
            if record["kind"] == "MODEL" and record["semantic_profile"] == "G13.TEST.SEMANTICS.v1"
        )
        authorities = {
            record["authority_id"]: digest
            for digest, record in (
                (item["ref"]["digest"], json.loads(objects[item["ref"]["digest"]]))
                for item in manifest["inventory"]
                if item["ref"]["expected_kind"] == "AUTHORITY"
            )
        }
        context_digests = {ref["digest"] for ref in g13_model["authority_context"]}
        self.assertEqual(
            context_digests,
            {authorities["G10.RULES.v1.0"], authorities["G12.STATE.SERIAL.v2"]},
        )

    def test_arbitrary_verifier_path_is_rejected_before_execution(self) -> None:
        fake = self.root / "fake_verifier.py"
        fake.write_text("raise SystemExit(0)\n", encoding="utf-8", newline="\n")
        self.assert_store_rejects(
            lambda: run_independent_verifier(fake, FINAL_BUNDLE, self.root / "fake-ledger.json"),
            "path is not the frozen G14 verifier",
        )

    def test_concurrent_duplicate_publication_retains_exact_bytes(self) -> None:
        store = ProofStore(self.root / "concurrent-store")
        data = b"concurrent immutable CAS publication\n"
        with ThreadPoolExecutor(max_workers=8) as executor:
            refs = list(executor.map(lambda _: store.put_bytes(data), range(32)))
        self.assertEqual(len({ref["digest"] for ref in refs}), 1)
        self.assertEqual(store.read(refs[0]), data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
