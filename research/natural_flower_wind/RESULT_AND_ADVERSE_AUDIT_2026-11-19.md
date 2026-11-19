# Natural-flower wind study: biological results and adverse within-day falsification

**Date:** 2026-11-19  
**Status:** complete retrospective, exploratory *three-bee-guild* comparison in Irish oilseed-rape flowers, plus separate behavioral-overlap negative result from independent Wyoming field videos. **No general causal wind result established.**

## Source integrity and scientific estimands

Two independent real-data sources were processed without redistributing the original records.

**Ireland**: Karbassioon & Stanley (2023), *Basic and Applied Ecology*, DOI [10.1016/j.baae.2023.06.001](https://doi.org/10.1016/j.baae.2023.06.001); Zenodo 10869660 / Dryad 10.5061/dryad.jq2bvq8dw, published file `1_osr_abundance_and_weather_data.csv`, MD5 `85cc235a323d45c0fa52efcc27db9f82`, SHA256 `07c902217da47953966f93319ef8db4ef1a83d7911f41c86cbe735368e7820b5`. **496 source rows consist of exactly four copies of each of 124 unique full-row transects**. No row is an independent replicate of its identical copies. After exact deduplication, source weather missing in two transects and effort outside 10–25 minutes in two: **120 qualifying transects**, three fields, 10 dates and 17 field×date groups. **3,282 observed visits by three bee guilds** (honeybee 1,675; bumblebee 1,540; solitary bee 67). The original `butterfly` is not a hoverfly field; **original four-guild test remains HOLD**, never converted silently.

**Wyoming**: Weschler (2025/2026), DOI [10.1002/njb.04996](https://doi.org/10.1002/njb.04996); Zenodo [15447016](https://zenodo.org/records/15447016), CSV MD5 `9bcab4765c4fe5a9edaaf096867caf5b`, SHA256 `55f514b6dfae277fcbae43e105e796667af77a897a1da558407f5c15929647e0`. **472 actual insect–wildflower video-coded interactions**, 15 source `Unique_ID` site/date sessions (NOT presumed 17), six sites. Two UID groups encompass multiple plant taxa, which is retained rather than misread as a single flower type. Original source publication already identifies multiple behaviors per interaction.

## Ireland: ecological amount versus visitor-identity estimands

- **Amount**: three-bee-guild total encounters per measured 15-minute-equivalent transect. 
- **Identity**: conditional share of honeybee/bumblebee/solitary bee among visits. Zero-visit transects remain for count analysis.
- **Exposure**: measured source mean wind speed, within-field centering and scaling by source wind IQR, 0.95758 m/s.

All effects observational. They are not proofs of wind-caused changes in pollinator availability, local population size, pollen deposition or seed set.

### Initial exploratory result, site + field position + quadratic time model

| Response | Effect | Session wind shuffles (999, site×daypart) |
| --- | ---: | ---: |
| Total bee visits | rate ratio per wind IQR = **0.79894** | **p = 0.016** |
| Bee-guild composition | wind deviance improvement | **p = 0.001** |

The fitted conditional guild share differences for one wind-IQR contrast were honeybee **−13.2 percentage points**, bumblebee **+11.3**, and solitary bees **+1.9**. These are fitted share contrasts, not species preference or pollination effectiveness. The initial test is a comparison across site/time-of-day contexts, *not* a within-field-day confirmation.

### Adverse sensitivity A: shuffle wind only within field×date, original model unchanged

Of 17 field×date groups, 14 permit within-day wind exchange (101 transects). Using 999 whole-transect shuffles within these same-day groups, **without modifying the original reduced/full models**:

| Response | p |
| --- | ---: |
| Total bee visits | **0.982** |
| Bee-guild composition | **0.641** |

These null distributions are not equivalent to the original site×daypart null. Under the stronger same-day restriction, original claimed ecological wind associations are **not supported**. The p-values must not be presented as interchangeable estimates of one single null.

### Adverse sensitivity B: include 17 field×date fixed effects in both models

The two count models remain full-rank and are estimable. The separate three-guild multinomial fits are unstable/near-separated with fixed field×date effects and remain **HOLD**.

- Total-visitation wind rate ratio per source wind IQR: **1.399994** — the *opposite direction* to the initial 0.798942.
- Full-minus-reduced count deviance: **22.248678**.
- Restricting 999 wind shuffles within the 14 eligible field×date groups: **100 null gains at least as large; plus-one p = 0.101**.
- Zero failed Poisson permutation fits.
- Three-guild composition within-day p: **not calculated**; insufficient stable estimation. Do not impute a null or promote the earlier p=0.001.

**Scientific disposition: no robust same-day wind effect established for either the number or the guild identity of observed bee flower visits.** The strong original association can reflect day-to-day ecological and weather covariation. This is an inference vulnerability, not a causal proof of weather/day confounding.

An additional post-outcome temperature + sunlight adjustment of the initial model weakens the amount ratio from about 0.799 to **0.9095**. This does not substitute for a calibrated causal weather design.

## Wyoming: coexistence of biological activities within real flower visits

The recorded binary behavior labels are separately positive, and can coexist within a visit (not necessarily the same instant). This is a genuinely behavioral outcome, not a classifier confidence score.

- Valid interactions: **472/472**, across **15** source UID site/date units and six locations.
- Recorded pollen collection: **198**; nectar drinking: **39**.
- Recorded both: **20**; expectation from independent behavior-label assignment within each UID: **20.2216**.
- Within-UID 999-permutation two-sided **p = 1.000**, observational overlap-to-expected ratio **0.989**.
- Wind association with residual overlap is **descriptive only** because there are 15 wind-observation contexts, original wind/plant/turbine context confounding, and no prospective randomization.

**Disposition:** behaviors can co-occur in real visits, but this does **not** demonstrate excess pollen–nectar co-occurrence beyond matched within-session margins. Do not claim instant simultaneity, pollination effectiveness, or a general law of ecological process-superposition. Original article already reports multibehavioral visits; this secondary co-occurrence-versus-null test is not an independent new discovery of multi-behavioral interactions.

## Connection to TNOA's original design intent

TNOA separates biological-process propositions and what an observation licenses. The observational ecological sidecar has respected that separation:

1. Physical wind is an environmental exposure and potential biological driver **and** potential observation confound; not by definition TNOA nuisance `N`.
2. Amount, taxon identity, and within-visit behaviors are different ecological targets, none can be inferred by simply thresholding a camera detection record.
3. Genuine co-occurrence of behavior labels does not automatically imply an above-null biological interaction. The reference truth, sampling unit and what is identifiable must be specified before claiming a causal mechanism.
4. An environmental contrast that passes a pooled association screen can fail when observation dates are conditioned upon. More rows are not the same as more independent environmental contrasts.

These results are **real ecological data analyses** but do **not** validate TNOA's four-state observer architecture on wild field truth, prove C2's optimal-intervention prediction, establish a universal wind–visitation law, or supply a clean ecological novel phenomenon. This remains source- and model-conditioned observational evidence.

## Provenance and next scientific stopping rule

- Irish source and exact fourfold replication: `intake.py`, `audit_semantics.py`, `test_three_bee_guilds.py`.
- Irish stricter matched-date tests: `date_block_sensitivity.py` and `within_date_fixed_effect.py`.
- Wyoming source/schema audit: `weschler_source_intake.py`, `audit_weschler_session_key.py`, `weschler_behavior_pair_test.py`.
- Scientific owner: `research/natural_flower_wind/` sidecar, **not** TNOA MEE primary manuscript; no upstream raw data redistributed.
- Authoritative successful original-blob → reanalysis → result/hold gates CI [44531016995](https://github.com/zuizui0223/tnoa/actions/runs/44531016995), commit `abe8428f0a53c61adf8e583628fa65aa483cd8c4`.
- The four-guild question is HOLD; the three-guild within-day composition model is HOLD; Wyoming behavior excess is NOT SUPPORTED.

**Next independent biological test must supply** wind and taxon-specific interactions by independently timed field periods, enough variation within date and site, credible site/date recording effort, and/or wind/odor treatments that disentangle ecological behavior changes from weather-correlated observation. Without that, additional testing on the same source is exploratory specification search, not increasing generality.
