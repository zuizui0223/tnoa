# MEE synthetic ecological consequence and weighting audit

## Status

This is a **post-freeze derived analysis** of the immutable V14b phase surface. It does not rerun the generator, alter either frozen observer, change the nuisance alpha contract, or replace the locked V14b/V14c result.

Authoritative source:

- workflow `32932634622`;
- phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`;
- 30,625 coordinates;
- 183,750 coordinate × latent-regime rows;
- 5,880,000 synthetic worlds.

The executable D1 derivation is `scripts/analyze_mee_synthetic_consequences.py`; the compact locked result is `derived/mee_synthetic_consequences.json`. D3 reason-resolution is in `scripts/analyze_observation_vocabulary_ablation.py`, and the D4 prevalence/composition-weight audit is in `scripts/analyze_prevalence_weighting_sensitivity.py`.

## 1. Downstream ecological estimand

### Question

The original Paper-1 comparison showed that forcing every non-`TARGET` output to absence missed 35.69% of latent target-present worlds under equal-grid/equal-regime weighting. That is a sensor-decision result. For MEE, the more consequential question is downstream:

> If the ecological estimand is target/visit prevalence, how much information is lost when B/T/N/U is collapsed to a binary target/not-target record?

### Synthetic estimand

Target truth is known for the six frozen latent regimes:

```text
baseline                    0
target_only                 1
nuisance_only               0
target_coupled              1
target_nuisance_superposed  1
target_nuisance_coupled     1
```

We enumerate the six-regime prevalence simplex on a deterministic 0.1 lattice. This gives 3,003 possible regime compositions. The lattice is a design-space device, **not an ecological prior**.

For each composition we obtain the expected B/T/N/U observation distribution from the frozen emission matrix and compare three objects:

1. **Naive forced-binary point estimate:** the observed `TARGET` fraction is treated as target prevalence and every other state as absence.
2. **Binary calibrated partial identification:** retain only `TARGET` versus not-`TARGET`, but allow every latent-regime composition compatible with that collapsed observation.
3. **TNOA partial identification:** retain B/T/N/U and allow every latent-regime composition compatible with the full four-state observation distribution.

The partial-identification calculation does not assume that N, B or U certifies target absence. It asks which latent target prevalences remain observationally compatible with the calibrated frozen emission map.

### Result

Across the 3,003 synthetic regime compositions:

- naive forced-binary prevalence was negatively biased in **99.63%** of compositions;
- median naive bias was **-0.2377** prevalence units;
- median binary-collapse identification width was **0.2656**;
- median B/T/N/U identification width was **0.0299**;
- the median relative width reduction, among compositions with non-zero binary width, was **84.45%**;
- B/T/N/U was never wider than its binary collapse, as required because the binary observation is a deterministic coarsening of the full observation;
- the true synthetic target prevalence remained inside the TNOA-compatible set for every enumerated composition.

The result is not that TNOA estimates field prevalence. The result is narrower:

> **Collapsing reasoned observation states to a binary record can destroy information needed to identify an ecological prevalence, even when the underlying sensor emissions are perfectly calibrated.**

The magnitude of the information loss is empirical to this frozen synthetic geometry; the direction that coarsening cannot add identification information is structural.

### Registered-axis slice check

The same prevalence-simplex calculation was repeated after conditioning the frozen surface on every registered level of each Pi axis: **34 axis slices** total.

- TNOA-compatible prevalence intervals were never wider than binary intervals in any slice.
- The median ratio of TNOA width / binary width across slices with non-zero binary width was approximately **0.110**.
- The result is not uniformly dramatic. At the extreme `Pi2=0.01` and `Pi2=100` slices, the calibrated binary emission alone essentially identifies prevalence, so keeping extra states adds no practical width reduction.
- At `Pi3=0`, both representations remain weak: median TNOA width is about **0.897** versus binary width **1.0**. This is consistent with the frozen structural loss of the direct target channel.

These boundary cases should remain visible; the MEE claim is information preservation, not universal superiority of a four-state encoding.

### Target-prevalence and composition-weight sensitivity

The 3,003-point simplex is not uniform in target prevalence. Only `141/3003 = 4.70%` of compositions have known target prevalence `<=0.2`, so the global median by itself gives little weight to rare-target conditions.

A post-freeze reviewer-motivated audit therefore stratified by known target prevalence and separately reweighted the composition lattice. In the `theta<=0.2` subset, median identification widths were `0.07410` for target/not-target, `0.07386` for target/nuisance/other, `0.000175` for B/T/N/U and `0.0` to numerical tolerance for reason-resolved U. Thus the information-preservation advantage does not disappear in the rare-target portion of this frozen simplex.

We then placed a bounded density-ratio class directly on the 3,003 composition weights. At `kappa=10`, an adversarial composition weighting could not reduce the weighted-mean fraction of binary width removed by B/T/N/U below **0.575**, and could not reduce the additional fraction of generic-U width removed by reason-resolved U below **0.400**. These are worst-case weighted-mean ratios, not weighted medians and not ecological priors. Full values are in `docs/PREVALENCE_WEIGHTING_SENSITIVITY.md`.

## 2. Phase-space/equal-grid weighting sensitivity

### Why this analysis is needed

The pooled V14b rates are equal-grid/equal-regime summaries. They are not ecological frequencies. Merely saying so does not establish that qualitative conclusions survive different design-space weights.

We therefore use a bounded density-ratio sensitivity class. Relative to the original equal weight, each row receives multiplier `r` satisfying

```text
1/kappa <= r <= kappa
mean(r) = 1
```

No ecological prior is asserted. `kappa` simply states how far an alternative weighting is allowed to move from the registered design.

### 2.1 Overlap/attribution remains the robust U result

Minimum possible overlap/attribution share of U within the reweighting class:

| kappa | worst-case overlap/attribution share of U |
| ---: | ---: |
| 1.0 | 0.894 |
| 2.0 | 0.766 |
| 5.0 | 0.611 |
| 10.0 | 0.520 |

Thus the statement that most U is associated with overlap/attribution rather than no-supported-evidence survives every tested reweighting through `kappa=10`.

### 2.2 Pi1 nonmonotonicity is not a robust headline

We ask whether one common reweighting over the Pi2-Pi6/regime strata can make total U monotone non-increasing over Pi1.

- impossible through `kappa=1.5`;
- feasible at `kappa=1.6` and above in the tested grid.

Therefore the original equal-grid statement that longer observation does not monotonically remove U remains a valid description of the registered design, but **it should not be promoted as a weighting-robust ecological law**.

### 2.3 The Pi2=1 pooled contrast is highly weight-sensitive

Define the local pooled contrast

`U(Pi2=1) - mean[U(Pi2=0.316...), U(Pi2=3.162...)]`.

Under equal weighting it is only about `+0.00646`. With `kappa=1.25`, the admissible range already spans approximately `-0.0195` to `+0.0327`.

This reinforces the retired narrow-ridge hypothesis: there is no stable global timescale-collision ridge whose sign survives even modest design-space reweighting.

## 3. Final consequence for the MEE manuscript

The main results are ordered as follows:

1. **C6 -> C7 operational calibration result:** ranking survived a nuisance-representation change while the inherited raw threshold lost its operating meaning; a predeclared family-conditional false-attribution criterion restored the declared held-out semantics.
2. **D1/D3/D4 downstream information consequence:** progressive observation coarsening widens compatible ecological estimands; reason-resolved U retains additional information; and the magnitude remains substantial in rare-target compositions and under bounded composition reweighting.
3. **C2 negative result:** the preregistered narrow `Pi2` collision ridge was not supported.
4. **Secondary geometry:** robust U-reason composition, conditional Pi1 reason substitution and uneven effective axis separation.
5. **Structural/design diagnostics:** Pi3 zero/positive and C13 remain design-induced diagnostics, not method-performance headlines.

This aligns `MEE_SYNTHETIC_CONSEQUENCES.md`, `STRUCTURAL_RESULT_AUDIT.md`, the active manuscript and the claim-audit order.

## 4. Claim boundary

Allowed:

- synthetic target-prevalence bias against known latent truth;
- partial-identification width comparisons under the frozen calibrated emission map;
- prevalence-stratified summaries on the registered simplex;
- explicit bounded reweighting sensitivity over both phase-space rows and simplex compositions;
- axis-slice sensitivity within the registered synthetic grid.

Still forbidden without external validation:

- field visit prevalence or field abundance estimates;
- field detection accuracy;
- field biological absence certification;
- a claim that the frozen emission matrix transfers numerically to another camera, site or taxon;
- a universal claim that four-state TNOA is always more informative in practice than every calibrated binary model;
- a claim of greater information per annotation or per unit calibration cost, because the present comparison conditions on a frozen effectively known emission map.
