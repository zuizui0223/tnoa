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
    "scripts/build_mee_initial_submission_source.py",
    "scripts/audit_initial_submission_readiness.py",
    "scripts/build_mee_anonymous_manuscript.py",
    "scripts/build_anonymous_review_bundle.py",
    "scripts/validate_anonymous_review_bundle.py",
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
    if payload.get("schema") != "tnoa-mee-submission-package-v3":
        fail("submission manifest must be v3 after initial-submission assembly implementation")
    if payload.get("target_journal") != "Methods in Ecology and Evolution":
        fail("target journal drifted")
    if payload.get("scientific_submission_blockers") != 0:
        fail("submission package cannot claim readiness while scientific blockers remain")
    if payload.get("scientific_claim_boundary_unchanged") is not True:
        fail("MEE production package must not change the scientific claim boundary")
    if payload.get("scientific_source_manifest") != "paper_manifest.json":
        fail("scientific source manifest drifted")

    anon = payload.get("anonymous_manuscript", {})
    expected_anon = {
        "audited_body": "manuscript/TNOA_MEE_DRAFT.md",
        "historical_body_retained": "manuscript/TNOA_P1_DRAFT.md",
        "claim_audit": "scripts/audit_manuscript_claims.py",
        "initial_submission_builder": "scripts/build_mee_initial_submission_source.py",
        "initial_submission_output": "submission/generated/MEE_INITIAL_SUBMISSION_SOURCE.md",
        "readiness_audit": "scripts/audit_initial_submission_readiness.py",
        "readiness_report": "submission/generated/initial_submission_readiness.json",
        "anonymous_builder": "scripts/build_mee_anonymous_manuscript.py",
        "anonymous_output": "submission/generated/MEE_ANONYMOUS_MANUSCRIPT.md",
    }
    for key, expected in expected_anon.items():
        if anon.get(key) != expected:
            fail(f"anonymous manuscript field {key} drifted")
    for key in (
        "numbered_abstract_1_to_4",
        "data_code_peer_review_statement",
        "materials_and_methods_heading_normalized_in_submission_source",
        "figure_callouts_and_captions_added_in_submission_source",
        "internal_c_tags_removed_from_review_copy",
        "public_owner_strings_forbidden",
        "email_addresses_forbidden",
        "final_formatted_word_count_must_be_rechecked",
    ):
        if anon.get(key) is not True:
            fail(f"anonymous manuscript invariant {key} must remain true")
    if anon.get("word_count_conservative_ceiling") != 8000:
        fail("conservative Standard Article word-count ceiling drifted")

    title_state = payload.get("title_page", {})
    if title_state.get("template") != "submission/TITLE_PAGE_TEMPLATE.md":
        fail("title-page template path drifted")
    if title_state.get("separate_upload_required") is not True:
        fail("title page must remain a separate upload")
    for key in (
        "manuscript_title_complete",
        "data_availability_initial_wording_complete",
        "data_sources_statement_complete",
        "scope_ethics_statement_complete",
    ):
        if title_state.get(key) is not True:
            fail(f"non-author title-page field {key} must remain complete")
    for key in (
        "author_metadata_complete",
        "author_contributions_complete",
        "acknowledgements_complete",
        "funding_and_competing_interests_complete",
    ):
        if title_state.get(key) is not False:
            fail(f"author-specific title-page field {key} must remain explicitly incomplete until supplied")

    front = (ROOT / "submission" / "MEE_FRONT_MATTER.md").read_text(encoding="utf-8")
    title_page = (ROOT / "submission" / "TITLE_PAGE_TEMPLATE.md").read_text(encoding="utf-8")
    active_title = front.splitlines()[0].removeprefix("# ").strip()
    title_marker = "## Manuscript title\n\n"
    if title_marker not in title_page:
        fail("title page lacks manuscript-title section")
    title_value = title_page.split(title_marker, 1)[1].split("\n\n", 1)[0].strip()
    if title_value != active_title:
        fail(f"title-page manuscript title is out of sync with active MEE title: {title_value!r}")
    for phrase in (
        "validated anonymized reviewer-only package",
        "persistent archive/repository",
        "No field biological dataset is used",
        "does not report a new organismal, human-subject or field-site experiment",
    ):
        if phrase not in title_page:
            fail(f"title-page non-author wording missing: {phrase}")

    peer = payload.get("peer_review_code_data", {})
    expected_peer = {
        "bundle_builder": "scripts/build_anonymous_review_bundle.py",
        "bundle_validator": "scripts/validate_anonymous_review_bundle.py",
        "bundle_schema": "tnoa-anonymous-review-bundle-v2",
        "expected_zip": "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.zip",
        "expected_receipt": "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.receipt.json",
        "source_A_commit": "f3b266897f3e9139e6c3fe9ce6b645e25371e092",
        "source_B_commit": "1664a190cec47142e8d14cc5157302a7af18d019",
    }
    for key, expected in expected_peer.items():
        if peer.get(key) != expected:
            fail(f"peer-review bundle field {key} drifted")
    if "CI-validated" not in str(peer.get("status", "")):
        fail("peer-review bundle must be registered as CI-validated")
    if peer.get("private_or_reviewer_only_location_required") is not True:
        fail("anonymous code/data package must use reviewer-only/private location")
    if peer.get("public_owner_identifying_url_allowed_in_anonymous_manuscript") is not False:
        fail("anonymous manuscript cannot expose owner-identifying repository URL")
    if peer.get("locked_scientific_generation_rerun_required_for_routine_review") is not False:
        fail("routine reviewer bundle must not require rerunning the frozen scientific generation")
    if peer.get("final_author_institution_literals_must_be_scanned_at_upload") is not True:
        fail("final author/institution literal scan is not registered")
    if peer.get("ci_bundle_artifact_is_validation_only_not_final_delivery_location") is not True:
        fail("CI bundle must not be represented as the final reviewer delivery location")

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

    for label in ("**1.**", "**2.**", "**3.**", "**4.**"):
        if label not in front:
            fail(f"numbered abstract label missing: {label}")
    if "## Data/Code for peer review statement" not in front:
        fail("Data/Code for peer review statement missing")
    if "closed-world rather than field-calibrated" not in front:
        fail("front matter lost the closed-world field-calibration boundary")

    reviewer = (ROOT / "submission" / "ANONYMOUS_PEER_REVIEW_PACKAGE.md").read_text(encoding="utf-8")
    for token in (
        "mee_figure_data.json",
        "validate_mee_figure_data.py",
        "build_mee_figures.py",
        "build_anonymous_review_bundle.py",
        "validate_anonymous_review_bundle.py",
        "--forbid-literal",
    ):
        if token not in reviewer:
            fail(f"anonymous reviewer package missing current component: {token}")
    if "build_paper_figures.py" in reviewer:
        fail("anonymous reviewer package still points to the historical figure builder")

    remaining = payload.get("remaining_initial_upload_tasks", [])
    required_remaining_phrases = (
        "single-column double-line-spaced",
        "final formatted word count",
        "author names, affiliations",
        "funding and competing-interest",
        "author/institution literals",
        "reference-style",
        "claim audit",
    )
    joined = "\n".join(str(item) for item in remaining)
    for phrase in required_remaining_phrases:
        if phrase not in joined:
            fail(f"remaining initial-upload task missing concept: {phrase}")

    svg = (ROOT / "figures" / "fig1_tnoa_architecture.svg").read_text(encoding="utf-8")
    for token in ("World / process layer", "Evidence layer", "Decision layer", "Development safeguards"):
        if token not in svg:
            fail(f"Figure 1 semantic layer missing: {token}")

    print(
        "MEE submission package OK: scientific blockers 0; manuscript/readiness/reviewer bundle aligned; "
        "non-author title-page fields complete; author-specific metadata still explicitly pending"
    )


if __name__ == "__main__":
    main()
