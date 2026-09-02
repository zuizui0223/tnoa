# Vocabulary-rank control for the D3 U-reason ablation

## Status

This is a **reviewer-motivated, post-freeze control analysis** of the immutable V14b phase surface. It was specified after inspection of D3 and is therefore **not preregistered**. It changes no observer, threshold, latent regime or synthetic world.

The purpose is to separate two mechanisms that D3 had previously conflated:

1. extra information because the recorded U split has ecologically meaningful labels;
2. extra information because any regime-dependent split adds an independent observation column and therefore reduces the compatible-mixture null space.

Authoritative source: InsePi workflow `32932634622`, phase-surface SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`.

## 1. Rank ladder already implicit in D3

For the six registered latent regimes, the target-prevalence constraint system has:

| retained vocabulary | constraint rank | null-space dimension | median target-prevalence width |
| --- | ---: | ---: | ---: |
| TARGET / not-TARGET | 2 | 4 | 0.265631 |
| TARGET / NUISANCE / other | 3 | 3 | 0.188614 |
| B / T / N / U | 4 | 2 | 0.029921 |
| B / T / N / two recorded U columns | 5 | 1 | 0.004078 |

Thus the D3 ladder simultaneously enriches semantics **and** increases constraint rank. The numerical narrowing cannot be attributed to semantic meaning without a control that holds category count/rank opportunity comparable.

## 2. Constant-split negative control

We first replaced generic U by `0.5 U` and `0.5 U` in every latent regime. This creates two labels but no new regime-discriminating direction. The constraint rank remains 4, null-space dimension remains 2 and target-prevalence median width remains `0.029921`.

Therefore merely duplicating a category does not help. An added column must carry regime-discriminating information.

## 3. Random regime-dependent two-way splits

We then generated 500 deterministic pseudo-random controls with NumPy `default_rng(seed=0)`. For each split and each of the six latent regimes, a proportion `p` was drawn from `Uniform(0,1)` and generic U was replaced by `pU` and `(1-p)U`.

Every such split increased constraint rank from 4 to 5 and reduced the null-space dimension from 2 to 1, exactly as the recorded V14b two-reason split does.

For target prevalence:

- generic B/T/N/U median width: `0.0299207`;
- median across the 500 arbitrary two-way splits: **`0.0050075`**;
- recorded V14b two-reason split: **`0.0040780`**;
- recorded/random-median ratio: `0.814`;
- **48.0%** of arbitrary splits produced a median width at or below the recorded split.

The same comparison across all five D3 estimands was:

| estimand | median arbitrary split | recorded two-reason split | arbitrary splits at or below recorded |
| --- | ---: | ---: | ---: |
| target prevalence | 0.00501 | 0.00408 | 48.0% |
| nuisance prevalence | 0.01460 | 0.01263 | 48.8% |
| T+N co-occurrence | 0.01729 | 0.01484 | 48.8% |
| coupled-response prevalence | 0.02118 | 0.07510 | 67.2% |
| any-deviation prevalence | 0.00230 | 0.00187 | 48.0% |

The recorded split is therefore not exceptional relative to arbitrary regime-discriminating two-way refinements. For coupled-response prevalence it is less identifying than the median arbitrary split.

## 4. Random three-way split control

A three-way regime-dependent split of generic U adds two independent columns relative to B/T/N/U. We generated 500 controls using `Dirichlet(1,1,1)` proportions independently for each latent regime.

All 500 controls reached constraint rank 6, null-space dimension 0 and target-prevalence median width exactly `0` to numerical tolerance. This shows directly that, with six registered latent regimes, the number and linear independence of retained observation columns can dominate identification width even when the added labels have no ecological semantics.

## 5. Revised interpretation of D3

D3 remains a valid descriptive result: the actual recorded V14b two-reason split narrows compatible sets relative to generic U. What this experiment **does not** establish is that the magnitude of that narrowing is caused by the ecological meaning of `no-supported-evidence` versus `overlap-or-attribution`.

The supported statement is:

> In the frozen six-regime design, regime-discriminating refinement of U can greatly narrow compatible sets. The observed D3 reduction is not distinguishable here from the generic rank/identifiability gain obtained by adding an informative observation column.

The semantic value of reason provenance must therefore be justified by independent measurement meaning, downstream actionability or external validation, not inferred from D3 width reduction alone.

This control **does not invalidate D1**. D1 compares B/T/N/U with target/not-target and therefore tests loss of distinct baseline, nuisance and unresolved observation-process states under binary coarsening.

## 6. V14b reason record versus reusable API reasons

The frozen V14b decision layer has only two U reasons:

- `INFORMATION_ABSENT`;
- `OVERLAP_OR_ATTRIBUTION`.

The latter pools both simultaneous target+nuisance support and indirect-only target-response cases lacking unique attribution. The later reusable `tnoa/core.py` exposes four U reasons:

- `no_supported_evidence`;
- `target_nuisance_overlap`;
- `missing_attribution`;
- `insufficient_observability`.

These are **not a one-to-one validated mapping**. V14b provides direct support only for its own two-category provenance. In particular, V14b does not separately validate `target_nuisance_overlap`, `missing_attribution` and `insufficient_observability` as four independent information-bearing columns.

## Reproduction

```bash
python scripts/analyze_vocabulary_rank_control.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/vocabulary_rank_control.json
python scripts/validate_vocabulary_rank_control.py
```
