#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "derived" / "prevalence_weighting_sensitivity.json"


def fail(message: str) -> None:
    raise SystemExit(f"prevalence-weighting sensitivity validation failed: {message}")


def close(a: float, b: float, tol: float = 1e-10) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> None:
    d = json.loads(PATH.read_text(encoding="utf-8"))
    if d.get("schema") != "tnoa-prevalence-weighting-sensitivity-v1":
        fail("schema drifted")
    source = d["source"]
    if source["phase_surface_sha256"] != "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34":
        fail("surface SHA drifted")
    if source["mixture_count"] != 3003 or source["simplex_step"] != 0.1:
        fail("simplex design drifted")

    counts = d["prevalence_lattice_counts"]
    if sum(counts.values()) != 3003:
        fail("prevalence strata do not cover the simplex")
    if counts != {"0.0": 11, "0.1": 40, "0.2": 90, "0.3": 160, "0.4": 245, "0.5": 336, "0.6": 420, "0.7": 480, "0.8": 495, "0.9": 440, "1.0": 286}:
        fail("prevalence lattice counts drifted")

    rare = d["rare_target_subsets"]["theta_le_0.2"]
    if rare["count"] != 141 or not close(rare["uniform_lattice_mass"], 141 / 3003):
        fail("rare-target simplex mass drifted")
    if not close(rare["median_width_binary"], 0.07409970878498642):
        fail("rare-target binary median width drifted")
    if not close(rare["median_width_btnu"], 0.0001746269687759039):
        fail("rare-target B/T/N/U median width drifted")
    if not close(rare["median_width_reason_resolved"], 0.0):
        fail("rare-target reason-resolved median width drifted")

    strata = d["prevalence_strata"]
    for key, row in strata.items():
        if row["median_width_btnu"] > row["median_width_binary"] + 1e-9:
            fail(f"B/T/N/U wider than binary at theta={key}")
        if row["median_width_reason_resolved"] > row["median_width_btnu"] + 1e-9:
            fail(f"reason-resolved U wider than generic U at theta={key}")

    sens = d["composition_density_ratio_sensitivity"]["minimum_fraction_width_removed"]
    if not close(sens["1.0"]["btnu_vs_binary"], 0.8426328123074449):
        fail("uniform weighted-mean B/T/N/U gain drifted")
    if not close(sens["10.0"]["btnu_vs_binary"], 0.5746863884992289):
        fail("kappa=10 B/T/N/U worst-case gain drifted")
    if not close(sens["10.0"]["reason_resolved_vs_btnu"], 0.4000338180837051):
        fail("kappa=10 reason-resolved worst-case gain drifted")
    btnu = [sens[str(k)]["btnu_vs_binary"] for k in (1.0, 1.25, 1.5, 1.6, 2.0, 3.0, 5.0, 10.0)]
    resolved = [sens[str(k)]["reason_resolved_vs_btnu"] for k in (1.0, 1.25, 1.5, 1.6, 2.0, 3.0, 5.0, 10.0)]
    if any(a < b - 1e-12 for a, b in zip(btnu, btnu[1:])):
        fail("B/T/N/U worst-case gain should not increase with kappa")
    if any(a < b - 1e-12 for a, b in zip(resolved, resolved[1:])):
        fail("reason-resolved worst-case gain should not increase with kappa")

    boundary = " ".join(d.get("claim_boundary", [])).lower()
    for phrase in ("not an ecological prior", "no field prevalence", "annotation-budget efficiency"):
        if phrase not in boundary:
            fail(f"claim boundary missing: {phrase}")

    print("Prevalence/composition sensitivity PASS: 11 prevalence strata, rare-target stress test, kappa<=10 weighting audit")


if __name__ == "__main__":
    main()
