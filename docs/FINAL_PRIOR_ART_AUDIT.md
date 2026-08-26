# Final targeted prior-art audit for TNOA Paper 1

Status: **completed targeted audit for manuscript positioning**.

This is not a systematic review. Its purpose is narrower: test the strongest TNOA novelty statement against the method families most likely to invalidate it.

## 1. Search scope

The final audit explicitly checked the following neighbouring families:

- selective classification / reject option;
- conformal classifiers with rejection guarantees;
- partial and set-valued reject options;
- open-set / open-world recognition;
- Dempster–Shafer belief functions and evidential reasoning;
- evidential deep learning / subjective-logic uncertainty;
- ecological occupancy and imperfect-detection models;
- occupancy models with false-positive and false-negative observation errors;
- hierarchical/state-space process-versus-observation models;
- camera-trap component detection processes;
- sensor fusion and conflict-aware multisource reasoning;
- adaptive/preferential ecological sampling.

The search was deliberately adversarial: a neighbouring framework only needs to invalidate a component-level novelty claim, not reproduce the entire TNOA implementation.

## 2. Component claims that are NOT novel

### 2.1 Abstention / rejection

Reject-option and selective-classification methods already formalise withholding a prediction to reduce predictive risk. Conformal reject methods can additionally provide finite-sample or distribution-free error guarantees under their assumptions.

Therefore TNOA must not claim to invent:

- abstention;
- risk–coverage trade-offs;
- error-controlled rejection;
- confidence-based refusal to classify.

### 2.2 Partial or set-valued decisions

Partial-reject and set-valued classifiers can retain multiple hypotheses rather than force a singleton class.

Therefore TNOA must not claim that retaining more than one plausible hypothesis is itself new.

### 2.3 Unknown / open-set handling

Open-set recognition explicitly addresses samples that belong to classes unavailable during training and allows rejection of unknowns.

Therefore TNOA must not equate its U state with a novel form of open-set recognition or claim that handling unknown conditions is new.

### 2.4 Ignorance, conflict and incomplete evidence

Belief-function / Dempster–Shafer methods and subjective-logic/evidential approaches can represent ignorance, conflicting evidence, belief assigned to sets of hypotheses, and decisions that remain incomplete or incomparable.

Therefore TNOA must not claim to invent:

- explicit ignorance;
- evidence conflict;
- uncertainty represented separately from a singleton class probability;
- undecided decision states under incomplete evidence.

### 2.5 Non-detection is not absence

Occupancy and imperfect-detection methods established long ago that nondetection does not imply absence when detection probability is below one. Generalized occupancy models also handle both false-negative and false-positive observations.

Therefore TNOA must not claim to be the first ecological framework to separate:

- biological state from observation;
- nondetection from absence;
- false-positive from false-negative observation errors.

### 2.6 Process and observation separation

Hierarchical and state-space ecological models explicitly distinguish latent ecological process from observation process/error.

Therefore the process/observation split by itself is not a TNOA novelty.

### 2.7 Sensor fusion and evidence conflict

Multisensor and evidential fusion methods already combine heterogeneous evidence and explicitly study conflict among sources.

Therefore TNOA must not claim to invent conflict-aware sensor fusion.

### 2.8 Adaptive / preferential sampling

Adaptive ecological sampling and preferential-sampling literature already treats data-dependent observation as a design problem that can alter the sampled distribution.

Therefore the historical PolliPi/InsePi allocation work is not a basis for claiming invention of adaptive ecological sampling.

## 3. What survives the audit

No audited neighbouring family was found that, in the ecological sensor-decision setting, simultaneously makes all of the following the explicit object of the method:

1. **T and N are positive, non-complementary process hypotheses.**
2. **T+N coexistence is legitimate** and is not automatically converted to conflict, error, or one winning class.
3. **O is a positive measurement-support variable** separate from target confidence and nuisance burden.
4. **Low T cannot certify absence.**
5. **A− is optional and must be independently supported** if certified absence is desired.
6. **C is only usable when a local response is independently attributed** to the focal target interaction.
7. **U has reasoned provenance**: unsupported evidence is distinct from overlap/attribution and from representation defects.
8. **N is defined by finite process effects on inference** (mimic, mask, corrupt attribution, degrade support), not an open-ended cause list.
9. **Operational boundaries are tied to false-certainty contracts** rather than inherited raw score scales.
10. **Resolvability is measured over a dimensionless process phase space** after observer rules are frozen.
11. **Failed generations are retained as scientific provenance** and constrain later claims.

The defensible novelty is therefore the **integrated ecological sensing architecture and its experimentally frozen decision geometry**, not any one primitive.

## 4. Strongest safe novelty statement

Preferred manuscript wording:

> TNOA integrates established ideas about imperfect observation, abstention and evidence uncertainty into a process-preserving ecological sensing architecture in which target and nuisance are independent positive hypotheses, observability is a separate measurement property, absence requires independent evidence if it is to be certified, and abstention is retained when the available channels do not license a unique biological statement. Its methodological contribution is the resulting decision contract and its frozen dimensionless resolvability geometry.

Shorter wording:

> The novelty of TNOA lies in the integrated process/evidence architecture and frozen decision geometry, not in abstention, imperfect-detection correction or uncertainty representation individually.

## 5. Wording that is now prohibited

Do not write:

- “TNOA is the first abstaining ecological classifier.”
- “TNOA is the first method to separate process and observation.”
- “TNOA introduces the idea that nondetection is not absence.”
- “TNOA is the first method to represent ignorance or conflicting evidence.”
- “TNOA uniquely allows multiple hypotheses.”
- “No previous method can retain target and nuisance simultaneously.”

The last statement is too broad even though the audited nearest ecological-sensing literature did not reveal the same full architecture.

## 6. Most important neighbours to cite explicitly

The manuscript should explicitly cite and distinguish at least:

- El-Yaniv & Wiener 2010; Geifman & El-Yaniv 2017/2019; Hendrickx et al. 2024 — selective/reject classification;
- Karlsson & Hössjer 2024 — partial/set-valued reject options;
- García-Galindo et al. 2024 and Szabadváry et al. 2025 — conformal reject guarantees;
- Geng et al. 2021 — open-set recognition;
- Denœux 2019 and Gao et al. 2026 — belief/evidential uncertainty and decision under ignorance;
- MacKenzie et al. 2002 — imperfect detection and nondetection/absence separation;
- Royle & Link 2006 — simultaneous false-positive/false-negative occupancy errors;
- Royle & Dorazio 2008; Auger-Méthé et al. 2021 — hierarchical/state-space process/observation separation;
- Hofmeester et al. 2019; Findlay et al. 2020 — component detectability in camera sensing;
- Henrys et al. 2024; Pescott 2025 — adaptive ecological sampling.

## 7. Remaining uncertainty

This audit reduces but cannot eliminate prior-art risk. TNOA should still avoid absolute priority claims because:

- relevant work may exist under different terminology in robotics, fault diagnosis, active perception or evidence theory;
- the audit is targeted, not systematic;
- conceptual similarity does not require identical notation.

This residual uncertainty is handled by claiming the tested **integration and decision geometry**, not historical priority for each concept.
