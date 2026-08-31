# Final targeted prior-art audit for TNOA Paper 1

Status: **expanded targeted adversarial audit for manuscript positioning**.

This is not a systematic review. Its purpose is narrower: search the method families most likely to invalidate TNOA's strongest novelty statement, surrender component-level priority wherever prior art exists, and identify the residual contribution that remains defensible.

## 1. Search scope

The audit covers:

- ecological occupancy, multistate and multievent models with imperfect, ambiguous, equivocal or partial observations;
- continuous-score and AI-assisted ecological inference;
- ecological models that propagate image/audio classification error;
- selective classification, reject options, conformal/risk-controlling prediction sets and multilabel partial abstention;
- open-set recognition and evidential/belief-function uncertainty;
- confidence calibration and uncertainty under dataset shift;
- Blackwell comparison/garbling of statistical experiments and partial identification;
- camera-trap component detection, sensor fusion and adaptive/preferential sampling.

The search is deliberately adversarial. A neighbouring method only needs to invalidate one priority claim; it need not reproduce the full TNOA architecture.

## 2. Strong claims that prior art invalidates

### 2.1 TNOA is not the first ecological method to retain uncertain observations

Multievent models explicitly accommodate uncertain state assignment [@pradel2005multievent]. Multistate occupancy models allow multiple ecological states under imperfect detection and ambiguous state information [@mackenzie2009multistate]. Later ecological methods explicitly retain uncertain, ambiguous, equivocal or partially observed events [@hollanders2022stateuncertainty; @campbellgrant2023partial].

Therefore TNOA must not claim:

- the first ecological unresolved observation;
- the first ecological representation of ambiguous/equivocal events;
- the first separation of nondetection from absence.

### 2.2 TNOA is not the first non-binary use of machine-learning output in ecological inference

A continuous-score occupancy model already incorporates uncertain machine-learning scores directly without first thresholding them to detections [@rhinehart2022continuous]. AI-to-inference workflows explicitly address how automated classifier confidence and uncertainty enter ecological analyses [@cowans2026aiworkflow; @kitzes2026aiworkflow]. Classification-error models and empirical audits show that confusion and systematic classifier bias alter ecological results [@spence2025classification; @santoro2025bias].

Therefore TNOA must not claim:

- the first threshold-free ecological use of classifier output;
- the first continuous-score ecological inference method;
- the first recognition that AI error propagates into ecological inference.

### 2.3 Abstention, coexistence and partial decisions are established machine-learning ideas

Selective/reject methods formalize abstention [@elyaniv2010selective; @hendrickx2024reject]. Partial/set-valued and multilabel abstention methods can preserve multiple labels and refuse only part of a multilabel decision [@karlsson2024partialreject; @nguyen2020partialabstention]. Open-set and evidential methods represent unknowns, ignorance and conflict [@geng2021openset; @denoeux2019belief; @gao2026evidential].

Therefore TNOA must not claim:

- invention of abstention;
- invention of simultaneous labels or partial refusal;
- invention of explicit ignorance or conflict.

T+N coexistence remains important to TNOA's semantics, but coexistence alone is not a historical-priority claim.

### 2.4 Error control and calibration have stronger formal precedents

Conformal/reject methods and risk-controlling prediction sets can provide formal error guarantees under specified assumptions [@garciagalindo2024conformalreject; @szabadvary2025reject; @bates2021riskcontrol]. Confidence calibration is known to depend on model representation, and predictive uncertainty can degrade under dataset shift [@guo2017calibration; @ovadia2019shift].

The TNOA nuisance experiment therefore supports a narrower claim: a historical raw threshold lost its registered operating meaning after representation change, while a **predeclared family-conditional false-attribution criterion** could be recalibrated on the new score representation and checked held-out. The observed rates `0/43,200` and `1,920/43,200 = 0.04444` are closed-world empirical checks. They are not classical family-wise error-rate control and not a distribution-free finite-sample guarantee.

### 2.5 Deterministic coarsening and partial-identification bounds are not TNOA inventions

Blackwell's comparison of experiments formalizes information loss under garbling [@blackwell1953comparison]. Partial-identification theory formalizes identified sets when data and assumptions do not point-identify an estimand [@manski2005partial].

Therefore the statement that a deterministic coarsening cannot be more informative is structural prior art. TNOA's empirical result is the **magnitude and ecological consequence** of that information loss for its frozen observation experiment.

## 3. What remains distinct

The residual object is not a generic uncertain label or a single continuous target-confidence score. TNOA defines an **upstream process-semantic observation contract** in which:

1. T is positive support for the focal target process;
2. N is separate positive support for an exogenous process that can mimic, mask, corrupt attribution or degrade support;
3. T and N are non-complementary and may coexist;
4. O is a measurement-support proposition rather than target confidence or nuisance burden;
5. C is a local target-coupled response that is not promoted without independent attribution;
6. A−, if used, requires independent positive support for absence;
7. U retains reason provenance rather than serving only as a generic reject label;
8. process-support decisions are calibrated to declared error semantics rather than inherited raw-score values;
9. the resulting record is evaluated by the downstream ecological information lost when it is deliberately coarsened.

The strongest contribution is therefore functional rather than combinatorial: **define a process-semantic observation record upstream of ecological inference, then experimentally measure the decision-relevant information destroyed when that record is garbled to coarser vocabularies.**

## 4. New post-freeze evidence motivated by this audit

The prior-art comparison raised a question not answered by the original D1 analysis: if uncertain events and non-binary outputs are already known, does TNOA gain anything specifically from preserving the **reason** for unresolvedness?

A deterministic post-freeze vocabulary ablation on the immutable V14b surface addresses that question. It is explicitly literature-audit-motivated and **not preregistered**. No observer, threshold or synthetic world was changed.

Across the same 3,003 six-regime mixtures, median target-prevalence identification width was:

- TARGET/not-TARGET: `0.2656`;
- TARGET/NUISANCE/other: `0.1886`;
- B/T/N/U: `0.02992`;
- B/T/N/U with no-support and overlap/attribution U separated: `0.00408`.

For T+N co-occurrence prevalence the corresponding widths were `0.7231`, `0.5136`, `0.10494` and `0.01484`. Reason-resolved U reduced median width by a further `86.37%` for target prevalence and `85.86%` for T+N co-occurrence relative to generic B/T/N/U. All five fixed estimands and all 34 registered-axis slices are reported in `docs/OBSERVATION_VOCABULARY_ABLATION.md`.

The nested never-wider direction is structural; the numerical reductions are the post-freeze empirical result.

## 5. Nearest-neighbour comparison

The detailed comparison is retained in `docs/NEAREST_NEIGHBOUR_METHODS.md`. The key distinctions are:

- continuous-score occupancy preserves one classifier-score stream; TNOA preserves heterogeneous process propositions;
- multievent/partial-observation ecology models uncertain observed events; TNOA constructs the upstream event vocabulary from sensor evidence;
- multilabel abstention allows coexistence/refusal among labels; TNOA's channels make different propositions and have different evidential requirements;
- Blackwell/Manski supply the information-ordering and identified-set language; TNOA contributes the frozen ecological observation experiment and measured loss magnitude.

## 6. Strongest safe novelty statement

> TNOA contributes a tested upstream ecological observation contract that separates positive target support, positive nuisance support, measurement observability, attribution-gated coupled response and independently supported absence; preserves reason-resolved unresolved observations before downstream analysis; calibrates process-support decisions against predeclared family-conditional errors; and quantifies under frozen known truth the decision-relevant information lost when this record is garbled to coarser observation vocabularies.

This wording deliberately does not claim priority for abstention, uncertain ecological events, continuous classifier scores, multilabel coexistence, calibration theory, information ordering or partial identification.

## 7. Prohibited wording

Do not write:

- “TNOA is the first abstaining ecological classifier.”
- “TNOA is the first ecological method to retain uncertain observations.”
- “TNOA is the first method to use non-binary classifier output in ecological inference.”
- “TNOA is the first method to allow target and nuisance to coexist.”
- “TNOA proves family-wise error-rate control.”
- “TNOA provides a distribution-free risk guarantee.”
- “TNOA discovers that richer deterministic records are never less informative.”
- “No previous method can retain multiple hypotheses or conflicting evidence.”

## 8. Remaining uncertainty

This audit reduces but cannot eliminate prior-art risk because it is targeted rather than systematic, relevant work may use different terminology, and adjacent results may exist in robotics, fault diagnosis, active perception, source separation or evidence theory. Those outer-ring literatures are reasons to avoid absolute priority claims, not reasons to delay Paper 1 until every technical field has been systematically reviewed.

The paper should therefore claim a tested **ecological observation contract and measured coarsening consequence**, not historical ownership of its individual mathematical or machine-learning ingredients.
