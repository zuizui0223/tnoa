# TNOA novelty positioning

This document states the current novelty claim **before final literature audit**. The categories below are positioning targets to verify systematically against the literature before submission.

## 1. Not merely reject-option / selective classification

Neighbouring methods often allow a classifier to abstain when predictive confidence is low.

TNOA differs in what abstention means.

In TNOA,

\[
U \neq \text{low model confidence only}.
\]

U can arise because:

- the measurement channel lacks support;
- target and nuisance processes are genuinely superposed;
- a local biological response lacks independent attribution;
- positive evidence channels do not support a unique inference;
- information may exist but is not represented adequately by the current observer.

Thus abstention is defined by the **epistemic structure of the observation problem**, not only by posterior uncertainty of one classifier.

## 2. Not ordinary multiclass classification

TNOA does not model target and nuisance as mutually exclusive labels.

\[
T=1,\quad N=1
\]

is allowed and sometimes expected.

This makes the method closer to process decomposition than to a `target vs noise` classifier.

The final B/T/N/U vocabulary is a decision vocabulary, not a statement that the latent world has only one active process.

## 3. Not ordinary sensor fusion

Sensor-fusion systems often combine multiple measurements to improve one latent-state estimate.

TNOA instead preserves epistemically different channels because they answer different questions:

- direct target evidence asks whether the focal event is supported;
- coupled evidence asks whether a local response is attributable to the focal interaction;
- nuisance evidence asks whether an exogenous process can alter inference;
- observability asks whether the measurement channel preserved the relevant state;
- A−, if available, asks whether target absence is independently supported.

Premature fusion would erase distinctions needed to interpret non-detection and superposition.

## 4. Not ensemble disagreement as acquisition

The early PolliPi/InsePi programme explicitly tested whether observer disagreement should drive finite-budget acquisition.

Locked negative generations showed that disagreement can be diagnostically useful without being a robust allocation score.

TNOA therefore treats contradiction/disagreement primarily as:

- a way to localise definition defects;
- a way to localise representation defects;
- a way to expose missing information channels;
- a development/falsification signal.

It does **not** assume that high disagreement is intrinsically the best place to sample.

## 5. Not merely uncertainty quantification

Uncertainty quantification estimates uncertainty around a model output. TNOA adds distinctions that are external to the target model itself.

Examples:

- a sensor may be certain that it saw little target evidence while the scene was unobservable;
- target evidence and nuisance evidence may both be strong;
- a strong local response may still be unattributed;
- absence may remain uncertified despite excellent observability.

The method therefore separates uncertainty about an estimate from uncertainty about whether the requested inference is justified.

## 6. Relation to missing-data and observability concepts

TNOA shares concerns with missing-data theory and observability analysis but places them inside an ecological sensing decision architecture.

The key distinction is:

\[
O\text{ is a positive measurement-support variable, not a residual category.}
\]

A quiet window is not automatically observable, and a noisy window is not automatically unobservable.

## 7. Relation to preferential/adaptive ecological sampling

Adaptive ecological sensing changes the observation distribution because the system records more intensively under selected conditions.

Earlier generations of the project addressed this explicitly through exploration guards and preserved negative results about disagreement-based allocation.

TNOA's current paper is narrower: it focuses on **safe inference from an observation window**. Sampling-distribution control is historical and potentially complementary, but should not dominate the present manuscript unless needed to explain why observation-process variables must remain explicit.

## 8. Main novelty claim

The strongest current positioning is:

> **TNOA is a process-preserving ecological sensing framework that separates positive target evidence, target-coupled attribution, exogenous nuisance processes, measurement observability and optional independent absence evidence, and uses abstention to control false certainty when those channels do not justify a unique biological decision.**

The contribution is therefore not one new classifier. It is a **decision architecture for ecological observation**.

## 9. What must be established in the literature audit

Before submission, the literature review must test whether an existing framework already combines all of the following:

1. non-complementary T and N hypotheses;
2. explicit legitimate T+N superposition;
3. O separated from both T and N;
4. low target evidence explicitly forbidden from implying absence;
5. optional independently validated A−;
6. target-coupled response requiring independent attribution;
7. U derived from evidence geometry rather than confidence alone;
8. operational thresholds tied to false-certainty risk contracts;
9. dimensionless phase-space mapping of resolvability;
10. negative-generation-preserving, freeze-before-evaluation development.

Novelty should be claimed at the **combination and formal integration** level unless literature review establishes stronger component-level novelty.

## 10. Safe wording for the manuscript

Preferred:

> Existing methods address abstention, sensor fusion, uncertainty, adaptive sampling, and observability in partially overlapping ways. TNOA integrates a distinct set of constraints motivated by ecological sensing: target and nuisance may co-occur, observability is a separate positive property of the measurement channel, and absence requires evidence not obtainable by simply negating target support.

Avoid until literature audit is complete:

> No previous method separates these quantities.

or

> TNOA is the first abstaining ecological classifier.
