#!/usr/bin/env python3
"""Validate the post-freeze TNOA observation-vocabulary ablation."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "derived" / "observation_vocabulary_ablation.json"
SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
EXPECTED_MEDIANS = {
    "target_prevalence": [0.2656306018443621, 0.18861428571428596, 0.02992070478107567, 0.004077995920098443],
    "nuisance_prevalence": [1.0, 0.42330030506237437, 0.08923538672581777, 0.012631643480150667],
    "target_nuisance_cooccurrence": [0.7230694417428517, 0.5136354794787008, 0.10493504246086616, 0.014840229278269765],
    "coupled_response_prevalence": [0.8589231290213343, 0.7658539338525793, 0.3999026031009051, 0.07510112725107763],
    "any_deviation_prevalence": [0.4559214285714286, 0.08646341530809643, 0.01371606776231138, 0.0018694101219792758],
}
VOCAB = [
    "binary_target_not_target",
    "target_nuisance_other",
    "btnu_collapsed",
    "btnu_reason_resolved",
]
EXPECTED_STRICT_SLICE_IMPROVEMENTS = {
    "target_prevalence": 27,
    "nuisance_prevalence": 29,
    "target_nuisance_cooccurrence": 29,
    "coupled_response_prevalence": 29,
    "any_deviation_prevalence": 29,
}


def fail(message: str) -> None:
    raise SystemExit(f"observation-vocabulary ablation validation failed: {message}")


def close(actual: float, expected: float, atol: float = 1e-10) -> bool:
    return math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=atol)


def main() -> None:
    if not RESULT.is_file():
        fail("missing derived result")
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    if payload.get("schema") != "tnoa-observation-vocabulary-ablation-v1":
        fail("schema drifted")
    status = str(payload.get("status", ""))
    for token in ("post-freeze", "no observer retuning", "not preregistered"):
        if token not in status:
            fail(f"status lost boundary: {token}")
    source = payload.get("source", {})
    if source.get("workflow_run_id") != 32932634622:
        fail("source workflow drifted")
    if source.get("phase_surface_sha256") != SURFACE_SHA:
        fail("source surface SHA drifted")
    if source.get("coordinate_count") != 30625 or source.get("row_count") != 183750:
        fail("source dimensions drifted")
    if source.get("mixture_count") != 3003:
        fail("mixture count drifted")
    if payload.get("vocabulary_order") != VOCAB:
        fail("vocabulary order drifted")

    estimands = payload.get("estimands", {})
    for name, expected in EXPECTED_MEDIANS.items():
        if name not in estimands:
            fail(f"missing estimand: {name}")
        actual = [
            estimands[name][v]["identification_width"]["median"]
            for v in VOCAB
        ]
        for got, want in zip(actual, expected):
            if not close(got, want):
                fail(f"median width drift for {name}: {actual}")
        if not all(
            estimands[name][v].get("true_prevalence_coverage") == 1.0
            for v in VOCAB
        ):
            fail(f"true-value coverage drift for {name}")
        if not all(
            estimands[name][v].get("never_wider_than_previous") is True
            for v in VOCAB[1:]
        ):
            fail(f"nested coarsening order failed for {name}")

    slices = payload.get("axis_slice_summary", {})
    for name, strict_expected in EXPECTED_STRICT_SLICE_IMPROVEMENTS.items():
        rec = slices.get(name, {})
        if rec.get("slice_count") != 34 or rec.get("reason_resolved_never_wider_count") != 34:
            fail(f"34-slice never-wider guard failed for {name}")
        if rec.get("strict_median_improvement_count") != strict_expected:
            fail(f"strict slice-improvement count drifted for {name}")

    target = estimands["target_prevalence"]
    if not close(target["reason_resolved_relative_median_width_reduction_vs_btnu_collapsed"], 0.8637065553790797):
        fail("target reason-resolved gain drifted")
    co = estimands["target_nuisance_cooccurrence"]
    if not close(co["reason_resolved_relative_median_width_reduction_vs_btnu_collapsed"], 0.8585769926780733):
        fail("T+N cooccurrence reason-resolved gain drifted")

    boundary = str(payload.get("claim_boundary", ""))
    for token in ("structural", "no field prevalence", "no field prevalence"):
        if token not in boundary:
            fail(f"claim boundary lost token: {token}")
    print("Observation-vocabulary ablation PASS: 5 estimands, 4 nested vocabularies, 34 registered axis slices")


if __name__ == "__main__":
    main()
