# MEE synthetic ecological consequence and weighting audit

## Status

This document synthesizes post-freeze derived analyses of the immutable V14b phase surface. None of D1–D5 reruns the generator, retunes either observer, changes a threshold, or replaces the locked V14b/V14c result.

Authoritative frozen source:

- workflow `32932634622`;
- phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`;
- 30,625 coordinates;
- 183,750 coordinate × latent-regime rows;
- 5,880,000 synthetic worlds.

The relevant post-freeze analyses are D1 (`mee_synthetic_consequences`), D3 (`observation_vocabulary_ablation`), D4 (`prevalence_weighting_sensitivity`) and D5 (`reason_split_specificity_control`). D3–D5 are explicitly not preregistered.

## 1. Core downstream ecological estimand: D1

### Question

> If the ecological estimand is known latent target prevalence, how much identifying information is lost when B/T/N/U is collapsed to target/not-target?

Target truth for the six frozen regimes is

```text
baseline                    0
target_only                 1
nuisance_only               0
target_coupled              1
target_nuisance_superposed  1
target_nuisance_coupled     1
```

We enumerate the six-regime prevalence simplex on a deterministic 0.1 lattice, yielding 3,003 compositions. This lattice is a design-space device, not an ecological prior.

For each composition, the frozen emission matrix gives the expected B/T/N/U record. We compare (i) a deliberately naive TARGET-fraction point comparator, (ii) partial identification after binary target/not-target coarsening and (iii) partial identification with B/T/N/U retained.

Because binary target/not-target is a deterministic garbling of B/T/N/U, the richer record cannot have a wider compatible set. That direction is structural, not a TNOA performance discovery. The empirical result is the magnitude of the loss in this frozen observation process.

Across the 3,003 compositions:

- median binary identification width = **0.2656**;
- median B/T/N/U identification width = **0.0299**;
- median relative width reduction among non-zero binary widths = **84.45%**;
- the known synthetic truth remains covered by the compatible set for every composition;
- the naive TARGET-fraction comparator is negatively biased in **99.63%** of compositions with median bias about **-0.2377**, retained only as a secondary diagnostic.

The same calculation was repeated over all 34 registered single-axis slices. The never-wider relation holds in every slice, while the size of the gain varies substantially. At the extreme `Pi2=0.01` and `Pi2=100` slices the binary emission nearly identifies prevalence already; at `Pi3=0` both encodings remain weak (median B/T/N/U width about 0.897 versus binary 1.0).

The central D1 claim is therefore:

> **Premature binary coarsening can discard substantial downstream ecological identifying information when B, N and U represent distinct observation-process outcomes.**

This is a closed-world known-emission result, not a field prevalence estimator.

## 2. Target-prevalence and composition-weight sensitivity: D4

The 3,003-point simplex is highly non-uniform in target prevalence. Only `141/3003 = 4.70%` of compositions have known target prevalence `<=0.2`, so a global median gives little weight to rare-target conditions.

D4 therefore stratifies the same compositions by known target prevalence and separately reweights the composition lattice with a bounded density-ratio class.

For `theta<=0.2`, median target-prevalence widths are:

- target/not-target: **0.07410**;
- target/nuisance/other: **0.07386**;
- B/T/N/U: **0.000175**.

Thus the core D1 B/T/N/U-versus-binary advantage does not disappear in the rare-target part of this frozen simplex.

For direct composition reweighting, each multiplier satisfies `1/kappa <= r_i <= kappa` and mean `r_i=1`. At `kappa=10`, an adversarial weighting cannot reduce the weighted-mean fraction of binary width removed by B/T/N/U below approximately **0.575**. These are worst-case weighted-mean ratios within the stated class, not ecological priors or arbitrary-distribution guarantees.

D4 is reviewer-motivated, post-freeze and not preregistered. Its role is to qualify the design dependence of D1, not to establish natural prevalence weighting.

## 3. D3 vocabulary refinement requires the D5 specificity control

D3 compared four nested observation vocabularies:

1. TARGET / not-TARGET;
2. TARGET / NUISANCE / other;
3. B / T / N / U;
4. B / T / N / U with the frozen U bucket split into no-supported-evidence versus overlap/attribution.

For target prevalence, the median widths were `0.2656`, `0.1886`, `0.02992` and `0.00408`. For T+N co-occurrence they were `0.7231`, `0.5136`, `0.10494` and `0.01484`.

Those numbers are reproducible, but **they do not by themselves establish that the semantic meanings of the two frozen U labels caused the additional narrowing**. Any non-redundant regime-dependent observation column can reduce the dimension of the compatible latent-mixture set.

D5 directly tests this issue while keeping the same frozen emission matrix and 3,003 compositions.

For target prevalence:

- generic B/T/N/U median width: `0.0299207`;
- constant 50:50 split of U: `0.0299207` (no gain; redundant column);
- 500 unlabeled regime-dependent random two-way U splits: median `0.0050075`;
- frozen two-reason split: `0.0040780`;
- **48.0%** of random two-way splits are equal to or narrower than the frozen semantic split.

Across all five reported estimands, the fraction of random two-way splits equal to or better than the frozen split ranges from `0.480` to `0.672`.

The rank/null-space ladder for the six latent regimes is:

| observation record | null-space dimension |
| --- | ---: |
| target / not-target | 4 |
| target / nuisance / other | 3 |
| B / T / N / U | 2 |
| B / T / N / split-U | 1 |
| B / T / N / three-way-split-U | 0 |

All 500 random three-way U splits in D5 are full rank and point-identify all five estimands to numerical tolerance. The exact width at a fixed rank still depends on the orientation of the added column, so state count/rank does not determine every numeric width by itself.

The correct D3/D5 interpretation is therefore:

> **Additional non-redundant observation structure can sharply narrow compatible latent mixtures in this six-regime design, but the present experiment does not isolate a semantic-specific information advantage of the selected U-reason labels.**

D3/D5 are supporting self-critical diagnostics, not a primary reason-semantics performance claim.

## 4. Frozen two-reason surface versus reusable four-reason API

The frozen V14b decision surface contains only two U reason buckets: historical `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`. Source code shows that the latter combines simultaneous T+N support and unresolved indirect-only attribution.

The later reusable API exposes four U reasons: no-supported-evidence, target+nuisance overlap, missing attribution and insufficient observability. `insufficient_observability` has no separate frozen D3 column. Therefore the frozen D3/D5 analysis does **not** empirically validate a one-to-one four-reason API decomposition.

The four-reason API remains a process-semantic implementation contract whose individual reason channels require domain-specific calibration/validation.

## 5. Phase-space/equal-grid weighting sensitivity

A separate D1 audit reweights the frozen coordinate × regime rows, not the 3,003 latent-mixture compositions. With `1/kappa <= r <= kappa` and mean `r=1`:

- overlap/attribution remains more than half of U through the tested `kappa=10` class;
- the exact Pi1 total-U curve is not robust enough to headline as a general non-monotonic law (a monotone non-increasing curve becomes feasible by about `kappa=1.6`);
- the small pooled Pi2=1 centre contrast can change sign by `kappa=1.25`, reinforcing the preregistered negative ridge result.

These analyses constrain the interpretation of the frozen design; they do not define an ecological prior.

## 6. Final result hierarchy for MEE

1. **C6 -> C7 — primary operational calibration result.** Nuisance ranking survived a representation change while the inherited raw threshold lost its operating meaning; a predeclared family-conditional false-attribution criterion recovered the declared held-out semantics.
2. **D1 + D4 — primary downstream information result.** B/T/N/U versus binary coarsening shows large known-truth information loss, with explicit prevalence and composition-weight sensitivity.
3. **C2 — preregistered negative result.** The narrow matched-timescale ambiguity ridge was not supported.
4. **D3 + D5 — supporting self-critical refinement diagnostic.** Finer non-redundant columns can narrow identification, but the selected frozen reason semantics do not show an isolated information premium.
5. **C10/C11/D2 — secondary mechanism/design interpretation.** Pi1 reason substitution, U composition and uneven effective axis separation remain conditional/descriptive.
6. **C13/Pi3/world count — design/provenance diagnostics, not performance evidence.**

## 7. Claim boundary

Allowed:

- D1 B/T/N/U-versus-binary partial-identification magnitude;
- D4 prevalence-stratified and bounded composition-weight sensitivity;
- D3 numerical refinement values when interpreted with D5;
- D5 random-split and rank/null-space controls;
- phase-space row reweighting and registered axis-slice sensitivity.

Not supported:

- a semantic-specific information premium for the two frozen U reason labels;
- empirical validation of the later four-reason API by D3/D5;
- field visit prevalence, abundance or detection accuracy;
- biological absence certification;
- numerical transfer of the frozen emission matrix to another system;
- universal superiority of four-state TNOA over every calibrated binary model;
- information-per-annotation, cost or field-hour superiority under a finite calibration budget.
