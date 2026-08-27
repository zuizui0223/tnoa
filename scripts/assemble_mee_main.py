#!/usr/bin/env python3
"""Assemble an anonymised MEE-facing Markdown main text from audited TNOA sources.

The canonical scientific draft remains `manuscript/TNOA_P1_DRAFT.md`. This script
replaces its free-form abstract/front matter with the journal-facing numbered
abstract and statements, then preserves the audited Introduction onward. It does
not alter locked result wording or C-ID provenance comments.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "TNOA_P1_DRAFT.md"
FRONT = ROOT / "submission" / "MEE_ABSTRACT_AND_STATEMENTS.md"
DEFAULT_OUT = ROOT / "submission" / "generated" / "TNOA_P1_MEE_MAIN.md"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    draft = DRAFT.read_text(encoding="utf-8")
    front = FRONT.read_text(encoding="utf-8")

    intro_marker = "## 1. Introduction"
    if intro_marker not in draft:
        raise SystemExit("canonical draft lacks Introduction marker")
    body = intro_marker + draft.split(intro_marker, 1)[1]
    body = body.replace("## 2. Methods", "## 2. Materials and Methods", 1)

    title = draft.splitlines()[0].strip()
    if not title.startswith("# "):
        raise SystemExit("canonical draft must start with a Markdown H1 title")

    # The front-matter source begins with an implementation heading that is useful
    # in-repo but should not appear in the assembled manuscript.
    front_lines = front.splitlines()
    if front_lines and front_lines[0].startswith("# MEE front matter"):
        front_lines = front_lines[1:]
    front_text = "\n".join(front_lines).lstrip()

    assembled = (
        title
        + "\n\n"
        + front_text
        + "\n\n---\n\n"
        + body
        + "\n"
    )

    # Author-identifying placeholders belong only to the separate title page.
    forbidden = ("[Author 1 full name]", "[Corresponding author name]", "## Authors")
    for token in forbidden:
        if token in assembled:
            raise SystemExit(f"author-identifying title-page token leaked into main text: {token}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(assembled, encoding="utf-8")
    print(f"Wrote anonymised MEE main text: {args.output}")


if __name__ == "__main__":
    main()
