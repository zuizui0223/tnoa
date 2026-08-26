#!/usr/bin/env python3
"""Build TNOA Paper-1 quantitative figures from locked InsePi artifacts only.

The script fails closed unless the three authoritative source files match the
Git blob SHA-1 values recorded when the TNOA figure package was defined.  It does
not refit observers, recompute the phase surface, or reinterpret historical
one-shot outputs.

Usage
-----
python scripts/build_paper_figures.py --insepi-root ../insepi

Outputs are written to ``figures/generated`` by default as SVG + PNG plus a
machine-readable provenance sidecar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

INSEPI_SOURCE_COMMIT = "1664a190cec47142e8d14cc5157302a7af18d019"
PHASE_SURFACE_SHA256 = "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34"

SOURCES = {
    "figure_data": {
        "path": "benchmarks/v14b_frozen_ternary_phase_figure_data.json",
        "git_blob_sha1": "4c8c2935e61c9266697da315b40f58ba13e89f2c",
    },
    "surface_result": {
        "path": "benchmarks/v14b_frozen_ternary_phase_surface_result.json",
        "git_blob_sha1": "feffae4c9457a9defd4f5b640cda781409a6b4ed",
    },
    "nuisance_risk": {
        "path": "benchmarks/v14b_nuisance_familywise_risk_result.json",
        "git_blob_sha1": "19b7432d0551e2526750f7f6cfa09d07421d7c11",
    },
}


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _load_locked_json(insepi_root: Path, key: str) -> tuple[dict[str, Any], dict[str, str]]:
    spec = SOURCES[key]
    path = insepi_root / spec["path"]
    if not path.is_file():
        raise SystemExit(f"missing locked InsePi source: {path}")
    raw = path.read_bytes()
    blob = _git_blob_sha1(raw)
    if blob != spec["git_blob_sha1"]:
        raise SystemExit(
            f"locked source mismatch for {spec['path']}: expected Git blob "
            f"{spec['git_blob_sha1']}, got {blob}"
        )
    return json.loads(raw.decode("utf-8")), {
        "path": spec["path"],
        "git_blob_sha1": blob,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def _validate_sources(
    figure_data: dict[str, Any],
    surface: dict[str, Any],
    nuisance: dict[str, Any],
) -> None:
    src = figure_data["source"]
    if src["workflow_run_id"] != 32932634622:
        raise SystemExit("unexpected final phase-surface workflow id")
    if src["phase_surface_sha256"] != PHASE_SURFACE_SHA256:
        raise SystemExit("figure data do not point to the locked phase surface")

    provenance = surface["provenance"]
    if provenance["workflow_run_id"] != 32932634622:
        raise SystemExit("surface result workflow does not match locked workflow")
    if provenance["phase_surface_sha256"] != PHASE_SURFACE_SHA256:
        raise SystemExit("surface result SHA does not match locked phase surface")
    summary = surface["global_summary"]
    if summary["coordinate_count"] != 30625 or summary["world_count"] != 5880000:
        raise SystemExit("final phase-surface dimensions drifted")
    if summary["observer_retuned"] is not False:
        raise SystemExit("final surface unexpectedly reports observer retuning")

    if nuisance["workflow_run_id"] != 32931223272:
        raise SystemExit("unexpected nuisance-risk workflow id")
    if nuisance["alpha"] != 0.05:
        raise SystemExit("nuisance alpha must remain 0.05")
    if nuisance["nuisance_decision_contract_freezable"] is not True:
        raise SystemExit("nuisance decision contract is not the frozen passing result")


def _save(fig: plt.Figure, out_dir: Path, stem: str) -> None:
    fig.savefig(out_dir / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(out_dir / f"{stem}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _fig_u_composition(figure_data: dict[str, Any], out_dir: Path) -> None:
    panel = figure_data["panels"]["pi1_deviation_lines"]
    x = panel["pi1"]

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.plot(x, panel["undetermined_total_rate"], marker="o", label="Total U")
    # Historical source field name is retained in the source JSON, but V14c/TNOA
    # semantics require the paper label below.
    ax.plot(
        x,
        panel["undetermined_information_absent_rate"],
        marker="o",
        label="No-supported-evidence U",
    )
    ax.plot(
        x,
        panel["undetermined_overlap_or_attribution_rate"],
        marker="o",
        label="Overlap / attribution U",
    )
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Pi_1$: observation window / target timescale")
    ax.set_ylabel("Decision-space rate")
    ax.set_ylim(0, 0.4)
    ax.legend(frameon=False)
    ax.set_title("Abstention changes composition as observation length increases")
    fig.tight_layout()
    _save(fig, out_dir, "fig2_u_composition_by_pi1")


def _fig_pi1_pi2_heatmap(figure_data: dict[str, Any], out_dir: Path) -> None:
    panel = figure_data["panels"]["pi1_pi2_deviation"]
    matrix = panel["undetermined_total_rate"]

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    image = ax.imshow(matrix, aspect="auto", origin="lower")
    ax.set_xticks(range(len(panel["pi2"])), [f"{v:g}" for v in panel["pi2"]])
    ax.set_yticks(range(len(panel["pi1"])), [f"{v:g}" for v in panel["pi1"]])
    ax.set_xlabel(r"$\Pi_2$: nuisance / target timescale")
    ax.set_ylabel(r"$\Pi_1$: observation window / target timescale")
    ax.set_title("Total U shows no narrow critical ridge at $\Pi_2=1$")
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("Total U rate")
    fig.tight_layout()
    _save(fig, out_dir, "fig3_pi1_pi2_total_u")


def _fig_pi3_boundary(figure_data: dict[str, Any], out_dir: Path) -> None:
    panel = figure_data["panels"]["pi3_target_truth_lines"]
    x = panel["pi3"]

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.plot(x, panel["target_rate"], marker="o", label="T decision rate")
    ax.plot(x, panel["undetermined_total_rate"], marker="o", label="U rate")
    ax.plot(
        x,
        panel["forced_binary_false_negative_rate"],
        marker="o",
        label="Forced-binary false-negative rate",
    )
    # Symlog retains the structural zero while spacing the positive ratio levels.
    ax.set_xscale("symlog", linthresh=0.05)
    ax.set_xlabel(r"$\Pi_3$: direct target amplitude / nuisance amplitude")
    ax.set_ylabel("Rate among target-present worlds")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False)
    ax.set_title("Structural direct-channel availability dominates the frozen geometry")
    fig.tight_layout()
    _save(fig, out_dir, "fig4_pi3_structural_boundary")


def _fig_nuisance_risk(nuisance: dict[str, Any], out_dir: Path) -> None:
    families = ["target_only", "target_nuisance_coupled"]
    labels = ["Target only", "Target + nuisance + coupling"]
    values = [nuisance["heldout_family_fpr"][family] for family in families]
    alpha = nuisance["alpha"]

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.bar(labels, values)
    ax.axhline(alpha, linestyle="--", label=r"Prefrozen $\alpha=0.05$")
    ax.set_ylabel("Held-out false nuisance attribution rate")
    ax.set_ylim(0, max(0.065, alpha * 1.25))
    ax.legend(frameon=False)
    ax.set_title("Family-wise false-certainty contract")
    fig.tight_layout()
    _save(fig, out_dir, "fig5_familywise_nuisance_risk")


def _write_sidecar(
    out_dir: Path,
    source_meta: dict[str, dict[str, str]],
    surface: dict[str, Any],
    nuisance: dict[str, Any],
) -> None:
    payload = {
        "schema": "tnoa-paper-figure-provenance-v1",
        "paper_generation": "TNOA-P1",
        "insepi_source_commit": INSEPI_SOURCE_COMMIT,
        "locked_phase_surface_sha256": PHASE_SURFACE_SHA256,
        "source_files": source_meta,
        "figures": {
            "fig2_u_composition_by_pi1": {
                "claims": ["C10", "C11"],
                "source_panel": "pi1_deviation_lines",
                "semantic_guard": "historical information-absent field is labeled no-supported-evidence under V14c/TNOA",
            },
            "fig3_pi1_pi2_total_u": {
                "claims": ["C2"],
                "source_panel": "pi1_pi2_deviation",
                "semantic_guard": "descriptive frozen surface; no universal timescale law",
            },
            "fig4_pi3_structural_boundary": {
                "claims": ["C12", "C13"],
                "source_panel": "pi3_target_truth_lines",
                "semantic_guard": "Pi3 zero/positive contrast is a structural synthetic rule result, not a field SNR threshold",
            },
            "fig5_familywise_nuisance_risk": {
                "claims": ["C7"],
                "source": "v14b_nuisance_familywise_risk_result.json",
                "semantic_guard": "closed-world false-certainty calibration only; not a field threshold or field FPR",
            },
        },
        "surface_artifact_digest": surface["provenance"]["artifact_digest"],
        "nuisance_artifact_digest": nuisance["artifact_digest"],
        "claim_boundary": "closed-world paper figures only; no field accuracy, prevalence, or universal threshold claim",
    }
    (out_dir / "figure_provenance.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--insepi-root",
        type=Path,
        required=True,
        help="Path to an InsePi checkout containing the locked benchmark artifacts",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "figures" / "generated",
    )
    args = parser.parse_args()

    source_meta: dict[str, dict[str, str]] = {}
    figure_data, source_meta["figure_data"] = _load_locked_json(args.insepi_root, "figure_data")
    surface, source_meta["surface_result"] = _load_locked_json(args.insepi_root, "surface_result")
    nuisance, source_meta["nuisance_risk"] = _load_locked_json(args.insepi_root, "nuisance_risk")
    _validate_sources(figure_data, surface, nuisance)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    _fig_u_composition(figure_data, args.output_dir)
    _fig_pi1_pi2_heatmap(figure_data, args.output_dir)
    _fig_pi3_boundary(figure_data, args.output_dir)
    _fig_nuisance_risk(nuisance, args.output_dir)
    _write_sidecar(args.output_dir, source_meta, surface, nuisance)

    print(f"Built four locked TNOA figures in {args.output_dir}")


if __name__ == "__main__":
    main()
