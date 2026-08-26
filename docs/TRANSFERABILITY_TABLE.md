# Cross-system transferability map

TNOA is intended as a sensing architecture, not a flower-visitor-specific classifier. This table demonstrates structural transfer without claiming that the frozen flower-visitor synthetic calibration transfers quantitatively to other systems.

The rule is conservative: if a domain does not supply a defensible C or A- channel, that channel remains absent rather than being invented.

| Sensor domain | T — direct target evidence | C — target-coupled response | N — positive nuisance process | O — measurement support | A- — certified absence candidate | What U can mean |
| --- | --- | --- | --- | --- | --- | --- |
| Flower-visitor camera | visible insect/local actor evidence | flower displacement/contact response **only with independent attribution** | wind, moving shadow, camera motion, exogenous flower/background motion insofar as it mimics/masks/corrupts attribution | flower-zone coverage, visibility, resolution, photometry, temporal continuity | no default A- in V15-v2; low T is insufficient | direct actor absent but flower response unattributed; T+N coexistence; poor O; no supported evidence |
| Wildlife camera trap | visible animal evidence in the detection zone | optional target-linked response such as bait interaction or substrate/contact event **only if independently attributable**; may be omitted | vegetation motion, thermal/illumination artifacts, camera shake, non-target animals/processes that mimic/mask target evidence | effective detection-zone coverage, trigger/registration support, image quality, temporal continuity | possible only with independently validated detection/coverage mechanism; ordinary non-trigger is not A- | animal evidence obscured by nuisance; insufficient trigger/registration support; target and nuisance jointly present |
| Passive acoustic event sensor | target call/song/event evidence in spectrotemporal data | optional target-linked response in a second channel, e.g. independently attributed reply/interaction; often absent | wind, rain, anthropogenic noise, heterospecific overlap, clipping or reverberation when these mimic/mask/corrupt attribution | microphone/channel health, usable bandwidth, SNR support, clipping state, temporal coverage | only if a validated counterfactual listening/detection channel can certify that a target event would have been observable; otherwise absent | overlapping sources, audible event but unresolved identity, silent interval with poor O, no positive target support |
| Nest / feeding interaction camera | visible focal visitor/parent/predator evidence | nest movement, feeding response or prey transfer only when attributable to the focal actor | wind-driven nest movement, vegetation occlusion, non-target movement, camera motion, illumination | nest-zone coverage, visibility, spatial resolution, photometry, frame continuity | could exist with independent continuous nest occupancy/visibility instrumentation; otherwise absent | movement without attributable actor; target+nuisance coexistence; occluded interaction window |
| Phenology / plant camera | direct evidence for the focal phenological event when visually observable | usually **not required**; if a downstream local response is studied, it needs an independent link | illumination shifts, snow/wetness, camera movement, shadows or background changes that mimic/mask phenological change | canopy/organ coverage, focus/resolution, exposure, colour/photometric sufficiency, temporal continuity | potentially available for some states only with an independently validated observation model; not inferred from low change score | scene change with ambiguous source; quiet image under poor O; target-like and nuisance changes superposed |
| Remote camera / general anomaly monitoring | direct evidence for a predefined ecological event | optional response channel only if a causal/attribution link exists | exogenous processes that mimic, mask or corrupt the event interpretation | channel-specific measurement support | optional; requires a separate validated negative-evidence mechanism | event evidence and nuisance coexist; unresolved attribution; unsupported inference |

## Transfer rules

### 1. T is always positive evidence

A target observer answers “what supports the focal event/process?” It does not define N as everything not classified as T.

### 2. C is optional

C exists only when the biological target can exhibit a local response that may carry information about the focal interaction. A domain without a defensible response channel should use T/N/O without C.

If C exists, response magnitude alone is insufficient. TNOA requires an attribution/link component before the response can support the focal target process.

### 3. N is defined by effect on inference

Across systems, nuisance is not a fixed list of causes. A process enters N when it can positively support one or more finite effects such as:

- mimic target evidence;
- mask target evidence;
- corrupt attribution;
- degrade observation support.

The same physical cause can matter differently across sensors, and different causes can instantiate the same nuisance effect.

### 4. O is sensor-specific but conceptually stable

O asks the counterfactual measurement question:

> If the focal event occurred in the defined observation opportunity, did the sensor preserve enough information to attempt inference?

Its components vary by sensor, but O must not be computed as `1 - N`, `1 - uncertainty`, or from biological truth.

### 5. A- is never mandatory

A- should be absent unless a system has an independently validated route for biological negative evidence. Ordinary non-detection, low T, quiet background or good O are not sufficient by themselves.

### 6. U is not one universal uncertainty cause

The same final abstention state can arise from different reasons:

- no supported evidence;
- inadequate O;
- target-coupled response without attribution;
- T+N superposition where unique attribution is not licensed;
- evidence conflict that reveals a representation/definition defect.

These reasons should remain available in the diagnostic layer even if the ecological output vocabulary closes as B/T/N/U.

## What transfers and what does not

### Intended to transfer

- positive T/N definitions;
- separation of O from T and N;
- optional C with independent attribution;
- optional A-;
- preservation of T+N superposition;
- abstention as an inferential output;
- false-certainty-oriented calibration;
- freeze-before-held-out development rules.

### Not claimed to transfer

- PolliPi state thresholds;
- V14b numerical nuisance threshold;
- the six current Pi-axis ranges;
- the pooled B/T/N/U rates from the 5.88M-world grid;
- the structural Pi3 boundary as a universal law;
- any field accuracy or detection probability.

A new domain must define and validate its own measurement functions and locate itself relative to an appropriate dimensionless phase space before quantitative transfer claims are made.
