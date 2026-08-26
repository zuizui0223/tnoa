# TNOA novelty positioning

Status: **updated after the targeted final prior-art audit** documented in [`FINAL_PRIOR_ART_AUDIT.md`](FINAL_PRIOR_ART_AUDIT.md).

This is not a historical-priority claim and the audit is not a systematic review. The purpose of this document is to state the strongest manuscript novelty claim that remains defensible after comparison with the nearest method families.

## 1. Not reject-option / selective classification

Selective classification and reject-option methods already allow a model to abstain when prediction risk is judged too high. Conformal variants can attach finite-sample or distribution-free error guarantees under their assumptions.

TNOA therefore does **not** claim to invent abstention, risk–coverage control, or guaranteed rejection.

TNOA differs in the structure that determines why a sensor abstains. In TNOA,

\[
U \neq \text{low model confidence only}.
\]

U can arise because:

- the measurement channel has no sufficient support;
- target and nuisance processes are both supported but unique attribution is unavailable;
- a local target response lacks an independent attribution channel;
- the current representation does not encode information that may exist in the world.

The contribution is the ecological process/evidence contract upstream of the reject decision.

## 2. Not partial or set-valued rejection

Partial-reject and set-valued classification methods already permit non-singleton predictions, retaining multiple candidate classes rather than forcing a unique label.

TNOA therefore does not claim that retaining more than one hypothesis is new.

The relevant distinction is semantic: T and N are not merely alternative class labels. They are positive process hypotheses that can both be true in the same world. T+N therefore represents process coexistence, not merely classifier indecision between two mutually exclusive labels.

## 3. Not open-set recognition

Open-set recognition addresses samples from unknown or unseen classes and often rejects them rather than forcing them into known categories.

TNOA U is not synonymous with an unknown class. U may occur even when all process types are known—for example when target and nuisance coexist but the available channels do not license unique attribution.

TNOA therefore does not claim invention of unknown/open-set handling.

## 4. Not belief functions or evidential uncertainty

Dempster–Shafer belief functions, subjective logic and evidential-learning approaches can represent ignorance, conflict, non-singleton hypothesis sets and evidence uncertainty.

TNOA therefore does not claim invention of:

- explicit ignorance;
- evidence conflict;
- non-probabilistic uncertainty;
- incomplete or incomparable decisions.

The TNOA distinction is again architectural and ecological: it predefines what counts as positive T, attributed C, positive N, positive O and optional A−, and then measures where those channels license B/T/N decisions or require U over a frozen process phase space.

## 5. Not ordinary multiclass classification

TNOA does not model target and nuisance as mutually exclusive labels.

\[
T=1,\quad N=1
\]

is allowed and physically expected in some worlds.

The final B/T/N/U vocabulary is a **decision vocabulary**, not a claim that the latent world contains exactly one active class.

## 6. Not ordinary sensor fusion

Sensor-fusion systems often combine heterogeneous measurements to sharpen one latent-state estimate. Conflict-aware fusion can also retain source disagreement.

TNOA keeps several channels separate because they answer different questions:

- direct T asks whether the focal biological event has positive support;
- C asks whether a local response is attributable to that focal interaction;
- N asks whether an exogenous process has a positive effect on inference;
- O asks whether the measurement channel preserved the relevant state;
- A−, if available, asks whether target absence itself has independent support.

Premature fusion is forbidden when it would convert low T into absence, N into `1-T`, or O into `1-N`.

## 7. Not occupancy or imperfect-detection theory

Occupancy and related hierarchical ecological models established that non-detection does not imply absence and that ecological state must be separated from the observation process. False-positive occupancy models also handle both false-positive and false-negative observations.

TNOA therefore does not claim priority for:

- nondetection ≠ absence;
- latent-state / observation-process separation;
- false-positive / false-negative observation modeling.

TNOA operates one level earlier at the sensor-decision interface: it determines what evidence statement a measurement window may emit before that output enters an occupancy, abundance, interaction-rate or other ecological estimator.

## 8. Not ensemble disagreement as acquisition

The early PolliPi/InsePi programme explicitly tested whether observer disagreement should drive finite-budget acquisition. Locked negative generations showed that disagreement can be diagnostically useful without being a robust acquisition score.

TNOA therefore treats disagreement mainly as a development/falsification signal for localising:

- definition defects;
- representation defects;
- missing evidence channels;
- genuine process coupling.

It does **not** claim that high disagreement is intrinsically the best place to sample.

## 9. Relation to adaptive/preferential ecological sampling

Adaptive ecological sampling already studies efficiency and bias when observation effort depends on previous observations or environmental state.

TNOA Paper 1 is upstream of that problem. Its main question is what a single observation window is entitled to say. Sampling-distribution control can be added later, but it is not the novelty claim of Paper 1.

## 10. Main novelty claim after audit

The strongest defensible positioning is:

> **TNOA integrates established ideas about imperfect observation, abstention and evidence uncertainty into a process-preserving ecological sensing architecture in which target and nuisance are independent positive hypotheses, observability is a separate measurement property, coupled responses require attribution, absence requires independent evidence if it is to be certified, and abstention is retained when those channels do not license a unique biological statement. Its methodological contribution is the resulting decision contract and its frozen dimensionless resolvability geometry.**

The contribution is therefore the combination of:

1. positive non-complementary T/N process hypotheses;
2. legitimate T+N superposition;
3. O separate from T/N confidence and nuisance burden;
4. optional independently supported A−;
5. attribution-gated C;
6. reasoned U provenance;
7. finite process-effect nuisance vocabulary;
8. false-certainty rather than inherited-score decision calibration;
9. dimensionless closed-world phase mapping after freeze;
10. negative-generation retention and freeze-before-measurement development.

## 11. What the prior-art audit did and did not establish

The targeted audit did **not** find a directly matching ecological sensor-decision framework that combines all ten elements above and evaluates the resulting decision geometry over a frozen dimensionless process space.

That finding is not evidence for an absolute historical-priority statement. Relevant analogues may exist under different terminology in robotics, fault diagnosis, active perception or evidence theory.

Therefore the paper should claim **methodological integration and tested geometry**, not “first ever”.

## 12. Safe wording for the manuscript

Preferred:

> Existing methods address imperfect detection, abstention, set-valued decisions, evidence uncertainty, sensor fusion and adaptive sampling in partially overlapping ways. TNOA contributes an integrated ecological sensor-decision contract in which target and nuisance may co-occur, observability is a separate positive property of the measurement channel, coupled response requires attribution, and absence cannot be obtained by simply negating target support.

Also acceptable:

> The novelty of TNOA lies in the integrated process/evidence architecture and frozen decision geometry, not in abstention, imperfect-detection correction or uncertainty representation individually.

## 13. Prohibited priority language

Do not write:

- “TNOA is the first abstaining ecological classifier.”
- “No previous method separates these quantities.”
- “TNOA is the first framework to separate process and observation.”
- “TNOA introduces the idea that nondetection is not absence.”
- “TNOA uniquely represents ignorance or conflict.”
- “TNOA is the first method to retain multiple hypotheses.”

Use [`FINAL_PRIOR_ART_AUDIT.md`](FINAL_PRIOR_ART_AUDIT.md) and [`FINAL_CLAIM_AUDIT.md`](FINAL_CLAIM_AUDIT.md) as the submission guardrails.
