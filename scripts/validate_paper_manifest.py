#!/usr/bin/env python3
"""Validate TNOA MEE paper manifest and repository-level provenance contracts."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "paper_manifest.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"

REQUIRED_REPO_FILES = (
    "README.md", "paper_manifest.json", "pyproject.toml", "references.bib",
    "requirements-figures.txt", "requirements-analysis.txt",
    "manuscript/TNOA_P1_DRAFT.md", "manuscript/TNOA_MEE_DRAFT.md",
    "submission/MEE_FRONT_MATTER.md",
    "docs/CONCEPTUAL_FRAMEWORK.md", "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md", "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/NEAREST_NEIGHBOUR_METHODS.md", "docs/REVIEWER_ATTACK_MATRIX.md",
    "docs/TRANSFERABILITY_TABLE.md", "docs/CLAIM_BOUNDARY.md", "docs/CLAIM_TRACEABILITY.md",
    "docs/SOURCE_PROVENANCE.md", "docs/MEE_VOCABULARY_MAP.md",
    "docs/MEE_SYNTHETIC_CONSEQUENCES.md", "docs/STRUCTURAL_RESULT_AUDIT.md",
    "docs/OBSERVATION_VOCABULARY_ABLATION.md", "docs/PREVALENCE_WEIGHTING_SENSITIVITY.md",
    "docs/REASON_SPLIT_SPECIFICITY_CONTROL.md", "docs/REUSABLE_IMPLEMENTATION.md",
    "docs/FIGURE_PLAN.md", "docs/MEE_FIGURE_VALIDATION.md",
    "derived/mee_synthetic_consequences.json", "derived/structural_axis_audit.json",
    "derived/observation_vocabulary_ablation.json", "derived/prevalence_weighting_sensitivity.json",
    "derived/reason_split_specificity_control.json", "derived/mee_figure_data.json",
    "tnoa/__init__.py", "tnoa/core.py", "tnoa/cli.py",
    "examples/minimal_evidence.csv", "tests/test_minimal_api.py",
    "scripts/analyze_mee_synthetic_consequences.py", "scripts/validate_mee_synthetic_consequences.py",
    "scripts/analyze_structural_axis_audit.py", "scripts/validate_structural_axis_audit.py",
    "scripts/analyze_observation_vocabulary_ablation.py", "scripts/validate_observation_vocabulary_ablation.py",
    "scripts/analyze_prevalence_weighting_sensitivity.py", "scripts/validate_prevalence_weighting_sensitivity.py",
    "scripts/analyze_reason_split_specificity_control.py", "scripts/validate_reason_split_specificity_control.py",
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


def close(actual: float, expected: float, atol: float = 1e-10) -> bool:
    return math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=atol)


def validate_derived_entry(d: dict, name: str, expected_status: str) -> None:
    if d.get("status") != expected_status:
        fail(f"{name}: status drifted")
    if d.get("source_workflow_run_id") != 32932634622 or d.get("source_phase_surface_sha256") != SURFACE_SHA:
        fail(f"{name}: frozen source provenance drifted")
    for path_key in ("script", "result", "validation", "documentation"):
        require_file(str(d.get(path_key, "")), f"{name} {path_key}")
    if d.get("field_claims_allowed") is not False:
        fail(f"{name}: field claims must remain false")


def main() -> None:
    for relative in REQUIRED_REPO_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing required repository file: {relative}")

    p = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if p.get("schema") != "tnoa-paper-manifest-v9":
        fail("manifest schema must be tnoa-paper-manifest-v9")
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
    if summary.get("observer_retuned") is not False or final.get("result_sha256") != SURFACE_SHA:
        fail("frozen final-surface contract drifted")

    nuisance = by_id["v14b_nuisance_familywise_risk_freeze"].get("registered_summary", {})
    if nuisance.get("target_only_heldout_count") != 43200 or nuisance.get("target_nuisance_coupled_heldout_count") != 43200:
        fail("nuisance held-out denominators drifted")
    if nuisance.get("target_only_false_nuisance_attribution_count") != 0 or nuisance.get("target_nuisance_coupled_false_nuisance_attribution_count") != 1920:
        fail("nuisance held-out numerators drifted")
    if nuisance.get("distribution_free_finite_sample_guarantee_claimed") is not False:
        fail("nuisance lock must not claim distribution-free guarantee")

    sequence = p.get("development_evidence", {}).get("nuisance_threshold_sequence", [])
    expected_stages = [
        "inherited_threshold_failure", "score_scale_diagnosis", "pooled_risk_failure",
        "max_over_predeclared_negative_families_freeze",
    ]
    if [row.get("stage") for row in sequence] != expected_stages:
        fail("nuisance threshold evidence sequence drifted")
    for row in sequence:
        if not SHA256.fullmatch(str(row.get("artifact_digest", ""))) or not HEX64.fullmatch(str(row.get("result_sha256", ""))):
            fail(f"invalid development evidence provenance: {row.get('stage')}")

    derived = p.get("derived_analyses", {})
    validate_derived_entry(
        derived.get("mee_synthetic_consequences", {}), "D1",
        "post_freeze_deterministic_derivation_no_observer_retuning",
    )
    validate_derived_entry(
        derived.get("structural_axis_audit", {}), "D2",
        "post_freeze_deterministic_derivation_no_observer_retuning",
    )

    d3 = derived.get("observation_vocabulary_ablation", {})
    validate_derived_entry(d3, "D3", "literature_audit_motivated_post_freeze_deterministic_derivation_not_preregistered")
    for key in ("preregistered", "observer_retuned", "new_synthetic_worlds_generated", "semantic_specificity_demonstrated"):
        if d3.get(key) is not False:
            fail(f"D3 boundary {key} must remain false")
    d3s = d3.get("summary", {})
    if d3s.get("mixture_count") != 3003 or d3s.get("vocabulary_count") != 4 or d3s.get("estimand_count") != 5 or d3s.get("registered_axis_slice_count") != 34:
        fail("D3 design summary drifted")
    expected_target = [0.2656306018443621, 0.18861428571428596, 0.02992070478107567, 0.004077995920098443]
    if len(d3s.get("target_prevalence_median_widths", [])) != 4 or any(not close(a, b) for a, b in zip(d3s["target_prevalence_median_widths"], expected_target)):
        fail("D3 target widths drifted")
    if d3s.get("all_estimands_all_34_slices_refined_record_never_wider") is not True:
        fail("D3 slice nesting drifted")
    if "not specific" not in str(d3s.get("interpretation", "")):
        fail("D3 interpretation must defer semantic specificity to D5")

    d4 = derived.get("prevalence_weighting_sensitivity", {})
    validate_derived_entry(d4, "D4", "reviewer_motivated_post_freeze_design_sensitivity_not_preregistered")
    for key in ("preregistered", "observer_retuned", "new_synthetic_worlds_generated", "annotation_budget_efficiency_claimed"):
        if d4.get(key) is not False:
            fail(f"D4 boundary {key} must remain false")
    d4s = d4.get("summary", {})
    if d4s.get("mixture_count") != 3003 or d4s.get("rare_target_theta_le_0_2_compositions") != 141:
        fail("D4 simplex/rare-target count drifted")
    for key, expected in (
        ("rare_target_theta_le_0_2_uniform_lattice_mass", 141 / 3003),
        ("rare_target_theta_le_0_2_median_width_binary", 0.07409970878498642),
        ("rare_target_theta_le_0_2_median_width_btnu", 0.0001746269687759039),
        ("composition_kappa_10_min_fraction_binary_width_removed_by_btnu", 0.5746863884992289),
    ):
        if not close(d4s.get(key), expected):
            fail(f"D4 summary drifted: {key}")

    d5 = derived.get("reason_split_specificity_control", {})
    validate_derived_entry(d5, "D5", "reviewer_motivated_post_freeze_random_split_control_not_preregistered")
    for key in ("preregistered", "observer_retuned", "new_synthetic_worlds_generated", "semantic_specificity_demonstrated"):
        if d5.get(key) is not False:
            fail(f"D5 boundary {key} must remain false")
    d5s = d5.get("summary", {})
    for key, expected in (
        ("random_seed", 0),
        ("two_way_random_split_count", 500),
        ("three_way_random_split_count", 500),
        ("target_generic_u_median_width", 0.02992070478107567),
        ("target_semantic_two_reason_median_width", 0.004077995920098443),
        ("target_random_two_way_median_width", 0.005007513005321984),
        ("target_fraction_random_equal_or_narrower_than_semantic", 0.48),
        ("random_three_way_full_rank_fraction", 1.0),
        ("random_three_way_point_identification_fraction_all_estimands", 1.0),
    ):
        if not close(d5s.get(key), expected):
            fail(f"D5 summary drifted: {key}")
    if d5s.get("rank_nullspace_dimensions") != [4, 3, 2, 1, 0]:
        fail("D5 rank ladder drifted")

    software = p.get("reusable_implementation", {})
    if software.get("status") != "minimal_reusable_api_and_cli_implemented":
        fail("reusable implementation status drifted")
    for key in ("python_api", "cli", "documentation", "example", "tests", "packaging"):
        require_file(str(software.get(key, "")), f"reusable implementation {key}")
    if software.get("universal_raw_thresholds_shipped") is not False or software.get("field_calibration_claimed") is not False:
        fail("reusable implementation overclaims calibration")
    if software.get("frozen_v14b_reason_count") != 2 or software.get("reusable_api_unresolved_reason_count") != 4:
        fail("frozen/API reason vocabulary counts drifted")
    if software.get("one_to_one_frozen_to_api_reason_validation_claimed") is not False:
        fail("reusable implementation must not claim frozen four-way reason validation")

    manuscript = p.get("manuscript_package", {})
    for key in ("draft", "historical_draft", "front_matter", "vocabulary_map", "claim_traceability", "claim_scanner", "anonymous_builder"):
        require_file(str(manuscript.get(key, "")), f"manuscript package {key}")
    if manuscript.get("internal_result_provenance_tags") != "C1-C15 plus D1-D5 post-freeze derived analyses":
        fail("internal result provenance tag range drifted")
    hierarchy = manuscript.get("result_hierarchy", [])
    if len(hierarchy) < 4 or not hierarchy[0].startswith("C6-C7") or not hierarchy[1].startswith("D1-D4") or not hierarchy[2].startswith("C2") or not hierarchy[3].startswith("D3-D5"):
        fail("MEE result hierarchy drifted")

    figures = p.get("figure_package", {})
    for key in ("plan", "validation_document", "figure_data", "validator", "builder", "requirements"):
        require_file(str(figures.get(key, "")), f"figure package {key}")
    if figures.get("figure_data_git_blob_sha1") != "74fdac2a049c6c13833bb31f7a4ff0b7228a44a6":
        fail("MEE figure-data Git blob drifted")
    if figures.get("d3_new_main_figure_required") is not False or figures.get("d4_new_main_figure_required") is not False or figures.get("d5_new_main_figure_required") is not False:
        fail("D3/D4/D5 must not silently create a new main-figure requirement")

    literature = p.get("literature_positioning", {})
    for key in ("evidence_map", "final_prior_art_audit", "nearest_neighbour_matrix", "reviewer_attack_matrix", "bibliography", "transferability_map"):
        require_file(str(literature.get(key, "")), f"literature {key}")
    if literature.get("absolute_priority_claimed") is not False or literature.get("quantitative_cross_system_transfer_claimed") is not False or literature.get("systematic_review_claimed") is not False:
        fail("literature positioning overclaims novelty/transfer/review scope")
    if "finer reason semantics require independent validation" not in str(literature.get("central_defensible_novelty", "")):
        fail("literature novelty must retain D5 semantic-specificity correction")

    boundary = p.get("paper_claim_boundary", {})
    false_keys = (
        "field_accuracy", "field_absence_certification", "field_target_prevalence",
        "universal_pi3_law", "universal_optimal_abstention", "component_level_priority",
        "c13_performance_claim", "six_axes_equal_effective_dimensions_claim",
        "classical_familywise_error_rate_control_claim", "distribution_free_finite_sample_risk_guarantee_claim",
        "d3_preregistered_claim", "d3_semantic_specificity_claim", "d3_arbitrary_weighting_robustness_claim",
        "d4_preregistered_claim", "d4_arbitrary_ecological_weighting_robustness_claim",
        "d5_preregistered_claim", "d5_random_controls_are_ecological_reason_systems_claim",
        "annotation_budget_efficiency_claim", "api_four_reason_vocabulary_validated_by_frozen_d3_claim",
    )
    for key in false_keys:
        if boundary.get(key) is not False:
            fail(f"claim boundary {key} must remain false")
    for key in ("closed_world_method_claims", "synthetic_known_truth_estimand_claims", "weighting_robustness_only_within_tested_class"):
        if boundary.get(key) is not True:
            fail(f"claim boundary {key} must remain true")

    if p.get("submission_blockers") != []:
        fail("scientific submission blockers must be empty")
    readiness = p.get("target_journal_readiness", {})
    if readiness.get("target") != "Methods in Ecology and Evolution" or readiness.get("remaining_scientific_blockers") != []:
        fail("MEE readiness drifted")
    completed = readiness.get("completed", [])
    for item in (
        "downstream synthetic ecological estimand",
        "minimal reusable implementation callable on calibrated evidence outputs",
        "expanded nearest-neighbour prior-art audit",
        "post-freeze observation-vocabulary ablation with five estimands and 34 registered axis slices",
        "post-freeze target-prevalence stratification and direct composition-level bounded density-ratio sensitivity",
        "reviewer-motivated D5 random-split control demonstrating that D3 additional narrowing is not semantic-specific",
        "frozen two-reason versus reusable four-reason vocabulary boundary documented explicitly",
        "annotation/calibration budget asymmetry registered as an explicit limitation rather than silently ignored",
    ):
        if item not in completed:
            fail(f"missing completed MEE item: {item}")

    editorial = p.get("editorial_tasks_before_upload")
    if not isinstance(editorial, list) or not editorial:
        fail("editorial tasks must remain explicit")

    print(
        "TNOA MEE manifest OK: 5 frozen science anchors; C6/C7 + D1/D4 primary; D3/D5 specificity correction enforced; 0 scientific blockers"
    )


if __name__ == "__main__":
    main()
