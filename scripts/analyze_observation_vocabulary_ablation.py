#!/usr/bin/env python3
"""Post-freeze observation-vocabulary ablation for frozen TNOA V14b.

This analysis is literature-audit motivated and was specified after inspecting
prior results. It is therefore not preregistered evidence. It never reruns or
retunes the frozen observers. The only input is the immutable phase_surface.json
from InsePi workflow 32932634622.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

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
REASON_COLUMNS = [
    "baseline_rate",
    "target_rate",
    "nuisance_rate",
    "undetermined_information_absent_rate",
    "undetermined_overlap_or_attribution_rate",
]
AXES = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6"]
ESTIMANDS = {
    "target_prevalence": np.array([0, 1, 0, 1, 1, 1], dtype=float),
    "nuisance_prevalence": np.array([0, 0, 1, 0, 1, 1], dtype=float),
    "target_nuisance_cooccurrence": np.array([0, 0, 0, 0, 1, 1], dtype=float),
    "coupled_response_prevalence": np.array([0, 0, 0, 1, 0, 1], dtype=float),
    "any_deviation_prevalence": np.array([0, 1, 1, 1, 1, 1], dtype=float),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total - value, parts - 1, prefix + (value,))


def simplex(denominator: int = 10) -> np.ndarray:
    return np.array(list(compositions(denominator, 6)), dtype=float) / denominator


def nullspace(matrix: np.ndarray) -> np.ndarray:
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > 1e-11 * singular_values[0])) if singular_values.size else 0
    return vh[rank:].T


def bounds_for_simplex(
    mixes: np.ndarray,
    emission: np.ndarray,
    observed_columns: list[int],
    estimand: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    constraints = np.vstack([np.ones(6), emission[:, observed_columns].T])
    directions = nullspace(constraints)
    truth = mixes @ estimand
    lower = truth.copy()
    upper = truth.copy()
    dimension = directions.shape[1]
    if dimension == 0:
        return lower, upper

    for active in itertools.combinations(range(6), dimension):
        square = directions[list(active), :]
        if abs(np.linalg.det(square)) < 1e-12:
            continue
        displacement = -mixes[:, list(active)] @ np.linalg.inv(square).T
        candidate = mixes + displacement @ directions.T
        feasible = np.min(candidate, axis=1) >= -1e-9
        if not np.any(feasible):
            continue
        values = candidate @ estimand
        lower[feasible] = np.minimum(lower[feasible], values[feasible])
        upper[feasible] = np.maximum(upper[feasible], values[feasible])
    return np.clip(lower, 0.0, 1.0), np.clip(upper, 0.0, 1.0)


def qstats(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {
        "min": float(np.min(values)),
        "q05": float(np.quantile(values, 0.05)),
        "median": float(np.median(values)),
        "mean": float(np.mean(values)),
        "q95": float(np.quantile(values, 0.95)),
        "max": float(np.max(values)),
    }


def emission_matrix(rows: list[dict]) -> np.ndarray:
    sums = {regime: np.zeros(5) for regime in REGIMES}
    counts: Counter[str] = Counter()
    for row in rows:
        regime = row["latent_regime"]
        sums[regime] += np.array([float(row[column]) for column in REASON_COLUMNS], dtype=float)
        counts[regime] += 1
    return np.vstack([sums[regime] / counts[regime] for regime in REGIMES])


def vocabularies(reason_emission: np.ndarray) -> dict[str, tuple[np.ndarray, list[int]]]:
    return {
        "binary_target_not_target": (reason_emission[:, [1]].copy(), [0]),
        "target_nuisance_other": (
            np.column_stack(
                [
                    reason_emission[:, 1],
                    reason_emission[:, 2],
                    reason_emission[:, 0] + reason_emission[:, 3] + reason_emission[:, 4],
                ]
            ),
            [0, 1],
        ),
        "btnu_collapsed": (
            np.column_stack(
                [
                    reason_emission[:, 0],
                    reason_emission[:, 1],
                    reason_emission[:, 2],
                    reason_emission[:, 3] + reason_emission[:, 4],
                ]
            ),
            [0, 1, 2],
        ),
        "btnu_reason_resolved": (reason_emission.copy(), [0, 1, 2, 3]),
    }


def width_summary(mixes: np.ndarray, reason_emission: np.ndarray, estimand: np.ndarray) -> dict:
    truth = mixes @ estimand
    out: dict[str, dict] = {}
    previous_width: np.ndarray | None = None
    for name, (emission, observed_columns) in vocabularies(reason_emission).items():
        lower, upper = bounds_for_simplex(mixes, emission, observed_columns, estimand)
        width = np.maximum(0.0, upper - lower)
        entry = {
            "identification_width": qstats(width),
            "true_prevalence_coverage": float(
                np.mean((lower - 1e-8 <= truth) & (truth <= upper + 1e-8))
            ),
            "zero_width_fraction": float(np.mean(width <= 1e-9)),
        }
        if previous_width is not None:
            entry["never_wider_than_previous"] = bool(np.all(width <= previous_width + 1e-9))
        previous_width = width
        out[name] = entry
    collapsed = out["btnu_collapsed"]["identification_width"]["median"]
    resolved = out["btnu_reason_resolved"]["identification_width"]["median"]
    out["reason_resolved_relative_median_width_reduction_vs_btnu_collapsed"] = (
        (collapsed - resolved) / collapsed if collapsed > 1e-12 else None
    )
    return out


def axis_slice_summary(rows: list[dict], mixes: np.ndarray) -> dict[str, dict]:
    records: list[tuple[str, float, dict[str, dict]]] = []
    for axis in AXES:
        levels = sorted({float(row[axis]) for row in rows})
        for value in levels:
            subset = [
                row
                for row in rows
                if math.isclose(float(row[axis]), value, rel_tol=0.0, abs_tol=1e-12)
            ]
            emission = emission_matrix(subset)
            records.append(
                (
                    axis,
                    value,
                    {
                        name: width_summary(mixes, emission, estimand)
                        for name, estimand in ESTIMANDS.items()
                    },
                )
            )

    output: dict[str, dict] = {}
    for estimand_name in ESTIMANDS:
        ratios: list[float] = []
        never_wider = 0
        strict = 0
        for _, _, summaries in records:
            collapsed = summaries[estimand_name]["btnu_collapsed"]["identification_width"]["median"]
            resolved = summaries[estimand_name]["btnu_reason_resolved"]["identification_width"]["median"]
            if resolved <= collapsed + 1e-9:
                never_wider += 1
            if resolved < collapsed - 1e-9:
                strict += 1
            if collapsed > 1e-12:
                ratios.append(resolved / collapsed)
        output[estimand_name] = {
            "slice_count": len(records),
            "reason_resolved_never_wider_count": never_wider,
            "strict_median_improvement_count": strict,
            "median_reason_resolved_to_collapsed_width_ratio": float(np.median(ratios)),
            "min_reason_resolved_to_collapsed_width_ratio": float(np.min(ratios)),
            "max_reason_resolved_to_collapsed_width_ratio": float(np.max(ratios)),
        }
    return output


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
    global_emission = emission_matrix(rows)
    global_results = {
        name: width_summary(mixes, global_emission, estimand)
        for name, estimand in ESTIMANDS.items()
    }
    result = {
        "schema": "tnoa-observation-vocabulary-ablation-v1",
        "status": "literature-audit-motivated post-freeze deterministic derivation; no observer retuning; not preregistered",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "coordinate_count": source["coordinate_count"],
            "row_count": len(rows),
            "mixture_count": len(mixes),
        },
        "vocabulary_order": [
            "binary_target_not_target",
            "target_nuisance_other",
            "btnu_collapsed",
            "btnu_reason_resolved",
        ],
        "estimands": global_results,
        "axis_slice_summary": axis_slice_summary(rows, mixes),
        "claim_boundary": "post-freeze descriptive information-loss audit of the frozen synthetic emission matrix; nested never-wider relations are structural; no field prevalence, cross-sensor transfer, or preregistered-result claim",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
