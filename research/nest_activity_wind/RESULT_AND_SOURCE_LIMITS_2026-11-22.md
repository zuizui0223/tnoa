# TNOA ecological extension: all-weather nest-return records and wind, source-limited negative result

**Analysis date:** 2026-11-22  
**Disposition:** **NOT SUPPORTED** — no robust within-source-day association between wind and relative recorded honeybee-versus-bumblebee arrivals in the available antenna-active, weather-unambiguous windows. This is a *retrospective exploratory analysis*, not a new causally identified biological relationship.

## Why this test exists

The previously merged [independent-flower sidecar](../natural_flower_wind/RESULT_AND_ADVERSE_AUDIT_2026-11-19.md) found that associations between recorded flower-visitor numbers, visitor composition and wind were unstable when survey date was controlled. We examined a complementary **nest-return observation channel** within the same Irish source archive (Karbassioon & Stanley 2023), with individual RFID timestamps and contemporaneous 30-second weather. This is **not a second independent study**, and nest returns are **not direct flower visits**.

## Original source identifiers and data integrity

The publisher [Zenodo 10869660](https://zenodo.org/records/10869660) original file bytes and their published MD5s were verified before analysis:

| Source | Original records | SHA256 |
| --- | ---: | --- |
| `2_bumblebee_rfid_data.csv` | 25,158 | `0d900614ff715944fb44304bdb6fd0a5d4c30275feb7db1292816dae3db247de` |
| `3_honeybee_rfid_data.csv` | 20,774 | `28fae38017fe0fb4459cc0147420419d3ca87508e322ec99fb67dff5996d5431` |
| `4_rfid_weather_data.csv` | 102,392 | `1f6b28b9be072ecf0160fb587e4c5f60dc16f4694252071106957ead2d29de5a` |

**Serious, unresolved provenance conflict**: the original methods state **2021** for the RFID study, whereas all raw RFID and weather timestamps use **2020**. They do match one another in 2020. No date-shifting or implied confirmation of the source year was performed. A publication-quality field-calendar interpretation requires author/source clarification.

**Serious, unresolved weather-provenance conflict:** the 102,392 weather rows have 80,808 unique timestamps, of which **19,410 exact timestamps** have conflicting meteorological values. There is no weather-station ID column to decide which observation is applicable. Never choose a favorable duplicate, average conflicting values, or silently declare them distinct locations. An entire 15-minute interval is rejected if **any** exact timestamp has conflicting values. Only 15-minute intervals with at least 20 distinct clean 30-second weather observations were admitted. All equal duplicate rows at the same exact time were collapsed.

RFID `direction` is explicit and contains **Arriving / Departing / Unknown**. Only positive Arriving labels count as measured returns. The original 5-minute same-tag minimum gap is respected; the extra fractional-second field is `firstimefound` (sic) for bumblebees, `firsttimefound` for honeybees. Its clock minute differs from `timestamp` by **−1 or 0 minute only**, enabling literal event time reconstruction (not an invented timestamp or a 1-year offset).

## Eligible biological observation population

- Distinct conflict-free 15-minute weather bins with ≥20 30-second samples: **1,974**.
- Daytime (06:00–22:00) candidate bins with at least one raw RFID antenna read for **both** taxa: **475 across 18 literal days**.
- Source-day threshold ≥8 such bins: **12 accepted literal 2020 dates, 459 bins**.
- Bins with one or more valid recorded Arriving events in either taxon: **391**; 68 bins have no known Arriving label and are excluded from the conditional composition likelihood.
- Five-minute tag-deduplicated Arriving labels in the 459 safe bins: **463 honeybee** and **602 bumblebee**; these are event records, **not** numbers of distinct individuals or independently observed days.
- On the full original source the accepted Arriving tags after five-minute de-duplication represent **107 honeybee tag IDs** and **159 bumblebee tag IDs**.

The denominator is selected on *some raw RFID antenna reading for BOTH taxa*. That is a limited proxy for operating receiver presence, **not proof of loggers' full uptime**. A no-return bin cannot be certified as biological absence. The sampling selection may itself depend on animal activity.

## Fixed exploratory comparison

**Ecological observation target:** the conditional fraction of *recorded returns* attributed to honeybees vs bumblebees among bins with at least one recognized arrival, not species abundance, pollination, or whole-nest foraging. Reduced binomial model: source literal day fixed effects + quadratic clock time. Full model: reduced + within-day centred mean wind, scaled by the IQR of admitted wind values.

- Recorded honeybee-vs-bumblebee return **odds ratio 0.76836** per source wind IQR (**2.87983 m/s**).
- Extra wind deviance **0.60451**.
- **999 complete** source-day × daypart whole-bin wind permutations, fixed seed 20261122, 32 permutable strata / 390 positive-return bins, **370** null deviances at least as large, **p = 0.371**; **0** failed optimizations.
- Adding concurrent temperature and solar radiation changes the wind odds ratio to **0.92285**, with extra wind deviance **0.04613**.

**Scientific disposition: NOT SUPPORTED.** The initial sign is not independent evidence that wind suppresses honeybee foraging more than bumblebee foraging. The model tests **recorded** arrivals and is not comparable to population abundance.

## Interpretation and protected boundaries

1. The year discrepancy (2020 in all source files vs 2021 in source methods) remains unresolved; time alignment is **only within the literal 2020 source files**.
2. Weather sensor provenance is ambiguous for 19,410 unique timestamps; 15-minute windows containing conflicts were excluded. Conditioning on conflict-free windows may induce selection bias.
3. The study has **three colonies per species**, with unequal tagging and observed RFID detection; a taxon×wind contrast cannot separate physical behavioral changes from sensor response if detectability itself varies with weather.
4. Source honeybees were chosen as pollen-bearing returning foragers whereas source bumblebees included tagged workers. These are not identical denominator populations.
5. A 15-minute bin with raw reads from both taxa is not a guaranteed full-coverage exposure interval. No biological absence/true visit rate is estimated.
6. The source author already reported stronger mid-day honeybee activity versus flatter bumblebee activity; TNOA does not claim that finding.
7. The field flower surveys (favorable-weather crop visits, June/July) and nest RFID sessions (all-weather, different sites) do **not** share identical populations, dates or observational targets. Their p-values are not a cross-system comparative test.
8. 999 permutations of already observed days are Monte Carlo reference draws, not 999 independent day-level biological replications. The intra-day exchangeability assumption is questionable for temporally correlated weather.
9. No pollen movement, seed output, natural community replacement, new ecological law of process superposition, or TNOA field observation-classifier validation is claimed.

## Reproduction and scientific ownership

- `research/nest_activity_wind/PROTOCOL_2026-11-22.md` — question and observation semantics locked before biological outcomes.
- `research/nest_activity_wind/intake.py` — raw Zenodo original MD5/SHA256, row and field diagnostics.
- `audit_temporal_support.py`, `audit_clean_windows.py`, `audit_arrival_timing.py` — year mismatch, conflicting weather, source clock.
- `build_safe_15min.py` — binary source --> **derived per-bin counts only**, raw RFID tag IDs never redistributed.
- `test_rfid_relative_arrivals.py` — date/time-conditioned binomial model, 999 grouped permutations and temperature/solar sensitivity.
- `.github/workflows/allweather-bee-rfid.yml` — public source re-download, checksums, numerical anchor gates and derived artifact.

The negative biological result and severe source limits are the finished sidecar. **Do not add it as a positive natural-wind effect to the frozen TNOA MEE paper, C2 TREE Opinion or REC observational distortion paper.** A new genuinely independent field data set with contemporaneous identified flower visits, within-site/date weather replication and observation effort/uptime truth is still required for a general ecological claim.
