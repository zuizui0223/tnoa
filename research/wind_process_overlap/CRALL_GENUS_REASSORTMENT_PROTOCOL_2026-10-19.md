# Crall male-orchid-bee wind × taxon-composition exploratory test

**Frozen as an exploratory analysis plan on 19 October 2026, before opening bee genus counts or wind-conditioned genus contrasts.** Original paper's ecological findings, source schema and publication denominators were already available; this is NOT a prospective or preregistered independent confirmation.

## Why this is ecology, not detection engineering

The focal ecological object is **the identity and number of male orchid bees arriving at chemical scent baits** under variable wind, turbulence and forest landscape context. No natural flower visits, pollen transfer, female reproductive success, or independent observer false negatives are measured by this system. Wind is part of the **physical ecology**, not automatically a TNOA "nuisance" class.

**New comparative question:** does wind change the *composition* of bee genera at scent stations, beyond the already-published association with the **total number** of male bees arriving?

Crall et al. 2020 already reported wind speed and turbulence positively covarying with total scent-bait visitation within sites, and forest cover predicting differences between sites. **These are source-author discoveries, not ours.** This independent reanalysis is not advertised as the first study of wind, pollinators, or community composition.

## Fixed raw source, identity and admission

- Article: Crall et al. (2020), *Biology Letters* 16, 20200103, DOI `10.1098/rsbl.2020.0103`.
- ZIP: [Zenodo v2](https://zenodo.org/records/3675327), DOI `10.5281/zenodo.3675327`, original SHA256 `d5b217261e4695e2098bde90576238018ad978c581f4b7799c15e429be19384b`.
- Exactly **70 observation sessions** (including 3 zero-bee sessions) at **9 sites** across **29 observation days**, two scent compounds (cineole/methyl salicylate).
- Of **450 bee specimen records**, **409** join uniquely by the **date × site × scent** combination to the 70 included sessions. The remaining **41** observations are from dates outside the included session frame; exclude them without imputing wind. The joined 409 exactly equals the sum of the session `count` field and matches original article. Seven joined individual `time` values differ from session start time; use date/site/scent, not exact time, as the documented unique matching key.
- Each session is the ecological count/composition replicate; 409 bees are **not** 409 independent wind conditions. `keep`=1 across all 70; all sessions have measured wind.
- Missing/ambiguous taxonomic genus labels must be reported and retained as `unknown` for denominator audit, never guessed. Exclude only from the identified-composition subset, not from total visit counts.

## Locked outcomes and gating

**Already published reference outcome (not novelty):** `count` per 20-minute scent-bait session, including zero sessions. Show descriptive comparison to establish what the new taxon-composition endpoint adds, not a new independent claim of wind-driven abundance.

**Primary exploratory endpoint:** multinomial distribution of taxonomic `genus` across the matched bee records, conditioned on a session having at least one identified bee. Group all named genera with **≥15 identified bees across ≥8 distinct sessions** as individual categories; pool others into an explicit `other_identified` group. Eligibility is based only on total taxonomic support, not wind associations. If fewer than two categories have enough support (or wind varies too little within sites), classify the primary endpoint **HOLD**, do not fit a forced significance model.

**A priori environmental exposure**: `log(wind.mean)` (positive m/s), analyzed as a continuous variable; standardized by pooled interquartile distance for reporting. Distinguish `wind.mean` from `wind.KE` and `turbInt` (not interchangeable). Check values/zeros/NA before testing. If `wind.mean <= 0`, exclude such sessions from log-wind fits but retain them in source audit.

**Primary composition model**: session-level multinomial genus counts (including zero-count genus cells), comparing a site+ bait+ calendar-day control model to the same model + within-site standardized log wind. Include site as a fixed effect, `scent` as a factor, day of study as a linear covariate (support sensitivity if date slope makes results unstable). A genus label never substitutes for a species-specific pollination role.

**Primary test**: reduction in multinomial deviance when adding wind (joint all-genus coefficient comparison). Conduct at least **999 permutation replicates** assigning wind values among sessions within each physical site; preserve observed bee counts/genus counts, bait, dates and sites; control exposures in each permuted fit. The permutation tests a conditional, *exchangeability-assuming* association, not randomization of wind, and is not a population-level causal test. If convergence or rank fails, report method HOLD, not unqualified p-values.

**Secondary interpretation**: (i) direction and uncertainty of pre-supported genus-specific coefficients from full model, (ii) leave-one-site-out sign stability, (iii) check bait-stratified support and whether site×bait wind variation allows identifiable comparison; if not, state unsupported. (iv) report sensitivity to relative turbulence (`turbInt.3d` and `wind.KE`) only if field semantics and finite support admit modeling without collinearity. Do not invent a 2×2 factorial intervention from observational wind.

**Separate reallocation metric**: compare normalized between-session genus compositions (weighted Hellinger or Bray–Curtis) against wind differences **within sites** as an effect-size companion. Beware low-count sessions; evaluate sensitivity excluding <3-bee sessions. Permutation must occur at the session level, not at the individual-bee level.

## Interpretation and falsification

- **Supported ecological reallocation hypothesis** requires a conditional wind-composition association surviving at least the site-stratified permutation, plus no single site controlling the entire directional result. A positive joint test alone does not prove wind influences genus identity causally.
- **Null/adverse result**: report if genus composition does not change with wind after controlling site, bait and calendar time, even if total visits change. This would be biologically informative—wind could modulate attraction/encounter rates without strong genus sorting in this scent-foraging system.
- **Nonidentifiability**: if the 409 matched bees do not provide reliable genus/session support, stop. Do not treat presence of multiple bee species in original as sample-size equivalence for taxonomic wind responses.
- **No result borrowing:** UK Balfour and Australian Coates Dryad data currently return anti-bot HTML from direct download, and no raw ecological outcome has been opened from those sources. A cross-study generality claim is **HOLD** pending independent source admission.
- **Novelty boundary:** any finding here is a secondary analysis of previously published data. Do not overwrite source-owner Crall publication claims, TNOA Paper 1, C2 TREE Opinion, REC, or InsePi physical observer research.

## Fixed evaluation outputs

A machine-readable report must include raw source SHA, counts and exclusions, per-genus category totals, number of suitable sessions, site/scent/date wind support, control/full model deviance and convergence, site-stratified permutation distribution/p-value if valid, leave-site-out diagnostics, and original-study versus new analysis claim boundaries. No significant finding may be generated by post-result changing the 15-bee/8-session eligibility gate or the permutation strata.
