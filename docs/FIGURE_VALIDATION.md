# TNOA Paper-1 figure validation

Status: **initial paper-grade quantitative figure package rendered and visually audited**.

This note records the validation of the quantitative figure builder without changing any scientific result.

## Authoritative source lock

All quantitative panels are defined against InsePi commit:

- `1664a190cec47142e8d14cc5157302a7af18d019`

The builder refuses source files whose Git blob SHA-1 differs from the following authoritative values:

- `benchmarks/v14b_frozen_ternary_phase_figure_data.json`
  - Git blob SHA-1: `4c8c2935e61c9266697da315b40f58ba13e89f2c`
- `benchmarks/v14b_frozen_ternary_phase_surface_result.json`
  - Git blob SHA-1: `feffae4c9457a9defd4f5b640cda781409a6b4ed`
- `benchmarks/v14b_nuisance_familywise_risk_result.json`
  - Git blob SHA-1: `19b7432d0551e2526750f7f6cfa09d07421d7c11`

The three SHA values above were independently re-read from GitHub at the pinned source commit during the figure audit.

The phase-surface SHA retained by both the source result and figure-data artifact is:

- `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`

## Rendered quantitative figures

### Figure 2 — U composition by Pi1

Stem: `fig2_u_composition_by_pi1`

Visual audit:

- total U, no-supported-evidence U and overlap/attribution U are distinguishable;
- log Pi1 axis is appropriate for the registered dimensionless levels;
- the historical source variable `undetermined_information_absent_rate` is not exposed under that overstrong name; the TNOA/V14c label is `No-supported-evidence U`;
- the plot supports only the registered closed-world statement that longer observation does not monotonically remove total U.

Status: **accepted for initial manuscript assembly**.

### Figure 3 — Pi1 x Pi2 total-U surface

Stem: `fig3_pi1_pi2_total_u`

Visual audit:

- all 5 registered Pi1 levels and 7 registered Pi2 levels are displayed;
- the shallow/broad structure around Pi2=1 is visible without implying a narrow critical ridge;
- the color scale is descriptive and does not introduce a new threshold.

Status: **accepted for initial manuscript assembly**.

### Figure 4 — structural Pi3 boundary

Stem: `fig4_pi3_structural_boundary`

Initial audit found one presentation defect: a symlog x-axis made the registered zero and positive Pi3 levels visually awkward and could suggest a continuous field-SNR interpretation.

Correction:

- plot the five **registered Pi3 levels as equal-spaced categories**;
- retain their actual values as tick labels: `0`, `0.1`, `0.316228`, `1`, `3.16228`;
- label the axis explicitly as registered Pi3 levels.

This makes the intended claim visually explicit: the result is a structural `Pi3=0` versus `Pi3>0` contrast under the frozen synthetic rule, not a universal continuous ecological SNR law.

Status after correction: **accepted for initial manuscript assembly**.

### Figure 5 — family-wise false-certainty contract

Stem: `fig5_familywise_nuisance_risk`

Visual audit:

- target-only false nuisance attribution is shown at 0;
- target+nuisance+coupling false attribution is shown at `0.044444...`;
- the prefrozen `alpha=0.05` line is visible;
- no field threshold or field-FPR interpretation is encoded.

Status: **accepted for initial manuscript assembly**.

## What this validation does not mean

This validation does **not**:

- rerun the 5.88M-world scientific generation;
- alter any observer or decision rule;
- re-estimate a phase surface;
- validate field accuracy;
- certify target absence;
- convert the synthetic Pi3 result into a field SNR law;
- claim the present typography is the final publisher-specific layout.

## Canonical regeneration

With an InsePi checkout at the pinned source commit:

```bash
python -m pip install -r requirements-figures.txt
python scripts/build_paper_figures.py --insepi-root ../insepi
```

The builder generates SVG + 300-dpi PNG and `figure_provenance.json`.

The vector/data geometry should not be manually edited after generation. Publisher-specific typography changes should be reproduced in code where practical.
