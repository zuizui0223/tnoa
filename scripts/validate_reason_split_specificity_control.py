#!/usr/bin/env python3
"""Validate the pinned D5 random-split specificity control."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "derived" / "reason_split_specificity_control.json"
SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"


def fail(message: str) -> None:
    raise SystemExit(f"D5 specificity-control validation failed: {message}")


def close(actual, expected, atol=1e-12):
    return math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=atol)


def main() -> None:
    if not RESULT.is_file():
        fail("result missing")
    d = json.loads(RESULT.read_text(encoding="utf-8"))
    if d.get("schema") != "tnoa-reason-split-specificity-control-v1":
        fail("schema drifted")
    if "not preregistered" not in str(d.get("status", "")):
        fail("post-freeze/not-preregistered boundary missing")
    source = d.get("source", {})
    if source.get("workflow_run_id") != 32932634622 or source.get("phase_surface_sha256") != SURFACE_SHA:
        fail("source provenance drifted")
    if source.get("mixture_count") != 3003 or source.get("latent_regime_count") != 6:
        fail("design dimensions drifted")
    control = d.get("control_design", {})
    if control.get("random_seed") != 0 or control.get("two_way_random_split_count") != 500 or control.get("three_way_random_split_count") != 500:
        fail("random-control contract drifted")

    rank = d.get("rank_ladder", {})
    expected_dims = {
        "target_not_target": 4,
        "target_nuisance_other": 3,
        "btnu_generic_u": 2,
        "btnu_semantic_two_reason_split": 1,
        "random_three_way_u_split": 0,
    }
    for key, expected in expected_dims.items():
        if rank.get(key, {}).get("nullspace_dimension") != expected:
            fail(f"nullspace dimension drifted: {key}")
    if not close(rank["random_three_way_u_split"].get("full_rank_fraction"), 1.0):
        fail("three-way controls must remain full rank")

    target = d.get("estimands", {}).get("target_prevalence", {})
    checks = {
        "generic_u_median_width": 0.02992070478107567,
        "constant_split_median_width": 0.02992070478107489,
        "semantic_two_reason_split_median_width": 0.004077995920098443,
        "fraction_random_two_way_splits_equal_or_narrower_than_semantic": 0.48,
        "semantic_width_divided_by_random_median": 0.8143755025227791,
        "random_three_way_point_identification_fraction": 1.0,
    }
    for key, expected in checks.items():
        if not close(target.get(key), expected):
            fail(f"target-prevalence control drifted: {key}")
    random_median = target.get("random_two_way_split_median_width_distribution", {}).get("median")
    if not close(random_median, 0.005007513005321984):
        fail("random two-way median drifted")

    fractions = {
        name: row.get("fraction_random_two_way_splits_equal_or_narrower_than_semantic")
        for name, row in d.get("estimands", {}).items()
    }
    expected_fractions = {
        "target_prevalence": 0.48,
        "nuisance_prevalence": 0.488,
        "target_nuisance_cooccurrence": 0.488,
        "coupled_response_prevalence": 0.672,
        "any_deviation_prevalence": 0.48,
    }
    if set(fractions) != set(expected_fractions):
        fail("estimand set drifted")
    for name, expected in expected_fractions.items():
        if not close(fractions[name], expected):
            fail(f"random-control fraction drifted: {name}")
        if not close(d["estimands"][name].get("random_three_way_point_identification_fraction"), 1.0):
            fail(f"three-way point-identification control drifted: {name}")

    boundary = str(d.get("claim_boundary", "")).lower()
    if "not shown to be specific to reason semantics" not in boundary:
        fail("semantic-specificity claim boundary missing")

    print("D5 specificity control PASS: semantic split is informative but not exceptional against random regime-discriminating splits")


if __name__ == "__main__":
    main()
