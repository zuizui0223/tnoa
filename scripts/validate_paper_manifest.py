#!/usr/bin/env python3
"""Validate TNOA Paper-1 manifest and repository-level provenance contracts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "paper_manifest.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_REPO_FILES = (
    "README.md",
    "paper_manifest.json",
    "references.bib",
    "requirements-figures.txt",
    "requirements-analysis.txt",
    "manuscript/TNOA_P1_DRAFT.md",
    "docs/CONCEPTUAL_FRAMEWORK.md",
    "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md",
    "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/REVIEWER_ATTACK_MATRIX.md",
    "docs/TRANSFERABILITY_TABLE.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md",
    "docs/FINAL_CLAIM_AUDIT.md",
    "docs/SOURCE_PROVENANCE.md",
    "docs/METHOD_PAPER_BLUEPRINT.md",
    "docs/FIGURE_PLAN.md",
    "docs/FIGURE_VALIDATION.md",
    "docs/MEE_SYNTHETIC_CONSEQUENCES.md",
    "derived/mee_synthetic_consequences.json",
    "scripts/build_paper_figures.py",
    "scripts/analyze_mee_synthetic_consequences.py",
    "scripts/validate_mee_synthetic_consequences.py",
    "scripts/audit_manuscript_claims.py",
)

REQUIRED_LOCKED_IDS = {
    "v14a2_first_spatiotemporal_sweep",
    "v14a2_corrected_observation_safe_audit",
    "v14b_target_observer_freeze",
    "v14b_nuisance_familywise_risk_freeze",
    "v14b_final_ternary_phase_surface",
}


def fail(message: str) -> None:
    raise SystemExit(f"TNOA manifest validation failed: {message}")


def require_file(path: str, label: str) -> None:
    if not path or not (ROOT / path).is_file():
        fail(f"missing or invalid {label}: {path!r}")


def main() -> None:
    for relative in REQUIRED_REPO_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing required repository file: {relative}")

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("schema") != "tnoa-paper-manifest-v5":
        fail("manifest schema must be tnoa-paper-manifest-v5")
    if payload.get("paper_generation") != "TNOA-P1":
        fail("paper_generation must be TNOA-P1")
    if "closed-world methods paper" not in str(payload.get("scope", "")):
        fail("scope must retain the closed-world Paper-1 boundary")

    repos = payload.get("source_repositories", {})
    for repo_name in ("pollipi", "insepi"):
        if repo_name not in repos:
            fail(f"missing source repository: {repo_name}")
    if not HEX40.fullmatch(repos["pollipi"].get("main_commit_at_seed", "")):
        fail("PolliPi source commit must be 40-hex")
    if not HEX40.fullmatch(repos["insepi"].get("main_commit_at_seed", "")):
        fail("InsePi source commit must be 40-hex")
    if not HEX40.fullmatch(repos["pollipi"].get("target_evidence_adapter_git_blob_sha1", "")):
        fail("PolliPi target adapter blob must be 40-hex")

    locked = payload.get("locked_results")
    if not isinstance(locked, list) or not locked:
        fail("locked_results must be a non-empty list")
    ids = [row.get("id") for row in locked]
    if len(ids) != len(set(ids)):
        fail("locked result IDs must be unique")
    missing_ids = REQUIRED_LOCKED_IDS - set(ids)
    if missing_ids:
        fail(f"missing required locked result IDs: {sorted(missing_ids)}")

    by_id = {row["id"]: row for row in locked}
    for result_id, row in by_id.items():
        if not HEX40.fullmatch(str(row.get("execution_commit", ""))):
            fail(f"{result_id}: execution_commit must be 40-hex")
        if not SHA256.fullmatch(str(row.get("artifact_digest", ""))):
            fail(f"{result_id}: artifact_digest must be sha256: + 64-hex")
        result_sha = row.get("result_sha256")
        if result_sha is not None and not HEX64.fullmatch(str(result_sha)):
            fail(f"{result_id}: result_sha256 must be 64-hex when present")
        source_path = str(row.get("source_path", ""))
        if not source_path.startswith("benchmarks/"):
            fail(f"{result_id}: source_path must point to an InsePi benchmark artifact")

    final = by_id["v14b_final_ternary_phase_surface"]
    summary = final.get("registered_summary", {})
    if summary.get("coordinate_count") != 30625:
        fail("final coordinate_count must remain 30625")
    if summary.get("world_count") != 5880000:
        fail("final world_count must remain 5880000")
    if summary.get("observer_retuned") is not False:
        fail("final observer_retuned must remain false")

    boundary = payload.get("paper_claim_boundary", {})
    for key in (
        "field_accuracy",
        "field_absence_certification",
        "universal_pi3_law",
        "universal_optimal_abstention",
        "component_level_priority",
    ):
        if boundary.get(key) is not False:
            fail(f"claim boundary {key} must remain false for Paper 1")
    if boundary.get("closed_world_method_claims") is not True:
        fail("closed_world_method_claims must remain true")
    if boundary.get("synthetic_known_truth_estimand_claims") is not True:
        fail("Paper 1 must explicitly permit the synthetic known-truth estimand")
    if boundary.get("weighting_robustness_only_within_tested_class") is not True:
        fail("weighting robustness must remain limited to the tested class")

    literature = payload.get("literature_positioning", {})
    if literature.get("status") != "targeted_final_prior_art_audit_complete_not_systematic_review":
        fail("literature positioning must record completed targeted audit without claiming systematic review")
    for key in (
        "evidence_map",
        "final_prior_art_audit",
        "reviewer_attack_matrix",
        "bibliography",
        "transferability_map",
    ):
        require_file(str(literature.get(key, "")), f"literature positioning path {key}")
    if literature.get("absolute_priority_claimed") is not False:
        fail("absolute historical priority must remain unclaimed")
    if literature.get("quantitative_cross_system_transfer_claimed") is not False:
        fail("quantitative cross-system transfer must remain unclaimed")

    reproducibility = payload.get("reproducibility", {})
    for key in (
        "claim_traceability",
        "entry_point",
        "manifest_validator",
        "manuscript_claim_scanner",
        "ci_workflow",
    ):
        require_file(str(reproducibility.get(key, "")), f"reproducibility path {key}")

    derived = payload.get("derived_analyses", {}).get("mee_synthetic_consequences", {})
    if derived.get("status") != "post_freeze_deterministic_derivation_no_observer_retuning":
        fail("MEE derived analysis must remain explicitly post-freeze")
    if derived.get("source_workflow_run_id") != 32932634622:
        fail("MEE derived analysis source workflow drifted")
    if derived.get("source_artifact_id") != 9593775550:
        fail("MEE derived analysis source artifact drifted")
    if derived.get("source_phase_surface_sha256") != final.get("result_sha256"):
        fail("MEE derived analysis must point to the final frozen phase surface")
    for key in ("script", "result", "requirements", "validation", "documentation"):
        require_file(str(derived.get(key, "")), f"derived-analysis path {key}")
    if derived.get("field_claims_allowed") is not False:
        fail("post-freeze synthetic derivation must not authorize field claims")

    figures = payload.get("figure_package", {})
    if figures.get("status") != "initial_paper_grade_quantitative_set_rendered_and_visually_audited":
        fail("figure_package status must record the render-audited quantitative set")
    for key in ("builder", "plan", "validation", "requirements"):
        require_file(str(figures.get(key, "")), f"figure-package path {key}")
    if figures.get("insepi_source_commit") != repos["insepi"]["main_commit_at_seed"]:
        fail("figure-package InsePi commit must match the pinned paper source commit")
    if figures.get("locked_phase_surface_sha256") != final.get("result_sha256"):
        fail("figure-package phase-surface SHA must match the final locked result")
    expected_blobs = figures.get("source_git_blob_sha1", {})
    for name in ("figure_data", "surface_result", "nuisance_risk"):
        if not HEX40.fullmatch(str(expected_blobs.get(name, ""))):
            fail(f"figure-package source Git blob missing/invalid: {name}")
    stems = figures.get("quantitative_figure_stems", [])
    if len(stems) != 4 or len(set(stems)) != 4:
        fail("figure-package must define four unique historical quantitative figure stems")
    if figures.get("manual_data_geometry_editing_allowed") is not False:
        fail("manual data-geometry editing must remain forbidden")
    if figures.get("field_claims_from_figures_allowed") is not False:
        fail("Paper-1 figures must not authorize field claims")

    manuscript = payload.get("manuscript_package", {})
    if manuscript.get("status") != "full_working_draft_instantiated_and_claim_audited":
        fail("manuscript package must be instantiated and claim-audited")
    for key in ("draft", "blueprint", "final_claim_audit"):
        require_file(str(manuscript.get(key, "")), f"manuscript path {key}")
    if manuscript.get("internal_result_provenance_tags") != "C1-C15":
        fail("historical manuscript must retain C1-C15 internal result provenance tags until the MEE rewrite is instantiated")

    blockers = payload.get("submission_blockers")
    if blockers != []:
        fail("generic scientific submission_blockers must remain empty after frozen-result audits")

    readiness = payload.get("target_journal_readiness", {})
    if readiness.get("target") != "Methods in Ecology and Evolution":
        fail("target_journal_readiness must name Methods in Ecology and Evolution")
    completed = readiness.get("completed", [])
    for item in ("downstream synthetic ecological estimand", "equal-grid weighting sensitivity"):
        if item not in completed:
            fail(f"missing completed MEE item: {item}")
    remaining = readiness.get("remaining_blockers", [])
    if not isinstance(remaining, list) or not remaining:
        fail("MEE-specific remaining blockers must stay explicit")

    editorial = payload.get("editorial_tasks_before_upload")
    if not isinstance(editorial, list) or not editorial:
        fail("editorial tasks must remain explicit")

    print(
        "TNOA manifest OK: "
        f"{len(locked)} locked results, "
        f"{len(payload.get('retained_failures', []))} retained failures, "
        "post-freeze MEE derivation pinned, "
        f"{len(remaining)} MEE-specific blockers remaining"
    )


if __name__ == "__main__":
    main()
