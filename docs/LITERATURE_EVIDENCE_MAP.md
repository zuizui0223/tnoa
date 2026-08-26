# Literature evidence map for TNOA Paper 1

This document is an initial evidence-backed positioning map, not a systematic review. Its purpose is to identify the nearest methodological neighbours that a reviewer is likely to invoke and to state exactly where TNOA overlaps and where it differs.

## 1. Selective classification / reject option

Selective classification trades prediction coverage against prediction risk: a model may abstain on examples for which prediction is judged unsafe. Foundational and modern formulations include El-Yaniv & Wiener (2010), Geifman & El-Yaniv (2017), SelectiveNet (Geifman & El-Yaniv 2019), and the reject-option survey of Hendrickx et al. (2024).

### Shared ground

- abstention is an allowed output rather than a software failure;
- risk can be controlled by sacrificing coverage;
- a decision system should avoid overconfident predictions.

### TNOA difference

TNOA does not define U as low classifier confidence or as a learned rejection region around a single prediction problem.

The TNOA sensing world contains positively defined, non-complementary process/evidence channels:

- T: focal target evidence;
- C: target-coupled response, usable only when independently attributable;
- N: exogenous nuisance-process evidence;
- O: measurement support/observability;
- optional A-: independently validated target-absence evidence.

T and N may both be supported. U can therefore arise even when both channels are strong, because coexistence does not establish unique attribution. Conversely, a low T score is not negative biological evidence. This makes TNOA a process-preserving observation/inference architecture, not simply a classifier with a rejector.

### Claim discipline

Do not claim that TNOA invents abstention or risk-coverage control. The contribution is the ecological observation ontology and decision contract that determines *why* a sensor must abstain and prevents positive target, nuisance, observability and absence evidence from being collapsed into complements.

## 2. Imperfect detection and occupancy models

MacKenzie et al. (2002) established the core ecological principle that non-detection does not imply absence when detection probability is below one. Occupancy and related hierarchical observation models explicitly separate latent ecological state from observation/detection processes.

### Shared ground

- non-detection is not biological absence;
- observation processes must be modeled separately from ecological state;
- inferential validity depends on the measurement process.

### TNOA difference

Occupancy methods generally infer latent occupancy over replicated surveys by statistically modeling detection conditional on presence. TNOA works one level earlier at the sensor-decision interface: before a detection/non-detection datum is allowed to enter an ecological estimator, it asks whether the observation supports a target process, a nuisance process, both, neither, or no unique attribution.

TNOA therefore complements occupancy rather than replaces it. A TNOA output can be viewed as a provenance-rich input layer for later occupancy or abundance models. In particular, TNOA distinguishes:

- lack of positive T evidence;
- inadequate O;
- positive N evidence;
- T+N superposition;
- target-coupled evidence without attribution;
- independently certified absence A- when such a channel exists.

### Claim discipline

Do not claim that TNOA is the first framework to separate biological state from detection. Its stronger claim is narrower: it formalizes sensor-level positive process hypotheses, superposition and abstention before ecological non-detection is treated as data.

## 3. State-space and ecological observation models

State-space models separate latent process dynamics from observation error and are a standard ecological framework for time series (e.g. Auger-Méthé et al. 2021).

### Shared ground

- ecological process and observation process are distinct;
- measurement error should not be absorbed into biological dynamics;
- uncertainty has multiple sources.

### TNOA difference

TNOA is not a replacement state-space model and does not estimate a latent population trajectory. It is a pre-model observation contract for event sensors. Its distinctive object is the decision geometry of a measurement window under multiple simultaneously valid positive process hypotheses.

The central TNOA question is not “what latent state generated the time series?” but “what biological statement is this sensor entitled to emit from this window?”

## 4. Camera-trap detectability and component detection processes

Camera-trap work has already shown that detection is a sequence of component processes and that failures at encounter, triggering, registration and image-quality stages can create false negatives. Findlay et al. (2020) explicitly decomposed these component processes. Hofmeester et al. (2019) reviewed multiple animal, camera, setup and environmental factors affecting detection.

### Shared ground

- detectability is not a scalar property of the animal alone;
- observation hardware and environment influence whether a biological event is recoverable;
- observation failure should be diagnosed rather than silently treated as absence.

### TNOA difference

TNOA generalizes this logic into O as an independent measurement-support object and separates it from N. A scene may be noisy but observable, or quiet but unobservable. TNOA also adds explicit positive nuisance-process hypotheses and allows target+nuisance superposition rather than treating all environmental effects as a single detection penalty.

## 5. Adaptive and preferential ecological sampling

Henrys, Mondain-Monval & Jarvis (2024) review adaptive sampling in ecology and emphasize both its efficiency potential and risks from preferential sampling. Pescott (2025) further addresses adaptive monitoring when source data are biased.

### Shared ground

- adaptive observation can improve resource allocation;
- data-dependent sampling can distort the sampled distribution;
- selection rules must be part of the inferential design.

### TNOA difference

TNOA Paper 1 is not primarily an adaptive-sampling optimizer. Earlier InsePi generations tested disagreement-driven allocation and retained its failure. The current TNOA contribution is upstream: define valid evidence and abstention before deciding whether or how to allocate additional effort.

This distinction is important because disagreement between target and nuisance observers is retained as a diagnostic of ontology/representation/measurement defects, not assumed to be an optimal acquisition score.

## 6. Sensor fusion and multimodal decision systems

Multi-sensor fusion combines information from different instruments or modalities to improve state estimation, robustness and safety. Modern safety-critical sensing literature increasingly stresses measurement physics, uncertainty propagation and integrity monitoring.

### Shared ground

- different evidence channels have different failure modes;
- one sensor score should not necessarily dominate all downstream decisions;
- safety requires explicit treatment of sensing limitations.

### TNOA difference

TNOA deliberately does not require all evidence to fuse into one latent class or posterior. The architecture can terminate with T+N superposition or U. Its main operation is therefore not “fusion for a sharper estimate” but “preservation of epistemically different channels until a unique ecological statement is justified.”

## 7. Closest novelty statement

The strongest defensible novelty claim is:

> TNOA is a process-preserving ecological sensing architecture that separates positive target, target-coupled, nuisance and observability evidence, permits target+nuisance superposition, requires an independent channel for certified absence, and treats abstention as an inferential output when the measurement structure does not justify a unique biological decision.

The novelty is the combination of this ontology with:

1. a dimensionless closed-world phase-space analysis;
2. frozen observer development and retained negative generations;
3. false-certainty rather than inherited raw-score calibration;
4. explicit separation of no-supported-evidence from attribution/overlap U;
5. a field bridge that can later locate real systems on the synthetic phase geometry without rewriting the closed-world result.

## 8. What would falsify the paper's novelty claim

The claim should be weakened if a prior method is found that already satisfies all of the following simultaneously:

- T and N are positively defined and can coexist;
- O is separate from N and from target confidence;
- target-coupled evidence requires independent attribution;
- low target evidence cannot certify absence;
- abstention reasons distinguish unsupported evidence from attribution/superposition;
- the architecture is evaluated over a controlled process phase space rather than only by classifier confidence/coverage.

Finding prior work on any single element does not erase the contribution; the literature already contains several of the individual ideas. The paper must therefore claim the integrated ecological sensing architecture and its tested decision geometry, not ownership of each component concept.

## 9. Initial reference set

- El-Yaniv R, Wiener Y. 2010. On the Foundations of Noise-Free Selective Classification. Journal of Machine Learning Research 11:1605–1641.
- Geifman Y, El-Yaniv R. 2017. Selective Classification for Deep Neural Networks. Advances in Neural Information Processing Systems 30.
- Geifman Y, El-Yaniv R. 2019. SelectiveNet: A Deep Neural Network with an Integrated Reject Option. Proceedings of Machine Learning Research 97:2151–2159.
- Hendrickx K, Perini L, Van der Plas D, Meert W, Davis J. 2024. Machine learning with a reject option: a survey. Machine Learning 113:3073–3110. doi:10.1007/s10994-024-06534-x.
- MacKenzie DI, Nichols JD, Lachman GB, Droege S, Royle JA, Langtimm CA. 2002. Estimating site occupancy rates when detection probabilities are less than one. Ecology 83:2248–2255. doi:10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2.
- Hofmeester TR, Cromsigt JPGM, Odden J, Andrén H, Kindberg J, Linnell JDC. 2019. Framing pictures: A conceptual framework to identify and correct for biases in detection probability of camera traps enabling multi-species comparison. Ecology and Evolution 9:2320–2336. doi:10.1002/ece3.4878.
- Findlay MA, Briers RA, White PJC. 2020. Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives. Mammal Research 65:167–180. doi:10.1007/s13364-020-00478-y.
- Auger-Méthé M et al. 2021. A guide to state-space modeling of ecological time series. Ecological Monographs. doi:10.1002/ecm.1470.
- Henrys PA, Mondain-Monval TO, Jarvis SG. 2024. Adaptive sampling in ecology: Key challenges and future opportunities. Methods in Ecology and Evolution 15:1483–1496. doi:10.1111/2041-210X.14393.
- Pescott OL. 2025. Adaptive sampling for ecological monitoring using biased data: a stratum-based approach. Oikos 2025:e11115. doi:10.1002/oik.11115.

## 10. MEE fit

Methods in Ecology and Evolution explicitly accepts analytical, practical and conceptual methods and emphasizes methodological development rather than ecological application results. Its Research Article guidance says new computational methods normally should be tested using simulations or benchmark datasets, and methods should be broadly applicable across taxa/systems. This is compatible with TNOA Paper 1 if the manuscript demonstrates transferability beyond flower visitors and avoids presenting the work as a workflow that merely links existing methods.

The broad-applicability argument should therefore be demonstrated with process-level mappings for at least camera traps, acoustic event sensors, nest/feeding interaction monitors and phenology/remote cameras, even if the locked quantitative experiment remains the flower-visitor synthetic generator.
