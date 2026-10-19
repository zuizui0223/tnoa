# Secondary, post-gate exploration: wind and species redistribution WITHIN Euglossa

Date: 2026-10-19. **Secondary design adopted after the genus-level composition gate failed** (399/409 original published bees = *Euglossa*, only 10 = *Eulaema*). The original genus-level HOLD is permanent. This document is frozen **before inspecting within-*Euglossa* species support/counts or any wind–species association**. It is NOT independent preregistration.

## Biological question and limitations

Within the dominant genus `Euglossa`, do wind speed differences among repeated chemical scent-bait sessions relate to **which male bee species** arrive, not just to total numbers? This asks about olfactory foraging/arrival **at artificial scent baits**, *not natural floral interactions or reproductive fitness*. The same known wind/turbulence total-count association is from Crall et al. 2020 and is not our result.

The admissible source is the fixed Crall 2020 Zenodo v2 ZIP, SHA256 `d5b217261e4695e2098bde90576238018ad978c581f4b7799c15e429be19384b`. The only exposure units are the 70 20-minute sampling sessions across 9 sites and 29 dates. 409 uniquely linked bees; 41 unmatched bees excluded, and 3 session-count zeros retained for quantity comparisons.

## Predeclared species support / HOLD gate

1. Identify a species as `genus + species` exactly as in the original `beedata.csv`; do not reassign species from sequence or rename a taxon after inspecting wind contrasts.
2. To enter a named outcome category, require **at least 25 specimens**, occurring in **at least 8 sessions** and **at least 3 physical sites**, counted from all linked records irrespective of wind.
3. Pool remaining named *Euglossa* species into `other_Euglossa`; do not silently discard sparse species or move to genus-level after results.
4. Analysis admissible only if **at least 2 named species** pass, there are **at least 6 sites** with nonzero support, and at least 2 different log-wind values per qualifying site. Otherwise record support-HOLD; do not relax thresholds post outcome. All linked *Eulaema* are excluded from this within-genus response, reported in denominator audit.
5. Unknown genus or species excluded from species-composition outcome with explicit counts, but retained in the independent total-visitation counts.

## Primary fixed model

- Response: joint multinomial categorical counts of qualifying *Euglossa* species plus `other_Euglossa` per **session**; 0-event sessions contribute no conditional composition likelihood but remain in the amount/occurrence dataset.
- Continuous exposure: `log(wind.mean)`; all 70 site-session wind values must be positive, otherwise exclude only offending sessions and report.
- Reduced nuisance/confounding model includes **site fixed effects**, **bait (`scent`) fixed effect**, and **observation date linear day-of-year covariate**.
- Full adds **within-site centred log-wind**, so the intended slope is temporal within-site variation rather than a cross-landscape comparison. Site controls are essential.
- Primary statistic: total multinomial negative-log-likelihood improvement of the full fit over reduced model on the **same session sample**. Evaluate with **999 preseeded session-level permutations** shuffling wind within site × bait *where at least two sessions*; otherwise fixed values. Preserve entire multinomial response vector within its original session, covariate identities and date, and re-fit both reduced/full. This requires sufficient within-stratum permutation support: ≥30 sessions distributed across ≥6 exchangeable site×bait groups each of size ≥2; otherwise inference-HOLD.
- To guard finite-sample overfitting, include penalty-free effect size (within-site per-IQR wind predicted changes in category share) and a **leave-one-site-out** stability analysis. Interpret site-wise directional contrast only if no single site flips an aggregate effect into apparent strong support.
- Report independent date/time and repeated bee/potential cohort dependence, and that permutation exchangeability conditional on site×bait is an untested ecological assumption. Do not use 399 individual bees as independent weather replicates.

## Secondary checks fixed before outcome

- Descriptive taxon richness and named-species shares among sessions with ≥1 bee, plus separate total-count association explicitly marked **Crall et al.'s published endpoint**.
- Scent-stratified, site-stratified positivity and wind range; if scarce, report no independent scent interaction test.
- Turbulence (relative `wind.KE` or `turbInt.3d`) as a **separate exploratory model only** if measures and log-wind do not create critical collinearity. No claim to independently manipulate wind speed and turbulence.
- Sensitivity excluding sessions with fewer than **3 Euglossa individuals** to distinguish composition changes from singletons and zero-heavy instability; no reselecting species categories for this subset.

## Outcome and novelty ceilings

The claim is supported for this *single published dataset* only if (i) the pre-gated species composition model shows a positive empirical deviance gain outside the within-site × bait randomization null, (ii) estimates survive leave-site-out sensitivity and time adjustment, and (iii) the effect is not driven only by session-count imbalance. Otherwise report unconfirmed, adverse or HOLD.

Original authors' positive wind-total-visitation finding is not a discovery. The study offers at most a **new ecological secondary association** in a scent-foraging system, not external source replication, causal proof, species preference or natural pollen delivery. TNOA Paper-1 methods scope remains unchanged.
