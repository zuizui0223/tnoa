# Independent natural-flower WIND–MULTIPLE-BEHAVIOR field validation path

**Locked source-first exploratory question:** 2026-11-19 before reading individual video-coded behavior outcomes in the publicly archived CSV.
**Scientific role:** ecological interaction/co-occurrence inference only; not TNOA observer calibration or C2 next-measurement prediction.

## Third-party source
Weschler M. (2025/2026), [Insect pollinator behavior as a function of distance to the nearest turbine](https://zenodo.org/records/15447016), version v3, original `WindPollinatorData110823.csv` (publisher MD5 `9bcab4765c4fe5a9edaaf096867caf5b`) and independently archived original analysis `Bee_Behavior_CLEAN.R` (MD5 `5789f8f51791ae6b549abb20a2cde5c9`). Research article published 2026 in *Nordic Journal of Botany*, doi `10.1002/njb.04996`.

Original authors documented **472 insect–flower interactions**, about **45 hours of recording** over **15 days** and **17 physical video sessions** near and up to 28 km from a Wyoming wind facility. Wind speed measured at start/end of each session; many visitors could only be assigned coarse taxa. Visit behavior labels include pollen collection, nectar drinking, crawling into blooms, resting and touching, plus contact with conspecifics/heterospecifics. Multiple behavior labels can be positive in one biological interaction. The original paper *already* reported wind and turbine-distance associations for individual behavior types. Repeating those would not be a new biological discovery.

## New biological estimands
**Primary B1 (within-visit behavioral coexistence):** do pollen collection and nectar drinking co-occur more or less frequently **within the same individual flower interaction** than expected if those two activities were independently assigned within each recorded physical session? The null redistributes one binary label among interaction rows *within exactly the same video session*, preserving session-specific margins, hence cannot be dismissed as site/overall weather composition alone. Do not confuse source behavior co-occurrence with TNOA's nuisance superposition.

**Secondary B2 (environmental modification):** does the **pollen×nectar co-occurrence departure from within-session independence** differ between lower- and higher-wind sessions? This requires at least 12 independently recorded sessions with measured wind, ≥4 sessions on each side of the median wind, and ≥3 physical sites represented in each wind stratum; otherwise **HOLD**. Given 17 sessions and observational wind, any association is exploratory and subject to temporal/site/plant-taxon confounding.

**Secondary B3 (different response axes):** compare across sessions (i) flower interactions per camera-hour if effort source exists; (ii) fraction with pollen; (iii) fraction with nectar; (iv) within-interaction joint behavior. If exact video effort or true zero sessions are missing, HOLD (i). No group of 472 interactions is considered 472 independent weather measurements.

## Admission rules
1. Verify original MD5 of both Zenodo files; source raw rows are never copied into Git. Admit only when video session ID, at least the two behavior flags, wind and site information can be mapped to original author documentation without guessed aliases.
2. Need at least 12 video sessions, 300 total observed interactions, ≥15 behavior-positive pollen observations and ≥15 nectar-positive observations, with each positive represented in ≥5 distinct sessions. Otherwise B1 **HOLD**.
3. Pairwise overlap needs ≥10 observed overlaps OR ≥10 independent-null-expected overlaps. Without the pair support, report rarity/HOLD rather than fitting artificial structure.
4. Use 999 deterministic within-session label permutations (seed `20261119`), shuffling one recorded behavior among interaction rows within each session. Preserve counts, site/time, original other behavior labels and wind, and report observed/expected pair overlap, pairwise excess (observed minus null median), and two-sided plus-one permutation p. No post-hoc choice of the best pair. B1 may remain negative or uncertain.

## Inference limits
The two behaviors can both be coded 1 without representing simultaneous instantaneous actions; the recorded **interaction** is the grain. Co-occurrence within a visit can mean sequence. The original article reports a mean of 1.7 behaviors per interaction, so the existence of multi-behavior records is prior art; the question is *which activities co-occur relative to a matched null*, not whether any do. Camera records can miss behavior, and video frames/individual bees may repeat. Five additional sites near one turbine are not independent geographic wind-farm replicates. Wind is associated with turbine distance, vegetation, temperature, taxon mixture and plant identity; no causal effect or pollen delivery claim.

**Stop if source quality fails**. This fallback is independent from Crall's male orchid-bee scent-bait study and the unresolved Karbassioon survey semantics, but ecological outcome labels will be opened only after its own source gate passes.
