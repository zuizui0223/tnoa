#!/usr/bin/env python3
"""Validate TNOA MEE paper manifest and repository-level provenance contracts."""
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
    "README.md", "paper_manifest.json", "pyproject.toml", "references.bib",
    "requirements-figures.txt", "requirements-analysis.txt",
    "manuscript/TNOA_P1_DRAFT.md", "manuscript/TNOA_MEE_DRAFT.md",
    "submission/MEE_FRONT_MATTER.md",
    "docs/CONCEPTUAL_FRAMEWORK.md", "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md", "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/REVIEWER_ATTACK_MATRIX.md", "docs/TRANSFERABILITY_TABLE.md",
    "docs/CLAIM_BOUNDARY.md", "docs/CLAIM_TRACEABILITY.md",
    "docs/SOURCE_PROVENANCE.md", "docs/MEE_VOCABULARY_MAP.md",
    "docs/MEE_SYNTHETIC_CONSEQUENCES.md", "docs/STRUCTURAL_RESULT_AUDIT.md",
    "docs/REUSABLE_IMPLEMENTATION.md", "docs/FIGURE_PLAN.md",
    "docs/MEE_FIGURE_VALIDATION.md",
    "derived/mee_synthetic_consequences.json", "derived/structural_axis_audit.json",
    "derived/mee_figure_data.json",
    "tnoa/__init__.py", "tnoa/core.py", "tnoa/cli.py",
    "examples/minimal_evidence.csv", "tests/test_minimal_api.py",
    "scripts/analyze_mee_synthetic_consequences.py", "scripts/validate_mee_synthetic_consequences.py",
    "scripts/analyze_structural_axis_audit.py", "scripts/validate_structural_axis_audit.py",
    "scripts/validate_mee_figure_data.py", "scripts/build_mee_figures.py",
    "scripts/audit_manuscript_claims.py", "scripts/build_mee_anonymous_manuscript.py",
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

    p = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if p.get("schema") != "tnoa-paper-manifest-v6":
        fail("manifest schema must be tnoa-paper-manifest-v6")
    if p.get("paper_generation") != "TNOA-P1-MEE":
        fail("paper_generation must be TNOA-P1-MEE")
    if "field validation remains external" not in str(p.get("scope", "")):
        fail("scope must retain external field-validation boundary")

    repos = p.get("source_repositories", {})
    for name in ("pollipi", "insepi"):
        if name not in repos:
            fail(f"missing source repository: {name}")
    if not HEX40.fullmatch(repos["pollipi"].get("main_commit_at_seed", "")):
        fail("PolliPi source commit invalid")
    if not HEX40.fullmatch(repos["insepi"].get("main_commit_at_seed", "")):
        fail("InsePi source commit invalid")
    if not HEX40.fullmatch(repos["pollipi"].get("target_evidence_adapter_git_blob_sha1", "")):
        fail("PolliPi adapter blob invalid")

    locked = p.get("locked_results", [])
    ids = [row.get("id") for row in locked]
    if REQUIRED_LOCKED_IDS - set(ids):
        fail(f"missing locked result IDs: {sorted(REQUIRED_LOCKED_IDS-set(ids))}")
    if len(ids) != len(set(ids)):
        fail("locked result IDs not unique")
    by_id = {row["id"]: row for row in locked}
    for result_id, row in by_id.items():
        if not HEX40.fullmatch(str(row.get("execution_commit", ""))):
            fail(f"{result_id}: invalid execution commit")
        if not SHA256.fullmatch(str(row.get("artifact_digest", ""))):
            fail(f"{result_id}: invalid artifact digest")
        rsha = row.get("result_sha256")
        if rsha is not None and not HEX64.fullmatch(str(rsha)):
            fail(f"{result_id}: invalid result SHA")

    final = by_id["v14b_final_ternary_phase_surface"]
    summary = final.get("registered_summary", {})
    if summary.get("coordinate_count") != 30625 or summary.get("world_count") != 5880000:
        fail("frozen design size drifted")
    if summary.get("observer_retuned") is not False:
        fail("observer_retuned must remain false")

    sequence = p.get("development_evidence", {}).get("nuisance_threshold_sequence", [])
    if [row.get("stage") for row in sequence] != [
        "inherited_threshold_failure", "score_scale_diagnosis", "pooled_risk_failure", "familywise_risk_freeze"
    ]:
        fail("nuisance threshold evidence sequence drifted")
    expected_runs = [32929245729, 32929754709, 32930855374, 32931223272]
    if [row.get("workflow_run_id") for row in sequence] != expected_runs:
        fail("nuisance threshold workflow provenance drifted")
    for row in sequence:
        if not SHA256.fullmatch(str(row.get("artifact_digest", ""))) or not HEX64.fullmatch(str(row.get("result_sha256", ""))):
            fail(f"invalid development evidence provenance: {row.get('stage')}")

    derived = p.get("derived_analyses", {})
    for key in ("mee_synthetic_consequences", "structural_axis_audit"):
        d = derived.get(key, {})
        if d.get("status") != "post_freeze_deterministic_derivation_no_observer_retuning":
            fail(f"{key}: post-freeze status drifted")
        if d.get("source_workflow_run_id") != 32932634622:
            fail(f"{key}: source workflow drifted")
        if d.get("source_phase_surface_sha256") != final.get("result_sha256"):
            fail(f"{key}: source surface SHA drifted")
        for path_key in ("script", "result", "validation", "documentation"):
            require_file(str(d.get(path_key, "")), f"{key} {path_key}")
        if d.get("field_claims_allowed") is not False:
            fail(f"{key}: field claims must remain false")

    software = p.get("reusable_implementation", {})
    if software.get("status") != "minimal_reusable_api_and_cli_implemented":
        fail("reusable implementation status drifted")
    for key in ("python_api", "cli", "documentation", "example", "tests", "packaging"):
        require_file(str(software.get(key, "")), f"reusable implementation {key}")
    if software.get("universal_raw_thresholds_shipped") is not False or software.get("field_calibration_claimed") is not False:
        fail("reusable implementation overclaims calibration")

    manuscript = p.get("manuscript_package", {})
    if manuscript.get("status") != "mee_focused_draft_instantiated_and_claim_guarded":
        fail("MEE manuscript status drifted")
    for key in ("draft", "historical_draft", "front_matter", "vocabulary_map", "claim_traceability", "claim_scanner", "anonymous_builder"):
        require_file(str(manuscript.get(key, "")), f"manuscript package {key}")
    if manuscript.get("draft") != "manuscript/TNOA_MEE_DRAFT.md":
        fail("MEE draft is not the active manuscript")
    hierarchy = manuscript.get("result_hierarchy", [])
    if len(hierarchy) < 3 or not hierarchy[0].startswith("C6-C7") or not hierarchy[1].startswith("D1") or not hierarchy[2].startswith("C2"):
        fail("MEE result hierarchy drifted")

    figures = p.get("figure_package", {})
    if figures.get("status") != "mee_priority_figure_data_and_builder_pinned":
        fail("MEE figure package status drifted")
    for key in ("plan", "validation_document", "figure_data", "validator", "builder", "requirements"):
        require_file(str(figures.get(key, "")), f"figure package {key}")
    if figures.get("figure_data_git_blob_sha1") != "74fdac2a049c6c13833bb31f7a4ff0b7228a44a6":
        fail("MEE figure-data Git blob drifted")
    if len(figures.get("primary_panels", [])) != 7 or figures.get("supplementary_panels") != ["figS2_axis_separation"]:
        fail("MEE figure panel contract drifted")
    if figures.get("manual_data_geometry_editing_allowed") is not False or figures.get("field_claims_from_figures_allowed") is not False:
        fail("figure claim/edit boundary drifted")

    literature = p.get("literature_positioning", {})
    if literature.get("status") != "targeted_final_prior_art_audit_complete_not_systematic_review":
        fail("literature audit status drifted")
    for key in ("evidence_map", "final_prior_art_audit", "reviewer_attack_matrix", "bibliography", "transferability_map"):
        require_file(str(literature.get(key, "")), f"literature {key}")
    if literature.get("absolute_priority_claimed") is not False or literature.get("quantitative_cross_system_transfer_claimed") is not False:
        fail("literature positioning overclaims novelty/transfer")

    boundary = p.get("paper_claim_boundary", {})
    for key in (
        "field_accuracy", "field_absence_certification", "field_target_prevalence",
        "universal_pi3_law", "universal_optimal_abstention", "component_level_priority",
        "c13_performance_claim", "six_axes_equal_effective_dimensions_claim",
    ):
        if boundary.get(key) is not False:
            fail(f"claim boundary {key} must remain false")
    for key in ("closed_world_method_claims", "synthetic_known_truth_estimand_claims", "weighting_robustness_only_within_tested_class"):
        if boundary.get(key) is not True:
            fail(f"claim boundary {key} must remain true")

    if p.get("submission_blockers") != []:
        fail("scientific submission blockers must be empty")
    readiness = p.get("target_journal_readiness", {})
    if readiness.get("target") != "Methods in Ecology and Evolution":
        fail("target journal drifted")
    if readiness.get("remaining_scientific_blockers") != []:
        fail("MEE scientific blockers should be empty after rewrite and figure package")
    completed = readiness.get("completed", [])
    for item in (
        "downstream synthetic ecological estimand",
        "equal-grid weighting sensitivity",
        "Pi1 reason-decomposition and structural-axis audit",
        "C13 design-composition audit",
        "minimal reusable implementation callable on calibrated evidence outputs",
        "ecological-statistical vocabulary and result-hierarchy rewrite",
        "MEE-priority figure data and reproducible builder",
    ):
        if item not in completed:
            fail(f"missing completed MEE item: {item}")

    editorial = p.get("editorial_tasks_before_upload")
    if not isinstance(editorial, list) or not editorial:
        fail("editorial tasks must remain explicit")

    print(
        "TNOA MEE manifest OK: 5 frozen science anchors, 4-stage nuisance evidence sequence, "
        "2 post-freeze audits, runnable API, MEE manuscript and figure package; 0 scientific blockers"
    )


if __name__ == "__main__":
    main()
