#!/usr/bin/env python3
"""Build the anonymous MEE manuscript source from audited TNOA components.

The builder does not change scientific wording in the body. It:
- replaces the working-draft title/abstract/keywords with the numbered MEE front matter;
- appends the audited manuscript body beginning at Introduction;
- removes internal C-ID HTML comments from the reviewer copy;
- fails if common identity-bearing strings remain.

The output is Markdown source for journal-format conversion, not a replacement for
the separate title-page upload.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
DRAFT = ROOT / "manuscript" / "TNOA_P1_DRAFT.md"
OUT_DIR = ROOT / "submission" / "generated"
OUT = OUT_DIR / "MEE_ANONYMOUS_MANUSCRIPT.md"

BODY_MARKER = "## 1. Introduction"
C_TAG = re.compile(r"\s*<!--\s*C\d+(?:\s+C\d+)*\s*-->")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)

# The public repository-owner string is known from the source repository URL and
# must not appear in the anonymous reviewer manuscript.
FORBIDDEN_LITERAL = (
    "zuizui0223",
    "github.com/zuizui0223",
    "raw.githubusercontent.com/zuizui0223",
)


def fail(message: str) -> None:
    raise SystemExit(f"MEE anonymous manuscript build failed: {message}")


def main() -> None:
    if not FRONT.is_file() or not DRAFT.is_file():
        fail("required front matter or working manuscript is missing")

    front = FRONT.read_text(encoding="utf-8").strip()
    draft = DRAFT.read_text(encoding="utf-8")
    if BODY_MARKER not in draft:
        fail(f"working manuscript does not contain body marker: {BODY_MARKER}")

    body = BODY_MARKER + draft.split(BODY_MARKER, 1)[1]
    body = C_TAG.sub("", body)

    # Remove assembly instructions from the reviewer manuscript while retaining
    # the numbered abstract, keywords and Data/Code statement.
    front = front.split("## Manuscript structure after this front matter", 1)[0].rstrip()

    output = front + "\n\n---\n\n" + body.lstrip()

    lower = output.lower()
    for literal in FORBIDDEN_LITERAL:
        if literal.lower() in lower:
            fail(f"identity-bearing literal remains: {literal}")
    if EMAIL.search(output):
        fail("email address remains in anonymous manuscript")
    if "<!-- C" in output:
        fail("internal C-ID comments remain in reviewer manuscript")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(output.rstrip() + "\n", encoding="utf-8")
    print(f"Built anonymous MEE manuscript source: {OUT}")


if __name__ == "__main__":
    main()
