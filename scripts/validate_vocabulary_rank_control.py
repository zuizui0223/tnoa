#!/usr/bin/env python3
"""Fail-closed validation for the post-freeze vocabulary-rank control (D5)."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "derived" / "vocabulary_rank_control.json"
SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"


def fail(message: str) -> None:
    raise SystemExit(f"Vocabulary-rank control validation failed: {message}")


def close(actual: float, expected: float, atol: float = 1e-12) -> bool:
    return math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=atol)


def main() -> None:
    if not RESULT.is_file():
        fail("derived/vocabulary_rank_control.json missing")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    if data.get("schema") != "tnoa-vocabulary-rank-control-v1":
        fail("schema drifted")
    status = str(data.get("status", ""))
    if "post-freeze" not in status or "not preregistered" not in status:
        fail("post-freeze/not-preregistered boundary missing")
    source = data.get("source", {})
    if source.get("workflow_run_id") != 32932634622:
        fail("workflow provenance drifted")
    if source.get("phase_surface_sha256") != SURFACE_SHA:
        fail("phase-surface SHA drifted")
    if source.get("row_count") != 183750 or source.get("mixture_count") != 3003:
        fail("source dimensions drifted")

    design = data.get("control_design", {})
    if design.get("random_seed") != 0:
        fail("random-control seed drifted")
    if design.get("random_two_way_split_count") != 500:
        fail("two-way split count drifted")
    if design.get("random_three_way_split_count") != 500:
        fail("three-way split count drifted")

    ladder = data.get("target_prevalence_rank_ladder", {})
    expected_ladder = {
        "binary_target_not_target": (0.2656306018443621, 4, 2),
        "target_nuisance_other": (0.18861428571428596, 3, 3),
        "btnu_collapsed": (0.02992070478107567, 2, 4),
        "semantic_two_way_u_split": (0.004077995920098443, 1, 5),
    }
    for name, (width, dim, rank) in expected_ladder.items():
        row = ladder.get(name, {})
        if not close(row.get("target_prevalence_median_width"), width):
            fail(f"{name} width drifted")
        if row.get("nullspace_dimension") != dim or row.get("constraint_rank") != rank:
            fail(f"{name} rank/nullspace drifted")

    const = data.get("constant_two_way_split", {}).get("target_prevalence", {})
    if not close(const.get("median_width"), 0.02992070478107489):
        fail("constant-split control no longer matches generic U")
    if const.get("nullspace_dimension") != 2 or const.get("constraint_rank") != 4:
        fail("constant-split rank drifted")

    random_target = data.get("random_two_way_splits", {}).get("target_prevalence", {})
    distribution = random_target.get("random_split_median_width_distribution", {})
    if not close(distribution.get("median"), 0.005007513005321984):
        fail("random two-way target median drifted")
    if not close(random_target.get("semantic_split_median_width"), 0.004077995920098443):
        fail("semantic target width drifted")
    if not close(random_target.get("fraction_random_splits_at_or_below_semantic"), 0.48):
        fail("semantic-specificity control fraction drifted")
    if not close(random_target.get("semantic_to_random_median_ratio"), 0.8143755025227791):
        fail("semantic/random target median ratio drifted")
    if random_target.get("all_random_nullspace_dimensions") != [1]:
        fail("random two-way nullspace dimension drifted")
    if random_target.get("all_random_constraint_ranks") != [5]:
        fail("random two-way rank drifted")

    expected_fraction = {
        "target_prevalence": 0.48,
        "nuisance_prevalence": 0.488,
        "target_nuisance_cooccurrence": 0.488,
        "coupled_response_prevalence": 0.672,
        "any_deviation_prevalence": 0.48,
    }
    for estimand, expected in expected_fraction.items():
        actual = data["random_two_way_splits"][estimand][
            "fraction_random_splits_at_or_below_semantic"
        ]
        if not close(actual, expected):
            fail(f"random-control fraction drifted for {estimand}")

    three = data.get("random_three_way_target_prevalence", {})
    if three.get("point_identified_count") != 500:
        fail("three-way point-identification count drifted")
    if three.get("all_nullspace_dimensions") != [0] or three.get("all_constraint_ranks") != [6]:
        fail("three-way full-rank control drifted")
    if not close(three["median_width_distribution"]["median"], 0.0):
        fail("three-way target median must remain zero")

    boundary = " ".join(data.get("claim_boundary", [])).lower()
    for phrase in (
        "not preregistered",
        "do not invalidate d1",
        "no semantic-specific information advantage",
        "unregistered latent regimes",
        "later reusable api's four u reasons",
    ):
        if phrase not in boundary:
            fail(f"claim boundary missing: {phrase}")

    print(
        "Vocabulary-rank control PASS: constant split no gain; "
        "500 random two-way splits median=0.0050075 with 48.0% <= semantic; "
        "500 random three-way splits full-rank/point-identified"
    )


if __name__ == "__main__":
    main()
