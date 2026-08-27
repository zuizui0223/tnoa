#!/usr/bin/env python3
"""Classify bibliography entries by active-manuscript versus prior-art-audit use."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = (
    ROOT / "manuscript" / "TNOA_MEE_DRAFT.md",
    ROOT / "submission" / "MEE_FRONT_MATTER.md",
)
AUDIT = (
    ROOT / "docs" / "FINAL_PRIOR_ART_AUDIT.md",
    ROOT / "docs" / "LITERATURE_EVIDENCE_MAP.md",
    ROOT / "docs" / "NOVELTY_POSITIONING.md",
    ROOT / "docs" / "REVIEWER_ATTACK_MATRIX.md",
)
BIB = ROOT / "references.bib"
REPORT = ROOT / "submission" / "generated" / "reference_scope_audit.json"
CITE = re.compile(r"@([A-Za-z0-9_:\-.]+)")
BIBKEY = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", re.M)


def fail(message: str) -> None:
    raise SystemExit(f"reference-scope audit failed: {message}")


def keys(paths: tuple[Path, ...]) -> set[str]:
    result: set[str] = set()
    for path in paths:
        if not path.is_file():
            fail(f"missing source: {path.relative_to(ROOT)}")
        result.update(CITE.findall(path.read_text(encoding="utf-8")))
    return result


def main() -> None:
    if not BIB.is_file():
        fail("references.bib missing")
    bib = set(BIBKEY.findall(BIB.read_text(encoding="utf-8")))
    active = keys(ACTIVE)
    audit = keys(AUDIT)

    missing_active = sorted(active - bib)
    missing_audit = sorted(audit - bib)
    if missing_active:
        fail(f"active manuscript citations missing from bibliography: {missing_active}")
    if missing_audit:
        fail(f"prior-art audit citations missing from bibliography: {missing_audit}")

    active_entries = sorted(active & bib)
    audit_only = sorted((audit - active) & bib)
    orphan = sorted(bib - active - audit)
    if orphan:
        fail(f"bibliography entries are unused by both active manuscript and prior-art audit: {orphan}")

    report = {
        "schema": "tnoa-reference-scope-audit-v1",
        "active_manuscript_entry_count": len(active_entries),
        "active_manuscript_entries": active_entries,
        "prior_art_only_entry_count": len(audit_only),
        "prior_art_only_entries": audit_only,
        "orphan_entry_count": 0,
        "orphan_entries": [],
        "interpretation": "Prior-art-only entries remain intentionally in the shared bibliography; no entry is orphaned from both the active paper and its adversarial literature audit.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "Reference scope OK: "
        f"{len(active_entries)} active-paper entries, {len(audit_only)} prior-art-only entries, 0 orphan entries"
    )
    if audit_only:
        print("Prior-art-only keys: " + ", ".join(audit_only))


if __name__ == "__main__":
    main()
