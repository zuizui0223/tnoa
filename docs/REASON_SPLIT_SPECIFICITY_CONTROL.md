# D5 — random-split control for U-reason specificity

Status: **reviewer-motivated post-freeze control; not preregistered**.

This analysis was added after the D3 vocabulary-ablation result was challenged on a structural-identifiability ground. It does not rerun the generator, add latent regimes, retune observers or change thresholds. It uses the same immutable V14b phase surface and the same 3,003 six-regime simplex mixtures as D1/D3.

## Question

D3 showed that splitting generic U into the frozen V14b reasons `no-supported-evidence` and `overlap-or-attribution` reduced the median target-prevalence identification width from `0.0299207` to `0.0040780`.

That result alone does **not** establish that the narrowing comes from the ecological meaning of those reason labels. Adding a non-collinear observation column can reduce the degrees of freedom of the compatible latent-regime mixture even if the added column has arbitrary labels.

D5 therefore asks:

> Is the semantic two-way U split unusually informative relative to unlabeled regime-dependent U splits with the same number of observation columns?

## Controls

Three controls are deterministic once random seed `0` is fixed.

1. **Constant two-way split.** Every regime's U emission is divided 50:50. This creates another column but no new regime discrimination.
2. **500 random two-way splits.** For each latent regime independently, `p ~ Uniform(0,1)` and generic U is divided into `pU` and `(1-p)U`. The two new columns have no semantics.
3. **500 random three-way splits.** For each regime independently, proportions are drawn from `Dirichlet(1,1,1)` and generic U is divided among three unlabeled columns.

These are rank/category controls, not proposed ecological reason systems.

## Target-prevalence result

| record | median identification width |
| --- | ---: |
| B/T/N/U | `0.0299207` |
| constant 50:50 U split | `0.0299207` |
| 500 random regime-dependent two-way U splits, median | **`0.0050075`** |
| frozen semantic two-reason split | **`0.0040780`** |

Among the 500 random two-way splits, **48.0%** had median target-prevalence width equal to or narrower than the frozen semantic split. The semantic width was `0.814` times the random-split median. Thus the semantic split was informative but not exceptional relative to arbitrary regime-discriminating refinements of the same U column.

The constant split did nothing because its new column was linearly redundant with U. The random regime-dependent splits usually added an independent direction and narrowed the compatible set.

## Five-estimand control

The same conclusion is not specific to target prevalence.

| estimand | semantic median width | random two-way median | fraction random <= semantic |
| --- | ---: | ---: | ---: |
| target prevalence | `0.0040780` | `0.0050075` | `0.480` |
| nuisance prevalence | `0.0126316` | `0.0146017` | `0.488` |
| T+N co-occurrence | `0.0148402` | `0.0172924` | `0.488` |
| coupled-response prevalence | `0.0751011` | `0.0211813` | `0.672` |
| any-deviation prevalence | `0.0018694` | `0.0022955` | `0.480` |

For coupled-response prevalence, the frozen semantic split was actually less informative than the median arbitrary split. D5 therefore provides no basis for claiming a semantic-specific information advantage of the two frozen reason labels. **The D3 refinement gain is therefore not semantic-specific in this frozen experiment.**

## Rank / null-space mechanism

For six latent regimes, the compatible-mixture constraint system had the following dimensions in this frozen design:

| retained record | constraint rank | null-space dimension |
| --- | ---: | ---: |
| target / not-target | 2 | 4 |
| target / nuisance / other | 3 | 3 |
| B/T/N/U | 4 | 2 |
| B/T/N/U with one informative two-way U split | 5 | 1 |
| generic random three-way U split | 6 | 0 |

All 500 random three-way splits were full rank and produced median identification width exactly zero to numerical tolerance for all five estimands.

The precise width is not determined by state count alone: the orientation of the added column relative to the estimand also matters, and some two-way random splits point-identify an estimand while others do not. But the large D3 narrowing is substantially explained by the generic rank/identifiability gain from adding a regime-discriminating observation column.

## Interpretation change for D3

Allowed conclusion:

> In the frozen six-regime design, the recorded two-way U refinement is informative, but comparable narrowing is commonly produced by arbitrary regime-discriminating U refinements. The experiment therefore demonstrates the value of additional non-redundant observation structure, not a semantic-specific advantage of the selected U reasons.

Not supported:

> The no-support versus overlap/attribution semantics themselves explain the additional `86.37%` target-prevalence width reduction.

D3 remains useful as a vocabulary/refinement diagnostic, but it is no longer a primary empirical basis for recommending reason provenance. The primary information-preservation result remains D1: collapsing distinct B/N/U observation-process states into a target/not-target record discards observation structure that cannot be recovered downstream.

## Reproduction

```bash
python scripts/analyze_reason_split_specificity_control.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/reason_split_specificity_control.json
python scripts/validate_reason_split_specificity_control.py
```
