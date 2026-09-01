# TNOA Paper-1 reproducibility entry point

TNOA does not rerun locked upstream scientific generations by default. Reproduction is split into six levels.

## Level 1 — validate the paper package

```bash
python scripts/validate_paper_manifest.py
python scripts/validate_mee_synthetic_consequences.py
python scripts/validate_observation_vocabulary_ablation.py
python scripts/validate_prevalence_weighting_sensitivity.py
python scripts/validate_reason_split_specificity_control.py
python scripts/validate_structural_axis_audit.py
python scripts/audit_manuscript_claims.py
```

These guards verify frozen provenance, D1–D5 status, the D5 semantic-specificity correction, the frozen-two-reason/current-four-reason API boundary, and the prohibitions on field accuracy, distribution-free guarantees, arbitrary-weighting robustness and annotation-budget efficiency claims.

## Level 2 — verify authoritative locked sources

Use the exact source commits and artifact identifiers in `paper_manifest.json`. Do not replace a historical one-shot result by a later rerun. The final V14b phase-surface artifact is workflow `32932634622`, artifact `9593775550`; extracted `phase_surface.json` must have SHA-256:

```text
1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34
```

Install the derived-analysis requirements with:

```bash
python -m pip install -r requirements-analysis.txt
```

## Level 3 — D1 downstream estimand / phase-space weighting

```bash
python scripts/analyze_mee_synthetic_consequences.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/mee_synthetic_consequences.json
python scripts/validate_mee_synthetic_consequences.py
```

D1 is the primary downstream information-preservation analysis. It compares B/T/N/U with target/not-target under known synthetic truth. The deterministic never-wider direction is structural; the empirical result is the magnitude and conditions of the width loss.

## Level 4 — D3 observation-vocabulary refinement

```bash
python scripts/analyze_observation_vocabulary_ablation.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/observation_vocabulary_ablation.json
python scripts/validate_observation_vocabulary_ablation.py
```

D3 is literature-audit-motivated, post-freeze and not preregistered. It reports four nested vocabularies, five estimands and 34 registered axis slices. Its final two-way U refinement is a numerical refinement result only. **D3 must be interpreted together with D5; it does not demonstrate a semantic-specific reason-information premium.**

## Level 5 — D4 target-prevalence / composition-weight sensitivity

```bash
python scripts/analyze_prevalence_weighting_sensitivity.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/prevalence_weighting_sensitivity.json
python scripts/validate_prevalence_weighting_sensitivity.py
```

D4 is reviewer-motivated, post-freeze and not preregistered. It directly stress-tests the 3,003 composition lattice. Only `141/3003` compositions have θ≤0.2; in that subset median target-prevalence width is about `0.07410` after binary collapse versus `0.000175` with B/T/N/U. At `kappa=10`, B/T/N/U still removes at least `57.5%` of adversarially weighted mean binary width. These are design sensitivities, not ecological priors.

## Level 6 — D5 random-split semantic-specificity control

```bash
python scripts/analyze_reason_split_specificity_control.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/reason_split_specificity_control.json
python scripts/validate_reason_split_specificity_control.py
```

D5 is reviewer-motivated, post-freeze and not preregistered. With random seed `0` it compares the frozen two-way U split against a redundant constant split, 500 unlabeled regime-dependent two-way splits and 500 unlabeled three-way splits.

For target prevalence:

- generic B/T/N/U median width: `0.0299207`;
- constant 50:50 U split: `0.0299207`;
- random two-way median: `0.0050075`;
- frozen two-reason split: `0.0040780`;
- `48.0%` of random two-way splits are equal to or narrower than the frozen split.

All 500 random three-way splits produce a full-rank six-regime constraint system and point-identify all five estimands to numerical tolerance. The correct conclusion is therefore generic rank/identifiability gain from non-redundant observation columns, **not** semantic-specific superiority of the frozen U-reason labels.

## Frozen reason-vocabulary boundary

The frozen V14b D3/D5 surface contains only two U reason buckets: historical `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`. The later reusable API exposes four U reasons. There is no one-to-one empirical four-reason mapping validated by the frozen surface; see `docs/REUSABLE_IMPLEMENTATION.md`.

## Reproduction and claim boundary

All D1/D3/D4/D5 information analyses condition on the frozen effectively known emission map. They do not establish information per annotation, unit cost or field hour. D3–D5 are usable only with their post-freeze/not-preregistered labels and the D5 semantic-specificity correction intact.

## Required reviewer/submission materials

The package should include the active manuscript/front matter, `paper_manifest.json`, claim-boundary/traceability documents, all D1–D5 derived JSONs and validators, figure scripts/data, prior-art documents, `references.bib`, and exact source commits/artifact digests.

## Current status

The scientific package is assembled with C6/C7 and D1/D4 as the primary evidence, C2 as the preregistered negative result, and D3/D5 as a self-critical supporting refinement control. Remaining pre-upload work is human-facing: author/title-page metadata, visual inspection, publisher-facing word count and the final identity-scanned reviewer ZIP.
