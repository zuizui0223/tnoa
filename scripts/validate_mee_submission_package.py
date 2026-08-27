#!/usr/bin/env python3
"""Validate non-scientific MEE submission-package invariants for TNOA."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "submission" / "submission_manifest.json"

REQUIRED = (
    "LICENSE",
    "submission/MEE_SUBMISSION_CHECKLIST.md",
    "submission/MEE_FRONT_MATTER.md",
    "submission/TITLE_PAGE_TEMPLATE.md",
    "submission/ANONYMOUS_PEER_REVIEW_PACKAGE.md",
    "submission/submission_manifest.json",
    "scripts/build_mee_anonymous_manuscript.py",
    "scripts/audit_manuscript_claims.py",
    "manuscript/TNOA_MEE_DRAFT.md",
    "manuscript/TNOA_P1_DRAFT.md",
    "docs/FIGURE_PLAN.md",
    "docs/MEE_FIGURE_VALIDATION.md",
    "derived/mee_figure_data.json",
    "scripts/validate_mee_figure_data.py",
    "scripts/build_mee_figures.py",
    "requirements-figures.txt",
    "figures/fig1_tnoa_architecture.svg",
)


def fail(message: str) -> None:
    raise SystemExit(f"MEE submission package validation failed: {message}")


def main() -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if not license_text.startswith("MIT License"):
        fail("LICENSE is not the expected MIT license text")

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("target_journal") != "Methods in Ecology and Evolution":
        fail("target journal drifted")
    if payload.get("scientific_submission_blockers") != 0:
        fail("submission package cannot claim readiness while scientific blockers remain")
    if payload.get("scientific_claim_boundary_unchanged") is not True:
        fail("MEE production package must not change the scientific claim boundary")
    if payload.get("scientific_source_manifest") != "paper_manifest.json":
        fail("scientific source manifest drifted")

    anon = payload.get("anonymous_manuscript", {})
    if anon.get("audited_body") != "manuscript/TNOA_MEE_DRAFT.md":
        fail("anonymous manuscript must use the active MEE draft")
    if anon.get("historical_body_retained") != "manuscript/TNOA_P1_DRAFT.md":
        fail("historical Paper-1 draft retention is not registered")
    if anon.get("claim_audit") != "scripts/audit_manuscript_claims.py":
        fail("MEE claim audit drifted")
    if anon.get("builder") != "scripts/build_mee_anonymous_manuscript.py":
        fail("anonymous manuscript builder drifted")
    if anon.get("numbered_abstract_1_to_4") is not True:
        fail("numbered 1-4 abstract is not registered")
    if anon.get("public_owner_strings_forbidden") is not True:
        fail("anonymous manuscript must forbid public owner strings")
    if anon.get("email_addresses_forbidden") is not True:
        fail("anonymous manuscript must forbid email addresses")

    peer = payload.get("peer_review_code_data", {})
    if peer.get("private_or_reviewer_only_location_required") is not True:
        fail("anonymous code/data package must use reviewer-only/private location")
    if peer.get("public_owner_identifying_url_allowed_in_anonymous_manuscript") is not False:
        fail("anonymous manuscript cannot expose owner-identifying repository URL")

    figures = payload.get("figures", {})
    expected_figures = {
        "plan": "docs/FIGURE_PLAN.md",
        "validation_document": "docs/MEE_FIGURE_VALIDATION.md",
        "quantitative_figure_data": "derived/mee_figure_data.json",
        "quantitative_figure_validator": "scripts/validate_mee_figure_data.py",
        "quantitative_figure_builder": "scripts/build_mee_figures.py",
        "quantitative_figure_requirements": "requirements-figures.txt",
    }
    for key, expected in expected_figures.items():
        if figures.get(key) != expected:
            fail(f"MEE figure package {key} drifted")

    front = (ROOT / "submission" / "MEE_FRONT_MATTER.md").read_text(encoding="utf-8")
    for label in ("**1.**", "**2.**", "**3.**", "**4.**"):
        if label not in front:
            fail(f"numbered abstract label missing: {label}")
    if "## Data/Code for peer review statement" not in front:
        fail("Data/Code for peer review statement missing")
    if "closed-world rather than field-calibrated" not in front:
        fail("front matter lost the closed-world field-calibration boundary")

    reviewer = (ROOT / "submission" / "ANONYMOUS_PEER_REVIEW_PACKAGE.md").read_text(encoding="utf-8")
    for token in ("mee_figure_data.json", "validate_mee_figure_data.py", "build_mee_figures.py"):
        if token not in reviewer:
            fail(f"anonymous reviewer package missing current MEE figure component: {token}")
    if "build_paper_figures.py" in reviewer:
        fail("anonymous reviewer package still points to the historical figure builder")

    svg = (ROOT / "figures" / "fig1_tnoa_architecture.svg").read_text(encoding="utf-8")
    for token in ("World / process layer", "Evidence layer", "Decision layer", "Development safeguards"):
        if token not in svg:
            fail(f"Figure 1 semantic layer missing: {token}")

    print("MEE submission package OK: license, anonymous front matter, title-page split, peer-review plan and Figure 1 registered")


if __name__ == "__main__":
    main()
