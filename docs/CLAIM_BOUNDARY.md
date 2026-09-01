# TNOA claim boundary

This file is the hard manuscript guardrail for Paper 1. The paper is a closed-world methods study. Later field implementation may validate, revise or reject individual evidence adapters without changing these boundaries retroactively.

## A. Claims currently supportable

### A1. Observation architecture

TNOA separates positive target support, positive nuisance support, measurement observability, attribution-gated coupled response and optional independently supported absence. T and N are non-complementary and may coexist. Low target support is not biological absence.

### A2. C6 -> C7 threshold/calibration result

The frozen development history supports the following methodological result:

- nuisance ranking remained useful after the score representation changed;
- the inherited raw threshold `0.55` lost its registered operating meaning;
- pooled calibration failed one predeclared negative-family criterion;
- max-over-predeclared-families calibration produced held-out false nuisance attribution `0/43,200` and `1,920/43,200 = 0.04444`, both within `alpha=0.05`.

Use **predeclared family-conditional false-attribution criterion**, not classical family-wise error-rate control. These are closed-world empirical rates, not a distribution-free finite-sample guarantee and not field FPRs.

### A3. D1 core downstream information-loss result

Using known synthetic truth and the frozen six-regime emission map, Paper 1 may compare target-prevalence partial-identification sets after retaining B/T/N/U versus deterministic target/not-target coarsening.

The never-wider direction is structural: the binary record is a deterministic garbling of B/T/N/U. It is not a performance discovery. The empirical result is the **magnitude and design dependence** of the information loss. The registered global median widths are approximately `0.0299207` for B/T/N/U and `0.2656306` for binary collapse. The deliberately naive target-fraction bias remains a secondary comparator only.

### A4. D4 prevalence/composition-weight sensitivity

D4 is reviewer-motivated, post-freeze and not preregistered. It may support the core D1 result within its explicit design class:

- only `141/3003 = 4.70%` of the 0.1-step simplex compositions have target prevalence `<=0.2`;
- in that subset, median target-prevalence width is `0.07410` after binary collapse versus `0.000175` with B/T/N/U;
- under `kappa=10` bounded adversarial composition weighting, B/T/N/U still removes at least `57.5%` of weighted-mean binary width.

This is not an ecological prior and not arbitrary-distribution robustness.

### A5. C2 negative result

The preregistered narrow ambiguity-ridge prediction near `Pi2 ~= 1` was not supported and was retired without changing the generator to rescue it.

### A6. U composition and Pi1 reason substitution

Within the frozen V14b semantics, no-supported-evidence U and the combined overlap/attribution U bucket may be reported. Overlap/attribution remains a majority of U through the tested row-level bounded reweighting class to `kappa=10`. The Pi1 result is a secondary reason-substitution illustration: after `Pi1=1`, no-support decreases while the combined overlap/attribution bucket continues to increase. Do not headline generic non-monotonicity.

### A7. Structural/design diagnostics

The six registered coordinates are not six equally effective ecological dimensions. Pi3 is effectively zero-versus-positive in the frozen observer; Pi4/Pi5 are weak marginal separators. C13 `0.3569 = 0.2*1.0 + 0.8*0.196125` is a design-compositional comparator diagnostic, not performance.

## B. D3/D5: refinement is informative; semantic specificity is not demonstrated

### B1. D3 numerical refinement result

D3 is literature-audit-motivated, post-freeze and not preregistered. It may report the numerical nested-vocabulary widths, including target prevalence

`0.2656306 -> 0.1886143 -> 0.0299207 -> 0.0040780`.

The final step is the frozen V14b two-way U split (`no-supported-evidence` versus the aggregate `overlap-or-attribution`). Deterministic never-wider relations are structural.

### B2. D5 random-split specificity control

D5 is reviewer-motivated, post-freeze and not preregistered. It is required whenever D3's final split is interpreted.

For target prevalence:

- generic B/T/N/U median width: `0.0299207`;
- constant 50:50 U split: `0.0299207`;
- median of 500 unlabeled regime-dependent two-way random splits: `0.0050075`;
- frozen two-reason split: `0.0040780`;
- `48.0%` of random two-way splits are equal to or narrower than the frozen split.

Across the five estimands, the random-equal-or-better fraction ranges `0.480`–`0.672`. All 500 unlabeled three-way random U splits are full rank for the six-regime constraint system and point-identify all five estimands to numerical tolerance.

### B3. Correct D3/D5 interpretation

Allowed:

> The frozen two-way U split is informative, but comparable narrowing is commonly produced by arbitrary regime-discriminating U refinements. The current experiment therefore demonstrates the value of additional non-redundant observation structure, not a semantic-specific information advantage of the selected U reasons.

Also allowed:

> The large D3 refinement effect is substantially explained by rank/identifiability gain as non-collinear observation columns are added; exact width still depends on column orientation relative to the estimand.

Not allowed:

- the selected reason meanings explain the `86.37%` reduction;
- D3 demonstrates an information premium for reason semantics;
- more categories are always scientifically better;
- state count alone determines the exact width;
- the frozen six-regime result predicts the effect size for a larger/different latent-regime set.

D3/D5 are supporting diagnostics, not primary evidence. The core information-preservation claim remains D1 B/T/N/U versus binary collapse.

## C. Frozen two-reason surface versus reusable four-reason API

The frozen V14b source contains only two unresolved reason buckets:

1. historical `INFORMATION_ABSENT`, reported conservatively as no-supported-evidence;
2. `OVERLAP_OR_ATTRIBUTION`.

The frozen decision code places both simultaneous T+N support and unresolved indirect-only attribution into `OVERLAP_OR_ATTRIBUTION`.

The later reusable API exposes four U reasons:

- `no_supported_evidence`;
- `target_nuisance_overlap`;
- `missing_attribution`;
- `insufficient_observability`.

There is **no one-to-one empirical four-way mapping validated by D3**. Overlap and missing attribution cannot be separated from the frozen aggregate reason-rate column, and insufficient observability has no separate frozen D3 column. The API vocabulary is a later implementation contract whose reason semantics require independent deployment-specific validation.

## D. Weighting and annotation boundaries

Any robustness statement must be tied to the explicit class tested. Row-level phase-space reweighting, composition-level simplex reweighting and registered axis slices are distinct sensitivity analyses.

All D1/D3/D4/D5 information comparisons condition on a frozen, effectively known emission map. Paper 1 does not compare information per annotation, per unit cost or per field hour. Under finite calibration data, uncertainty in a richer emission map could offset some of the identification gain. A fixed-budget comparison requires a new measurement-design specification and is outside Paper 1.

## E. Field/generalization boundaries

Paper 1 does not claim:

- field flower-visitor detection accuracy or nuisance rates;
- field target prevalence, abundance or visitation-rate accuracy;
- biological absence certification without independently validated A−;
- pollination effectiveness;
- universal raw thresholds, alpha, Pi3 laws or optimal abstention;
- numerical transfer of the synthetic emission matrix to another camera/site/taxon;
- validation across camera, acoustic or interaction-monitoring domains;
- distribution-free risk control;
- systematic-review completeness or historical priority for abstention, uncertain events, multilabel prediction, continuous-score inference, Blackwell ordering or partial identification.

The field translation pathway is an implementation template, not a Paper-1 empirical result.

## F. Terminology guardrails

Use:

- `target-supported`, not `target-present`, unless truth is known;
- `nuisance-supported`, not generic `noise`, for formal N;
- `no-supported-evidence`, not `information absent`, for manuscript interpretation of the historical source label;
- `predeclared family-conditional false-attribution criterion`, not `family-wise error control`;
- `registered six-coordinate design`, not `six-dimensional ecological complexity`;
- `synthetic target-prevalence estimand`, not `field visit rate`;
- `frozen two-way U split` or `D3 refinement`, not `semantic information premium`;
- `D5 random-split specificity control`, not an ecological alternative-reason experiment;
- `bounded reweighting sensitivity`, not `prior robustness`;
- `design-compositional comparator rate`, not classifier performance.

Paper 1 must remain scientifically valid if later field validation or finer reason calibration is null or adverse.
