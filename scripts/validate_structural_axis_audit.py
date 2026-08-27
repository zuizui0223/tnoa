#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "derived" / "structural_axis_audit.json"


def fail(message: str) -> None:
    raise SystemExit(f"structural axis audit validation failed: {message}")


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    if payload.get("schema") != "tnoa-structural-axis-audit-v1":
        fail("schema drifted")
    source = payload.get("source", {})
    if source.get("workflow_run_id") != 32932634622:
        fail("source workflow drifted")
    if source.get("phase_surface_sha256") != "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34":
        fail("source surface SHA drifted")

    pi1 = payload["pi1_reason_decomposition"]["rows"]
    by = {float(r["pi1"]): r for r in pi1}
    if not by[3.1622776601683795]["no_supported_evidence_u"] < by[1.0]["no_supported_evidence_u"]:
        fail("Pi1 no-support decline after 1 was lost")
    if not by[3.1622776601683795]["overlap_attribution_u"] > by[1.0]["overlap_attribution_u"]:
        fail("Pi1 overlap increase after 1 was lost")
    if min(r["overlap_share_of_u"] for r in pi1) < 0.83:
        fail("overlap dominance across registered Pi1 levels drifted")

    axes = payload["axis_separation"]
    if axes["pi3"]["distinct_marginal_decision_vectors_at_1e-10"] != 2:
        fail("Pi3 no longer behaves as two marginal decision vectors")
    if axes["pi5"]["max_total_variation_between_level_mean_decisions"] >= 0.03:
        fail("Pi5 weak-separation audit drifted")
    if axes["pi3"]["max_total_variation_between_level_mean_decisions"] <= 0.6:
        fail("Pi3 structural separation drifted")

    c13 = payload["forced_binary_structural_decomposition"]
    if not close(c13["reported_equal_grid_target_present_false_negative_rate"], 0.3569):
        fail("C13 aggregate drifted")
    if not close(c13["reconstructed_rate"], 0.3569):
        fail("C13 structural reconstruction drifted")
    if not close(c13["false_negative_rate_by_pi3"]["0.0"], 1.0):
        fail("Pi3=0 forced-binary FN must remain 1 in the frozen audit")
    if not close(c13["non_target_false_positive_rate"], 0.0):
        fail("registered non-target FP drifted")

    print("Structural axis audit OK: Pi1 reason substitution, uneven effective axes, and C13 design composition pinned")


if __name__ == "__main__":
    main()
