#!/usr/bin/env python3
"""Build the MEE-priority quantitative figure panels from pinned derived data.

This script does not rerun observers or the synthetic generator. Its only data
input is ``derived/mee_figure_data.json``, which records the immutable source
workflows/artifacts from which each displayed quantity was reduced.
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


def _save(fig: plt.Figure, out_dir: Path, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(out_dir / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(out_dir / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2a_threshold_failure(data: dict, out_dir: Path) -> None:
    d = data["figure2_risk_calibration"]["inherited_threshold_failure"]
    fig, ax = plt.subplots(figsize=(5.6, 4.1))
    labels = ["AUC vs\ntarget only", "AUC vs\ntarget+coupled", "Nuisance recall\nat 0.55"]
    values = [d["auc_nuisance_vs_target_only"], d["auc_nuisance_vs_target_coupled"], d["coherent_nuisance_recall_at_0_55"]]
    ax.bar(labels, values)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Registered diagnostic value")
    ax.set_title("Ranking survived while the inherited threshold lost coverage")
    _save(fig, out_dir, "fig2a_threshold_failure")


def fig2b_score_diagnosis(data: dict, out_dir: Path) -> None:
    rows = data["figure2_risk_calibration"]["diagnosis_by_pi5"]
    x = [r["pi5"] for r in rows]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.plot(x, [r["spatial_pass_at_0_55"] for r in rows], marker="o", label="Spatial component")
    ax.plot(x, [r["temporal_pass_at_0_55"] for r in rows], marker="o", label="Temporal component")
    ax.plot(x, [r["combined_pass_at_0_55"] for r in rows], marker="o", label="Combined nuisance score")
    ax.set_xscale("log")
    ax.set_ylim(0, 0.7)
    ax.set_xlabel(r"Registered $\Pi_5$")
    ax.set_ylabel("Pass rate at inherited threshold 0.55")
    ax.legend(frameon=False)
    ax.set_title("The old numerical threshold was not a stable process boundary")
    _save(fig, out_dir, "fig2b_score_diagnosis")


def fig2c_error_control(data: dict, out_dir: Path) -> None:
    d = data["figure2_risk_calibration"]
    pooled = d["pooled_risk_calibration"]
    family = d["familywise_risk_calibration"]
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    x = [0, 1]
    ax.bar(x, [pooled["coupled_negative_fpr"], family["coupled_negative_fpr"]])
    ax.axhline(pooled["alpha"], linestyle="--", label=r"Prespecified $\alpha=0.05$")
    ax.set_xticks(x, ["Pooled\ncalibration", "Family-conditional\ncalibration"])
    ax.set_ylabel("Held-out false nuisance attribution")
    ax.set_ylim(0, 0.105)
    ax.legend(frameon=False)
    ax.set_title("Family-conditional calibration met the declared criterion")
    _save(fig, out_dir, "fig2c_error_control")


def fig3a_prevalence_bias(data: dict, out_dir: Path) -> None:
    d = data["figure3_estimand"]["quantile_curves"]
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(d["q"], d["naive_bias"], marker="o", markersize=3)
    ax.axhline(0, linestyle="--")
    ax.set_xlabel("Quantile across 3,003 registered regime compositions")
    ax.set_ylabel("Naive binary prevalence bias")
    ax.set_title("Binary coarsening systematically underestimates target prevalence")
    _save(fig, out_dir, "fig3a_prevalence_bias")


def fig3b_identification_width(data: dict, out_dir: Path) -> None:
    d = data["figure3_estimand"]["quantile_curves"]
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(d["q"], d["tnoa_width"], marker="o", markersize=3, label="Retain B/T/N/U")
    ax.plot(d["q"], d["binary_width"], marker="o", markersize=3, label="Binary coarsening")
    ax.set_xlabel("Quantile across 3,003 registered regime compositions")
    ax.set_ylabel("Compatible target-prevalence width")
    ax.set_ylim(0, 0.4)
    ax.legend(frameon=False)
    ax.set_title("Retaining observation states preserves downstream information")
    _save(fig, out_dir, "fig3b_identification_width")


def fig4a_pi1_reasons(data: dict, out_dir: Path) -> None:
    rows = data["figure4_unresolved_reasons"]["pi1"]
    x = [r["pi1"] for r in rows]
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(x, [r["no_support_u"] for r in rows], marker="o", label="No-supported-evidence U")
    ax.plot(x, [r["overlap_u"] for r in rows], marker="o", label="Overlap / attribution U")
    ax.plot(x, [r["total_u"] for r in rows], marker="o", label="Total U")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Pi_1$: observation window / target timescale")
    ax.set_ylabel("Registered design-space rate")
    ax.set_ylim(0, 0.38)
    ax.legend(frameon=False)
    ax.set_title("Longer windows can exchange evidence shortage for attribution conflict")
    _save(fig, out_dir, "fig4a_pi1_reason_substitution")


def fig4b_weighting_robustness(data: dict, out_dir: Path) -> None:
    d = data["figure4_unresolved_reasons"]["bounded_reweighting_min_overlap_share"]
    x = [float(k) for k in d]
    y = [d[k] for k in d]
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(x, y, marker="o")
    ax.axhline(0.5, linestyle="--")
    ax.set_xscale("log")
    ax.set_xlabel(r"Density-ratio bound $\kappa$")
    ax.set_ylabel("Minimum overlap/attribution share of U")
    ax.set_ylim(0.45, 0.95)
    ax.set_title("Overlap/attribution remains the majority U reason under bounded reweighting")
    _save(fig, out_dir, "fig4b_weighting_robustness")


def figs2_axis_separation(data: dict, out_dir: Path) -> None:
    d = data["supplement_axis_separation"]
    axes = ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6"]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.bar([x.upper() for x in axes], [d[x]["max_tv"] for x in axes])
    ax.set_ylabel("Maximum TV between marginal level means")
    ax.set_title("Registered coordinates have uneven effective separation")
    _save(fig, out_dir, "figS2_axis_separation")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, default=ROOT / "figures" / "mee_generated")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data.get("schema") != "tnoa-mee-figure-data-v1":
        raise SystemExit("unexpected MEE figure-data schema")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig2a_threshold_failure(data, args.output_dir)
    fig2b_score_diagnosis(data, args.output_dir)
    fig2c_error_control(data, args.output_dir)
    fig3a_prevalence_bias(data, args.output_dir)
    fig3b_identification_width(data, args.output_dir)
    fig4a_pi1_reasons(data, args.output_dir)
    fig4b_weighting_robustness(data, args.output_dir)
    figs2_axis_separation(data, args.output_dir)

    sidecar = {
        "schema": "tnoa-mee-figure-provenance-v1",
        "source_data": str(DATA.relative_to(ROOT)),
        "source_data_sha256": _sha256(DATA),
        "source_provenance": data["provenance"],
        "panels": [
            "fig2a_threshold_failure", "fig2b_score_diagnosis", "fig2c_error_control",
            "fig3a_prevalence_bias", "fig3b_identification_width",
            "fig4a_pi1_reason_substitution", "fig4b_weighting_robustness",
            "figS2_axis_separation"
        ],
        "claim_boundary": "closed-world paper figures; no field accuracy, prevalence, universal threshold or intrinsic-dimension claim"
    }
    (args.output_dir / "figure_provenance.json").write_text(json.dumps(sidecar, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(sidecar['panels'])} MEE figure panels in {args.output_dir}")


if __name__ == "__main__":
    main()
