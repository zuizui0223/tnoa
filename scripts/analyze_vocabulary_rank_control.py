#!/usr/bin/env python3
"""Post-freeze vocabulary-rank control for the TNOA D3 observation ablation.

This reviewer-motivated control asks whether the D3 narrowing is specific to
the semantic U-reason split or is largely reproduced by any regime-dependent
refinement that adds an informative observation column.

No observer, threshold, latent regime, synthetic world, or frozen emission is
changed. The only scientific input is the immutable V14b phase_surface.json.
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
RANDOM_SEED = 0
N_RANDOM_SPLITS = 500
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
    rank = (
        int(np.sum(singular_values > 1e-11 * singular_values[0]))
        if singular_values.size
        else 0
    )
    return vh[rank:].T


def bounds_for_simplex(
    mixes: np.ndarray,
    emission: np.ndarray,
    observed_columns: list[int],
    estimand: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int, int]:
    constraints = np.vstack([np.ones(6), emission[:, observed_columns].T])
    directions = nullspace(constraints)
    rank = int(np.linalg.matrix_rank(constraints, tol=1e-11))
    truth = mixes @ estimand
    lower = truth.copy()
    upper = truth.copy()
    dimension = directions.shape[1]
    if dimension == 0:
        return lower, upper, dimension, rank

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
    return np.clip(lower, 0, 1), np.clip(upper, 0, 1), dimension, rank


def qstats(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {
        "min": float(np.min(values)),
        "q05": float(np.quantile(values, 0.05)),
        "q25": float(np.quantile(values, 0.25)),
        "median": float(np.median(values)),
        "mean": float(np.mean(values)),
        "q75": float(np.quantile(values, 0.75)),
        "q95": float(np.quantile(values, 0.95)),
        "max": float(np.max(values)),
    }


def emission_matrix(rows: list[dict]) -> np.ndarray:
    sums = {regime: np.zeros(5) for regime in REGIMES}
    counts: Counter[str] = Counter()
    for row in rows:
        regime = row["latent_regime"]
        sums[regime] += np.array(
            [float(row[column]) for column in REASON_COLUMNS],
            dtype=float,
        )
        counts[regime] += 1
    return np.vstack([sums[regime] / counts[regime] for regime in REGIMES])


def median_width(
    mixes: np.ndarray,
    emission: np.ndarray,
    observed_columns: list[int],
    estimand: np.ndarray,
) -> tuple[float, int, int]:
    lower, upper, dimension, rank = bounds_for_simplex(
        mixes, emission, observed_columns, estimand
    )
    return float(np.median(np.maximum(0.0, upper - lower))), dimension, rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-surface", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    actual = sha256(args.phase_surface)
    if actual != SURFACE_SHA:
        raise SystemExit(f"locked phase-surface SHA mismatch: {actual}")
    source = json.loads(args.phase_surface.read_text(encoding="utf-8"))
    rows = source.get("rows", [])
    if (
        source.get("coordinate_count") != 30625
        or source.get("row_count") != 183750
        or len(rows) != 183750
    ):
        raise SystemExit("locked phase-surface dimensions drifted")

    mixes = simplex(10)
    semantic = emission_matrix(rows)
    generic = np.column_stack(
        [semantic[:, 0], semantic[:, 1], semantic[:, 2], semantic[:, 3] + semantic[:, 4]]
    )
    total_u = generic[:, 3]

    tn_other = np.column_stack(
        [semantic[:, 1], semantic[:, 2], semantic[:, 0] + semantic[:, 3] + semantic[:, 4]]
    )
    ladder = {}
    target = ESTIMANDS["target_prevalence"]
    for name, matrix, observed in (
        ("binary_target_not_target", generic[:, [1]], [0]),
        ("target_nuisance_other", tn_other, [0, 1]),
        ("btnu_collapsed", generic, [0, 1, 2]),
        ("semantic_two_way_u_split", semantic, [0, 1, 2, 3]),
    ):
        width, dim, rank = median_width(mixes, matrix, observed, target)
        ladder[name] = {
            "target_prevalence_median_width": width,
            "constraint_rank": rank,
            "nullspace_dimension": dim,
        }

    constant = np.column_stack([generic[:, :3], 0.5 * total_u, 0.5 * total_u])
    constant_results = {}
    for name, estimand in ESTIMANDS.items():
        width, dim, rank = median_width(mixes, constant, [0, 1, 2, 3], estimand)
        constant_results[name] = {
            "median_width": width,
            "constraint_rank": rank,
            "nullspace_dimension": dim,
        }

    rng = np.random.default_rng(RANDOM_SEED)
    two_way_splits = [rng.random(6) for _ in range(N_RANDOM_SPLITS)]
    random_two_way = {}
    for estimand_name, estimand in ESTIMANDS.items():
        medians = []
        dimensions = []
        ranks = []
        for proportions in two_way_splits:
            matrix = np.column_stack(
                [generic[:, :3], total_u * proportions, total_u * (1.0 - proportions)]
            )
            width, dim, rank = median_width(mixes, matrix, [0, 1, 2, 3], estimand)
            medians.append(width)
            dimensions.append(dim)
            ranks.append(rank)

        semantic_width, semantic_dim, semantic_rank = median_width(
            mixes, semantic, [0, 1, 2, 3], estimand
        )
        medians_array = np.asarray(medians)
        random_two_way[estimand_name] = {
            "semantic_split_median_width": semantic_width,
            "random_split_median_width_distribution": qstats(medians_array),
            "fraction_random_splits_at_or_below_semantic": float(
                np.mean(medians_array <= semantic_width + 1e-15)
            ),
            "semantic_to_random_median_ratio": (
                float(semantic_width / np.median(medians_array))
                if np.median(medians_array) > 1e-15
                else None
            ),
            "all_random_nullspace_dimensions": sorted(set(dimensions)),
            "all_random_constraint_ranks": sorted(set(ranks)),
            "semantic_nullspace_dimension": semantic_dim,
            "semantic_constraint_rank": semantic_rank,
        }

    rng_three = np.random.default_rng(RANDOM_SEED)
    three_way_medians = []
    three_way_dimensions = []
    three_way_ranks = []
    for _ in range(N_RANDOM_SPLITS):
        proportions = rng_three.dirichlet(np.ones(3), size=6)
        matrix = np.column_stack([generic[:, :3], total_u[:, None] * proportions])
        width, dim, rank = median_width(mixes, matrix, [0, 1, 2, 3, 4], target)
        three_way_medians.append(width)
        three_way_dimensions.append(dim)
        three_way_ranks.append(rank)

    result = {
        "schema": "tnoa-vocabulary-rank-control-v1",
        "status": "reviewer-motivated post-freeze random-split control; not preregistered; no observer retuning or new synthetic worlds",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "coordinate_count": source["coordinate_count"],
            "row_count": len(rows),
            "mixture_count": len(mixes),
        },
        "control_design": {
            "random_seed": RANDOM_SEED,
            "random_two_way_split_count": N_RANDOM_SPLITS,
            "random_two_way_definition": "for each split and latent regime draw p~Uniform(0,1), then replace U by U*p and U*(1-p)",
            "constant_split_definition": "replace U by 0.5*U and 0.5*U",
            "random_three_way_split_count": N_RANDOM_SPLITS,
            "random_three_way_definition": "for each split and latent regime draw three proportions from Dirichlet(1,1,1), then partition U accordingly",
        },
        "target_prevalence_rank_ladder": ladder,
        "constant_two_way_split": constant_results,
        "random_two_way_splits": random_two_way,
        "random_three_way_target_prevalence": {
            "median_width_distribution": qstats(np.asarray(three_way_medians)),
            "point_identified_count": int(np.sum(np.asarray(three_way_medians) <= 1e-12)),
            "all_nullspace_dimensions": sorted(set(three_way_dimensions)),
            "all_constraint_ranks": sorted(set(three_way_ranks)),
        },
        "interpretation": "D3 demonstrates that a regime-discriminating refinement can greatly narrow compatible sets in this six-regime frozen design. The random controls show that the magnitude is not specific to the semantic meaning of the two recorded U reasons; rank/identifiability gain is a major mechanism. Semantic utility must therefore be justified independently rather than inferred from D3 width reduction alone.",
        "claim_boundary": [
            "D5 is post-freeze and not preregistered.",
            "The random controls do not invalidate D1 B/T/N/U versus binary coarsening.",
            "No semantic-specific information advantage of the recorded U reasons is claimed.",
            "No claim is made about what would happen after adding unregistered latent regimes.",
            "The V14b two-reason record is not identified with the later reusable API's four U reasons.",
        ],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
