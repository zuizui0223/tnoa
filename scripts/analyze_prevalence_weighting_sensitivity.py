#!/usr/bin/env python3
"""Post-freeze target-prevalence and composition-weight sensitivity for TNOA.

Uses only the immutable V14b phase surface. No observer, threshold, alpha,
latent regime or synthetic world is changed. This analysis was motivated after
review of the original D1/D3 results and is therefore not preregistered.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
WORKFLOW = 32932634622
REGIMES = [
    "baseline", "target_only", "nuisance_only", "target_coupled",
    "target_nuisance_superposed", "target_nuisance_coupled",
]
TARGET = np.array([0, 1, 0, 1, 1, 1], dtype=float)
REASON_COLUMNS = [
    "baseline_rate", "target_rate", "nuisance_rate",
    "undetermined_information_absent_rate",
    "undetermined_overlap_or_attribution_rate",
]
KAPPAS = [1.0, 1.25, 1.5, 1.6, 2.0, 3.0, 5.0, 10.0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total - value, parts - 1, prefix + (value,))


def simplex(denominator: int = 10) -> np.ndarray:
    return np.array(list(compositions(denominator, 6)), dtype=float) / denominator


def nullspace(matrix: np.ndarray) -> np.ndarray:
    _, s, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(s > 1e-11 * s[0])) if s.size else 0
    return vh[rank:].T


def bounds(mixes: np.ndarray, emission: np.ndarray, columns: list[int]) -> tuple[np.ndarray, np.ndarray]:
    constraints = np.vstack([np.ones(6), emission[:, columns].T])
    directions = nullspace(constraints)
    truth = mixes @ TARGET
    lower, upper = truth.copy(), truth.copy()
    dim = directions.shape[1]
    if dim == 0:
        return lower, upper
    for active in itertools.combinations(range(6), dim):
        square = directions[list(active), :]
        if abs(np.linalg.det(square)) < 1e-12:
            continue
        displacement = -mixes[:, list(active)] @ np.linalg.inv(square).T
        candidate = mixes + displacement @ directions.T
        feasible = np.min(candidate, axis=1) >= -1e-9
        values = candidate @ TARGET
        lower[feasible] = np.minimum(lower[feasible], values[feasible])
        upper[feasible] = np.maximum(upper[feasible], values[feasible])
    return np.clip(lower, 0, 1), np.clip(upper, 0, 1)


def emission_matrix(rows: list[dict]) -> np.ndarray:
    sums = {regime: np.zeros(5) for regime in REGIMES}
    counts: Counter[str] = Counter()
    for row in rows:
        regime = row["latent_regime"]
        sums[regime] += np.array([float(row[column]) for column in REASON_COLUMNS])
        counts[regime] += 1
    return np.vstack([sums[regime] / counts[regime] for regime in REGIMES])


def vocabulary_widths(mixes: np.ndarray, reason_emission: np.ndarray) -> dict[str, np.ndarray]:
    vocabs = {
        "binary": (reason_emission[:, [1]], [0]),
        "target_nuisance_other": (
            np.column_stack([
                reason_emission[:, 1], reason_emission[:, 2],
                reason_emission[:, 0] + reason_emission[:, 3] + reason_emission[:, 4],
            ]),
            [0, 1],
        ),
        "btnu": (
            np.column_stack([
                reason_emission[:, 0], reason_emission[:, 1], reason_emission[:, 2],
                reason_emission[:, 3] + reason_emission[:, 4],
            ]),
            [0, 1, 2],
        ),
        "reason_resolved": (reason_emission, [0, 1, 2, 3]),
    }
    out = {}
    for name, (emission, columns) in vocabs.items():
        lower, upper = bounds(mixes, emission, columns)
        out[name] = np.maximum(0, upper - lower)
    return out


def bounded_opt(values: np.ndarray, kappa: float) -> float:
    counts = np.ones(len(values), dtype=float)
    lower = counts / kappa
    upper = counts * kappa
    weights = lower.copy()
    remaining = float(len(values) - np.sum(weights))
    for index in np.argsort(values):
        if remaining <= 1e-12:
            break
        add = min(float(upper[index] - weights[index]), remaining)
        weights[index] += add
        remaining -= add
    return float(np.dot(weights, values) / np.sum(weights))


def minimum_ratio(numerator: np.ndarray, denominator: np.ndarray, kappa: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        q = (lo + hi) / 2
        if bounded_opt(numerator - q * denominator, kappa) >= 0:
            lo = q
        else:
            hi = q
    return float(lo)


def median_or_none(values: np.ndarray) -> float | None:
    finite = values[np.isfinite(values)]
    return float(np.median(finite)) if finite.size else None


def summarize_subset(mask: np.ndarray, widths: dict[str, np.ndarray]) -> dict:
    binary = widths["binary"][mask]
    btnu = widths["btnu"][mask]
    resolved = widths["reason_resolved"][mask]
    rel_btnu = np.divide(binary - btnu, binary, out=np.full_like(binary, np.nan), where=binary > 1e-12)
    rel_resolved = np.divide(btnu - resolved, btnu, out=np.full_like(btnu, np.nan), where=btnu > 1e-12)
    return {
        "count": int(np.sum(mask)),
        "median_width_binary": float(np.median(binary)),
        "median_width_target_nuisance_other": float(np.median(widths["target_nuisance_other"][mask])),
        "median_width_btnu": float(np.median(btnu)),
        "median_width_reason_resolved": float(np.median(resolved)),
        "median_relative_reduction_btnu_vs_binary": median_or_none(rel_btnu),
        "median_relative_reduction_reason_resolved_vs_btnu": median_or_none(rel_resolved),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-surface", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    actual = sha256(args.phase_surface)
    if actual != SURFACE_SHA:
        raise SystemExit(f"locked surface SHA mismatch: {actual}")
    source = json.loads(args.phase_surface.read_text(encoding="utf-8"))
    rows = source.get("rows", [])
    if source.get("coordinate_count") != 30625 or source.get("row_count") != 183750 or len(rows) != 183750:
        raise SystemExit("locked phase-surface dimensions drifted")

    mixes = simplex(10)
    truth = mixes @ TARGET
    widths = vocabulary_widths(mixes, emission_matrix(rows))
    binary, btnu, resolved = widths["binary"], widths["btnu"], widths["reason_resolved"]

    prevalence_strata = {}
    counts = {}
    for theta in np.arange(0, 1.0001, 0.1):
        key = f"{theta:.1f}"
        mask = np.isclose(truth, theta)
        counts[key] = int(np.sum(mask))
        prevalence_strata[key] = summarize_subset(mask, widths)

    rare = {}
    for cutoff in (0.1, 0.2, 0.3):
        mask = truth <= cutoff + 1e-12
        entry = summarize_subset(mask, widths)
        entry["uniform_lattice_mass"] = float(np.mean(mask))
        rare[f"theta_le_{cutoff:.1f}"] = entry

    sensitivity = {}
    for kappa in KAPPAS:
        sensitivity[str(kappa)] = {
            "btnu_vs_binary": minimum_ratio(binary - btnu, binary, kappa),
            "reason_resolved_vs_btnu": minimum_ratio(btnu - resolved, btnu, kappa),
        }

    result = {
        "schema": "tnoa-prevalence-weighting-sensitivity-v1",
        "status": "post-freeze design-sensitivity derivation from immutable V14b; no observer retuning; not preregistered",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "coordinate_count": source["coordinate_count"],
            "row_count": len(rows),
            "mixture_count": len(mixes),
            "simplex_step": 0.1,
        },
        "target_truth_vector": TARGET.tolist(),
        "prevalence_lattice_counts": counts,
        "prevalence_strata": prevalence_strata,
        "rare_target_subsets": rare,
        "composition_density_ratio_sensitivity": {
            "definition": "relative to uniform weighting of the 3,003 simplex compositions, each composition multiplier r satisfies 1/kappa <= r <= kappa and mean(r)=1; reported quantities are worst-case ratios of weighted mean width reductions, not weighted medians",
            "kappa_values": KAPPAS,
            "minimum_fraction_width_removed": sensitivity,
        },
        "claim_boundary": [
            "The simplex lattice remains a sensitivity design, not an ecological prior.",
            "Prevalence-stratified results are descriptive of the frozen emission map and fixed composition lattice.",
            "Composition-level density-ratio results vary composition weights only; they do not alter the observer, emission matrix, or latent regimes.",
            "No field prevalence, field accuracy, annotation-budget efficiency, or universal superiority claim is made.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
