#!/usr/bin/env python3
"""Fail-closed validator for the post-freeze coarsening-lattice audit."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "derived" / "coarsening_lattice_analysis.json"
EXPECTED_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"


def fail(message: str) -> None:
    raise SystemExit(f"Coarsening-lattice validation failed: {message}")


def close(actual: float, expected: float, tolerance: float = 1e-10) -> None:
    if not math.isclose(float(actual), expected, rel_tol=0.0, abs_tol=tolerance):
        fail(f"numeric drift: expected {expected}, got {actual}")


def main() -> None:
    if not RESULT.is_file():
        fail("missing derived/coarsening_lattice_analysis.json")
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    if payload.get("schema") != "tnoa-coarsening-lattice-v1":
        fail("schema drifted")
    if payload.get("status") != "post_freeze_deterministic_derivation_no_observer_retuning":
        fail("post-freeze status drifted")
    source = payload.get("source", {})
    if source.get("phase_surface_sha256") != EXPECTED_SHA:
        fail("source phase-surface SHA drifted")
    if source.get("row_count") != 183750 or source.get("coordinate_count") != 30625 or source.get("world_count") != 5880000:
        fail("source dimensions drifted")
    if payload.get("partition_count") != 15 or payload.get("mixture_count") != 3003:
        fail("partition/simplex size drifted")

    close(payload["full"]["width"]["median"], 0.02992070478107567)
    close(payload["binary_target_vs_rest"]["width"]["median"], 0.2656306018443619)

    tri = {item["preserve"]: item for item in payload["target_plus_one_non_target_distinction"]}
    if set(tri) != {"B", "N", "U"}:
        fail("target-plus-one tri-state inventory drifted")
    close(tri["U"]["width"]["median"], 0.16634048914535082)
    close(tri["B"]["width"]["median"], 0.1883900825109205)
    close(tri["N"]["width"]["median"], 0.18861428571428596)
    close(tri["U"]["relative_recovery_from_binary"]["median"], 0.4227903916844362)
    close(tri["B"]["relative_recovery_from_binary"]["median"], 0.2619844280391903)
    close(tri["N"]["relative_recovery_from_binary"]["median"], 0.10583781580909715)

    boundary = payload.get("claim_boundary", {})
    if boundary.get("observer_retuned") is not False:
        fail("observer-retuning boundary drifted")
    if boundary.get("field_prevalence_claimed") is not False or boundary.get("ecological_prior_claimed") is not False:
        fail("field/prior claim boundary drifted")
    print(
        "Coarsening-lattice audit PASS: 15 partitions; U is the strongest single restored non-target distinction, "
        "but full B/N/U separation remains complementary"
    )


if __name__ == "__main__":
    main()
