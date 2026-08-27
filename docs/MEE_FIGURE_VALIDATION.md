# MEE figure validation

The MEE-priority figures use one pinned numerical source, `derived/mee_figure_data.json`. `scripts/build_mee_figures.py` renders the audit-friendly component panels; `scripts/build_mee_composite_figures.py` assembles submission-facing Figure 2, Figure 3, Figure 4 and Supplementary Figure S2 from those same values. The figure-data file is a deterministic reduction of immutable or locked sources; no observer is refit and no threshold is selected during plotting.

## Figure 2 provenance: threshold failure -> diagnosis -> family-wise error control

- inherited-threshold failure: InsePi workflow `32929245729`, artifact `9592634107`, artifact digest `sha256:92b6c1588ac94fdec11c2da2b3fc345aa7c143545bbbe286495b116cafa25253`, result SHA-256 `c3f3ba3c036b8b3a0c337edb6f5a89548c9375b1b1b39bfeab19916506444853`;
- score-distribution diagnosis: workflow `32929754709`, artifact `9592803036`, digest `sha256:990adc30a779d893c0ec072b6264111083e0339c27d726b7c23a8ae0b15f6cdb`, result SHA-256 `7310178cf064fe1d06cf2564adf3b7e6b3df57b4ce446fd8b23fb48aff4ff6ee`;
- pooled risk calibration failure: workflow `32930855374`, artifact `9593167283`, digest `sha256:5fb01ef0a7d0952d8686f08b73f5aed8ac71673ff509098afb67720989e03d2b`, result SHA-256 `56b95a8f2ff819a73fca96e9c1268e6bfb26666dc24897e73a25c82a6fc02367`;
- family-wise risk freeze: workflow `32931223272`, artifact `9593286927`, digest `sha256:46777528229e45d01bea5195bdb271e7e764c87a16f378e25f2c4517cc928044`, result SHA-256 `e5f0fac6f0b5790192be46f923572e5f3f57b1913325d435a2f9f6320fb57617`.

The key plot sequence is fixed: AUC remained 1.0 while inherited-threshold nuisance recall was 0.23125; pooled alpha calibration produced coupled-negative FPR 0.08889 and failed the 0.05 criterion; family-wise calibration produced 0.04444 and passed.

## Figures 3-4 provenance

The downstream estimand, weighting and Pi1/axis summaries derive from the immutable V14b surface:

- workflow `32932634622`;
- artifact `9593775550`;
- artifact digest `sha256:66122ad367fc4f5334b4f4fa8756c9512f205ba4a1e18df3d1ac87a6176135fa`;
- phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`.

`derived/mee_synthetic_consequences.json` and `derived/structural_axis_audit.json` retain the full post-freeze analytical summaries. `derived/mee_figure_data.json` stores only the reduced values needed to reproduce the manuscript figures.

## Validation layers

`python scripts/validate_mee_figure_data.py` fails closed if the primary numerical sequence or provenance drifts. It cross-checks the estimand quantiles and summaries against `derived/mee_synthetic_consequences.json`, the Pi1/axis/C13 values against `derived/structural_axis_audit.json`, and workflow/artifact/result identifiers against `paper_manifest.json`.

`python scripts/build_mee_figures.py` generates eight component panels as SVG and 300-dpi PNG. These are the audit/reproduction layer and remain useful even if journal layout changes.

`python scripts/build_mee_composite_figures.py` generates four submission-facing composite figures from the same pinned JSON:

- `Figure2_nuisance_calibration` — three panels;
- `Figure3_downstream_estimand` — two panels;
- `Figure4_unresolved_reasons` — two panels;
- `FigureS2_axis_separation` — one panel.

Each is emitted as SVG and 300-dpi PNG together with `composite_figure_provenance.json`. The composite sidecar explicitly records `layout_only=true` and `manual_data_geometry_editing_required=false`. CI smoke-builds and uploads these outputs for short-retention visual inspection.

## Visual interpretation guard

The following are not permitted as visual headlines:

- 5.88M worlds as evidence magnitude;
- C13 0.3569 or zero target false positives as classifier performance;
- Pi3 positive magnitude as a continuous effect in the frozen generation;
- the exact Pi1 total-U curve as a weighting-robust law.

The intended hierarchy is Figure 2 risk-calibration evidence, Figure 3 downstream ecological-estimand information preservation, Figure 4 unresolved-reason structure, then design/falsification diagnostics in the supplement.

## Final human-only visual check

Before upload, inspect the code-assembled composite SVG/PNG files for typography, panel-label placement, line/legend overlap and journal sizing. Any correction must remain a reproducible layout/code change; do not manually alter plotted data geometry in a graphics editor.
