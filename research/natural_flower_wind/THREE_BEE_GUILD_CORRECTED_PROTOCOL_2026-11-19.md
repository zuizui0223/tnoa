# Source-corrected three-bee-guild natural-flower wind study (separate exploratory test)

**Frozen 2026-11-19 AFTER source identity/replication audit but BEFORE opening wind × bee-count/guild outcomes.** It is explicitly a NEW secondary analysis, not a retrospective rewrite of the original 4-guild protocol. The original four-guild/honeybee/bumblebee/solitary/hoverfly test remains **HOLD: no hoverfly field**.

## Source identity and exact-duplicate repair

Source Karbassioon & Stanley (2023), *Basic and Applied Ecology*, https://doi.org/10.1016/j.baae.2023.06.001; source on Zenodo record `10869660`, original `1_osr_abundance_and_weather_data.csv`, MD5 `85cc235a323d45c0fa52efcc27db9f82`, SHA256 `07c902217da47953966f93319ef8db4ef1a83d7911f41c86cbe735368e7820b5`.

The published binary contains **496 rows but exactly 124 unique FULL-row tuples**, each full tuple repeated **four times identically across all 18 fields**, with the same source `site + transect + datetimestart + location` repeated four times. These are **not 496 independent 15-minute transect events**. This source-only diagnostic was obtained before opening environmental outcome associations. Preserve the unchanged source file, programmatically collapse EXACT fourfold full-row replication, and label the inference population as **124 unique transects**. No arbitrary duplicate threshold is chosen based on ecological effects; any departure from exact 4× multiplicity aborts the study. Do not classify why the original archive contains fourfold copies without independent provenance.

The CSV includes `butterfly` (a source-labeled butterfly outcome; the original README says butterfly), **not hoverfly**. Never map this to a hoverfly/syrphid. Exclude butterflies from the three-bee quantity and composition denominators and report source butterfly frequency separately. Bee pollen/no-pollen tallies are summed within each of `honeybee`, `bumblebee`, `solitary` (no unobserved ecological visitor guild imputed). These three are behavioral/taxonomic survey classifications, not phylogenetically complete pollinator assemblage data.

## Estimands and support gates

- Amount: **total recorded bee flower-visitor encounters per field transect-time** (including 0-bee transects), among the three named bee guilds. No inference to field-wide abundance without effort/visibility correction.
- Identity: within-transect fraction/three-category composition of honeybees, bumblebees, solitary bees conditional on observed bee visits; exclude zero-bee transects from conditional multinomial log-likelihood only.
- Exposure: original `meanwindspd` m/s measured over each transect, continuous within-field-centred wind divided by pooled raw-wind IQR. Do not substitute "wind at turbine" or a Crall scent-bait proxy.
- Confounders: field fixed effects, field position (edge/center), local time quadratic. Date/field are repeated-group identifiers for uncertainty, and weather covariates temperature + sunlight enter separately as a sensitivity model.
- Effort: use actual source `datetimeend-datetimestart` minutes and include `log(minutes)` as a **Poisson offset**; expected 15 minutes, but accept 10–25 minute metadata excursions only if >=90% of observed windows lie in [14,16], with explicit range/count. Multinomial composition is conditional on encounters and does not use effort offset.

Gate before outcomes: exact 496/124/full-row-4× structure; 3 fields; >=6 source dates; >=95% of unique transects have finite nonnegative wind and valid duration; pooled wind IQR >0.1 m/s; >=2 of 3 fields contain >=3 distinct wind observations. Each named guild must have >=25 recorded encounters across >=10 unique transects and >=2 fields. If any gate fails, **HOLD**; no reclassifying species or modifying thresholds.

## Conditional associations and uncertainty

We compare:
1. Poisson amount: site + edge/center + quadratic time vs same + within-site-centred wind; measured-minute offset.
2. Multinomial three-guild composition: same two models without offset (counts within transect). This is NOT 3,412 independent weather measurements.
3. **999** whole-transect wind permutations within `site × daypart` (early <11, middle 11–16, late >=16 local hour), seed 20261119, preserving triad bee counts, source field/date/location, time, and all within-transect positive labels. At least six permutable site×daypart strata totalling >=30 unique transects required; if not, no permutation p.
4. Leave-one-field-out diagnostic, and temperature + radiation sensitivity if full design rank and data support permit. Only THREE fields, so no claims about broad population replication.
5. Separate raw effects and original publication's previously described time-of-day effects. Whether amounts differ from identity statistically requires a direct cross-response contrast; different p values alone are NOT evidence of differing slopes.

If multiple independent field-date windows create weather autocorrelation even within site×daypart, the permutation is not causal/strictly exchangeable; report this and downgrade the inferential statement accordingly. No claims about natural flowering plant success, stigma contact, species-level specificity, pollination effectiveness, or a universal TNOA causal interference law.

## Original four-guild protocol remains HOLD

`research/natural_flower_wind/PROTOCOL_2026-11-19.md` made a four-guild observational assumption before source opening. The verified original CSV does not satisfy it. This corrected program is a **new post-source audit study** and MUST NOT be presented as the original preregistered four-guild validation. An independently verified hoverfly survey source would be required for that original task.
