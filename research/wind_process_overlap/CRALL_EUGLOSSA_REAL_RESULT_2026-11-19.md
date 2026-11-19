# Crall 2020 secondary ecology: wind and within-*Euglossa* species composition

**Analysed:** 19 November 2026  
**Scientific disposition:** **not supported** for a wind-dependent within-*Euglossa* species-composition shift under the fixed exploratory conditional test. No ecological causal attribution, not a prospective confirmation.  
**Ownership:** TNOA ecological-extension sidecar only. Neither the frozen TNOA MEE manuscript nor C2 or REC is revised.

## Biological question

The original study found associations between wind/turbulence and **total male orchid-bee arrivals at chemical scent baits** in fragmented tropical forest. The new secondary question is distinct: **after conditioning on site, lure chemical and study date, does wind predict which *Euglossa* species arrive, rather than merely how many arrive?**

The dependent variable is *male-bee species composition at artificial scent baits*, **not flower visitation, pollen transfer or plant reproductive success**.

## Verified natural-data source and correct sampling unit

- Crall et al. (2020), *Biology Letters*, https://doi.org/10.1098/rsbl.2020.0103.
- Original Zenodo v2 data https://zenodo.org/records/3675327, original 74,632-byte ZIP SHA256 `d5b217261e4695e2098bde90576238018ad978c581f4b7799c15e429be19384b`.
- 450 specimen records, but **only 409** uniquely match the **70** published observation sessions by `date × site × scent`. The unmatched 41 specimens have no licensed wind attribution and are excluded.
- Original `count` across all 70 sessions sums to 409 and agrees exactly with the matched specimen count. Nine sites, 29 study dates, two lure types, three sessions with no bee arrivals. All 70 wind measures are finite and positive.
- 399/409 identified bees are *Euglossa* and only 10 are *Eulaema*. The **original primary genus-level gate remains HOLD** (only one genus qualified). This is an explicitly **secondary**, post-gate within-genus analysis.
- Within *Euglossa*, six species meet the pre-outcome `≥25 bees × ≥8 sessions × ≥3 sites` criterion: *E. championi* 110, *E. cybelia* 65, *E. flammea* 38, *E. maculilabris* 38, *E. mixta* 30, *E. dodsoni* 27. Other identified *Euglossa* together account for 91 bees.
- Unit of wind exposure is **session**, not the 399 individual bees. Nine site×scent exchangeable groups contain 67 sessions; the other three singleton groups are not permuted.

The original published observations are not independently replicated merely because repeated permutations or multiple species are evaluated.

## Frozen analysis and result

The pre-outcome secondary protocol is [CRALL_EUGLOSSA_SPECIES_FOLLOWUP_PROTOCOL_2026-10-19.md](CRALL_EUGLOSSA_SPECIES_FOLLOWUP_PROTOCOL_2026-10-19.md).

- Multinomial response with **seven categories**: six named *Euglossa* species plus `other_Euglossa`.
- Reduced model: site fixed effects + chemical scent bait + linear study date.
- Full model: reduced + log(mean wind) centred within each site, scaled by the original full-sample log-wind IQR.
- Model fit uses the unpenalized multinomial likelihood. Damped exact Newton iterations are solely a faster numerical optimizer, independently checked against the same likelihood fit using L-BFGS (initial exploratory model objectives agreed to about `10⁻⁶`; no candidate set, permutation count, or inferential method changed).
- Primary statistic: `2×(NLL_reduced - NLL_full)`.
- Null: **999** random permutations of the *session wind measurement*, restricted to each site×scent group; each permutation refits the full multinomial model on the same species counts. All 999 fits converge under the explicit numerical criterion; seed `20261019`.

| Quantity | Observed |
| --- | ---: |
| Reduced-model negative log-likelihood | 647.556675 |
| Full-model negative log-likelihood | 641.398230 |
| Deviance gain from wind | **12.316890** |
| Null permutations at least as large | **163 / 999** |
| Exact plus-one permutation p | **0.164** |
| Null median deviance gain | 7.112 |
| Null 95th percentile | 17.174 |
| Failed permutation optimizations | **0** |

**Result:** the preregistered-format exploratory joint test **does not support** a wind-dependent seven-category species-composition response after these controls. It does not establish zero wind effects or identical species responses.

## Published total-arrival relationship re-estimated as an auxiliary reference

We also refitted the original authors' **already-known wind–total-arrival** question on the same 70 sessions (409 male bees, including *Eulaema*) using a matched site + bait + linear-day Poisson mean model with and without within-site-centred log wind. We used the identical 999 site×bait whole-session wind permutations for a descriptive reanalysis, **not an independent confirmation**.

| Reference outcome | Source-verified matched specification |
| --- | ---: |
| Total arrivals: wind coefficient per pooled log-wind IQR | +0.32713 |
| Predicted arrival count ratio per IQR | **1.38698** |
| Poisson deviance gain | 15.28270 |
| Site×bait 999-permutation plus-one p | **0.008** |
| Pearson residual overdispersion | **1.905** |

Source CI reproduced these numbers with `crall_total_count_reference.py`. The comparison makes the biological endpoint difference concrete: **arrival quantity** retains a wind association under this model, while **within-*Euglossa* identity/composition** is not supported by the separate test (`p=0.164`). Different response measures and power prevent interpreting one p-value as a formal test of their difference. The count result was already reported in the original publication; only this matched-protocol juxtaposition is our secondary analysis. Temporal exchangeability, overdispersion, scent-bait limitation and all ecological observational boundaries apply.

## Effect-size description, not discoveries about individual species

Model-standardized, noncausal one-log-wind-IQR contrasts in predicted *conditional* arrival share are approximately:

| Category | Predicted share difference |
| --- | ---: |
| *E. championi* | −8.91 percentage points |
| *E. cybelia* | −3.72 |
| *E. dodsoni* | +4.98 |
| *E. flammea* | −0.69 |
| *E. maculilabris* | +2.73 |
| *E. mixta* | −0.73 |
| Other *Euglossa* | +6.33 |

**No species-specific significance or wind preference is claimed.** These are fitted model contrasts conditional on original site/scent/day support, and some implied within-site wind changes may extrapolate. The seven share changes sum to zero by definition.

All nine leave-one-site-out models were numerically estimable; the joint deviance gains ranged approximately **7.65–14.92**. This sensitivity is not independent site-level confirmation. Unpenalized nuisance fixed-effect estimates reached absolute values near 20, indicating near-separation/sparse cells, and several species have limited support. Results are therefore fragile to model/calibration choices.

## Biological interpretation and boundaries

The published source shows that wind-related conditions can coincide with changes in **numbers of male bees arriving** at chemical baits. The present secondary analysis **does not demonstrate** a corresponding change in species identity within the dominant genus after controlling for site, lure and linear date.

That difference between an *amount* response and an *identity/composition* response is the ecological distinction we set out to test. **It remains a within-study negative/uncertain result, not evidence that wind generally changes visitation but never community composition.** The test may lack sufficient independent sessions or species overlap.

Limitations are substantial: wind is observational and not manipulated; within-site×scent permutation exchangeability may fail under temporal weather structure; the dataset is dominated by one genus and one lure type; site and date are not biological population replicates; source authors already reported the abundance finding; and scent-bait encounters cannot be treated as plant-pollinator interactions.

The UK Balfour and Australian Coates original data routes were inaccessible to the hosted intake (publisher served anti-bot HTML). Those ecological sources have **not** been jointly analysed, and a cross-study comparative or meta-analytic biological finding is **not established**.

## Reproducible run and integrity

The associated workflow executes the entire chain:

`raw signed Zenodo ZIP -> SHA256 check -> source/session linkage -> derived session×species counts -> frozen eligibility gates -> site/bait/date-adjusted multinomial fit -> 999 within-stratum wind permutations -> leave-site-out sensitivity -> claim-boundary audit`.

- `research/wind_process_overlap/source_intake.py`
- `research/wind_process_overlap/crall_linkage_audit.py`
- `research/wind_process_overlap/crall_derived_matrix.py`
- `research/wind_process_overlap/crall_species_wind_test.py`
- `.github/workflows/wind-ecology-source-intake.yml`

Machine-readable result: CI artifact `crall_species_wind_result.json`. Do not copy original specimen-level raw datasets into this repository or silently revise the closed-world TNOA methodology paper.

**Final admissible claim:** In this archived scent-bait dataset, total arrivals were previously reported to vary with wind, but a new, source-verified, site/bait/day-conditioned 999-permutation test did not identify a robust wind-associated shift in within-*Euglossa* species composition (`p=0.164`).
