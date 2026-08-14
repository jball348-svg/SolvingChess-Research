#!/usr/bin/env python3
"""Loss-audited, standard-library DOCX-to-Markdown extraction.

The converter is intentionally conservative.  It preserves the original DOCX
as authority, emits useful agent-facing Markdown, and records every known class
of OOXML structure that Markdown cannot faithfully represent.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

try:  # Support both module use and direct script execution.
    from .inventory import canonical_json_bytes, sha256_bytes, sha256_file
except ImportError:  # pragma: no cover - exercised by the CLI entry point
    from inventory import canonical_json_bytes, sha256_bytes, sha256_file

TOOL_NAME = "solving-chess-stdlib-ooxml-to-markdown"
TOOL_VERSION = "1.0.0"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


class DocxConversionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ConversionResult:
    markdown: bytes
    audit: dict[str, object]


@dataclass
class _Stats:
    paragraphs: int = 0
    nonempty_paragraphs: int = 0
    headings: int = 0
    list_items: int = 0
    code_paragraphs: int = 0
    callouts: int = 0
    tables: int = 0
    table_rows: int = 0
    table_cells: int = 0
    drawings: int = 0
    pictures: int = 0
    math_objects: int = 0
    hyperlinks: int = 0
    tracked_insertions: int = 0
    tracked_deletions: int = 0
    content_controls: int = 0
    merged_table_cells: int = 0
    nested_tables: int = 0
    unsupported_body_elements: int = 0


@dataclass
class _Context:
    styles: dict[str, str]
    style_numbering: dict[str, tuple[str, int]]
    numbering: dict[tuple[str, int], str]
    relationships: dict[str, str]
    stats: _Stats = field(default_factory=_Stats)
    losses: list[dict[str, object]] = field(default_factory=list)
    source_blocks: list[str] = field(default_factory=list)

    def loss(self, code: str, severity: str, count: int, detail: str) -> None:
        if count:
            self.losses.append(
                {
                    "code": code,
                    "severity": severity,
                    "count": count,
                    "detail": detail,
                }
            )


def _qn_text(element: ET.Element) -> str:
    pieces: list[str] = []
    for node in element.iter():
        if node.tag == W + "t":
            pieces.append(node.text or "")
        elif node.tag == W + "tab":
            pieces.append("\t")
        elif node.tag in {W + "br", W + "cr"}:
            pieces.append("\n")
        elif node.tag == W + "noBreakHyphen":
            pieces.append("-")
        elif node.tag == W + "softHyphen":
            pieces.append("\u00ad")
        elif node.tag == W + "sym":
            value = node.get(W + "char", "")
            try:
                pieces.append(chr(int(value, 16)))
            except (TypeError, ValueError):
                pieces.append("[SYMBOL]")
    return "".join(pieces)


def _xml(zf: zipfile.ZipFile, name: str, *, required: bool = False) -> ET.Element | None:
    try:
        payload = zf.read(name)
    except KeyError:
        if required:
            raise DocxConversionError(f"DOCX is missing required part {name}")
        return None
    try:
        return ET.fromstring(payload)
    except ET.ParseError as exc:
        raise DocxConversionError(f"invalid XML in {name}: {exc}") from exc


def _parse_styles(zf: zipfile.ZipFile) -> tuple[dict[str, str], dict[str, tuple[str, int]]]:
    root = _xml(zf, "word/styles.xml")
    names: dict[str, str] = {}
    numbering: dict[str, tuple[str, int]] = {}
    if root is None:
        return names, numbering
    for style in root.findall(W + "style"):
        style_id = style.get(W + "styleId")
        if not style_id:
            continue
        name_node = style.find(W + "name")
        names[style_id] = (
            name_node.get(W + "val", style_id) if name_node is not None else style_id
        )
        num_pr = style.find(f"{W}pPr/{W}numPr")
        if num_pr is not None:
            num_id = num_pr.find(W + "numId")
            ilvl = num_pr.find(W + "ilvl")
            if num_id is not None:
                numbering[style_id] = (
                    num_id.get(W + "val", "0"),
                    int(ilvl.get(W + "val", "0")) if ilvl is not None else 0,
                )
    return names, numbering


def _parse_numbering(zf: zipfile.ZipFile) -> dict[tuple[str, int], str]:
    root = _xml(zf, "word/numbering.xml")
    if root is None:
        return {}
    abstracts: dict[str, dict[int, str]] = {}
    for abstract in root.findall(W + "abstractNum"):
        abstract_id = abstract.get(W + "abstractNumId", "")
        levels: dict[int, str] = {}
        for level in abstract.findall(W + "lvl"):
            ilvl = int(level.get(W + "ilvl", "0"))
            fmt = level.find(W + "numFmt")
            levels[ilvl] = fmt.get(W + "val", "decimal") if fmt is not None else "decimal"
        abstracts[abstract_id] = levels
    result: dict[tuple[str, int], str] = {}
    for num in root.findall(W + "num"):
        num_id = num.get(W + "numId", "")
        ref = num.find(W + "abstractNumId")
        if ref is None:
            continue
        for ilvl, fmt in abstracts.get(ref.get(W + "val", ""), {}).items():
            result[(num_id, ilvl)] = fmt
    return result


def _parse_relationships(zf: zipfile.ZipFile) -> dict[str, str]:
    root = _xml(zf, "word/_rels/document.xml.rels")
    if root is None:
        return {}
    relationships: dict[str, str] = {}
    for child in root:
        rel_id = child.get("Id")
        target = child.get("Target")
        if rel_id and target:
            relationships[rel_id] = target
    return relationships


def _paragraph_style(paragraph: ET.Element, context: _Context) -> tuple[str, str]:
    node = paragraph.find(f"{W}pPr/{W}pStyle")
    style_id = node.get(W + "val", "") if node is not None else ""
    return style_id, context.styles.get(style_id, style_id)


def _list_kind_and_level(
    paragraph: ET.Element, style_id: str, style_name: str, context: _Context
) -> tuple[str, int] | None:
    num_pr = paragraph.find(f"{W}pPr/{W}numPr")
    num_id = None
    level = 0
    if num_pr is not None:
        id_node = num_pr.find(W + "numId")
        level_node = num_pr.find(W + "ilvl")
        if id_node is not None:
            num_id = id_node.get(W + "val", "0")
        if level_node is not None:
            level = int(level_node.get(W + "val", "0"))
    elif style_id in context.style_numbering:
        num_id, level = context.style_numbering[style_id]

    normalized_style = re.sub(r"[\s_-]+", "", style_name or style_id).lower()
    if num_id is not None:
        fmt = context.numbering.get((num_id, level), "decimal")
        return ("bullet" if fmt == "bullet" else "number", level)
    if "listbullet" in normalized_style:
        suffix = re.search(r"(\d+)$", normalized_style)
        return "bullet", max(0, int(suffix.group(1)) - 1) if suffix else 0
    if "listnumber" in normalized_style:
        suffix = re.search(r"(\d+)$", normalized_style)
        return "number", max(0, int(suffix.group(1)) - 1) if suffix else 0
    return None


def _heading_level(style_id: str, style_name: str) -> int | None:
    combined = f"{style_id} {style_name}".strip()
    if re.search(r"\btitle\b", combined, re.IGNORECASE):
        return 1
    match = re.search(r"heading\s*([1-9])", combined, re.IGNORECASE)
    return min(6, int(match.group(1))) if match else None


def _render_hyperlinks(paragraph: ET.Element, context: _Context) -> str:
    """Extract paragraph text and retain external hyperlink targets."""

    output: list[str] = []
    for child in paragraph:
        if child.tag == W + "hyperlink":
            label = _qn_text(child)
            rel_id = child.get(R + "id")
            target = context.relationships.get(rel_id or "")
            context.stats.hyperlinks += 1
            output.append(f"[{label}]({target})" if label and target else label)
        elif child.tag == W + "pPr":
            continue
        else:
            output.append(_qn_text(child))
    return "".join(output)


def _render_paragraph(paragraph: ET.Element, context: _Context) -> tuple[str, str]:
    context.stats.paragraphs += 1
    text = _render_hyperlinks(paragraph, context)
    raw_text = _qn_text(paragraph)
    context.source_blocks.append(raw_text)
    if text.strip():
        context.stats.nonempty_paragraphs += 1
    style_id, style_name = _paragraph_style(paragraph, context)
    normalized_style = re.sub(r"[\s_-]+", "", style_name or style_id).lower()

    heading = _heading_level(style_id, style_name)
    if heading is not None and text.strip():
        context.stats.headings += 1
        return "normal", f"{'#' * heading} {text.strip()}"

    list_info = _list_kind_and_level(paragraph, style_id, style_name, context)
    if list_info is not None and text.strip():
        kind, level = list_info
        context.stats.list_items += 1
        marker = "-" if kind == "bullet" else "1."
        return "normal", f"{'    ' * level}{marker} {text.strip()}"

    if "code" in normalized_style and text:
        context.stats.code_paragraphs += 1
        return "code", text

    if any(token in normalized_style for token in ("callout", "quote")) and text.strip():
        context.stats.callouts += 1
        return "normal", "\n".join(f"> {line}" for line in text.strip().splitlines())

    if "subtitle" in normalized_style and text.strip():
        return "normal", f"*{text.strip()}*"
    return "normal", text.rstrip()


def _escape_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _cell_text(cell: ET.Element, context: _Context) -> str:
    pieces: list[str] = []
    for child in cell:
        if child.tag == W + "p":
            raw = _qn_text(child)
            context.source_blocks.append(raw)
            context.stats.paragraphs += 1
            if raw.strip():
                context.stats.nonempty_paragraphs += 1
            pieces.append(raw.strip())
        elif child.tag == W + "tbl":
            context.stats.nested_tables += 1
            pieces.append(_qn_text(child).strip())
    return "\n".join(piece for piece in pieces if piece)


def _render_table(table: ET.Element, context: _Context) -> str:
    context.stats.tables += 1
    rows: list[list[str]] = []
    for row in table.findall(W + "tr"):
        context.stats.table_rows += 1
        values: list[str] = []
        for cell in row.findall(W + "tc"):
            context.stats.table_cells += 1
            tc_pr = cell.find(W + "tcPr")
            if tc_pr is not None and (
                tc_pr.find(W + "gridSpan") is not None or tc_pr.find(W + "vMerge") is not None
            ):
                context.stats.merged_table_cells += 1
            values.append(_escape_table_cell(_cell_text(cell, context)))
        rows.append(values)
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    output = ["| " + " | ".join(rows[0]) + " |"]
    output.append("| " + " | ".join("---" for _ in range(width)) + " |")
    output.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(output)


def _block_children(body: ET.Element, context: _Context) -> Iterator[ET.Element]:
    for child in body:
        if child.tag in {W + "p", W + "tbl"}:
            yield child
        elif child.tag == W + "sdt":
            context.stats.content_controls += 1
            content = child.find(W + "sdtContent")
            if content is not None:
                yield from _block_children(content, context)
        elif child.tag != W + "sectPr":
            context.stats.unsupported_body_elements += 1


def _part_text(root: ET.Element | None) -> str:
    return _qn_text(root).strip() if root is not None else ""


def _package_timestamp(zf: zipfile.ZipFile) -> str:
    """Read a clone-stable timestamp from DOCX core properties, if present."""

    root = _xml(zf, "docProps/core.xml")
    if root is None:
        return "SOURCE_PACKAGE_TIMESTAMP_UNAVAILABLE"
    namespace = "{http://purl.org/dc/terms/}"
    for tag in ("modified", "created"):
        node = root.find(namespace + tag)
        if node is not None and (node.text or "").strip():
            return (node.text or "").strip()
    return "SOURCE_PACKAGE_TIMESTAMP_UNAVAILABLE"


def convert_docx(
    source: Path,
    *,
    derivative_filename: str | None = None,
    conversion_timestamp: str | None = None,
) -> ConversionResult:
    source = source.resolve()
    derivative_filename = derivative_filename or f"{source.stem}.md"
    source_hash = sha256_file(source)

    try:
        zf = zipfile.ZipFile(source)
    except (OSError, zipfile.BadZipFile) as exc:
        raise DocxConversionError(f"cannot open DOCX {source}: {exc}") from exc

    with zf:
        bad_member = zf.testzip()
        if bad_member:
            raise DocxConversionError(f"DOCX CRC failure in {bad_member}")
        document = _xml(zf, "word/document.xml", required=True)
        assert document is not None
        conversion_timestamp = conversion_timestamp or _package_timestamp(zf)
        styles, style_numbering = _parse_styles(zf)
        context = _Context(
            styles=styles,
            style_numbering=style_numbering,
            numbering=_parse_numbering(zf),
            relationships=_parse_relationships(zf),
        )
        body = document.find(W + "body")
        if body is None:
            raise DocxConversionError("word/document.xml has no w:body")

        rendered: list[str] = []
        code_lines: list[str] = []

        def flush_code() -> None:
            if code_lines:
                rendered.append("```text\n" + "\n".join(code_lines) + "\n```")
                code_lines.clear()

        for block in _block_children(body, context):
            if block.tag == W + "p":
                kind, value = _render_paragraph(block, context)
                if kind == "code":
                    code_lines.append(value)
                else:
                    flush_code()
                    if value:
                        rendered.append(value)
            else:
                flush_code()
                value = _render_table(block, context)
                if value:
                    rendered.append(value)
        flush_code()

        context.stats.drawings = len(document.findall(".//" + W + "drawing"))
        context.stats.pictures = len(document.findall(".//" + W + "pict"))
        context.stats.math_objects = len(document.findall(".//" + M + "oMath"))
        context.stats.tracked_insertions = len(document.findall(".//" + W + "ins"))
        context.stats.tracked_deletions = len(document.findall(".//" + W + "del"))

        header_texts: list[str] = []
        footer_texts: list[str] = []
        for name in sorted(zf.namelist()):
            if re.fullmatch(r"word/header\d+\.xml", name):
                header_texts.append(_part_text(_xml(zf, name)))
            elif re.fullmatch(r"word/footer\d+\.xml", name):
                footer_texts.append(_part_text(_xml(zf, name)))

        context.loss(
            "DRAWING_NOT_EMBEDDED",
            "material",
            context.stats.drawings + context.stats.pictures,
            "Raster/vector drawings remain in the controlling DOCX and are not embedded in Markdown.",
        )
        context.loss(
            "MATH_FLATTENED_TO_VISIBLE_TEXT",
            "material",
            context.stats.math_objects,
            "Office Math structure is not representable as exact Markdown math.",
        )
        context.loss(
            "TRACKED_CHANGES_FLATTENED",
            "material",
            context.stats.tracked_insertions + context.stats.tracked_deletions,
            "Inserted visible text is retained where present; revision metadata and deleted text are not reproduced.",
        )
        context.loss(
            "MERGED_TABLE_GEOMETRY_FLATTENED",
            "material",
            context.stats.merged_table_cells,
            "Markdown tables cannot preserve OOXML grid-span or vertical-merge geometry.",
        )
        context.loss(
            "NESTED_TABLE_FLATTENED",
            "material",
            context.stats.nested_tables,
            "Nested table cells are flattened to visible text.",
        )
        context.loss(
            "HEADER_FOOTER_NOT_IN_BODY_MARKDOWN",
            "documentary",
            sum(bool(value) for value in header_texts + footer_texts),
            "Header/footer visible text is recorded in audit metadata, not repeated in the body derivative.",
        )
        context.loss(
            "UNSUPPORTED_BODY_ELEMENT",
            "material",
            context.stats.unsupported_body_elements,
            "An unrecognized direct body element remains available only in the controlling DOCX.",
        )
        comment_parts = [name for name in zf.namelist() if name.startswith("word/comments")]
        footnote_parts = [name for name in zf.namelist() if name == "word/footnotes.xml"]
        endnote_parts = [name for name in zf.namelist() if name == "word/endnotes.xml"]
        context.loss(
            "ANNOTATION_PART_NOT_CONVERTED",
            "material",
            len(comment_parts) + len(footnote_parts) + len(endnote_parts),
            "Comments, footnotes, or endnotes remain in the controlling DOCX package.",
        )
        formatted_runs = len(document.findall(f".//{W}rPr"))
        context.loss(
            "RUN_FORMATTING_SIMPLIFIED",
            "documentary",
            formatted_runs,
            "Character-level Word formatting is simplified; visible text and block semantics are retained.",
        )

    provenance = [
        "<!--",
        "SOLVING CHESS NORMALIZED DERIVATIVE",
        f"original_filename: {source.name}",
        f"original_sha256: {source_hash}",
        f"derivative_filename: {derivative_filename}",
        f"conversion_method: {TOOL_NAME}",
        f"conversion_tool_version: {TOOL_VERSION}",
        f"conversion_timestamp: {conversion_timestamp}",
        "authority: This Markdown is a derivative; the immutable DOCX is controlling authority.",
        "-->",
        "",
        (
            "> **Derivative notice:** This Markdown is an agent-facing extraction. "
            "The immutable DOCX named above remains controlling authority."
        ),
        "",
    ]
    markdown_text = "\n".join(provenance + rendered).rstrip() + "\n"
    markdown = markdown_text.encode("utf-8")
    source_text_payload = "\n\0\n".join(context.source_blocks).encode("utf-8")
    losses = sorted(context.losses, key=lambda item: str(item["code"]))
    audit: dict[str, object] = {
        "schema_version": "1.0.0",
        "audit_kind": "DOCX_TO_MARKDOWN_CONVERSION",
        "conversion": {
            "method": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "timestamp": conversion_timestamp,
        },
        "source": {
            "filename": source.name,
            "sha256": source_hash,
            "size": source.stat().st_size,
            "authority": "CONTROLLING_IMMUTABLE_ORIGINAL",
            "visible_text_sequence_sha256": hashlib.sha256(source_text_payload).hexdigest(),
        },
        "derivative": {
            "filename": derivative_filename,
            "sha256": sha256_bytes(markdown),
            "size": len(markdown),
            "authority": "NON_AUTHORITATIVE_DERIVATIVE",
        },
        "statistics": vars(context.stats),
        "header_text": header_texts,
        "footer_text": footer_texts,
        "losses": losses,
        "status": "LOSS_AUDITED_WITH_LIMITATIONS" if losses else "NO_KNOWN_STRUCTURAL_LOSS",
    }
    return ConversionResult(markdown=markdown, audit=audit)


def _write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--timestamp")
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = convert_docx(
        args.source,
        derivative_filename=args.output.name,
        conversion_timestamp=args.timestamp,
    )
    _write(args.output, result.markdown)
    _write(args.audit, canonical_json_bytes(result.audit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
