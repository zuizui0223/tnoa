#!/usr/bin/env python3
"""Fail-closed structural validator for the anonymous MEE submission DOCX."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "submission" / "generated" / "docx_validation.json"
TITLE = "Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework"
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*")
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
OWNER = "zuizui0223"
MIN_WORDS = 3000
MAX_WORDS = 8000

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
}
W = "{" + NS["w"] + "}"


def fail(message: str) -> None:
    raise SystemExit(f"MEE DOCX validation failed: {message}")


def attr(node: ET.Element, name: str) -> str | None:
    return node.attrib.get(W + name)


def xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        fail(f"DOCX missing XML part: {name}")


def text_from(root: ET.Element) -> str:
    return " ".join((node.text or "") for node in root.findall(".//w:t", NS))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx_path", type=Path)
    args = parser.parse_args()
    path = args.docx_path
    if not path.is_file() or path.stat().st_size < 10000:
        fail(f"missing or implausibly small DOCX: {path}")

    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        for required in ("word/document.xml", "word/styles.xml", "docProps/core.xml"):
            if required not in names:
                fail(f"required DOCX part missing: {required}")

        document = xml(zf, "word/document.xml")
        styles = xml(zf, "word/styles.xml")
        core = xml(zf, "docProps/core.xml")
        doc_text = text_from(document)
        lower = doc_text.lower()

        if TITLE.lower() not in lower:
            fail("active MEE title missing from DOCX")
        for required_text in ("materials and methods", "results", "discussion", "references", "figure captions"):
            if required_text not in lower:
                fail(f"required rendered manuscript text missing: {required_text}")
        if "[@" in doc_text or "@mackenzie2002occupancy" in doc_text:
            fail("raw Pandoc citation syntax remains in DOCX")
        if OWNER in lower or "github.com/zuizui0223" in lower or EMAIL_RE.search(doc_text):
            fail("identity-bearing repository or email text remains in anonymous DOCX")

        words = len(WORD_RE.findall(doc_text))
        if not (MIN_WORDS <= words <= MAX_WORDS):
            fail(f"DOCX visible word count {words} outside {MIN_WORDS}--{MAX_WORDS} guard")

        normal = None
        for style in styles.findall(".//w:style", NS):
            if attr(style, "styleId") == "Normal":
                normal = style
                break
        if normal is None:
            fail("Normal style missing")
        spacing = normal.find("./w:pPr/w:spacing", NS)
        if spacing is None:
            fail("Normal style has no paragraph spacing definition")
        if attr(spacing, "line") != "480" or attr(spacing, "lineRule") != "auto":
            fail(
                f"Normal style is not double-spaced: line={attr(spacing, 'line')!r}, "
                f"lineRule={attr(spacing, 'lineRule')!r}"
            )

        sections = document.findall(".//w:sectPr", NS)
        if not sections:
            fail("no section properties found")
        for index, sect in enumerate(sections, start=1):
            line = sect.find("./w:lnNumType", NS)
            if line is None:
                fail(f"section {index} lacks line numbering")
            if attr(line, "countBy") != "1" or attr(line, "start") != "1" or attr(line, "restart") != "continuous":
                fail(f"section {index} line numbering is not continuous count-by-one")
            page = sect.find("./w:pgNumType", NS)
            if page is None or attr(page, "start") != "1":
                fail(f"section {index} page numbering is not registered from page 1")

        footer_parts = sorted(name for name in names if name.startswith("word/footer") and name.endswith(".xml"))
        if not footer_parts:
            fail("DOCX has no footer for page numbering")
        footer_text = " ".join(zf.read(name).decode("utf-8", errors="ignore") for name in footer_parts)
        if " PAGE " not in footer_text and ">PAGE<" not in footer_text:
            fail("PAGE field not found in footer")

        creator = core.find("dc:creator", NS)
        modifier = core.find("cp:lastModifiedBy", NS)
        if creator is None or (creator.text or "") != "Anonymous":
            fail("core creator is not Anonymous")
        if modifier is None or (modifier.text or "") != "Anonymous":
            fail("core lastModifiedBy is not Anonymous")

        reference_mentions = sum(1 for token in ("MacKenzie", "Royle", "Hofmeester", "Findlay") if token.lower() in lower)
        if reference_mentions < 3:
            fail("rendered bibliography appears incomplete")

    report = {
        "schema": "tnoa-mee-docx-validation-v1",
        "docx_file": path.name,
        "status": "PASS",
        "visible_word_count": words,
        "word_count_guard": {"minimum": MIN_WORDS, "maximum": MAX_WORDS},
        "double_spaced_normal_style": True,
        "continuous_line_numbering": True,
        "page_numbering_from_one": True,
        "page_number_footer_field": True,
        "anonymous_core_properties": True,
        "citations_rendered_no_raw_keys": True,
        "references_heading_present": True,
        "identity_scan_clean": True,
        "note": "Final visual inspection and publisher-side word-count check remain required before upload.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "MEE DOCX OK: double-spaced, continuous line/page numbering, anonymous metadata, "
        f"rendered citations/references, {words} visible words"
    )


if __name__ == "__main__":
    main()
