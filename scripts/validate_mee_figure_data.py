#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "derived" / "mee_figure_data.json"
CONSEQUENCES = ROOT / "derived" / "mee_synthetic_consequences.json"
STRUCTURAL = ROOT / "derived" / "structural_axis_audit.json"
MANIFEST = ROOT / "paper_manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"MEE figure-data validation failed: {message}")


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(float(a) - float(b)) <= tol


def require_close(actual: float, expected: float, label: str) -> None:
    if not close(actual, expected):
        fail(f"{label} drifted: {actual!r} != {expected!r}")


def require_close_sequence(actual: list[float], expected: list[float], label: str) -> None:
    if len(actual) != len(expected) or any(not close(a, e) for a, e in zip(actual, expected)):
        fail(f"{label} drifted")


def main() -> None:
    d = json.loads(PATH.read_text(encoding="utf-8"))
    consequences = json.loads(CONSEQUENCES.read_text(encoding="utf-8"))
    structural = json.loads(STRUCTURAL.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if d.get("schema") != "tnoa-mee-figure-data-v1":
        fail("schema drifted")
    if consequences.get("schema") != "tnoa-mee-synthetic-consequences-v1":
        fail("synthetic-consequence source schema drifted")
    if structural.get("schema") != "tnoa-structural-axis-audit-v1":
        fail("structural-audit source schema drifted")

    risk = d["figure2_risk_calibration"]
    old = risk["inherited_threshold_failure"]
    if not close(old["auc_nuisance_vs_target_only"], 1.0):
        fail("nuisance-vs-target AUC drifted")
    if not close(old["coherent_nuisance_recall_at_0_55"], 0.23125):
        fail("inherited-threshold recall drifted")
    pooled = risk["pooled_risk_calibration"]
    family = risk["familywise_risk_calibration"]
    if pooled["freezable"] is not False or family["freezable"] is not True:
        fail("pooled/family-wise pass-fail sequence drifted")
    if not pooled["coupled_negative_fpr"] > pooled["alpha"]:
        fail("pooled calibration should fail the coupled-negative alpha gate")
    if not family["coupled_negative_fpr"] <= family["alpha"]:
        fail("family-wise calibration should pass the coupled-negative alpha gate")

    est = d["figure3_estimand"]
    source_estimand = consequences["estimand"]
    source_global = source_estimand["global"]
    if est["mixture_count"] != source_estimand["simplex"]["mixture_count"]:
        fail("prevalence simplex mixture count drifted")
    s = est["summary"]
    source_summary = {
        "negative_naive_bias_fraction": source_global["naive_binary_negative_bias_fraction"],
        "median_naive_bias": source_global["naive_binary_bias"]["median"],
        "median_tnoa_width": source_global["tnoa_partial_identification_width"]["median"],
        "median_binary_width": source_global["binary_partial_identification_width"]["median"],
        "median_relative_width_reduction_nonzero_binary": source_global["relative_width_reduction_nonzero_binary"]["median"],
    }
    if set(s) != set(source_summary):
        fail("estimand summary keys drifted")
    for key, expected in source_summary.items():
        require_close(s[key], expected, f"estimand summary {key}")

    curves = est["quantile_curves"]
    expected_q = [i / 20 for i in range(21)]
    require_close_sequence(curves["q"], expected_q, "quantile grid")
    curve_sources = {
        "naive_bias": source_global["naive_binary_bias"],
        "tnoa_width": source_global["tnoa_partial_identification_width"],
        "binary_width": source_global["binary_partial_identification_width"],
    }
    for key, stats in curve_sources.items():
        values = curves[key]
        if len(values) != len(expected_q) or any(a > b + 1e-10 for a, b in zip(values, values[1:])):
            fail(f"{key} quantile curve is malformed or non-monotone")
        for index, stat_key in ((0, "min"), (1, "q05"), (10, "median"), (19, "q95"), (20, "max")):
            require_close(values[index], stats[stat_key], f"{key} {stat_key}")

    u = d["figure4_unresolved_reasons"]
    source_weighting = consequences["weighting_sensitivity"]["minimum_overlap_share_of_U"]
    if set(u["bounded_reweighting_min_overlap_share"]) != set(source_weighting):
        fail("bounded-reweighting kappa grid drifted")
    for key, expected in source_weighting.items():
        require_close(u["bounded_reweighting_min_overlap_share"][key], expected, f"bounded reweighting kappa={key}")
    if float(u["bounded_reweighting_min_overlap_share"]["10.0"]) <= 0.5:
        fail("overlap majority at kappa=10 drifted")
    source_pi1 = structural["pi1_reason_decomposition"]["rows"]
    if len(u["pi1"]) != len(source_pi1):
        fail("Pi1 reason row count drifted")
    for actual, expected in zip(u["pi1"], source_pi1):
        mapping = {
            "pi1": "pi1",
            "no_support_u": "no_supported_evidence_u",
            "overlap_u": "overlap_attribution_u",
            "total_u": "total_u",
            "overlap_share": "overlap_share_of_u",
        }
        for actual_key, source_key in mapping.items():
            require_close(actual[actual_key], expected[source_key], f"Pi1 {actual['pi1']} {actual_key}")
    pi1 = {float(r["pi1"]): r for r in u["pi1"]}
    if not pi1[3.1622776601683795]["no_support_u"] < pi1[1.0]["no_support_u"]:
        fail("Pi1 no-support substitution drifted")
    if not pi1[3.1622776601683795]["overlap_u"] > pi1[1.0]["overlap_u"]:
        fail("Pi1 overlap substitution drifted")

    axes = d["supplement_axis_separation"]
    source_axes = structural["axis_separation"]
    if set(axes) != set(source_axes):
        fail("axis-separation keys drifted")
    for axis, actual in axes.items():
        expected = source_axes[axis]
        require_close_sequence(actual["levels"], expected["registered_levels"], f"{axis} registered levels")
        if actual["distinct"] != expected["distinct_marginal_decision_vectors_at_1e-10"]:
            fail(f"{axis} distinct-vector count drifted")
        require_close(actual["max_tv"], expected["max_total_variation_between_level_mean_decisions"], f"{axis} max TV")
        require_close_sequence(actual["pair"], expected["max_tv_level_pair"], f"{axis} max-TV pair")
    if axes["pi3"]["distinct"] != 2 or not close(axes["pi3"]["max_tv"], 0.6431):
        fail("Pi3 effective-axis summary drifted")
    if axes["pi5"]["max_tv"] >= 0.03:
        fail("Pi5 weak marginal separation drifted")

    c13 = d["supplement_c13"]
    source_c13 = structural["forced_binary_structural_decomposition"]
    require_close(c13["equal_grid_fn"], source_c13["reported_equal_grid_target_present_false_negative_rate"], "C13 equal-grid FN")
    require_close(c13["pi3_zero_fn"], source_c13["false_negative_rate_by_pi3"]["0.0"], "C13 Pi3-zero FN")
    positive_fn = {float(value) for key, value in source_c13["false_negative_rate_by_pi3"].items() if float(key) > 0}
    if len(positive_fn) != 1:
        fail("C13 positive-Pi3 false-negative rates no longer collapse to one value")
    require_close(c13["positive_pi3_fn"], positive_fn.pop(), "C13 positive-Pi3 FN")
    if c13["identity"] != "0.2*1.0 + 0.8*0.196125":
        fail("C13 composition identity drifted")
    if not close(c13["equal_grid_fn"], 0.3569):
        fail("C13 equal-grid rate drifted")

    p = d["provenance"]
    locked = {row["id"]: row for row in manifest["locked_results"]}
    final = locked["v14b_final_ternary_phase_surface"]
    surface = p["v14b_phase_surface"]
    for key, expected in (
        ("workflow_run_id", final["workflow_run_id"]),
        ("artifact_id", final["artifact_id"]),
        ("artifact_digest", final["artifact_digest"]),
        ("surface_sha256", final["result_sha256"]),
    ):
        if surface[key] != expected:
            fail(f"surface provenance {key} drifted")
    sequence = {row["stage"]: row for row in manifest["development_evidence"]["nuisance_threshold_sequence"]}
    stage_map = {
        "nuisance_v1_failure": "inherited_threshold_failure",
        "nuisance_score_diagnosis": "score_scale_diagnosis",
        "pooled_risk_failure": "pooled_risk_failure",
        "familywise_risk_freeze": "familywise_risk_freeze",
    }
    for figure_key, stage in stage_map.items():
        actual = p[figure_key]
        expected = sequence[stage]
        for key in ("workflow_run_id", "artifact_id", "artifact_digest", "result_sha256"):
            if actual[key] != expected[key]:
                fail(f"{figure_key} provenance {key} drifted")

    print("MEE figure data OK: risk-calibration sequence, estimand, U reasons, axes and C13 are pinned")


if __name__ == "__main__":
    main()
