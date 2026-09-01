# Final targeted prior-art audit for TNOA Paper 1

Status: **expanded targeted adversarial audit for manuscript positioning; not a systematic review**.

The purpose is to surrender component-level priority wherever prior art exists and define the residual contribution that remains after direct controls.

## 1. Prior-art families that constrain the claim

The audit covers ecological occupancy/multievent/partial-observation models; continuous-score and AI-assisted ecological inference; classifier-error propagation; selective/reject methods; multilabel partial abstention; evidential uncertainty; calibration/risk control; Blackwell comparison and partial identification; and sensor/adaptive-monitoring neighbours.

The following ideas are established prior art and are **not** TNOA priority claims:

- unresolved, ambiguous or equivocal ecological observations;
- nondetection is not absence;
- non-binary/continuous machine-learning outputs in ecological inference;
- abstention, partial refusal, simultaneous labels and explicit ignorance/conflict;
- calibration and formal risk-control theory;
- deterministic garbling/information ordering;
- partial-identification bounds and identification width.

## 2. Residual methodological object

TNOA's residual contribution is an **upstream process-semantic ecological observation contract** in which target and nuisance are positive non-complements, observability is a separate measurement proposition, coupled response requires attribution before promotion to target support, and biological absence requires evidence distinct from low target support.

The paper then tests two primary consequences:

1. **C6/C7:** after a nuisance representation changed, ranking remained useful but the inherited raw threshold lost its operating meaning; a predeclared family-conditional false-attribution criterion was recalibrated and checked held-out (`0/43,200`, `1,920/43,200 = 0.04444`). This is not classical FWER or distribution-free risk control.
2. **D1/D4:** under frozen known truth, collapsing the core B/T/N/U record to target/not-target substantially expands the compatible set for target prevalence. The Blackwell never-wider direction is structural; TNOA contributes the measured magnitude and its prevalence/weight conditions.

The registered global target-prevalence median widths are about `0.0299207` with B/T/N/U and `0.2656306` after binary collapse. Only `141/3003 = 4.70%` simplex compositions have θ≤0.2, but in that subset medians remain `0.000175` versus `0.07410`; at composition-weight `kappa=10`, B/T/N/U still removes at least `57.5%` of weighted-mean binary width.

## 3. D3 does not establish a semantic-specific reason premium

The prior-art audit originally motivated D3: split the frozen generic U record into the two V14b reason buckets and quantify the additional narrowing. Numerically, target-prevalence median width changed `0.0299207 -> 0.0040780`.

That result initially invited a semantic interpretation: perhaps the **meaning** of the U reasons carried a special downstream information value. A later reviewer-motivated D5 control shows that interpretation is unsupported.

D5 keeps the same generic B/T/N/U matrix and changes only how U is split:

- constant 50:50 split: `0.0299207` — no gain because the added column is redundant;
- 500 unlabeled regime-dependent two-way splits: median `0.0050075`;
- frozen two-reason split: `0.0040780`;
- **48.0%** of random two-way splits are equal to or narrower than the frozen split for target prevalence.

Across all five estimands, the random-equal-or-better fraction ranges `0.480–0.672`. All 500 unlabeled three-way splits produce a full-rank six-regime constraint system and point-identify all five estimands to numerical tolerance.

Therefore D3 remains an informative **refinement/identifiability diagnostic**, but the size of its gain is not shown to be specific to the selected reason semantics. Much of the effect follows from adding non-collinear regime-discriminating observation columns and reducing latent-mixture degrees of freedom. Exact width also depends on column orientation relative to the estimand, so state count alone is not a complete explanation.

## 4. Frozen reason vocabulary is not the reusable API vocabulary

The frozen V14b D3/D5 surface has two unresolved buckets: historical `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`. The latter combines at least simultaneous T+N support and unresolved indirect-only attribution in the frozen decision code.

The later reusable API exposes four U reasons: no-supported-evidence, target+nuisance overlap, missing attribution and insufficient observability. The frozen experiment does **not** provide a one-to-one four-way empirical validation; insufficient observability has no separate D3 column, and overlap versus missing attribution cannot be separated from the frozen aggregate rate.

Reason provenance can still be a scientifically useful design feature because different unresolved situations motivate different follow-up measurements. But that practical semantic justification is independent of D3's identification-width effect and must be validated in the deployment where the reason is used.

## 5. Nearest-neighbour positioning

- continuous-score occupancy preserves a classifier-score stream; TNOA asks what process-semantic record should exist upstream of that downstream inference;
- multievent/partial-observation ecology already models uncertain observed events; TNOA constructs a sensor-side observation contract;
- multilabel abstention already permits coexistence/refusal; TNOA's T/N/O/C/A− propositions have different measurement meanings;
- Blackwell/Manski provide the formal information-ordering/identified-set language; TNOA's contribution is the frozen ecological experiment and measured coarsening magnitude;
- D5 prevents the novelty claim from relying on the number of finer categories or on an untested semantic-information interpretation.

## 6. Strongest safe novelty statement

> TNOA contributes a tested upstream ecological observation contract that separates target, nuisance, observability and attribution propositions; demonstrates that an inherited raw score threshold can lose its operating meaning after representation change and can instead be recalibrated against explicit family-conditional error semantics; and quantifies under frozen known truth the ecological information lost when core B/T/N/U observation-process distinctions are garbled to a binary record. Finer reason provenance remains part of the implementation contract only when independently justified; the present D3/D5 experiment does not demonstrate a semantic-specific information premium for the selected reason labels.

## 7. Prohibited wording

Do not claim:

- first abstaining/non-binary/uncertain-observation ecological method;
- first target+nuisance coexistence or multilabel method;
- family-wise error-rate control or a distribution-free guarantee;
- invention of Blackwell ordering or partial identification;
- that `0.00408` demonstrates semantic reason value;
- that the `86.37%` refinement is caused by the reason meanings;
- that the frozen two-reason surface validates the current four API reasons;
- that adding more categories is intrinsically better.

## 8. Remaining uncertainty

This is a targeted, not systematic, review. Adjacent work may use different terminology or appear in robotics, fault diagnosis, active perception, source separation or evidence theory. That residual uncertainty is a reason to avoid absolute priority claims, not a reason to expand Paper 1 indefinitely.

The paper should claim the tested ecological observation contract, C6/C7 calibration result and D1/D4 measured binary-coarsening consequence, with D3/D5 retained as a self-critical supporting control.
