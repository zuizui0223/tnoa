# Fail-closed field translation pathway

This document turns the TNOA observation-state framework into an implementation sequence without adding field-performance claims to Paper 1.

The central rule is simple:

> **Do not make a field support call before the corresponding evidence channel has been independently calibrated.**

A deployment may compute raw target, nuisance and observability diagnostics immediately, but until field calibration is frozen those diagnostics remain measurements rather than licensed T/N/O decisions. The safe default observation is unresolved (`U`), and the safe default control action is to leave the acquisition schedule unchanged.

## Stage 0 — keep a primary scientific record

The acquisition system should preserve a primary record whose sampling rule is interpretable independently of any adaptive detector. A camera system might use fixed high-resolution stills plus more frequent low-resolution probes; an acoustic system might use a fixed recording schedule plus low-cost streaming diagnostics.

Adaptive capture can be evaluated later, but the primary record must not disappear simply because a classifier considers a window uninteresting.

## Stage 1 — log raw evidence, not field truth

For each observation window, record the available evidence channels separately:

- **T raw evidence**: direct evidence for the focal actor/event;
- **N raw evidence**: positive diagnostics for exogenous processes that can mimic, mask or corrupt attribution;
- **O raw evidence**: image/audio quality, temporal support, geometry, occlusion, focus, exposure or other measurement-support diagnostics;
- **C raw evidence**: a local biological response that could be target-coupled;
- **A-**: unavailable unless a genuinely independent absence channel exists.

Two guardrails are essential.

First, a detector's broad `noise` or `not-target` class must not automatically become TNOA nuisance support. N is a positive process hypothesis, not the complement of T.

Second, a local target response must not automatically become target evidence. C requires independent attribution before it can support T.

Before field calibration, store calibrated-support fields as unavailable and retain the observation as:

```text
observation_state = U
reason = field_calibration_pending
action = observe_only
```

This is a development state, not a biological conclusion.

## Stage 2 — establish independent field truth

Calibration requires truth that is not defined from the algorithm being calibrated. For event-sensing systems, keep four truth layers separate:

1. **biological-event truth** — target absent/present/contact/event, or truth unresolved;
2. **target-coupled-response truth** — present/absent/unresolved attribution of the local response to the target;
3. **exogenous nuisance truth** — multi-label physical nuisance families and their possible inferential effects;
4. **primary-stream observability truth** — observable/compromised/unobservable for the focal inference.

A separate reference channel is required when the primary stream itself cannot establish hidden presence/absence. That reference may be a second camera, wider/higher-quality recording, independent observer or another justified measurement channel. It is used to establish truth and is never supplied to the algorithm under test.

If the reference truth is unresolved, retain `truth_unresolved`. Never convert it to absence.

Annotation should be blinded to target scores, nuisance scores, TNOA state and adaptive-policy output. At least a protected subset should be independently double-annotated before adjudication.

## Stage 3 — calibrate on development groups, not frames

Frames from one continuous observation are not independent calibration replicates. Split at a level such as:

```text
recording day × focal scene/individual × recording block
```

and reserve new days/scenes for held-out validation.

Calibrate each operational evidence channel against a declared error criterion rather than inheriting raw thresholds from another representation, device or experiment. For example:

- target support may require a declared miss/retention criterion;
- nuisance support may use family-wise false-attribution control;
- observability may use false-censor and unobservable-recall criteria;
- coupled response must control spurious rescue when resolved target truth is absent.

The calibration manifest should be versioned and frozen before held-out scoring.

## Stage 4 — validate observation semantics before adaptive control

Held-out evaluation should compare the full observation interface with simpler alternatives, for example:

- direct target-only binary output;
- target + coupled response without nuisance/support;
- target + nuisance without O;
- target + O without nuisance diagnosis;
- full T/C/N/O observation record.

Relevant field quantities include false biological absence, observable-window target recall, nuisance false attribution, false censoring, indirect target rescue, spurious coupled rescue and review/capture burden.

Only after the evidence semantics pass held-out validation should TNOA reasons be allowed to alter acquisition behaviour.

## Stage 5 — let unresolved reason choose the next measurement

The eventual adaptive policy should react to **why** an observation is unresolved rather than to one generic confidence score.

Examples:

| Unresolved reason | Useful next measurement |
| --- | --- |
| no supported evidence | longer or denser sampling |
| target+nuisance coexistence | preserve both; add temporal/reference evidence |
| attribution conflict | second view, continuous video or independent attribution channel |
| poor observability | restore visibility/focus/geometry rather than merely sampling faster |
| coupled response without target link | acquire actor/contact evidence rather than promoting C automatically |

The control policy remains separate from the scientific observation record. A system may log a `would_be_action` while leaving the applied acquisition schedule unchanged during shadow validation.

## Cross-system translation

The pathway is deliberately sensor-agnostic.

### Wildlife camera trap

- T: focal-species evidence;
- N: vegetation motion, non-target animals, glare or camera motion;
- O: field of view, trigger coverage, image quality and occlusion;
- C: a local response only if biologically meaningful and independently attributable.

### Passive acoustics

- T: focal call/song evidence;
- N: overlapping taxa, rain, wind, anthropogenic sound or clipping;
- O: microphone health, signal support and masking state;
- C: a target-linked environmental/receiver response only if a justified channel exists.

### Interaction camera

- T: direct actor evidence;
- N: exogenous movement/illumination/camera processes;
- O: interaction-zone visibility and image/temporal support;
- C: local response of the biological target, retained separately until attribution is supported.

The raw features and calibration rules change between systems. The logical sequence does not.

## Paper-1 boundary

This pathway is an implementation template, not a Paper-1 empirical result. Paper 1 remains a closed-world methodological study. No field accuracy, field prevalence, field nuisance rate, calibrated biological absence or universal threshold is licensed by this document.

Its role is to make the practical implication of the synthetic method explicit:

> preserve evidence channels first, calibrate their semantics independently, and only then allow observation states or adaptive actions to affect ecological inference.
