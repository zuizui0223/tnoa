# Observation-vocabulary ablation

Status: **literature-audit-motivated post-freeze deterministic derivation; not preregistered**.

This analysis asks how much downstream identification changes as the frozen observation record is progressively refined. D3 originally motivated a semantic interpretation of the two frozen U reasons. The later reviewer-motivated D5 random-split control shows that this interpretation was too strong: the D3 split is informative, but its additional narrowing is not distinguishable from the generic rank/identifiability gain produced by arbitrary regime-discriminating refinements of U.

## Immutable source and anti-tuning boundary

The only scientific input is the frozen V14b phase surface from InsePi workflow `32932634622`, SHA-256 `1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34`. The analysis uses the same 3,003 six-regime simplex mixtures as the existing downstream estimand audit. No observer, score, threshold, alpha, latent regime or synthetic world is changed.

Because this analysis was motivated by the final prior-art audit and preliminary values were inspected before it was written into the paper package, it is **not** presented as preregistered evidence. Its role is a post-freeze vocabulary ablation.

## Nested observation vocabularies

We compare four records, each a deterministic coarsening of the next richer record:

1. `TARGET / not-TARGET`;
2. `TARGET / NUISANCE / other`;
3. `B / T / N / U`, with unresolved reasons collapsed;
4. `B / T / N / U-no-supported-evidence / U-overlap-or-attribution`.

The nested never-wider relation is structural: deterministic garbling cannot create information absent from the richer record [@blackwell1953comparison]. The empirical question is the **magnitude** of the compatible-set expansion in the frozen ecological observation experiment. Identification widths are interpreted as partial-identification regions rather than confidence intervals [@manski2005partial].

## D3 numerical result

Median identification widths across the 3,003 registered regime mixtures were:

| Estimand | T/not-T | T/N/other | B/T/N/U | frozen two-way U split |
| --- | ---: | ---: | ---: | ---: |
| Target prevalence | 0.2656 | 0.1886 | 0.0299 | **0.00408** |
| Nuisance prevalence | 1.0000 | 0.4233 | 0.0892 | **0.01263** |
| T+N co-occurrence prevalence | 0.7231 | 0.5136 | 0.1049 | **0.01484** |
| Coupled-response prevalence | 0.8589 | 0.7659 | 0.3999 | **0.07510** |
| Any-deviation prevalence | 0.4559 | 0.08646 | 0.01372 | **0.00187** |

For target prevalence, the frozen two-way U split reduced the median width from `0.02992` to `0.00408`. For target+nuisance co-occurrence, the corresponding reduction was `0.10494` to `0.01484`.

## Registered-axis slices

The same calculation was repeated in all 34 registered single-axis slices. The refined record was never wider than generic U in all 34 slices for all five estimands, as required by the nested observation relationship. Median width was strictly smaller in 27/34 slices for target prevalence and 29/34 slices for each of the other four estimands.

These slice summaries show that the numerical refinement effect is not confined to one registered axis level, but they do not establish semantic specificity or robustness to arbitrary ecological prevalence weighting.

## D5 specificity control changes the interpretation

D5 keeps the same generic B/T/N/U emission matrix and splits only its U column.

- A constant 50:50 split leaves target-prevalence median width unchanged at `0.0299207`, because the added column is linearly redundant.
- Across 500 unlabeled regime-dependent two-way random splits, the median target-prevalence width was `0.0050075`.
- **48.0%** of those random splits were equal to or narrower than the frozen semantic split (`0.0040780`).
- The same non-exceptional pattern holds across all five estimands; the random-equal-or-better fraction ranges from `0.480` to `0.672`.
- Across 500 unlabeled three-way random U splits, the six-regime constraint system was full rank in every draw and all five estimands were point-identified to numerical tolerance.

Therefore D3 does **not** identify an information advantage specific to the meanings `no-supported-evidence` and `overlap-or-attribution`. The large additional narrowing is substantially explained by the generic rank/identifiability gain from adding a non-redundant regime-discriminating observation column. State count alone does not determine the exact width—the orientation of the added column relative to the estimand also matters—but semantic labels are not isolated as the cause of the D3 effect.

Full controls are documented in `docs/REASON_SPLIT_SPECIFICITY_CONTROL.md` and `derived/reason_split_specificity_control.json`.

## Correct interpretation

Supported:

> The frozen two-way U refinement is informative in this six-regime design, but arbitrary regime-discriminating refinements often provide comparable or greater narrowing. D3 therefore measures the value of additional non-redundant observation structure, not a semantic-specific information advantage of the selected U reasons.

Not supported:

> The selected U-reason semantics themselves explain the additional `86.37%` target-prevalence width reduction.

The architectural reason labels may still be scientifically useful because different unresolved situations motivate different follow-up measurements, but that practical semantic value is not established by D3's partial-identification width comparison.

## Reproduction

```bash
python scripts/analyze_observation_vocabulary_ablation.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/observation_vocabulary_ablation.json
python scripts/validate_observation_vocabulary_ablation.py

python scripts/analyze_reason_split_specificity_control.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/reason_split_specificity_control.json
python scripts/validate_reason_split_specificity_control.py
```
