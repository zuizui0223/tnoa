# Source-verified ecological process interaction: mammal gait × recorded RAIN label

**Date:** 2026-10-19  
**Status:** **exploratory, observational, external public source; not a causal weather result**  
**Scientific owner:** this TNOA ecological-extension sidecar. It does **not** revise TNOA Paper 1, C2, REC or InsePi V13.

## What is biological in this analysis?

**Question:** among independently CCTV-observed animal passes, does the association between the original dataset's recorded rain status and the proportion of passes classified as **walking** differ between foxes and badgers?

This response is the **animals' recorded gait**, not the camera sensor's trigger state. Thus, unlike a detection-efficiency benchmark, this question concerns an observed behavioral composition. Weather status here is not formally defined as TNOA's nuisance process. No empirical T/N/O attribution labels are claimed.

## Raw source identity

- Findlay, Briers & White (2020), *Mammal Research*: https://doi.org/10.1007/s13364-020-00478-y
- Original third-party data: https://github.com/melaniefindlay/CT-Detection
- Immutable source commit `abc72f535bb59ebed202fb7acca852fc1647e97a`
- File `REGISTRATION_FOX_BADGER.csv`, Git blob SHA1 `d2dc9852ca1f2a1380b991acba425d16e12327d5`.
- 881 CCTV-observed passage rows in source. Only explicit `RAIN=YES` and `RAIN=NO` are admitted; **4 `RAIN=N0` and 7 `RAIN=NA` rows are excluded without guessing**. Final 870 pass rows.

The original R script defines `GAIT=W` as walk and combines other categories `R` and `T` as run/trot. No individual animal or independent recording-day identifiers were found in this released table. The `RAIN` assignment and temporal matching protocol are not independently verified from its code/CSV; do not describe it as measured hourly precipitation or rain intensity.

## New exploratory descriptive result

| Species | RAIN=NO: walking | RAIN=YES: walking | Difference YES−NO |
| --- | ---: | ---: | ---: |
| Fox | 308/471 = **65.4%** | 78/87 = **89.7%** | **+24.26 percentage points** |
| Badger | 99/253 = **39.1%** | 14/59 = **23.7%** | **−15.40 points** |

Pooled species × RAIN difference in walking proportion = **+39.66 percentage points**.

As a descriptive physical-camera-position standardization (four positions with equal weight, **not four populations**):
- fox rain-minus-no walking difference **+23.82 points**;
- badger **−15.04 points**;
- species-by-rain contrast **+38.86 points**;
- same direction in **all 4/4 positions** for each species, though the weather-stratum support differs.

Sensitivity checks on the raw, untriggered pass world:
- `ORIENT=L` subset, 694 rows: pooled interaction **+41.35 points**.
- `LOIT=0` subset, 803 rows: **+45.72 points**.
- 1–7 m distance subset, 863 rows: **+39.65 points**.

Fixed-effect logistic descriptive fits (no inference from invalid independence) continue to show opposite-sign conditional standardized effects:
- physical position fixed effects only: interaction **+39.28 points**;
- position + recorded `AIR` covariate: **+37.98 points**;
- position + `AIR` + source `DIST` + `ORIENT`: **+37.83 points**.

**No p-values, confidence intervals, population-rate estimates or causal selective explanations are supplied**: source does not identify independent animals, dates, or a validated weather-exposure schedule.

## Separate observation-system check (not the biological target)

Using triggered-camera observations instead of all reference CCTV passes, the pooled species×RAIN gait interaction is **+32.73 points**; among final captured camera rows it is **+32.91 points**, versus **+39.66 points** in the independent reference pass records. These are retrospective *selected composition* differences, not a causal decomposition of missingness nor a detector benchmark.

## Biological interpretation and falsifiers

An **ecological hypothesis candidate** emerges: external weather context can coincide with oppositely signed movement-mode changes in different mammalian taxa, rather than imposing a universal direction. However, the sample does not show that rain caused gait changes: animal identity, time/day, locations and weather assignment may confound the contrasts. The 4 CT positions are observational strata, not independent animal-population replicates.

A genuine independent confirmation would require continuous or stratified mammal passages with animal/day/period identifiers, instrumental precipitation during each encounter (not undocumented binary metadata), contemporaneous absence-of-pass exposure for activity-rate endpoints, independent replicate sites and withheld future seasons. A separate camera observation reference should allow biological gait and camera detection effects to be fitted independently.

## Reproduction and governance

- Executable: `research/ecological_process_overlap/rain_gait_reference_replay.py`
- CI: `.github/workflows/tnoa-rain-gait-ecology.yml`
- Successful [source-verified CI run 39215348369](https://github.com/zuizui0223/tnoa/actions/runs/39215348369) including upstream Git blob check, 870 denominator, exact positional/intersection and sensitivity anchors, and no-causal-claim gate.
- The CI uploads derived machine-readable aggregate result `rain_gait_reference_result.json` as an artifact, without redistributing original CSV.
- This analysis was designed after observing the exploratory cross-tab and is **not confirmatory**. It does not validate TNOA's latent target+nuisance regime, wind-pollinator superposition, or the C2 prospective intervention ranking.

## Conclusion within scope

**Among actual CCTV-documented fox and badger passes in this external dataset, the observed relationship between the dataset's RAIN label and walking-vs-faster gait has opposite signs by species, and the pattern persists descriptively after position and measured pass-covariate adjustment.** This motivates, but does not establish, a general hypothesis of species-contingent behavioral responses to environmental conditions.
