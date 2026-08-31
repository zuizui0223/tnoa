# Target-prevalence and composition-weight sensitivity

## Status

This is a **post-freeze, reviewer-motivated design-sensitivity analysis** of the immutable V14b phase surface. It does not rerun or retune either observer, change any threshold, alter the six latent regimes or generate new synthetic worlds. It was specified after inspection of D1/D3 and is therefore **not preregistered**.

Authoritative source:

- InsePi workflow `32932634622`;
- phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`;
- 30,625 coordinates, 183,750 coordinate × regime rows and 5,880,000 worlds;
- the same 0.1-step six-regime simplex used by D1/D3: 3,003 compositions.

The executable derivation is `scripts/analyze_prevalence_weighting_sensitivity.py`; the locked compact result is `derived/prevalence_weighting_sensitivity.json`.

## 1. Why the uniform simplex summary needs a second audit

The 3,003 simplex points are a deterministic sensitivity lattice, not an ecological prior. Uniformly enumerating them does **not** give equal mass to target prevalence. Because four of the six registered regimes contain the target, the lattice is concentrated toward higher target prevalence.

Counts by known target prevalence are:

| target prevalence | compositions |
| ---: | ---: |
| 0.0 | 11 |
| 0.1 | 40 |
| 0.2 | 90 |
| 0.3 | 160 |
| 0.4 | 245 |
| 0.5 | 336 |
| 0.6 | 420 |
| 0.7 | 480 |
| 0.8 | 495 |
| 0.9 | 440 |
| 1.0 | 286 |

Thus only `141/3003 = 4.70%` of the uniform lattice has target prevalence `<=0.2`. Rare-target compositions are therefore deliberately inspected rather than assumed to be represented by the global median.

## 2. Prevalence-stratified information loss

Median target-prevalence identification widths by known prevalence are:

| true target prevalence | binary T/not-T | T/N/other | B/T/N/U | reason-resolved U |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | ~0 | 0 | 0 | 0 |
| 0.1 | 0.0464 | 0.0370 | 0 | 0 |
| 0.2 | 0.0941 | 0.0927 | 0.0171 | 0 |
| 0.3 | 0.1405 | 0.1298 | 0.0230 | 0 |
| 0.4 | 0.1883 | 0.1695 | 0.0295 | 0 |
| 0.5 | 0.2347 | 0.2064 | 0.0301 | 0.00408 |
| 0.6 | 0.2824 | 0.2404 | 0.0349 | 0.00408 |
| 0.7 | 0.3222 | 0.2311 | 0.0473 | 0.00408 |
| 0.8 | 0.3204 | 0.2203 | 0.0517 | 0.00408 |
| 0.9 | 0.2777 | 0.1777 | 0.0298 | 0.00408 |
| 1.0 | 0.1961 | 0.1961 | 0.0302 | 0.00408 |

The advantage does not disappear in the rare-target region. In the `theta<=0.2` subset (141 compositions), median widths are:

- binary target/not-target: `0.07410`;
- target/nuisance/other: `0.07386`;
- B/T/N/U: `0.000175`;
- reason-resolved U: `0.0` to numerical tolerance.

The same subset occupies only 4.70% of the uniformly enumerated lattice. This result therefore converts a potential weighting weakness into an explicit condition map: in the frozen emission geometry, the information-preservation gain is **not** driven only by balanced/high-prevalence mixtures.

This is not a claim that real field prevalence is low or that these numerical widths transfer to a field sensor. It is a conditional result under the frozen synthetic emission map.

## 3. Composition-level bounded density-ratio sensitivity

The earlier weighting audit varied weights over the registered phase-space/regime rows. That does not address weighting of the 3,003 latent-regime compositions used for the downstream estimand. We therefore apply an analogous bounded density-ratio class directly to the composition lattice.

Relative to uniform composition weighting, each composition multiplier `r_i` satisfies

```text
1/kappa <= r_i <= kappa
mean(r_i) = 1
```

For each `kappa`, we choose weights adversarially to minimize the ratio of weighted mean width removed. The statistic is therefore a **worst-case weighted-mean reduction ratio**, not a weighted median.

| kappa | minimum fraction of binary width removed by B/T/N/U | minimum additional fraction of B/T/N/U width removed by reason-resolved U |
| ---: | ---: | ---: |
| 1.0 | 0.843 | 0.863 |
| 1.25 | 0.819 | 0.838 |
| 1.5 | 0.800 | 0.814 |
| 1.6 | 0.794 | 0.805 |
| 2 | 0.770 | 0.771 |
| 3 | 0.728 | 0.697 |
| 5 | 0.672 | 0.585 |
| 10 | **0.575** | **0.400** |

Even when composition weights can move by a factor of ten around the uniform lattice, an adversarial weighting cannot reduce the weighted-mean B/T/N/U gain below about 57.5% of binary width, and cannot reduce the additional reason-resolved-U gain below about 40.0% of generic-U width.

The bounded class is not an ecological prior and does not cover arbitrary distribution shift. It asks only whether the information-loss magnitude can be made small by substantial but bounded reweighting of the registered composition lattice.

## 4. Interpretation

The structural statement remains Blackwell ordering: deterministic coarsening cannot add information. The new empirical statement is narrower:

> In the frozen V14b emission geometry, the **magnitude** of the identification gain persists across the rare-target portion of the registered simplex and under substantial bounded reweighting of simplex compositions.

This strengthens D1/D3 without converting a synthetic design into a field-frequency claim.

## 5. Annotation-budget boundary

All D1/D3/D4 comparisons condition on a frozen, effectively known emission map. This isolates information lost through observation coarsening, but it does not model the extra annotation and calibration burden of estimating a richer observation vocabulary from finite data. Under a fixed validation budget, uncertainty in a richer emission map could offset part of the identification gain reported here.

Therefore Paper 1 does **not** claim greater information per annotation, per unit cost or per field hour. A finite-budget comparison would require a new measurement-design specification for annotation allocation, grouped dependence, rare-state sampling and emission-matrix uncertainty; that is outside the present closed-world comparison.
