#!/usr/bin/env python3
"""Audit effective axis separation and structural rate composition in frozen V14b.

This script is post-freeze only: it reads the immutable phase_surface.json from
workflow 32932634622 and never reruns or retunes an observer.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

SURFACE_SHA = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"
WORKFLOW = 32932634622
AXES = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6"]
OUT = ["baseline_rate", "target_rate", "nuisance_rate", "undetermined_total_rate"]
TARGET_REGIMES = {
    "target_only",
    "target_coupled",
    "target_nuisance_superposed",
    "target_nuisance_coupled",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_vector(rows: list[dict]) -> np.ndarray:
    return np.mean([[float(r[k]) for k in OUT] for r in rows], axis=0)


def grouped(rows: list[dict], key: str) -> dict[float, list[dict]]:
    out: dict[float, list[dict]] = {}
    for row in rows:
        out.setdefault(float(row[key]), []).append(row)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase-surface", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    actual = sha256(args.phase_surface)
    if actual != SURFACE_SHA:
        raise SystemExit(f"locked surface SHA mismatch: {actual}")
    source = json.loads(args.phase_surface.read_text(encoding="utf-8"))
    rows = source.get("rows", [])
    if len(rows) != 183750:
        raise SystemExit("locked surface row count drifted")

    deviation = [r for r in rows if r["latent_regime"] != "baseline"]
    global_mean = mean_vector(deviation)
    total_var = float(
        np.mean(
            [
                np.sum((np.array([float(r[k]) for k in OUT]) - global_mean) ** 2)
                for r in deviation
            ]
        )
    )

    pi1_rows = []
    previous = None
    for level, subset in sorted(grouped(deviation, "pi1").items()):
        no_support = float(np.mean([r["undetermined_information_absent_rate"] for r in subset]))
        overlap = float(np.mean([r["undetermined_overlap_or_attribution_rate"] for r in subset]))
        total = float(np.mean([r["undetermined_total_rate"] for r in subset]))
        rec = {
            "pi1": level,
            "no_supported_evidence_u": no_support,
            "overlap_attribution_u": overlap,
            "total_u": total,
            "overlap_share_of_u": overlap / total if total else None,
        }
        if previous is not None:
            rec["delta_from_previous"] = {
                "no_supported_evidence_u": no_support - previous["no_supported_evidence_u"],
                "overlap_attribution_u": overlap - previous["overlap_attribution_u"],
                "total_u": total - previous["total_u"],
            }
        pi1_rows.append(rec)
        previous = rec

    axis_separation = {}
    for axis in AXES:
        level_groups = grouped(deviation, axis)
        levels = sorted(level_groups)
        means = np.vstack([mean_vector(level_groups[level]) for level in levels])
        max_tv = -1.0
        max_pair = None
        for i, j in itertools.combinations(range(len(levels)), 2):
            tv = float(0.5 * np.abs(means[i] - means[j]).sum())
            if tv > max_tv:
                max_tv = tv
                max_pair = [levels[i], levels[j]]
        between = float(np.mean(np.sum((means - global_mean) ** 2, axis=1)))
        axis_separation[axis] = {
            "registered_levels": levels,
            "distinct_marginal_decision_vectors_at_1e-10": int(
                np.unique(np.round(means, 10), axis=0).shape[0]
            ),
            "max_total_variation_between_level_mean_decisions": max_tv,
            "max_tv_level_pair": max_pair,
            "marginal_between_level_squared_fraction": between / total_var,
            "level_means": [
                {"level": level, **{name: float(value) for name, value in zip(OUT, vector)}}
                for level, vector in zip(levels, means)
            ],
        }

    target_rows = [r for r in rows if r["latent_regime"] in TARGET_REGIMES]
    fn_by_pi3 = {
        level: float(np.mean([r["forced_binary_false_negative_rate"] for r in subset]))
        for level, subset in sorted(grouped(target_rows, "pi3").items())
    }
    zero_fn = fn_by_pi3[0.0]
    positive_fn = float(np.mean([v for k, v in fn_by_pi3.items() if k > 0]))
    non_target_rows = [r for r in rows if r["latent_regime"] not in TARGET_REGIMES]
    non_target_fp = float(np.mean([r["forced_binary_false_positive_rate"] for r in non_target_rows]))

    result = {
        "schema": "tnoa-structural-axis-audit-v1",
        "status": "post-freeze deterministic audit; no observer retuning",
        "source": {
            "workflow_run_id": WORKFLOW,
            "phase_surface_sha256": SURFACE_SHA,
            "row_count": len(rows),
            "deviation_row_count": len(deviation),
        },
        "pi1_reason_decomposition": {
            "rows": pi1_rows,
            "interpretation": "No-support U peaks at Pi1=1 then declines, while overlap/attribution U continues to rise; total U is dominated by overlap at every registered Pi1 level.",
        },
        "axis_separation": axis_separation,
        "forced_binary_structural_decomposition": {
            "reported_equal_grid_target_present_false_negative_rate": float(
                source["forced_binary_false_negative_rate"]
            ),
            "false_negative_rate_by_pi3": {str(k): v for k, v in fn_by_pi3.items()},
            "equal_grid_identity": "0.2*FN(Pi3=0)+0.8*mean_FN(Pi3>0)",
            "reconstructed_rate": 0.2 * zero_fn + 0.8 * positive_fn,
            "pi3_zero_contribution_to_rate": 0.2 * zero_fn,
            "positive_pi3_contribution_to_rate": 0.8 * positive_fn,
            "non_target_false_positive_rate": non_target_fp,
            "interpretation": "The zero false-positive rate follows the frozen positive-target observer on the registered non-target regimes; the aggregate false-negative rate is strongly design-compositional and must not be presented as a standalone performance estimate.",
        },
        "claim_boundary": "descriptive audit of the frozen synthetic design only; no field performance, natural prevalence, or effective-dimensionality universality claim",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
