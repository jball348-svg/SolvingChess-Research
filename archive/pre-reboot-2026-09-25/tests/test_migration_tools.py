from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.migration.build_repository_snapshot import (
    build_snapshot,
    manifest_bytes,
)
from scripts.migration.docx_to_markdown import convert_docx
from scripts.migration.inventory import (
    CorpusInvariantError,
    discover_primary_corpus,
    primary_name_is_eligible,
)
from scripts.migration.migrate_corpus import (
    DEFAULT_MIGRATION_TIMESTAMP,
    MigrationError,
    apply_plan,
    build_plan,
    destination_for,
)

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

_SOURCE_TEMP: tempfile.TemporaryDirectory[str] | None = None
_SOURCE_ROOT: Path | None = None


def _migration_source_root() -> Path:
    """Provide an isolated flat seam before or after real relocation."""

    global _SOURCE_TEMP, _SOURCE_ROOT
    if _SOURCE_ROOT is not None:
        return _SOURCE_ROOT
    top_level = [
        path
        for path in ROOT.iterdir()
        if path.is_file() and primary_name_is_eligible(path.name)
    ]
    if len(top_level) == 129:
        sources = top_level
    else:
        sources = []
        for relative in (
            "roadmap/originals",
            "handoffs/originals",
            "legacy/originals",
        ):
            directory = ROOT / relative
            if directory.is_dir():
                sources.extend(path for path in directory.iterdir() if path.is_file())
    if len(sources) != 129 or len({path.name for path in sources}) != 129:
        raise AssertionError(
            f"cannot reconstruct the 129-file migration seam; found {len(sources)} files"
        )
    _SOURCE_TEMP = tempfile.TemporaryDirectory()
    _SOURCE_ROOT = Path(_SOURCE_TEMP.name)
    for source in sources:
        destination = _SOURCE_ROOT / source.name
        try:
            os.link(source, destination)
        except OSError:
            shutil.copy2(source, destination)
    return _SOURCE_ROOT


def tearDownModule() -> None:
    global _SOURCE_TEMP, _SOURCE_ROOT
    if _SOURCE_TEMP is not None:
        _SOURCE_TEMP.cleanup()
    _SOURCE_TEMP = None
    _SOURCE_ROOT = None


def _write_docx(path: Path) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    styles = f"""<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="{W_NS}">
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/></w:style>
  <w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/></w:style>
  <w:style w:type="paragraph" w:styleId="Callout"><w:name w:val="Callout"/></w:style>
  <w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/></w:style>
</w:styles>"""
    document = f"""<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="{W_NS}">
 <w:body>
  <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Frozen Heading</w:t></w:r></w:p>
  <w:p><w:r><w:t>Body text.</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr><w:r><w:t>List item</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="Callout"/></w:pPr><w:r><w:t>PASS; not promoted.</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr><w:r><w:t>hash = "abc"</w:t></w:r></w:p>
  <w:tbl>
   <w:tr><w:tc><w:p><w:r><w:t>Key</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Value</w:t></w:r></w:p></w:tc></w:tr>
   <w:tr><w:tc><w:p><w:r><w:t>Gate</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>HOLD</w:t></w:r></w:p></w:tc></w:tr>
  </w:tbl>
  <w:sectPr/>
 </w:body>
</w:document>"""
    with zipfile.ZipFile(path, "w") as archive:
        for name, payload in (
            ("[Content_Types].xml", content_types),
            ("_rels/.rels", rels),
            ("word/document.xml", document),
            ("word/styles.xml", styles),
        ):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            archive.writestr(info, payload.encode("utf-8"))


class InventoryTests(unittest.TestCase):
    def test_primary_selector_excludes_bootstrap_and_future_files(self) -> None:
        accepted = {
            "G13_Technical_Handoff.docx",
            "G8_Final_Closeout_Bundle.tar.gz",
            "Pilot_1_Follow_On_Experimental_Program.docx",
            "corrected_rank.bin",
        }
        rejected = {
            "README.md",
            "AGENTS.md",
            ".gitignore",
            ".gitmodules",
            "G14_NOT_STARTED.md",
            "pyproject.toml",
        }
        self.assertTrue(all(primary_name_is_eligible(name) for name in accepted))
        self.assertTrue(all(not primary_name_is_eligible(name) for name in rejected))

    def test_real_primary_seam_is_exact(self) -> None:
        files = discover_primary_corpus(_migration_source_root(), strict=True)
        self.assertEqual(len(files), 129)
        self.assertEqual(sum(item.size for item in files), 59_994_517)
        self.assertFalse(any("Other projects" in str(item.path) for item in files))

    def test_strict_invariant_rejects_partial_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "G13_Technical_Handoff.docx").write_bytes(b"x")
            with self.assertRaises(CorpusInvariantError):
                discover_primary_corpus(root, strict=True)


class DocxConverterTests(unittest.TestCase):
    def test_converter_retains_blocks_and_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.docx"
            _write_docx(source)
            first = convert_docx(
                source,
                derivative_filename="sample.md",
                conversion_timestamp=DEFAULT_MIGRATION_TIMESTAMP,
            )
            second = convert_docx(
                source,
                derivative_filename="sample.md",
                conversion_timestamp=DEFAULT_MIGRATION_TIMESTAMP,
            )
            self.assertEqual(first.markdown, second.markdown)
            self.assertEqual(first.audit, second.audit)
            text = first.markdown.decode("utf-8")
            self.assertIn("# Frozen Heading", text)
            self.assertIn("- List item", text)
            self.assertIn("> PASS; not promoted.", text)
            self.assertIn("```text\nhash = \"abc\"\n```", text)
            self.assertIn("| Key | Value |", text)
            self.assertIn("| Gate | HOLD |", text)
            self.assertEqual(first.audit["statistics"]["tables"], 1)
            self.assertEqual(first.audit["source"]["authority"], "CONTROLLING_IMMUTABLE_ORIGINAL")
            self.assertNotIn(str(source.stat().st_mtime), text)


class MigrationDriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = build_plan(
            _migration_source_root(),
            generated_at=DEFAULT_MIGRATION_TIMESTAMP,
            strict_source=True,
            include_archive_members=True,
        )

    def test_mapping_counts_and_paths(self) -> None:
        occurrences = self.plan.registry["occurrences"]
        self.assertEqual(len(occurrences), 129)
        self.assertEqual(
            sum(item["repository_path"].startswith("roadmap/originals/") for item in occurrences),
            4,
        )
        self.assertEqual(
            sum(item["repository_path"].startswith("handoffs/originals/") for item in occurrences),
            14,
        )
        self.assertEqual(
            sum(item["repository_path"].startswith("legacy/originals/") for item in occurrences),
            111,
        )
        self.assertEqual(len(self.plan.derivative_writes), 29)
        self.assertEqual(len(self.plan.audit_writes), 29)
        self.assertEqual(
            destination_for("G9_G10_Onwards_Long_Range_Plan.docx")[0].as_posix(),
            "roadmap/originals/G9_G10_Onwards_Long_Range_Plan.docx",
        )

    def test_registry_shape_duplicates_and_expected_missing(self) -> None:
        registry = self.plan.registry
        self.assertEqual(
            list(registry),
            [
                "schema_version",
                "registry_kind",
                "generated_at",
                "source_summary",
                "contents",
                "occurrences",
                "archive_members",
                "expected_missing",
                "audits",
            ],
        )
        self.assertEqual(registry["registry_kind"], "MIGRATION_ARTIFACT_REGISTRY")
        self.assertEqual(len(registry["contents"]), 124)
        self.assertEqual(len(registry["archive_members"]), 334)
        self.assertEqual(len(registry["expected_missing"]), 63)
        self.assertTrue(
            all(
                item["availability"] == "EXPECTED_ONLY_MISSING_FROM_MIGRATION_INPUT"
                and item["integrity_status"] == "NOT_CORRUPTION_NO_BYTES_SUPPLIED"
                for item in registry["expected_missing"]
            )
        )
        self.assertEqual(
            registry["audits"]["target_g12_bundle"]["status"], "FOUND_EXACTLY_ONCE"
        )
        self.assertEqual(
            registry["audits"]["checksum_references"]["present_hash_mismatches"], []
        )
        copy_policy = registry["audits"]["copy_policy"]
        self.assertEqual(copy_policy["status"], "PASS")
        self.assertEqual(copy_policy["scope"], "PRIMARY_INHERITED_CORPUS_ONLY")
        self.assertFalse(copy_policy["original_bytes_changed"])
        self.assertFalse(copy_policy["archives_exploded"])
        self.assertFalse(copy_policy["other_projects_touched"])
        internal = registry["audits"]["internal_archive_checksum_manifests"]
        self.assertEqual(internal["status"], "PASS")
        self.assertEqual(internal["manifest_occurrences"], 11)
        self.assertEqual(internal["reference_count"], 152)
        self.assertEqual(internal["resolved_exact"], 152)

    def test_plan_is_deterministic_and_dry_run_changes_nothing(self) -> None:
        second = build_plan(
            _migration_source_root(),
            generated_at=DEFAULT_MIGRATION_TIMESTAMP,
            strict_source=True,
            include_archive_members=True,
        )
        first_bytes = json.dumps(self.plan.registry, sort_keys=True).encode("utf-8")
        second_bytes = json.dumps(second.registry, sort_keys=True).encode("utf-8")
        self.assertEqual(first_bytes, second_bytes)
        self.assertEqual(
            [payload for _, payload in self.plan.derivative_writes],
            [payload for _, payload in second.derivative_writes],
        )
        self.assertFalse((_migration_source_root() / "roadmap" / "originals").exists())

    def test_apply_fixture_preserves_bytes_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "G9_Test.docx"
            _write_docx(source)
            plan = build_plan(
                root,
                generated_at=DEFAULT_MIGRATION_TIMESTAMP,
                strict_source=False,
                include_archive_members=True,
            )
            registry = root / "state" / "ARTIFACT_REGISTRY.json"
            apply_plan(root, plan, registry)
            destination = root / "legacy" / "originals" / source.name
            self.assertEqual(source.read_bytes(), destination.read_bytes())
            first_registry = registry.read_bytes()
            apply_plan(root, plan, registry)
            self.assertEqual(first_registry, registry.read_bytes())
            self.assertFalse((root / "Other projects").exists())

    def test_finalize_relocation_rejects_non_strict_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "G9_Test.docx"
            _write_docx(source)
            plan = build_plan(
                root,
                generated_at=DEFAULT_MIGRATION_TIMESTAMP,
                strict_source=False,
                include_archive_members=True,
            )
            with self.assertRaises(MigrationError):
                apply_plan(
                    root,
                    plan,
                    root / "state" / "ARTIFACT_REGISTRY.json",
                    finalize_relocation=True,
                )
            self.assertTrue(source.exists())

    def test_finalize_relocation_deletes_only_verified_explicit_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "G9_Test.docx"
            unrelated = root / "README.md"
            _write_docx(source)
            unrelated.write_text("keep", encoding="utf-8")
            plan = build_plan(
                root,
                generated_at=DEFAULT_MIGRATION_TIMESTAMP,
                strict_source=False,
                include_archive_members=True,
            )
            with mock.patch(
                "scripts.migration.migrate_corpus._verify_strict_relocation_sources"
            ) as verified:
                apply_plan(
                    root,
                    plan,
                    root / "state" / "ARTIFACT_REGISTRY.json",
                    finalize_relocation=True,
                )
            verified.assert_called_once()
            self.assertFalse(source.exists())
            self.assertTrue(unrelated.exists())
            self.assertTrue((root / "legacy" / "originals" / source.name).is_file())


class SnapshotTests(unittest.TestCase):
    def test_manifest_identity_and_zip_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "z.txt").write_bytes(b"z\n")
            (root / "a.txt").write_bytes(b"alpha")
            z_digest = hashlib.sha256(b"z\n").hexdigest()
            expected = (
                f"a.txt\t5\t{hashlib.sha256(b'alpha').hexdigest()}\n"
                f"z.txt\t2\t{z_digest}\n"
            ).encode()
            self.assertEqual(manifest_bytes(root, ["z.txt", "a.txt"]), expected)
            manifest1, zip1 = root / "m1.txt", root / "one.zip"
            manifest2, zip2 = root / "m2.txt", root / "two.zip"
            first = build_snapshot(root, manifest1, zip1, paths=["z.txt", "a.txt"])
            second = build_snapshot(root, manifest2, zip2, paths=["a.txt", "z.txt"])
            self.assertEqual(manifest1.read_bytes(), manifest2.read_bytes())
            self.assertEqual(zip1.read_bytes(), zip2.read_bytes())
            self.assertEqual(first.zip_sha256, second.zip_sha256)
            with zipfile.ZipFile(zip1) as archive:
                self.assertEqual(archive.namelist(), ["a.txt", "z.txt"])
                self.assertTrue(
                    all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist())
                )

    def test_git_selection_uses_tracked_plus_nonignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
            (root / "tracked.txt").write_text("tracked", encoding="utf-8")
            (root / "ignored.txt").write_text("ignored", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "tracked.txt"], check=True
            )
            (root / "untracked.txt").write_text("untracked", encoding="utf-8")
            result = build_snapshot(root, root / "manifest.txt", root / "snapshot.zip")
            self.assertEqual(result.file_count, 3)
            with zipfile.ZipFile(root / "snapshot.zip") as archive:
                self.assertEqual(
                    archive.namelist(), [".gitignore", "tracked.txt", "untracked.txt"]
                )


if __name__ == "__main__":
    unittest.main()
