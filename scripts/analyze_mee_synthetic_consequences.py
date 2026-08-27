#!/usr/bin/env python3
"""Derive MEE-facing ecological-estimand and weighting checks from frozen V14b.

This is a post-freeze analysis. It never reruns or retunes the V14b observers.
The input must be the immutable ``phase_surface.json`` artifact from workflow
32932634622.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
WORKFLOW = 32932634622
REGIMES = [
    "baseline",
    "target_only",
    "nuisance_only",
    "target_coupled",
    "target_nuisance_superposed",
    "target_nuisance_coupled",
]
TARGET = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 1.0])
OUT = ["baseline_rate", "target_rate", "nuisance_rate", "undetermined_total_rate"]
AXES = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6"]
KAPPAS = [1.0, 1.25, 1.5, 1.6, 2.0, 3.0, 5.0, 10.0]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_surface(path: Path) -> tuple[dict, list[dict]]:
    actual = sha256(path)
    if actual != SURFACE_SHA:
        raise SystemExit(f"locked surface SHA mismatch: {actual}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("coordinate_count") != 30625 or data.get("row_count") != 183750:
        raise SystemExit("locked surface dimensions drifted")
    rows = data.get("rows", [])
    if len(rows) != 183750:
        raise SystemExit("surface row payload is incomplete")
    for row in rows:
        if not np.isclose(sum(float(row[k]) for k in OUT), 1.0, atol=1e-10):
            raise SystemExit("B/T/N/U row does not sum to one")
    return data, rows


def compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total - value, parts - 1, prefix + (value,))


def simplex(denominator: int = 10) -> np.ndarray:
    return np.array(list(compositions(denominator, 6)), dtype=float) / denominator


def nullspace(a: np.ndarray) -> np.ndarray:
    _, s, vh = np.linalg.svd(a, full_matrices=True)
    rank = int(np.sum(s > 1e-11 * s[0])) if s.size else 0
    return vh[rank:].T


def bounds_for_simplex(
    mixes: np.ndarray, emission: np.ndarray, observed_columns: list[int]
) -> tuple[np.ndarray, np.ndarray]:
    """Exact prevalence bounds over mixtures with the same retained observables."""
    a = np.vstack([np.ones(6), emission[:, observed_columns].T])
    n = nullspace(a)
    dim = n.shape[1]
    truth = mixes @ TARGET
    low = truth.copy()
    high = truth.copy()
    if dim == 0:
        return low, high
    for active in itertools.combinations(range(6), dim):
        q = n[list(active), :]
        if abs(np.linalg.det(q)) < 1e-12:
            continue
        inv = np.linalg.inv(q)
        z = -mixes[:, list(active)] @ inv.T
        candidate = mixes + z @ n.T
        ok = np.min(candidate, axis=1) >= -1e-9
        if not np.any(ok):
            continue
        values = candidate @ TARGET
        low[ok] = np.minimum(low[ok], values[ok])
        high[ok] = np.maximum(high[ok], values[ok])
    return np.clip(low, 0.0, 1.0), np.clip(high, 0.0, 1.0)


def qstats(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return {"count": 0, "min": None, "q05": None, "median": None, "mean": None, "q95": None, "max": None}
    return {
        "count": int(x.size),
        "min": float(np.min(x)),
        "q05": float(np.quantile(x, 0.05)),
        "median": float(np.median(x)),
        "mean": float(np.mean(x)),
        "q95": float(np.quantile(x, 0.95)),
        "max": float(np.max(x)),
    }


def emission_matrix(rows: list[dict]) -> np.ndarray:
    sums = {r: np.zeros(4) for r in REGIMES}
    counts = Counter()
    for row in rows:
        regime = row["latent_regime"]
        sums[regime] += np.array([float(row[k]) for k in OUT])
        counts[regime] += 1
    return np.vstack([sums[r] / counts[r] for r in REGIMES])


def estimand_summary(emission: np.ndarray, mixes: np.ndarray) -> dict:
    truth = mixes @ TARGET
    observed = mixes @ emission
    naive = observed[:, 1]
    t_lo, t_hi = bounds_for_simplex(mixes, emission, [0, 1, 2])
    b_lo, b_hi = bounds_for_simplex(mixes, emission, [1])
    tw = np.maximum(0.0, t_hi - t_lo)
    bw = np.maximum(0.0, b_hi - b_lo)
    bias = naive - truth
    reduction = bw - tw
    rel = np.divide(reduction, bw, out=np.full_like(bw, np.nan), where=bw > 1e-12)
    return {
        "mixture_count": int(len(mixes)),
        "naive_binary_bias": qstats(bias),
        "naive_binary_negative_bias_fraction": float(np.mean(bias < -1e-9)),
        "naive_binary_exact_unbiased_fraction": float(np.mean(np.abs(bias) <= 1e-9)),
        "tnoa_partial_identification_width": qstats(tw),
        "binary_partial_identification_width": qstats(bw),
        "absolute_width_reduction": qstats(reduction),
        "relative_width_reduction_nonzero_binary": qstats(rel[np.isfinite(rel)]),
        "tnoa_true_prevalence_coverage": float(np.mean((t_lo - 1e-8 <= truth) & (truth <= t_hi + 1e-8))),
        "binary_true_prevalence_coverage": float(np.mean((b_lo - 1e-8 <= truth) & (truth <= b_hi + 1e-8))),
        "tnoa_strictly_narrower_fraction": float(np.mean(tw < bw - 1e-9)),
        "tnoa_never_wider": bool(np.all(tw <= bw + 1e-9)),
    }


def axis_slice_sensitivity(rows: list[dict], mixes: np.ndarray) -> dict:
    sums: dict[tuple[str, float, str], np.ndarray] = {}
    counts = Counter()
    levels = {a: set() for a in AXES}
    for row in rows:
        outcome = np.array([float(row[k]) for k in OUT])
        regime = row["latent_regime"]
        for axis in AXES:
            value = float(row[axis])
            levels[axis].add(value)
            key = (axis, value, regime)
            if key not in sums:
                sums[key] = np.zeros(4)
            sums[key] += outcome
            counts[key] += 1
    slices = []
    for axis in AXES:
        for value in sorted(levels[axis]):
            m = np.vstack([sums[(axis, value, r)] / counts[(axis, value, r)] for r in REGIMES])
            slices.append({"axis": axis, "value": value, **estimand_summary(m, mixes)})
    tm = np.array([s["tnoa_partial_identification_width"]["median"] for s in slices])
    bm = np.array([s["binary_partial_identification_width"]["median"] for s in slices])
    ratio = np.divide(tm, bm, out=np.full_like(tm, np.nan), where=bm > 1e-12)
    neg = np.array([s["naive_binary_negative_bias_fraction"] for s in slices])
    notable = [
        s for s in slices
        if (s["axis"] == "pi3" and np.isclose(s["value"], 0.0))
        or (s["axis"] == "pi2" and any(np.isclose(s["value"], v) for v in (0.01, 1.0, 100.0)))
        or (s["axis"] == "pi1" and any(np.isclose(s["value"], v) for v in (0.1, 10.0)))
    ]
    return {
        "simplex_step": 0.1,
        "mixture_count_per_slice": int(len(mixes)),
        "slice_count": len(slices),
        "summary": {
            "tnoa_median_width_across_slices": qstats(tm),
            "binary_median_width_across_slices": qstats(bm),
            "median_width_ratio_where_binary_nonzero": qstats(ratio[np.isfinite(ratio)]),
            "naive_binary_negative_bias_fraction_across_slices": qstats(neg),
            "all_slices_tnoa_never_wider": bool(all(s["tnoa_never_wider"] for s in slices)),
            "all_slices_true_prevalence_covered": bool(all(np.isclose(s["tnoa_true_prevalence_coverage"], 1.0) for s in slices)),
        },
        "notable_slices": notable,
    }


def bounded_opt(values: np.ndarray, counts: np.ndarray, kappa: float, maximize: bool = False) -> float:
    order_values = -values if maximize else values
    lower = counts / kappa
    upper = counts * kappa
    weights = lower.copy()
    remaining = float(np.sum(counts) - np.sum(weights))
    for i in np.argsort(order_values):
        if remaining <= 1e-12:
            break
        add = min(float(upper[i] - weights[i]), remaining)
        weights[i] += add
        remaining -= add
    return float(np.dot(weights, values) / np.sum(weights))


def minimum_overlap_share(rows: list[dict], kappa: float) -> float:
    grouped = Counter(
        (
            round(float(r["undetermined_overlap_or_attribution_rate"]), 12),
            round(float(r["undetermined_total_rate"]), 12),
        )
        for r in rows
    )
    overlap = np.array([k[0] for k in grouped])
    total = np.array([k[1] for k in grouped])
    counts = np.array(list(grouped.values()), dtype=float)
    lo, hi = 0.0, 1.0
    for _ in range(50):
        q = (lo + hi) / 2
        if bounded_opt(overlap - q * total, counts, kappa) >= 0:
            lo = q
        else:
            hi = q
    return float(lo)


def pi2_contrast(rows: list[dict]) -> np.ndarray:
    low, mid, high = 0.31622776601683794, 1.0, 3.1622776601683795
    strata = defaultdict(dict)
    for r in rows:
        p2 = float(r["pi2"])
        if p2 not in {low, mid, high}:
            continue
        key = (r["pi1"], r["pi3"], r["pi4"], r["pi5"], r["pi6"], r["latent_regime"])
        strata[key][p2] = float(r["undetermined_total_rate"])
    return np.array([v[mid] - 0.5 * (v[low] + v[high]) for v in strata.values()])


def pi1_delta_groups(rows: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    levels = sorted({float(r["pi1"]) for r in rows})
    strata = defaultdict(dict)
    for r in rows:
        key = (r["pi2"], r["pi3"], r["pi4"], r["pi5"], r["pi6"], r["latent_regime"])
        strata[key][float(r["pi1"])] = float(r["undetermined_total_rate"])
    grouped = Counter(
        tuple(round(float(x), 12) for x in np.diff([v[p] for p in levels]))
        for v in strata.values()
    )
    return np.array(list(grouped.keys())), np.array(list(grouped.values()), dtype=float)


def monotone_pi1_feasible(delta: np.ndarray, counts: np.ndarray, kappa: float) -> bool:
    total = float(np.sum(counts))
    result = linprog(
        c=np.zeros(len(counts)),
        A_ub=delta.T,
        b_ub=np.zeros(delta.shape[1]),
        A_eq=np.ones((1, len(counts))),
        b_eq=np.array([total]),
        bounds=list(zip(counts / kappa, counts * kappa)),
        method="highs",
    )
    return bool(result.success)


def weighting_sensitivity(rows: list[dict]) -> dict:
    c = pi2_contrast(rows)
    cgroup = Counter(round(float(x), 12) for x in c)
    cv = np.array(list(cgroup.keys()))
    cc = np.array(list(cgroup.values()), dtype=float)
    delta, counts = pi1_delta_groups(rows)
    return {
        "density_ratio_definition": "relative to equal-grid/equal-regime weighting, each row multiplier r satisfies 1/kappa <= r <= kappa and mean(r)=1",
        "kappa_values": KAPPAS,
        "minimum_overlap_share_of_U": {str(k): minimum_overlap_share(rows, k) for k in KAPPAS},
        "pi1_monotone_nonincreasing_U_feasible": {str(k): monotone_pi1_feasible(delta, counts, k) for k in KAPPAS},
        "pi1_transition_interpretation": "false means no allowed common reweighting over Pi2-Pi6/regime strata makes the Pi1 U curve monotone nonincreasing; true is an existence result only",
        "pi2_center_minus_neighbor_mean_U_contrast_range": {
            str(k): {"min": bounded_opt(cv, cc, k), "max": bounded_opt(cv, cc, k, maximize=True)} for k in KAPPAS
        },
        "pi2_contrast_definition": "U(Pi2=1) - mean[U(Pi2=0.316...), U(Pi2=3.162...)]",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase-surface", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    surface, rows = load_surface(args.phase_surface)
    mixes = simplex(10)
    emission = emission_matrix(rows)
    result = {
        "schema": "tnoa-mee-synthetic-consequences-v1",
        "status": "post-freeze derived analysis; no observer retuning",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "coordinate_count": surface["coordinate_count"],
            "row_count": surface["row_count"],
            "world_count": 5880000,
        },
        "estimand": {
            "target": "latent target prevalence across the six registered synthetic regimes",
            "regime_order": REGIMES,
            "target_truth_vector": TARGET.tolist(),
            "outcome_order": ["B", "T", "N", "U"],
            "simplex": {
                "step": 0.1,
                "mixture_count": int(len(mixes)),
                "interpretation": "deterministic composition lattice; summary frequencies are design-space descriptives, not ecological priors",
            },
            "equal_grid_regime_emission_matrix": emission.tolist(),
            "global": estimand_summary(emission, mixes),
            "axis_slice_sensitivity": axis_slice_sensitivity(rows, mixes),
        },
        "weighting_sensitivity": weighting_sensitivity(rows),
        "claim_guards": [
            "No field prevalence, field accuracy, or field absence-certification claim is made.",
            "The ecological estimand analysis uses known synthetic truth and frozen observer emissions.",
            "The B/T/N/U partial-identification result is a downstream information-preservation result, not a new field-calibrated estimator.",
            "Equal-grid pooled rates remain descriptive; robustness claims are limited to the explicit reweighting class or registered axis slices tested here.",
            "Pi1 nonmonotonicity should not be presented as weighting-robust once monotone decrease becomes feasible under moderate reweighting.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
