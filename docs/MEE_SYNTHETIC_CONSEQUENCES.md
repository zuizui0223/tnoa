# MEE synthetic ecological consequence and weighting audit

## Status

This is a **post-freeze derived analysis** of the immutable V14b phase surface. It does not rerun the generator, alter either frozen observer, change the nuisance alpha contract, or replace the locked V14b/V14c result.

Authoritative source:

- workflow `32932634622`;
- phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`;
- 30,625 coordinates;
- 183,750 coordinate × latent-regime rows;
- 5,880,000 synthetic worlds.

The executable derivation is `scripts/analyze_mee_synthetic_consequences.py`; the compact locked result is `derived/mee_synthetic_consequences.json`.

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

The result is not that TNOA magically estimates field prevalence. The result is narrower and more useful:

> **Collapsing reasoned observation states to a binary record can destroy information needed to identify an ecological prevalence, even when the underlying sensor emissions are perfectly calibrated.**

The magnitude of the information loss is empirical to this frozen synthetic geometry; the direction that coarsening cannot add identification information is structural.

### Registered-axis slice check

The same prevalence-simplex calculation was repeated after conditioning the frozen surface on every registered level of each Pi axis: **34 axis slices** total.

- TNOA-compatible prevalence intervals were never wider than binary intervals in any slice.
- The median ratio of TNOA width / binary width across slices with non-zero binary width was approximately **0.110**.
- The result is not uniformly dramatic. At the extreme `Pi2=0.01` and `Pi2=100` slices, the calibrated binary emission alone essentially identifies prevalence, so keeping extra states adds no practical width reduction.
- At `Pi3=0`, both representations remain weak: median TNOA width is about **0.897** versus binary width **1.0**. This is consistent with the frozen structural loss of the direct target channel.

These boundary cases should remain visible; the MEE claim is information preservation, not universal superiority of a four-state encoding.

## 2. Equal-grid weighting sensitivity

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

Thus the statement

> most U is associated with overlap/attribution rather than no-supported-evidence

survives every tested reweighting through `kappa=10`. This is a substantially stronger MEE-facing result than the pooled `U=0.2533` frequency.

### 2.2 Pi1 nonmonotonicity is not a robust headline

We ask whether one common reweighting over the Pi2-Pi6/regime strata can make total U monotone non-increasing over Pi1.

- impossible through `kappa=1.5`;
- feasible at `kappa=1.6` and above in the tested grid.

Therefore the original equal-grid statement that longer observation does not monotonically remove U remains a valid description of the registered design, but **it should not be promoted as a weighting-robust ecological law**. For MEE it belongs as a conditional/sensitivity result, not a headline conclusion.

### 2.3 The Pi2=1 pooled contrast is highly weight-sensitive

Define the local pooled contrast

`U(Pi2=1) - mean[U(Pi2=0.316...), U(Pi2=3.162...)]`.

Under equal weighting it is only about `+0.00646`. With `kappa=1.25`, the admissible range already spans approximately `-0.0195` to `+0.0327`.

This reinforces, rather than weakens, the retired narrow-ridge hypothesis: there is no stable global timescale-collision ridge whose sign survives even modest design-space reweighting.

## 3. Consequence for the MEE manuscript

The main results should now be ordered as follows:

1. **Ecological consequence:** binary collapse biases naive target/visit prevalence downward and greatly broadens calibrated partial identification in most synthetic regime mixtures.
2. **Robust decision geometry:** U is predominantly overlap/attribution across a broad explicit reweighting class.
3. **Conditional geometry:** Pi1 nonmonotonicity is descriptive and weight-sensitive, so it is retained but demoted.
4. **Negative result:** a narrow Pi2 collision ridge is not a stable property of the frozen design.
5. **Structural boundary:** Pi3 zero/positive remains explicitly a consequence of the frozen direct-channel rule, not a field SNR law.

This changes the paper's center of gravity from “a decision ontology plus a large simulation” to:

> **preserving observation-process states prevents avoidable loss of ecological estimand information, and the frozen phase surface identifies when that preservation matters.**

## 4. Claim boundary

Allowed:

- synthetic target-prevalence bias against known latent truth;
- partial-identification width comparisons under the frozen calibrated emission map;
- explicit bounded reweighting sensitivity;
- axis-slice sensitivity within the registered synthetic grid.

Still forbidden without external validation:

- field visit prevalence or field abundance estimates;
- field detection accuracy;
- field biological absence certification;
- a claim that the equal-grid emission matrix transfers numerically to another camera, site or taxon;
- a universal claim that four-state TNOA is always more informative in practice than every calibrated binary model.
