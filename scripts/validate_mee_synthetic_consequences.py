#!/usr/bin/env python3
"""Fail closed if the committed post-freeze MEE result drifts."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "derived" / "mee_synthetic_consequences.json"
EXPECTED_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"


def close(actual: float, expected: float, tol: float = 1e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=tol, abs_tol=tol):
        raise SystemExit(f"derived MEE result drift: {actual} != {expected}")


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data["schema"] != "tnoa-mee-synthetic-consequences-v1":
        raise SystemExit("unexpected derived-result schema")
    source = data["source"]
    if source["workflow_run_id"] != 32932634622:
        raise SystemExit("unexpected source workflow")
    if source["phase_surface_sha256"] != EXPECTED_SHA:
        raise SystemExit("derived result is not pinned to frozen V14b surface")
    if (source["coordinate_count"], source["row_count"], source["world_count"]) != (30625, 183750, 5880000):
        raise SystemExit("frozen surface dimensions drifted")

    global_result = data["estimand"]["global"]
    if global_result["mixture_count"] != 3003:
        raise SystemExit("simplex lattice drifted")
    close(global_result["naive_binary_negative_bias_fraction"], 0.9963369963369964)
    close(global_result["naive_binary_bias"]["median"], -0.23767428571428578)
    close(global_result["tnoa_partial_identification_width"]["median"], 0.02992070478107567)
    close(global_result["binary_partial_identification_width"]["median"], 0.2656306018443621)
    close(global_result["relative_width_reduction_nonzero_binary"]["median"], 0.8444740221005506)
    if global_result["tnoa_true_prevalence_coverage"] != 1.0 or not global_result["tnoa_never_wider"]:
        raise SystemExit("partial-identification safety contract drifted")

    slices = data["estimand"]["axis_slice_sensitivity"]
    if slices["slice_count"] != 34 or not slices["summary"]["all_slices_tnoa_never_wider"]:
        raise SystemExit("axis-slice sensitivity contract drifted")

    weight = data["weighting_sensitivity"]
    close(weight["minimum_overlap_share_of_U"]["10.0"], 0.5201367144782036)
    if weight["pi1_monotone_nonincreasing_U_feasible"]["1.5"] is not False:
        raise SystemExit("Pi1 kappa=1.5 sensitivity drifted")
    if weight["pi1_monotone_nonincreasing_U_feasible"]["1.6"] is not True:
        raise SystemExit("Pi1 kappa=1.6 sensitivity drifted")
    c = weight["pi2_center_minus_neighbor_mean_U_contrast_range"]["1.25"]
    if not (c["min"] < 0 < c["max"]):
        raise SystemExit("Pi2 sign-sensitivity result drifted")

    guard = " ".join(data["claim_guards"]).lower()
    for token in ("no field prevalence", "no observer retuning", "weighting-robust"):
        if token not in (data["status"] + " " + guard).lower():
            raise SystemExit(f"missing MEE claim guard: {token}")
    print("MEE synthetic-consequence result validation PASS")


if __name__ == "__main__":
    main()
