#!/usr/bin/env python3
"""Fail-closed structural checks for the TNOA MEE submission package.

This checker validates repository packaging only. It does not replace the locked
scientific claim audit and does not fetch or rerun historical one-shot results.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    "LICENSE",
    "manuscript/TNOA_P1_DRAFT.md",
    "submission/MEE_SUBMISSION_REQUIREMENTS_2026.md",
    "submission/MEE_TITLE_PAGE_TEMPLATE.md",
    "submission/MEE_ABSTRACT_AND_STATEMENTS.md",
    "submission/MEE_COVER_LETTER_DRAFT.md",
    "figures/fig1_tnoa_architecture.svg",
    "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/FINAL_CLAIM_AUDIT.md",
    "paper_manifest.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"MEE package check failed: {message}")


def rough_word_count(text: str) -> int:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w–-]+\b", text, flags=re.UNICODE))


def main() -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "MIT License" not in license_text:
        fail("open-source licence is missing or is not the expected MIT licence")

    front = (ROOT / "submission/MEE_ABSTRACT_AND_STATEMENTS.md").read_text(encoding="utf-8")
    for i in range(1, 5):
        if f"**{i}.**" not in front:
            fail(f"numbered abstract item {i} is missing")
    if "## Keywords" not in front:
        fail("Keywords section is missing")
    if "## Data/Code for peer review" not in front:
        fail("Data/Code for peer review statement is missing")

    title_page = (ROOT / "submission/MEE_TITLE_PAGE_TEMPLATE.md").read_text(encoding="utf-8")
    if "## Running headline" not in title_page:
        fail("title page lacks running headline")
    if "## Author contributions" not in title_page:
        fail("title page lacks author contribution section")
    if "## Data availability statement" not in title_page:
        fail("title page lacks data availability statement")

    manuscript = (ROOT / "manuscript/TNOA_P1_DRAFT.md").read_text(encoding="utf-8")
    for heading in ("## 1. Introduction", "## 2. Methods", "## 3. Results", "## 4. Discussion"):
        if heading not in manuscript:
            fail(f"main manuscript lacks required section: {heading}")
    if "<!-- C" not in manuscript:
        fail("main manuscript lacks internal locked-claim provenance tags")

    svg = (ROOT / "figures/fig1_tnoa_architecture.svg").read_text(encoding="utf-8")
    for token in ("Process world", "Evidence channels", "Decision contract", "Forbidden shortcuts"):
        if token not in svg:
            fail(f"conceptual Figure 1 lacks required concept: {token}")

    body_words = rough_word_count(manuscript)
    front_words = rough_word_count(front)
    print(f"MEE package structurally OK; rough manuscript words={body_words}, front-matter words={front_words}")
    if body_words > 8000:
        print("WARNING: manuscript body alone exceeds the journal's stated 7,000–8,000-word Research Article range")
    elif body_words > 7000:
        print("NOTE: manuscript body is already within the upper part of the stated 7,000–8,000-word range before references")
    else:
        print("NOTE: manuscript body is below 7,000 words by this rough Markdown count; final count must include references/captions/statements")


if __name__ == "__main__":
    main()
