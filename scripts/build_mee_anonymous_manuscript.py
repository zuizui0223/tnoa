#!/usr/bin/env python3
"""Build the anonymous MEE manuscript from the canonical initial-submission source.

The canonical assembly is produced by ``build_mee_initial_submission_source.py``.
Using one source prevents the journal manuscript and reviewer-bundle manuscript
from drifting in headings, figure callouts or captions.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLER = ROOT / "scripts" / "build_mee_initial_submission_source.py"
SOURCE = ROOT / "submission" / "generated" / "MEE_INITIAL_SUBMISSION_SOURCE.md"
OUT = ROOT / "submission" / "generated" / "MEE_ANONYMOUS_MANUSCRIPT.md"

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
FORBIDDEN_LITERAL = (
    "zuizui0223",
    "github.com/zuizui0223",
    "raw.githubusercontent.com/zuizui0223",
)


def fail(message: str) -> None:
    raise SystemExit(f"MEE anonymous manuscript build failed: {message}")


def main() -> None:
    if not ASSEMBLER.is_file():
        fail("canonical initial-submission assembler is missing")
    subprocess.run([sys.executable, str(ASSEMBLER)], check=True)
    if not SOURCE.is_file():
        fail("canonical initial-submission source was not produced")

    output = SOURCE.read_text(encoding="utf-8")
    lower = output.lower()
    for literal in FORBIDDEN_LITERAL:
        if literal.lower() in lower:
            fail(f"identity-bearing literal remains: {literal}")
    if EMAIL.search(output):
        fail("email address remains in anonymous manuscript")
    if re.search(r"<!--\s*[CD]\d+", output):
        fail("internal provenance comments remain in reviewer manuscript")
    if "## 2. Materials and Methods" not in output or "## Figure captions" not in output:
        fail("canonical MEE structure or figure captions missing")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(output.rstrip() + "\n", encoding="utf-8")
    print(f"Built anonymous MEE manuscript source: {OUT}")


if __name__ == "__main__":
    main()
