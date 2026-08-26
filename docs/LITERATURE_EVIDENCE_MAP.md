# Literature evidence map for TNOA Paper 1

Status: **targeted final evidence map complete; not a systematic review**. The adversarial synthesis and priority boundary are recorded in [`FINAL_PRIOR_ART_AUDIT.md`](FINAL_PRIOR_ART_AUDIT.md).

The purpose here is to identify the nearest methodological neighbours that a reviewer is likely to invoke, state the overlap precisely, and prevent TNOA from claiming ownership of established ideas.

## 1. Selective classification / reject option

Selective classification trades coverage against predictive risk: a model may abstain on examples for which prediction is unsafe [@elyaniv2010selective; @geifman2017selective; @geifman2019selectivenet; @hendrickx2024reject]. Conformal reject methods add explicit error guarantees under their assumptions [@garciagalindo2024conformalreject; @szabadvary2025reject].

### Shared ground

- abstention is a valid output;
- risk can be controlled by sacrificing coverage;
- overconfident predictions should be avoided.

### TNOA difference

TNOA does not define U from the confidence of one classifier. Its evidence architecture contains positive T, attributed C, positive N, positive O and optional A− channels. U can persist when several channels are strong because process coexistence does not necessarily license unique attribution.

**Claim boundary:** TNOA does not invent abstention, risk–coverage control or error-guaranteed rejection.

## 2. Partial / set-valued reject options

Partial-reject methods can return non-singleton class sets rather than either a single class or complete rejection [@karlsson2024partialreject].

### Shared ground

- a decision need not collapse immediately to one label;
- multiple hypotheses can be retained.

### TNOA difference

T and N are not simply alternative classes in a set-valued prediction. They are process hypotheses that can physically co-occur. T+N is therefore a valid latent/process configuration rather than merely uncertainty between mutually exclusive labels.

**Claim boundary:** retaining multiple hypotheses is not itself novel.

## 3. Open-set / open-world recognition

Open-set recognition explicitly detects or rejects samples belonging to classes outside the known training taxonomy [@geng2021openset].

### Shared ground

- a system should not force every observation into a known singleton class;
- unknown conditions should be allowed to remain unresolved.

### TNOA difference

TNOA U is not an unknown class. It can occur when all process types are known but the measurement structure cannot uniquely attribute a biological statement—for example when T and N are both supported or when C lacks a link channel.

**Claim boundary:** TNOA does not invent unknown/open-set handling.

## 4. Belief functions, evidential reasoning and ignorance

Belief-function theory explicitly represents ignorance, conflict and belief over sets of hypotheses [@denoeux2019belief]. Evidential deep-learning approaches likewise model uncertainty beyond a conventional softmax probability [@gao2026evidential].

### Shared ground

- incomplete evidence need not be converted to a sharp posterior;
- conflict and ignorance can be represented explicitly;
- a decision can remain unresolved.

### TNOA difference

TNOA is not proposed as a new uncertainty calculus. Its contribution is to fix ecological sensor semantics before uncertainty is combined: what qualifies as positive T, attributed C, positive exogenous N, measurement support O, and optional A−. The closed-world experiment then measures the decision geometry induced by those semantics.

**Claim boundary:** TNOA does not invent ignorance, conflict representation or non-probabilistic evidence fusion.

## 5. Imperfect detection and occupancy models

MacKenzie et al. established the core ecological principle that nondetection does not imply absence when detection probability is below one [@mackenzie2002occupancy]. Royle & Link extended occupancy modeling to simultaneous false-positive and false-negative errors [@roylelink2006occupancy]. Hierarchical ecological models formalize latent ecological and observation components more generally [@royle2008hierarchical].

### Shared ground

- nondetection is not biological absence;
- biological state and observation process must be separated;
- false positives and false negatives are distinct observation errors.

### TNOA difference

Occupancy methods infer latent states from replicated observations. TNOA operates earlier, at the sensor-decision interface: before a detection/non-detection datum is emitted, it asks whether the current window supports T, N, both, neither, adequate O, or independent A−.

A TNOA record can therefore become a provenance-rich input to occupancy or abundance analysis rather than a replacement for it.

**Claim boundary:** TNOA is not the first framework to distinguish nondetection from absence or process from observation.

## 6. State-space ecological observation models

State-space models separate latent process dynamics from observation error in ecological time series [@augermethe2021statespace].

### Shared ground

- process and observation are distinct;
- uncertainty has multiple sources;
- measurement error should not be absorbed into biological dynamics.

### TNOA difference

TNOA does not estimate a population trajectory. Its object is the **decision entitlement of an individual sensor window** under multiple positive process/evidence hypotheses. The main question is “what statement may this sensor emit?”, not “what latent trajectory generated the observations?”.

## 7. Camera-trap detection processes

Camera-trap research decomposes detectability into encounter, triggering, registration and image-quality processes and documents false-negative mechanisms [@hofmeester2019framing; @findlay2020detection].

### Shared ground

- detection depends on animal, environment, camera and setup;
- observation failure should not silently become absence;
- component failure modes matter.

### TNOA difference

TNOA turns measurement support into an explicit positive O object and separates O from exogenous N. A scene can be noisy but observable or quiet but unobservable. N is furthermore defined by its effects on inference—mimic, mask, corrupt attribution, degrade support—rather than by a list of environmental causes.

## 8. Sensor fusion and conflict-aware multisource reasoning

Sensor-fusion and evidence-fusion systems combine heterogeneous sources and may explicitly handle source conflict.

### Shared ground

- evidence channels have different failure modes;
- source disagreement can matter;
- uncertainty must propagate through decisions.

### TNOA difference

TNOA does not require all channels to collapse into one posterior or one winning class. Some combinations are deliberately terminal as U or retained as T+N process coexistence. Its defining operation is semantic preservation until an ecological statement is licensed.

**Claim boundary:** conflict-aware fusion is established prior art.

## 9. Adaptive and preferential ecological sampling

Adaptive sampling can improve efficiency while also creating preferential-sampling bias [@henrys2024adaptive; @pescott2025adaptive].

### Shared ground

- data-dependent effort changes the sampled distribution;
- selection rules belong to the inferential design.

### TNOA difference

TNOA Paper 1 is upstream of acquisition. Earlier PolliPi/InsePi generations tested disagreement-driven allocation and retained its failure. Current TNOA treats disagreement primarily as a development/falsification signal and asks what a window may safely report before deciding whether to sample more.

## 10. Closest defensible novelty statement

After the targeted final audit, the strongest safe claim is:

> TNOA integrates established ideas about imperfect observation, abstention and evidence uncertainty into a process-preserving ecological sensing architecture in which target and nuisance are independent positive hypotheses, observability is a separate measurement property, coupled responses require attribution, absence requires independent evidence if it is to be certified, and abstention is retained when those channels do not license a unique biological statement. Its methodological contribution is the resulting decision contract and its frozen dimensionless resolvability geometry.

The tested integration comprises:

1. positive, non-complementary T and N;
2. legitimate T+N coexistence;
3. O independent of T/N score semantics;
4. optional independently supported A−;
5. attribution-gated C;
6. reasoned U provenance;
7. finite nuisance process-effect vocabulary;
8. false-certainty decision contracts;
9. dimensionless phase-space measurement after observer freeze;
10. retained failed generations and freeze-before-measurement development.

## 11. Prior-art falsification condition

The integration-level novelty claim should be weakened further if prior work is found that already combines, in an ecological sensor-decision architecture, the ten elements above **and** evaluates its resolvability geometry over controlled process regimes after decision rules are frozen.

Finding prior work on any individual component does not support a priority claim for TNOA; most individual components have explicit prior art.

## 12. Core reference set for manuscript positioning

The bibliography in `references.bib` contains the auditable source list. At minimum, the Introduction/Discussion should cite:

- selective/reject classification: El-Yaniv & Wiener; Geifman & El-Yaniv; Hendrickx et al.;
- partial/set-valued rejection: Karlsson & Hössjer;
- conformal rejection: García-Galindo et al.; Szabadváry et al.;
- open-set recognition: Geng et al.;
- belief/evidential uncertainty: Denœux; Gao et al.;
- imperfect detection: MacKenzie et al.; Royle & Link;
- hierarchical/process-observation modeling: Royle & Dorazio; Auger-Méthé et al.;
- camera-trap detectability: Hofmeester et al.; Findlay et al.;
- adaptive ecological sampling: Henrys et al.; Pescott.

## 13. Methods in Ecology and Evolution fit

The intended MEE framing is methodological integration and tested ecological-sensing decision geometry, not a workflow that merely chains existing techniques. Broad applicability is argued **conceptually** through process-level mappings in `TRANSFERABILITY_TABLE.md`; quantitative transfer beyond the frozen flower-visitor generator is not claimed.

Paper 1 therefore remains a closed-world methods paper. V15 real-device calibration and field accuracy are external validation, not evidence manufactured to rescue the Paper-1 method claim.
