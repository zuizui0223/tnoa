#!/usr/bin/env python3
"""Build the anonymous MEE manuscript source from audited TNOA components.

The builder replaces title/abstract/keywords with numbered MEE front matter,
appends the MEE-focused body at Introduction, strips internal C/D provenance
comments, and fails if common identity-bearing strings remain.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
DRAFT = ROOT / "manuscript" / "TNOA_MEE_DRAFT.md"
OUT_DIR = ROOT / "submission" / "generated"
OUT = OUT_DIR / "MEE_ANONYMOUS_MANUSCRIPT.md"

BODY_MARKER = "## 1. Introduction"
PROVENANCE_TAG = re.compile(r"\s*<!--\s*[CD]\d+(?:\s+[CD]\d+)*\s*-->")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
FORBIDDEN_LITERAL = (
    "zuizui0223",
    "github.com/zuizui0223",
    "raw.githubusercontent.com/zuizui0223",
)


def fail(message: str) -> None:
    raise SystemExit(f"MEE anonymous manuscript build failed: {message}")


def main() -> None:
    if not FRONT.is_file() or not DRAFT.is_file():
        fail("required front matter or MEE manuscript is missing")

    front = FRONT.read_text(encoding="utf-8").strip()
    draft = DRAFT.read_text(encoding="utf-8")
    if BODY_MARKER not in draft:
        fail(f"MEE manuscript does not contain body marker: {BODY_MARKER}")

    body = BODY_MARKER + draft.split(BODY_MARKER, 1)[1]
    body = PROVENANCE_TAG.sub("", body)
    front = front.split("## Manuscript structure after this front matter", 1)[0].rstrip()
    output = front + "\n\n---\n\n" + body.lstrip()

    lower = output.lower()
    for literal in FORBIDDEN_LITERAL:
        if literal.lower() in lower:
            fail(f"identity-bearing literal remains: {literal}")
    if EMAIL.search(output):
        fail("email address remains in anonymous manuscript")
    if re.search(r"<!--\s*[CD]\d+", output):
        fail("internal provenance comments remain in reviewer manuscript")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(output.rstrip() + "\n", encoding="utf-8")
    print(f"Built anonymous MEE manuscript source: {OUT}")


if __name__ == "__main__":
    main()
