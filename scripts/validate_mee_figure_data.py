#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "derived" / "mee_figure_data.json"


def fail(message: str) -> None:
    raise SystemExit(f"MEE figure-data validation failed: {message}")


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> None:
    d = json.loads(PATH.read_text(encoding="utf-8"))
    if d.get("schema") != "tnoa-mee-figure-data-v1":
        fail("schema drifted")

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
    if est["mixture_count"] != 3003:
        fail("prevalence simplex mixture count drifted")
    s = est["summary"]
    if not close(s["negative_naive_bias_fraction"], 0.9963369963369964):
        fail("naive bias fraction drifted")
    if not close(s["median_tnoa_width"], 0.0299207047810754):
        fail("TNOA median identification width drifted")
    if not close(s["median_binary_width"], 0.2656306018443619):
        fail("binary median identification width drifted")

    u = d["figure4_unresolved_reasons"]
    if float(u["bounded_reweighting_min_overlap_share"]["10.0"]) <= 0.5:
        fail("overlap majority at kappa=10 drifted")
    pi1 = {float(r["pi1"]): r for r in u["pi1"]}
    if not pi1[3.1622776601683795]["no_support_u"] < pi1[1.0]["no_support_u"]:
        fail("Pi1 no-support substitution drifted")
    if not pi1[3.1622776601683795]["overlap_u"] > pi1[1.0]["overlap_u"]:
        fail("Pi1 overlap substitution drifted")

    axes = d["supplement_axis_separation"]
    if axes["pi3"]["distinct"] != 2 or not close(axes["pi3"]["max_tv"], 0.6431):
        fail("Pi3 effective-axis summary drifted")
    if axes["pi5"]["max_tv"] >= 0.03:
        fail("Pi5 weak marginal separation drifted")

    c13 = d["supplement_c13"]
    if c13["identity"] != "0.2*1.0 + 0.8*0.196125":
        fail("C13 composition identity drifted")
    if not close(c13["equal_grid_fn"], 0.3569):
        fail("C13 equal-grid rate drifted")

    p = d["provenance"]
    if p["v14b_phase_surface"]["workflow_run_id"] != 32932634622:
        fail("surface provenance drifted")
    if p["nuisance_v1_failure"]["workflow_run_id"] != 32929245729:
        fail("PR43 provenance drifted")
    if p["nuisance_score_diagnosis"]["workflow_run_id"] != 32929754709:
        fail("PR44 provenance drifted")
    if p["pooled_risk_failure"]["workflow_run_id"] != 32930855374:
        fail("PR45 provenance drifted")
    if p["familywise_risk_freeze"]["workflow_run_id"] != 32931223272:
        fail("PR46 provenance drifted")

    print("MEE figure data OK: risk-calibration sequence, estimand, U reasons, axes and C13 are pinned")


if __name__ == "__main__":
    main()
