# TNOA claim boundary

This file is a hard manuscript guardrail. Claims are grouped by what the current closed-world evidence can support.

## A. Claims currently supportable in a methods paper

### A1. Architecture

TNOA defines target, target-coupled response, nuisance and observability as non-equivalent evidence channels, with optional independent target-absence evidence.

### A2. Positive non-complementary T/N hypotheses

Target and nuisance are not complements, and the framework permits legitimate T+N superposition.

### A3. Abstention as a formal output

The final decision vocabulary includes U whenever the current evidence does not justify a unique target/nuisance inference. Abstention itself is established prior art and is not claimed as novel.

### A4. Low target evidence is not biological absence

Without an independently validated A− channel, low target evidence cannot certify target absence.

### A5. Observability is separate from target and nuisance

Good O does not prove target absence. High nuisance does not necessarily imply low O. Quiet scenes are not automatically observable.

### A6. Closed-world phase geometry

Under the registered synthetic design and frozen observers, resolvability can be mapped over six dimensionless coordinates.

### A7. Negative Pi2 result

The registered narrow ambiguity-ridge prediction near `Pi2 ~= 1` was not supported and was retired.

### A8. Attribution-channel dependence

Within the frozen synthetic representation, direct-visible target evidence is separable from nuisance-only worlds while indirect-only coupled response without independent attribution remains unresolved under the tested observation-safe statistic family.

### A9. Error-criterion principle

A raw score threshold need not retain meaning after representation changes. Operational decisions can instead be tied to predeclared false-attribution or false-certainty criteria.

The historical nuisance protocol used two predeclared negative families, computed a calibration boundary in each, and adopted the maximum boundary as one operational threshold. Manuscript prose should describe the inferential object as a **predeclared family-conditional false-attribution criterion** or **max-over-predeclared-families calibration**, not as classical family-wise error-rate control. The observed held-out rates (`0/43,200` and `1,920/43,200 = 0.04444`) are closed-world empirical rates. They are not distribution-free finite-sample guarantees.

### A10. Frozen final surface

The 30,625-coordinate / 5.88M-world frozen surface and its B/T/N/U rates may be reported as **registered design and provenance facts**. The world count is not evidence strength, and the pooled rates are not ecological prevalences.

### A11. Synthetic downstream ecological estimand

Using known latent truth and the frozen V14b emission map, Paper 1 may report how binary collapse versus retention of B/T/N/U changes inference about **synthetic target prevalence**.

The logical direction of the comparison is structural. Because TARGET/not-TARGET is a deterministic coarsening of B/T/N/U, every latent mixture compatible with the four-state record is also compatible with the binary record. Therefore the B/T/N/U compatible set cannot be wider. This **never-wider property is not an empirical performance result** and should be positioned as an information-ordering/garbling property rather than as TNOA novelty.

The empirical Paper-1 result is the magnitude and design dependence of the information loss under coarsening. Allowed outputs include:

- partial-identification bounds over latent-regime mixtures compatible with the retained observation states;
- identification-width magnitudes comparing full B/T/N/U with its binary coarsening, especially the registered median `0.030` versus `0.266` contrast;
- variation in the amount of narrowing across registered Pi-axis slices;
- the deliberately naive forced-binary prevalence bias as a **secondary comparator diagnostic**, not the primary information-preservation result.

This is a downstream information-preservation result. It is **not** a field-calibrated visit-rate estimator and does not promote any field prevalence claim into Paper 1.

### A12. Post-freeze observation-vocabulary ablation (D3)

Paper 1 may report the deterministic post-freeze comparison among four nested observation vocabularies:

1. TARGET / not-TARGET;
2. TARGET / NUISANCE / other;
3. B / T / N / U with U reasons collapsed;
4. B / T / N / U with no-supported-evidence U separated from overlap/attribution U.

The analysis must always be described as **literature-audit-motivated, post-freeze and not preregistered**. It uses the immutable V14b phase surface and the same 3,003 regime mixtures, with no observer retuning, threshold change or new synthetic world.

Allowed frozen-design results include:

- target-prevalence median widths `0.2656 -> 0.1886 -> 0.02992 -> 0.00408`;
- target+nuisance co-occurrence median widths `0.7231 -> 0.5136 -> 0.10494 -> 0.01484`;
- reason-resolved additional median-width reductions of approximately `86.37%` for target prevalence and `85.86%` for T+N co-occurrence relative to generic B/T/N/U;
- all five estimands in `derived/observation_vocabulary_ablation.json`;
- the registered 34-axis-slice summaries, including that reason-resolved U was never wider than generic U in all 34 slices and strictly improved the median in 27/34 target-prevalence slices and 29/34 slices for each other reported estimand.

The nested never-wider relations are structural consequences of deterministic coarsening. The **numerical magnitude** of the width reductions is the post-freeze empirical result.

Not allowed:

- calling D3 preregistered or confirmatory;
- claiming arbitrary weighting robustness from the 34 registered slices;
- treating reason-resolved U as universally sufficient in field systems;
- inferring field target/nuisance prevalence from the synthetic emission matrix.

### A13. Post-freeze prevalence/composition-weight sensitivity (D4)

Paper 1 may report the reviewer-motivated sensitivity analysis that conditions D1/D3 on known target prevalence and reweights the 3,003 regime compositions directly.

D4 must always be described as **post-freeze and not preregistered**. It does not change the observer, emission matrix, thresholds, latent regimes or synthetic worlds.

Allowed D4 results include:

- only `141/3003 = 4.70%` of uniformly enumerated compositions have known target prevalence `<=0.2`;
- in that rare-target subset, median target-prevalence width is `0.07410` for target/not-target, `0.07386` for target/nuisance/other, `0.000175` for B/T/N/U and `0.0` to numerical tolerance for reason-resolved U;
- under direct composition-level bounded density-ratio reweighting at `kappa=10`, the worst-case weighted-mean fraction of binary width removed by B/T/N/U remains at least `57.5%`;
- under the same `kappa=10` class, reason-resolved U removes at least a further `40.0%` of generic-U weighted-mean width.

Required qualifications:

- the 3,003-point lattice remains a sensitivity design, not an ecological prior;
- the composition-level statistic is a worst-case **weighted-mean reduction ratio**, not a weighted median;
- the bounded class does not imply robustness to arbitrary ecological prevalence distributions;
- rare-target results are conditional on the frozen emission map and do not estimate field rarity or field prevalence.

Not allowed:

- calling D4 preregistered or confirmatory;
- claiming the 3,003 compositions represent natural prevalence frequencies;
- treating `kappa=10` as an ecological prior class;
- claiming universal superiority under arbitrary composition weighting.

## B. Claims allowed only with explicit qualification

### B1. U is mainly attribution/overlap

Allowed wording:

> In the registered frozen design space, most U was assigned to attribution/overlap rather than no-supported-evidence cases.

Stronger wording is allowed only with the explicit weighting class:

> Under bounded density-ratio reweighting of the frozen rows, overlap/attribution remained more than half of U through the tested `kappa=10` class.

Not allowed:

> Most ecological uncertainty is caused by attribution overlap.

### B2. Observation duration and U

Preferred wording:

> In the registered equal-grid design, extending the observation window did not automatically resolve U. After `Pi1=1`, no-supported-evidence U decreased while overlap/attribution U continued to increase.

The reason decomposition is the result. The exact pooled total-U shape is secondary: overlap/attribution contributes about 84–94% of U across the registered Pi1 levels, and the total curve is not robust to moderate reweighting.

Do **not** headline this result as generic `non-monotonicity`. The post-freeze sensitivity audit finds that a monotone non-increasing Pi1 total-U curve becomes feasible by approximately `kappa=1.6` under the tested density-ratio class.

Not allowed:

> Longer monitoring generally increases uncertainty in ecological systems.

### B3. Pi3 boundary

Allowed:

> The exact `Pi3=0` versus `Pi3>0` transition is a structural result of the frozen exact-zero direct-channel observer.

Required effective-axis qualification:

> Although Pi3 was registered at five numeric levels, its marginal B/T/N/U decision vector has only two distinct levels in the frozen surface: zero and positive.

Not allowed:

> Any nonzero direct signal is sufficient for target identification in field ecology.

### B4. Generality

Allowed:

> The architecture is transferable to other sensing domains provided evidence channels and calibration are revalidated.

Not allowed:

> TNOA is validated across ecological sensor domains.

### B5. Superior safety

Allowed:

> TNOA prevents specific logically unsafe shortcuts such as low-target-to-absence inversion and forced T/N exclusivity.

Not allowed without comparative empirical/benchmark evidence:

> TNOA is safer or more accurate than all existing ecological classifiers.

### B6. Weighting robustness

Allowed:

> A qualitative result is robust only within the explicitly reported reweighting class or registered slices/strata actually tested.

For the current post-freeze analyses:

- overlap/attribution dominance of U survives phase-space-row reweighting through `kappa=10`;
- the exact Pi1 total-U shape does **not** survive all moderate reweightings and must remain conditional;
- the small pooled Pi2=1 contrast changes sign within the `kappa=1.25` admissible range and therefore cannot be presented as a stable ridge;
- D3's 34 registered-axis slices demonstrate slice-level nesting and frequent strict median improvement, but do not establish arbitrary ecological weighting robustness;
- D4 separately shows the information-preservation magnitude by known target prevalence and under bounded reweighting of the 3,003 **composition** lattice through `kappa=10`.

Not allowed:

> The phase-surface or vocabulary-ablation conclusions are prior-free or invariant to arbitrary ecological prevalence weighting.

### B7. Effective phase-space dimensionality

Allowed:

> The experiment used six registered dimensionless coordinates, but their marginal separation of the final B/T/N/U response was highly uneven in the frozen design.

Not allowed:

> The ecological problem has exactly two (or any fixed number of) intrinsic dimensions.

### B8. Forced-binary comparator C13

Allowed wording:

> The registered equal-grid comparator has target-present false-negative rate 0.3569, but this quantity is strongly design-compositional: `0.3569 = 0.2*1.0 + 0.8*0.196125` across the registered Pi3 levels.

The zero target false-positive rate is likewise a property of the frozen positive-target observer on the registered non-target regimes. C13 is a **design diagnostic**, not a performance estimate.

Not allowed:

> TNOA achieves zero false positives or prevents 35.69% misses in field sensing.

### B9. Fail-closed field translation pathway

Paper 1 may describe a **prospective implementation sequence** that moves a new sensor domain toward calibrated TNOA inputs. The pathway is implementation guidance, not a new result or field validation.

### B10. Annotation/calibration burden

The D1/D3/D4 information comparisons condition on a frozen, effectively known emission map. This is appropriate for isolating information loss caused by observation coarsening, but it does not answer a fixed-budget measurement-design question.

Required limitation:

> A richer observation vocabulary may require more annotation and calibration effort, and finite-sample uncertainty in a richer emission map could offset part of the identification gain under a fixed validation budget.

Allowed:

> Paper 1 compares information retained **conditional on the frozen calibrated emission map**.

Not allowed:

> TNOA provides more information per annotation, per unit cost or per field hour.

A finite-budget comparison would require a new specification for annotation allocation, grouped dependence, rare-state sampling and emission-matrix uncertainty.

## C. Claims not allowed in Paper 1

Do not claim:

- first non-binary ecological use of classifier output;
- first ecological representation of uncertain, ambiguous or equivocal observations;
- first multilabel coexistence or partial abstention method;
- first continuous-score or threshold-free ecological inference method;
- invention of information ordering, garbling, partial identification or identification widths;
- classical family-wise error-rate control or a distribution-free finite-sample guarantee for the current nuisance calibration;
- field flower-visitor detection accuracy;
- field-calibrated T/C/N/O probabilities;
- field-calibrated biological absence;
- field visit prevalence, abundance or visitation-rate accuracy;
- pollination or visitation effectiveness;
- universal superiority of the TNOA decision rule;
- universal optimality of any alpha, threshold, sampling budget or abstention rate;
- statistical independence of target-side and nuisance-side implementation errors;
- that every no-supported-evidence case is true information absence;
- that nuisance is fully represented by the current synthetic process families;
- that synthetic phase-space frequency or simplex composition frequency equals natural ecological frequency;
- that 5.88M synthetic worlds substitute for external ecological validation;
- that the equal-grid synthetic emission matrix transfers numerically to another camera, site, taxon or sensor domain;
- that the six registered coordinates are six equally effective or intrinsic ecological dimensions;
- that C13 is a field or transferable classifier-performance estimate;
- that D3 or D4 is preregistered;
- that the present analysis establishes information per annotation or cost efficiency;
- that a development shadow implementation, hardware smoke test or prospective calibration protocol constitutes field validation.

## D. Terminology guardrails

Use:

- `target-supported`, not `target-present`, unless truth is known;
- `nuisance-supported`, not `noise`, when referring to the formal N output;
- `no supported evidence`, not `information absent`, unless absence of information is independently established;
- `abstention` or `undetermined`, not `classification error`, for U by default;
- `ordinal evidence`, not `probability`, for a source-system 0/0.5/1 evidence adapter;
- `predeclared family-conditional false-attribution criterion`, not `family-wise error control`, for the manuscript interpretation of the historical nuisance protocol;
- `structural boundary`, not `field threshold`, for the exact-zero synthetic Pi3 result;
- `registered six-coordinate design`, not `six-dimensional ecological complexity`;
- `registered design space`, not `nature`, when reporting phase-surface frequencies;
- `synthetic target-prevalence estimand`, not `field visit-rate estimate`, for the known-truth downstream analysis;
- `post-freeze observation-vocabulary ablation`, not `preregistered vocabulary test`, for D3;
- `post-freeze prevalence/composition-weight sensitivity`, not `ecological prevalence prior robustness`, for D4;
- `bounded reweighting sensitivity`, not `prior robustness`, unless an actual ecological prior has been specified;
- `design-compositional comparator rate`, not `performance`, for C13;
- `field translation pathway` or `implementation template`, not `field validation`, for the prospective fail-closed deployment sequence.

## E. Paper-2 promotion rules

A claim may move from forbidden/conditional to empirical only when the empirical bridge freezes and validates the relevant channel.

Examples:

- O field claims require frozen support measurement/calibration and held-out validation;
- C indirect-rescue claims require independently validated attribution;
- N field claims require effect-specific nuisance calibration;
- absence claims require validated A− or an explicitly different study design;
- empirical visit-rate claims require frozen split/exposure/sampling design and held-out estimates;
- fixed-budget annotation-efficiency claims require a preregistered allocation and emission-uncertainty design.

The A11 synthetic known-truth estimand analysis, A12 vocabulary ablation, A13 prevalence/composition sensitivity and B9 implementation pathway do not satisfy or bypass these empirical promotion rules.

Paper 1 must remain valid if every later empirical result is null or adverse.
