#!/usr/bin/env python3
"""Audit every deterministic coarsening of the frozen B/T/N/U record."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

EXPECTED_SURFACE_SHA256 = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
EXPECTED_ROW_COUNT = 183_750
EXPECTED_COORDINATE_COUNT = 30_625
EXPECTED_WORLD_COUNT = 5_880_000
REGIMES = (
    "baseline",
    "target_only",
    "nuisance_only",
    "target_coupled",
    "target_nuisance_superposed",
    "target_nuisance_coupled",
)
TARGET_TRUTH = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 1.0], dtype=float)
OUTCOME_KEYS = (
    "baseline_rate",
    "target_rate",
    "nuisance_rate",
    "undetermined_total_rate",
)
LABELS = ("B", "T", "N", "U")


def read_surface(path: Path) -> tuple[bytes, dict]:
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            candidates = [name for name in archive.namelist() if name.endswith("phase_surface.json")]
            if len(candidates) != 1:
                raise ValueError(f"expected one phase_surface.json in ZIP; found {candidates}")
            raw = archive.read(candidates[0])
    else:
        raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SURFACE_SHA256:
        raise ValueError(f"phase-surface SHA drifted: {digest}")
    payload = json.loads(raw)
    if len(payload.get("rows", [])) != EXPECTED_ROW_COUNT:
        raise ValueError("phase-surface row count drifted")
    if int(payload.get("coordinate_count", -1)) != EXPECTED_COORDINATE_COUNT:
        raise ValueError("coordinate count drifted")
    if int(payload.get("world_count", -1)) != EXPECTED_WORLD_COUNT:
        raise ValueError("world count drifted")
    return raw, payload


def emission_matrix(rows: Sequence[dict]) -> np.ndarray:
    sums = {regime: np.zeros(4, dtype=float) for regime in REGIMES}
    counts: Counter[str] = Counter()
    for row in rows:
        regime = str(row["latent_regime"])
        if regime not in sums:
            raise ValueError(f"unexpected latent regime: {regime}")
        sums[regime] += np.array([float(row[key]) for key in OUTCOME_KEYS], dtype=float)
        counts[regime] += 1
    matrix = np.vstack([sums[regime] / counts[regime] for regime in REGIMES])
    if not np.allclose(matrix.sum(axis=1), 1.0, atol=1e-10):
        raise ValueError("emission rows do not sum to one")
    return matrix


def integer_compositions(total: int, parts: int, prefix: tuple[int, ...] = ()) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from integer_compositions(total - value, parts - 1, prefix + (value,))


def nullspace(matrix: np.ndarray) -> np.ndarray:
    _, singular, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular > 1e-11 * singular[0])) if singular.size else 0
    return vh[rank:].T


def identification_bounds(mixes: np.ndarray, emission: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    independent = list(range(max(0, emission.shape[1] - 1)))
    constraints = (
        np.vstack([np.ones(len(REGIMES)), emission[:, independent].T])
        if independent
        else np.ones((1, len(REGIMES)))
    )
    null = nullspace(constraints)
    truth = mixes @ TARGET_TRUTH
    lower = truth.copy()
    upper = truth.copy()
    dimension = null.shape[1]
    if dimension == 0:
        return lower, upper
    for active in itertools.combinations(range(len(REGIMES)), dimension):
        square = null[list(active), :]
        if abs(np.linalg.det(square)) < 1e-12:
            continue
        offsets = -mixes[:, list(active)] @ np.linalg.inv(square).T
        candidate = mixes + offsets @ null.T
        feasible = np.min(candidate, axis=1) >= -1e-9
        if not np.any(feasible):
            continue
        values = candidate @ TARGET_TRUTH
        lower[feasible] = np.minimum(lower[feasible], values[feasible])
        upper[feasible] = np.maximum(upper[feasible], values[feasible])
    return np.clip(lower, 0.0, 1.0), np.clip(upper, 0.0, 1.0)


def canonical_partition(blocks: Iterable[Iterable[int]]) -> tuple[tuple[int, ...], ...]:
    normalized = [tuple(sorted(block)) for block in blocks]
    return tuple(sorted(normalized, key=lambda block: (block[0], len(block), block)))


def partitions(items: Sequence[int]) -> Iterable[tuple[tuple[int, ...], ...]]:
    if not items:
        yield ()
        return
    first = items[0]
    for rest in partitions(items[1:]):
        yield canonical_partition(((first,),) + rest)
        for index in range(len(rest)):
            updated = list(rest)
            updated[index] = tuple(sorted(updated[index] + (first,)))
            yield canonical_partition(updated)


def summary(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {
        "min": float(values.min()),
        "q05": float(np.quantile(values, 0.05)),
        "median": float(np.median(values)),
        "mean": float(values.mean()),
        "q95": float(np.quantile(values, 0.95)),
        "max": float(values.max()),
    }


def analyse(surface: Path, simplex_denominator: int = 10) -> dict:
    raw, payload = read_surface(surface)
    emission = emission_matrix(payload["rows"])
    mixes = np.asarray(
        list(integer_compositions(simplex_denominator, len(REGIMES))), dtype=float
    ) / float(simplex_denominator)
    all_partitions = sorted(set(partitions(tuple(range(4)))), key=lambda part: (-len(part), part))
    if len(all_partitions) != 15:
        raise AssertionError(f"expected 15 set partitions, got {len(all_partitions)}")

    results: list[dict] = []
    for partition in all_partitions:
        aggregated = np.column_stack([emission[:, list(block)].sum(axis=1) for block in partition])
        lower, upper = identification_bounds(mixes, aggregated)
        width = np.maximum(0.0, upper - lower)
        name = " | ".join("+".join(LABELS[index] for index in block) for block in partition)
        results.append(
            {
                "partition_indices": partition,
                "name": name,
                "n_states": len(partition),
                "width_array": width,
                "width": summary(width),
                "zero_width_fraction": float(np.mean(width <= 1e-9)),
            }
        )

    full = next(result for result in results if result["n_states"] == 4)
    binary_key = canonical_partition(((1,), (0, 2, 3)))
    binary = next(result for result in results if result["partition_indices"] == binary_key)
    denominator = binary["width_array"] - full["width_array"]
    for result in results:
        result["increase_vs_full"] = summary(result["width_array"] - full["width_array"])
        mask = denominator > 1e-12
        recovery = (binary["width_array"][mask] - result["width_array"][mask]) / denominator[mask]
        result["relative_recovery_from_binary"] = summary(recovery) if np.any(mask) else None

    pairwise: list[dict] = []
    for result in results:
        if result["n_states"] == 3 and sorted(map(len, result["partition_indices"])) == [1, 1, 2]:
            merged = next(block for block in result["partition_indices"] if len(block) == 2)
            pairwise.append(
                {
                    "merge": "+".join(LABELS[index] for index in merged),
                    "name": result["name"],
                    "median_width": result["width"]["median"],
                    "mean_width": result["width"]["mean"],
                    "q95_width": result["width"]["q95"],
                    "median_increase_vs_full": result["increase_vs_full"]["median"],
                    "mean_increase_vs_full": result["increase_vs_full"]["mean"],
                }
            )

    target_plus_one: list[dict] = []
    for keep in (0, 2, 3):
        other = tuple(index for index in range(4) if index not in (1, keep))
        key = canonical_partition(((1,), (keep,), other))
        result = next(item for item in results if item["partition_indices"] == key)
        target_plus_one.append(
            {
                "preserve": LABELS[keep],
                "name": result["name"],
                "width": result["width"],
                "increase_vs_full": result["increase_vs_full"],
                "relative_recovery_from_binary": result["relative_recovery_from_binary"],
            }
        )

    def serializable(result: dict) -> dict:
        return {
            "partition": [[LABELS[index] for index in block] for block in result["partition_indices"]],
            "name": result["name"],
            "n_states": result["n_states"],
            "width": result["width"],
            "increase_vs_full": result["increase_vs_full"],
            "relative_recovery_from_binary": result["relative_recovery_from_binary"],
            "zero_width_fraction": result["zero_width_fraction"],
        }

    return {
        "schema": "tnoa-coarsening-lattice-v1",
        "status": "post_freeze_deterministic_derivation_no_observer_retuning",
        "source": {
            "phase_surface_sha256": hashlib.sha256(raw).hexdigest(),
            "row_count": len(payload["rows"]),
            "coordinate_count": int(payload["coordinate_count"]),
            "world_count": int(payload["world_count"]),
        },
        "regimes": list(REGIMES),
        "outcome_labels": list(LABELS),
        "emission_matrix": {
            regime: [float(value) for value in row]
            for regime, row in zip(REGIMES, emission, strict=True)
        },
        "simplex_step": 1.0 / simplex_denominator,
        "mixture_count": len(mixes),
        "partition_count": len(all_partitions),
        "full": serializable(full),
        "binary_target_vs_rest": serializable(binary),
        "pairwise_merge_losses": sorted(pairwise, key=lambda item: item["merge"]),
        "target_plus_one_non_target_distinction": target_plus_one,
        "partitions": [serializable(result) for result in results],
        "claim_boundary": {
            "field_prevalence_claimed": False,
            "ecological_prior_claimed": False,
            "observer_retuned": False,
            "structural_non_worsening_claim": "deterministic coarsening guarantee",
            "empirical_claim": "magnitude and allocation of identification-width loss in the registered synthetic experiment",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-surface", required=True, type=Path)
    parser.add_argument("--output", default=Path("derived/coarsening_lattice_analysis.json"), type=Path)
    args = parser.parse_args()
    result = analyse(args.phase_surface)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Coarsening lattice complete: {result['partition_count']} partitions, {result['mixture_count']} mixtures")


if __name__ == "__main__":
    main()
