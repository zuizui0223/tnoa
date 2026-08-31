# Observation-vocabulary ablation

Status: **literature-audit-motivated post-freeze deterministic derivation; not preregistered**.

This analysis asks a narrower question than the original D1 target-prevalence comparison: how much downstream identification is lost at successive stages of observation-record coarsening, and does retaining the reason for an unresolved record add information beyond retaining a single generic U state?

## Immutable source and anti-tuning boundary

The only scientific input is the frozen V14b phase surface from InsePi workflow `32932634622`, SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`. The analysis uses the same 3,003 six-regime simplex mixtures as the existing downstream estimand audit. No observer, score, threshold, alpha, latent regime or synthetic world is changed.

Because this analysis was motivated by the final prior-art audit and preliminary values were inspected before it was written into the paper package, it is **not** presented as preregistered evidence. Its role is a post-freeze vocabulary ablation.

## Nested observation vocabularies

We compare four records, each a deterministic coarsening of the next richer record:

1. `TARGET / not-TARGET`;
2. `TARGET / NUISANCE / other`;
3. `B / T / N / U`, with unresolved reasons collapsed;
4. `B / T / N / U-no-supported-evidence / U-overlap-or-attribution`.

The nested never-wider relation is structural: deterministic garbling cannot create information absent from the richer record [@blackwell1953comparison]. The empirical question is the **magnitude** of the compatible-set expansion in the frozen ecological observation experiment. Identification widths are interpreted as partial-identification regions rather than as confidence intervals [@manski2005partial].

## Results

Median identification widths across the 3,003 registered regime mixtures were:

| Estimand | T/not-T | T/N/other | B/T/N/U | U reason retained |
| --- | ---: | ---: | ---: | ---: |
| Target prevalence | 0.2656 | 0.1886 | 0.0299 | **0.00408** |
| Nuisance prevalence | 1.0000 | 0.4233 | 0.0892 | **0.01263** |
| T+N co-occurrence prevalence | 0.7231 | 0.5136 | 0.1049 | **0.01484** |
| Coupled-response prevalence | 0.8589 | 0.7659 | 0.3999 | **0.07510** |
| Any-deviation prevalence | 0.4559 | 0.08646 | 0.01372 | **0.00187** |

For target prevalence, resolving the two U reasons reduced the median width from `0.02992` to `0.00408`, an additional `86.37%` reduction relative to generic B/T/N/U. For target+nuisance co-occurrence, the corresponding reduction was from `0.10494` to `0.01484` (`85.86%`).

## Registered-axis slices

The same calculation was repeated in all 34 registered single-axis slices. Reason-resolved U was never wider than generic U in all 34 slices for all five estimands, as required by the nested observation relationship. Median width was **strictly** smaller in 27/34 slices for target prevalence and 29/34 slices for each of the other four estimands.

Across the 34 slices, the median ratio of reason-resolved to generic-U median width was `0.134` for target prevalence and `0.148` for T+N co-occurrence. These slice summaries reduce the risk that the global result is driven by one registered axis level, but they do not establish robustness to arbitrary ecological prevalence weighting.

## Interpretation

The main methodological implication is narrower than “more categories are always better.” Richer deterministic records are structurally at least as informative, but additional fields are useful only if their semantics are independently defensible. In the frozen experiment, distinguishing **why** an observation remained unresolved retained substantial information about target prevalence and especially about target–nuisance coexistence. This supports reason provenance as part of the observation contract rather than as logging metadata alone.

## Reproduction

Run:

```bash
python scripts/analyze_observation_vocabulary_ablation.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/observation_vocabulary_ablation.json
python scripts/validate_observation_vocabulary_ablation.py
```

The analysis fails closed if the immutable phase-surface SHA or dimensions drift.
