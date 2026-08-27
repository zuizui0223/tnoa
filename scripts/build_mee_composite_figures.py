#!/usr/bin/env python3
"""Assemble submission-ready MEE multi-panel figures from pinned figure data.

Reads only derived/mee_figure_data.json. It does not rerun observers, generators,
or analyses. This removes the need for manual data-geometry editing when assembling
Figures 2--4 and Supplementary Figure S2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "derived" / "mee_figure_data.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _save(fig: plt.Figure, out: Path, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(out / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(out / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _label(ax: plt.Axes, label: str) -> None:
    ax.text(-0.12, 1.06, label, transform=ax.transAxes, fontweight="bold", fontsize=12, va="top")


def figure2(data: dict, out: Path) -> None:
    d = data["figure2_risk_calibration"]
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.3))
    old = d["inherited_threshold_failure"]
    axes[0].bar(
        ["AUC vs\ntarget only", "AUC vs\ntarget+coupled", "Nuisance recall\nat 0.55"],
        [old["auc_nuisance_vs_target_only"], old["auc_nuisance_vs_target_coupled"], old["coherent_nuisance_recall_at_0_55"]],
    )
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("Registered diagnostic value")
    axes[0].set_title("Ranking retained; inherited threshold lost coverage")
    _label(axes[0], "a")

    rows = d["diagnosis_by_pi5"]
    x = [r["pi5"] for r in rows]
    axes[1].plot(x, [r["spatial_pass_at_0_55"] for r in rows], marker="o", label="Spatial")
    axes[1].plot(x, [r["temporal_pass_at_0_55"] for r in rows], marker="o", label="Temporal")
    axes[1].plot(x, [r["combined_pass_at_0_55"] for r in rows], marker="o", label="Combined")
    axes[1].set_xscale("log")
    axes[1].set_ylim(0, 0.7)
    axes[1].set_xlabel(r"Registered $\Pi_5$")
    axes[1].set_ylabel("Pass rate at threshold 0.55")
    axes[1].legend(frameon=False)
    axes[1].set_title("Old score boundary was not representation-stable")
    _label(axes[1], "b")

    pooled = d["pooled_risk_calibration"]
    family = d["familywise_risk_calibration"]
    axes[2].bar([0, 1], [pooled["coupled_negative_fpr"], family["coupled_negative_fpr"]])
    axes[2].axhline(pooled["alpha"], linestyle="--", label=r"Prespecified $\alpha=0.05$")
    axes[2].set_xticks([0, 1], ["Pooled", "Family-wise"])
    axes[2].set_ylabel("Held-out false nuisance attribution")
    axes[2].set_ylim(0, 0.105)
    axes[2].legend(frameon=False)
    axes[2].set_title("Family-wise calibration met the error criterion")
    _label(axes[2], "c")
    _save(fig, out, "Figure2_nuisance_calibration")


def figure3(data: dict, out: Path) -> None:
    d = data["figure3_estimand"]["quantile_curves"]
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3))
    axes[0].plot(d["q"], d["naive_bias"], marker="o", markersize=3)
    axes[0].axhline(0, linestyle="--")
    axes[0].set_xlabel("Quantile across 3,003 regime compositions")
    axes[0].set_ylabel("Naive binary prevalence bias")
    axes[0].set_title("Binary coarsening biases the naive estimand downward")
    _label(axes[0], "a")
    axes[1].plot(d["q"], d["tnoa_width"], marker="o", markersize=3, label="Retain B/T/N/U")
    axes[1].plot(d["q"], d["binary_width"], marker="o", markersize=3, label="Binary coarsening")
    axes[1].set_xlabel("Quantile across 3,003 regime compositions")
    axes[1].set_ylabel("Compatible target-prevalence width")
    axes[1].set_ylim(0, 0.4)
    axes[1].legend(frameon=False)
    axes[1].set_title("Four-state records retain more downstream information")
    _label(axes[1], "b")
    _save(fig, out, "Figure3_downstream_estimand")


def figure4(data: dict, out: Path) -> None:
    d = data["figure4_unresolved_reasons"]
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3))
    rows = d["pi1"]
    x = [r["pi1"] for r in rows]
    axes[0].plot(x, [r["no_support_u"] for r in rows], marker="o", label="No-supported-evidence U")
    axes[0].plot(x, [r["overlap_u"] for r in rows], marker="o", label="Overlap / attribution U")
    axes[0].plot(x, [r["total_u"] for r in rows], marker="o", label="Total U")
    axes[0].set_xscale("log")
    axes[0].set_xlabel(r"$\Pi_1$: observation window / target timescale")
    axes[0].set_ylabel("Registered design-space rate")
    axes[0].set_ylim(0, 0.38)
    axes[0].legend(frameon=False)
    axes[0].set_title("Longer windows shift the reason for unresolved records")
    _label(axes[0], "a")
    weighted = d["bounded_reweighting_min_overlap_share"]
    k = [float(key) for key in weighted]
    axes[1].plot(k, [weighted[key] for key in weighted], marker="o")
    axes[1].axhline(0.5, linestyle="--")
    axes[1].set_xscale("log")
    axes[1].set_xlabel(r"Density-ratio bound $\kappa$")
    axes[1].set_ylabel("Minimum overlap/attribution share of U")
    axes[1].set_ylim(0.45, 0.95)
    axes[1].set_title("Overlap/attribution remains the majority under tested reweighting")
    _label(axes[1], "b")
    _save(fig, out, "Figure4_unresolved_reasons")


def figure_s2(data: dict, out: Path) -> None:
    d = data["supplement_axis_separation"]
    order = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6"]
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    ax.bar([x.upper() for x in order], [d[x]["max_tv"] for x in order])
    ax.set_ylabel("Maximum TV between marginal level means")
    ax.set_title("Registered coordinates have uneven marginal separation")
    _save(fig, out, "FigureS2_axis_separation")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, default=ROOT / "figures" / "mee_composite")
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("schema") != "tnoa-mee-figure-data-v1":
        raise SystemExit("unexpected MEE figure-data schema")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure2(data, args.output_dir)
    figure3(data, args.output_dir)
    figure4(data, args.output_dir)
    figure_s2(data, args.output_dir)
    sidecar = {
        "schema": "tnoa-mee-composite-figure-provenance-v1",
        "source_data": str(DATA.relative_to(ROOT)),
        "source_data_sha256": _sha256(DATA),
        "source_provenance": data["provenance"],
        "outputs": ["Figure2_nuisance_calibration", "Figure3_downstream_estimand", "Figure4_unresolved_reasons", "FigureS2_axis_separation"],
        "layout_only": True,
        "manual_data_geometry_editing_required": False,
        "claim_boundary": "closed-world paper figures; no field accuracy, prevalence, universal threshold or intrinsic-dimension claim",
    }
    (args.output_dir / "composite_figure_provenance.json").write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(sidecar['outputs'])} MEE composite figures in {args.output_dir}")


if __name__ == "__main__":
    main()
