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
    "scripts/build_anonymous_review_bundle.py",
    "scripts/validate_anonymous_review_bundle.py",
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
    if payload.get("schema") != "tnoa-mee-submission-package-v2":
        fail("submission manifest schema must be v2")
    if payload.get("target_journal") != "Methods in Ecology and Evolution":
        fail("target journal drifted")
    if payload.get("scientific_submission_blockers") != 0:
        fail("submission package cannot claim readiness while scientific blockers remain")
    if payload.get("scientific_claim_boundary_unchanged") is not True:
        fail("MEE production package must not change the scientific claim boundary")

    anon = payload.get("anonymous_manuscript", {})
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
    if peer.get("deterministic_zip") is not True or peer.get("zip_sha256_receipt") is not True:
        fail("reviewer package must be deterministic and receipt-hashed")
    if peer.get("identity_scan") is not True:
        fail("reviewer package identity scan must remain enabled")
    if peer.get("ci_artifact_is_final_reviewer_location") is not False:
        fail("public-repo CI artifact cannot be treated as the final reviewer location")

    for key in ("bundle_builder", "bundle_validator"):
        path = peer.get(key)
        if not path or not (ROOT / path).is_file():
            fail(f"peer-review bundle path missing: {key}")

    front = (ROOT / "submission" / "MEE_FRONT_MATTER.md").read_text(encoding="utf-8")
    for label in ("**1.**", "**2.**", "**3.**", "**4.**"):
        if label not in front:
            fail(f"numbered abstract label missing: {label}")
    if "## Data/Code for peer review statement" not in front:
        fail("Data/Code for peer review statement missing")

    svg = (ROOT / "figures" / "fig1_tnoa_architecture.svg").read_text(encoding="utf-8")
    for token in ("World / process layer", "Evidence layer", "Decision layer", "Development safeguards"):
        if token not in svg:
            fail(f"Figure 1 semantic layer missing: {token}")

    print(
        "MEE submission package OK: license, anonymous manuscript, title-page split, "
        "deterministic reviewer bundle path and Figure 1 registered"
    )


if __name__ == "__main__":
    main()
