#!/usr/bin/env python3
"""Post-freeze control for semantic specificity of the D3 U split.

The analysis asks whether D3's narrowing is specific to the semantic U reasons,
or follows generically when the same U column is split into additional
regime-discriminating observation columns. It uses no new worlds or retuning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from analyze_observation_vocabulary_ablation import (
    ESTIMANDS,
    REASON_COLUMNS,
    REGIMES,
    bounds_for_simplex,
    emission_matrix,
    simplex,
)

SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
WORKFLOW = 32932634622
SEED = 0
N_SPLITS = 500


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def qstats(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {
        "min": float(values.min()),
        "q05": float(np.quantile(values, 0.05)),
        "q25": float(np.quantile(values, 0.25)),
        "median": float(np.median(values)),
        "q75": float(np.quantile(values, 0.75)),
        "q95": float(np.quantile(values, 0.95)),
        "max": float(values.max()),
        "mean": float(values.mean()),
    }


def median_width(mixes, emission, observed_columns, estimand):
    lower, upper = bounds_for_simplex(mixes, emission, observed_columns, estimand)
    constraints = np.vstack([np.ones(6), emission[:, observed_columns].T])
    rank = int(np.linalg.matrix_rank(constraints))
    return float(np.median(np.maximum(0.0, upper - lower))), 6 - rank, rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-surface", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if sha256(args.phase_surface) != SURFACE_SHA:
        raise SystemExit("locked phase-surface SHA mismatch")
    source = json.loads(args.phase_surface.read_text(encoding="utf-8"))
    rows = source.get("rows", [])
    if source.get("coordinate_count") != 30625 or len(rows) != 183750:
        raise SystemExit("locked phase-surface dimensions drifted")

    mixes = simplex(10)
    semantic = emission_matrix(rows)
    generic = np.column_stack([
        semantic[:, 0], semantic[:, 1], semantic[:, 2],
        semantic[:, 3] + semantic[:, 4],
    ])
    u = generic[:, 3]
    constant = np.column_stack([generic[:, :3], 0.5 * u, 0.5 * u])

    generic_medians = {}
    semantic_medians = {}
    constant_medians = {}
    for name, estimand in ESTIMANDS.items():
        generic_medians[name] = median_width(mixes, generic, [0, 1, 2], estimand)[0]
        semantic_medians[name] = median_width(mixes, semantic, [0, 1, 2, 3], estimand)[0]
        constant_medians[name] = median_width(mixes, constant, [0, 1, 2, 3], estimand)[0]

    rng = np.random.default_rng(SEED)
    random_two = {name: [] for name in ESTIMANDS}
    two_dims = []
    for _ in range(N_SPLITS):
        p = rng.random(6)
        emission = np.column_stack([generic[:, :3], u * p, u * (1.0 - p)])
        for name, estimand in ESTIMANDS.items():
            width, dim, _ = median_width(mixes, emission, [0, 1, 2, 3], estimand)
            random_two[name].append(width)
        two_dims.append(dim)

    rng3 = np.random.default_rng(SEED)
    random_three = {name: [] for name in ESTIMANDS}
    three_dims = []
    three_ranks = []
    for _ in range(N_SPLITS):
        proportions = rng3.dirichlet(np.ones(3), size=6)
        emission = np.column_stack([generic[:, :3], u[:, None] * proportions])
        for name, estimand in ESTIMANDS.items():
            width, dim, rank = median_width(mixes, emission, [0, 1, 2, 3, 4], estimand)
            random_three[name].append(width)
        three_dims.append(dim)
        three_ranks.append(rank)

    target = ESTIMANDS["target_prevalence"]
    binary = generic[:, [1]]
    tn_other = np.column_stack([generic[:, 1], generic[:, 2], generic[:, 0] + generic[:, 3]])
    _, bdim, brank = median_width(mixes, binary, [0], target)
    _, tdim, trank = median_width(mixes, tn_other, [0, 1], target)
    _, gdim, grank = median_width(mixes, generic, [0, 1, 2], target)
    _, sdim, srank = median_width(mixes, semantic, [0, 1, 2, 3], target)

    result = {
        "schema": "tnoa-reason-split-specificity-control-v1",
        "status": "reviewer-motivated post-freeze random-split control; not preregistered; no observer retuning or new synthetic worlds",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "row_count": len(rows),
            "mixture_count": len(mixes),
            "latent_regime_count": len(REGIMES),
        },
        "control_design": {
            "random_seed": SEED,
            "two_way_random_split_count": N_SPLITS,
            "three_way_random_split_count": N_SPLITS,
            "constant_split": "p=0.5 for every latent regime; creates no additional regime discrimination",
            "two_way_split": "for each latent regime independently draw p~Uniform(0,1), then split that regime's generic U emission as U1=pU and U2=(1-p)U; labels carry no semantics",
            "three_way_split": "for each latent regime independently draw proportions~Dirichlet(1,1,1), then split generic U into three unlabeled columns",
            "interpretation": "random controls probe category/rank effects only; they are not ecological alternative reason systems",
        },
        "rank_ladder": {
            "target_not_target": {"constraint_rank": brank, "nullspace_dimension": bdim},
            "target_nuisance_other": {"constraint_rank": trank, "nullspace_dimension": tdim},
            "btnu_generic_u": {"constraint_rank": grank, "nullspace_dimension": gdim},
            "btnu_semantic_two_reason_split": {"constraint_rank": srank, "nullspace_dimension": sdim},
            "random_three_way_u_split": {
                "constraint_rank": 6,
                "nullspace_dimension": 0,
                "full_rank_fraction": float(np.mean(np.asarray(three_ranks) == 6)),
            },
        },
        "estimands": {},
        "claim_boundary": "The semantic U split is informative, but its additional identification gain is not shown to be specific to reason semantics. Random regime-discriminating U splits often yield comparable or greater narrowing because extra non-collinear observation columns reduce latent-mixture degrees of freedom.",
    }

    for name in ESTIMANDS:
        random_values = np.asarray(random_two[name], dtype=float)
        three_values = np.asarray(random_three[name], dtype=float)
        semantic_value = semantic_medians[name]
        random_median = float(np.median(random_values))
        result["estimands"][name] = {
            "generic_u_median_width": generic_medians[name],
            "constant_split_median_width": constant_medians[name],
            "semantic_two_reason_split_median_width": semantic_value,
            "random_two_way_split_median_width_distribution": qstats(random_values),
            "fraction_random_two_way_splits_equal_or_narrower_than_semantic": float(np.mean(random_values <= semantic_value + 1e-12)),
            "semantic_width_divided_by_random_median": semantic_value / random_median if random_median > 0 else None,
            "random_three_way_split_median_width_distribution": qstats(three_values),
            "random_three_way_point_identification_fraction": float(np.mean(three_values <= 1e-12)),
        }

    if set(two_dims) != {1} or set(three_dims) != {0}:
        raise SystemExit("random split rank contract drifted")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
