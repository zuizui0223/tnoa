# V3 upstream measurement interface for TNOA

Status: **companion architecture note. This document does not change the frozen TNOA Paper-1 claim or quantitative results.**

## 1. Why this interface exists

TNOA separates target evidence, nuisance evidence, observability and abstention after a sensing system has represented the available measurement information.

A remaining upstream question is:

> Can the measurement representation itself be improved before TNOA decides what the evidence supports?

The PolliPi V3 latent-disturbance method is one candidate upstream representation. It uses target-free reference information to estimate a low-dimensional shared temporal nuisance subspace without requiring target recognition or pixel correspondence.

V3 and TNOA should therefore be treated as different layers:

- **V3:** representation layer;
- **TNOA:** evidence/decision-entitlement layer.

TNOA must remain valid without V3, and V3 must not be allowed to redefine TNOA semantics.

## 2. Shared principle

Both methods reject complement-based shortcuts.

V3 does not assume:

- residual = target truth;
- unexplained variance = target;
- low explained nuisance = no nuisance.

TNOA does not assume:

- `N = 1 - T`;
- `O = 1 - N`;
- `A- = low T`;
- `A- = good O + low T`.

The common principle is:

> **Represent positive support separately, and retain unresolved states when the available information does not justify a unique conclusion.**

## 3. V3 output semantics

For primary sequence `Y(t)` and target-free reference `R(t)`, V3 estimates a temporal basis `U` and decomposes each primary pixel time series `d` into:

`d_explained = U U^T d`

and

`d_residual = d - U U^T d`.

These are measurement representations, not TNOA states.

### `d_residual`

May be used as an input representation for a target observer.

It is not direct target truth and does not establish target absence when quiet.

### reference-explained diagnostics

May be used as candidate inputs for a nuisance observer after independent calibration.

They do not establish a named nuisance source and must not be copied directly into `N_supported=true`.

## 4. TNOA interface rules

### Rule 1 — representation is not evidence semantics

Changing the upstream representation may change target/nuisance observer performance, but the definitions of T, C, N, O and A- remain fixed.

### Rule 2 — residual quietness cannot create A-

`A-` remains independently validated absence evidence.

`quiet V3 residual -> A-` is forbidden.

### Rule 3 — explained variance cannot bypass nuisance calibration

A high reference-explained fraction can motivate positive nuisance evidence, but its operating threshold and effect interpretation require independent calibration.

### Rule 4 — observability remains explicit

V3 does not replace O. Photometric failure, temporal gaps, spatial insufficiency or unavailable target support can remain limiting even after nuisance projection.

### Rule 5 — uncertainty remains available

When V3 does not resolve a case, TNOA may retain U. Upstream method failure is not itself evidence for T, N or baseline.

## 5. Relation to the TNOA contradiction taxonomy

V3 provides a concrete upstream intervention for one TNOA contradiction class: **representation defect**.

Its development history is informative:

- ideal pixel-corresponding subtraction succeeded;
- spatial mismatch exposed a representation defect;
- single-pair alignment did not fix broad boundary residuals or local-sway identifiability;
- a temporal-subspace representation improved synthetic separation without pixel correspondence.

This is exactly the TNOA development rule:

1. identify the contradiction type;
2. modify only the implicated representation;
3. freeze siblings;
4. evaluate on a fresh locked generation;
5. retain negative generations.

V3 does not solve the other contradiction types automatically. Genuine information absence and target+nuisance superposition can still require U.

## 6. Joint falsifiable hypothesis

TNOA Paper 1 uses the risk-controlled principle:

`choose tolerated false certainty alpha, then measure safely resolvable coverage`.

The most useful companion hypothesis is therefore:

> **At the same frozen false-certainty budget alpha, a correctly coupled V3 representation should increase safely resolvable coverage compared with the raw representation, and a time-broken/mismatched V3 reference should not reproduce the same gain.**

Define:

`Delta C_alpha = C_alpha(matched V3 -> TNOA) - C_alpha(raw -> TNOA)`

and

`Delta C_coupling = C_alpha(matched V3 -> TNOA) - C_alpha(time-broken V3 -> TNOA)`.

A convincing joint result requires:

- the same prefrozen alpha;
- false-certainty guardrails remain satisfied;
- positive `Delta C_alpha`;
- positive `Delta C_coupling`;
- no post-heldout tuning of the V3 representation, TNOA evidence definitions or decision contract.

This tests whether better upstream representation converts some U/false-certainty cases into safely resolvable evidence without simply making the system more willing to decide.

## 7. What should be measured in joint validation

Primary outcome:

- safely resolvable coverage at fixed false-certainty budget.

Secondary outcomes:

- T/N/U decision fractions;
- U decomposition into no-support versus attribution/overlap reasons;
- target false certainty;
- nuisance false certainty;
- target/process estimand error;
- reference coupling / contamination quality;
- observability strata.

The confirmatory representation arms should be:

1. raw/no-reference;
2. correctly coupled V3;
3. time-broken or mismatched V3 negative control.

## 8. Paper boundary

This interface should **not** be retrofitted into the frozen TNOA Paper-1 novelty claim before external validation.

TNOA Paper 1 remains:

- an integrated ecological sensing architecture;
- closed-world synthetic theory and frozen decision geometry;
- positive non-complementary evidence channels;
- explicit abstention and false-certainty calibration.

V3 is a candidate upstream representation method that can later provide an external test of a stronger two-layer architecture.

A future joint paper or external-validation section may ask whether representation improvement increases safe decision coverage. Until then:

- do not claim V3 is required for TNOA;
- do not claim TNOA validates V3;
- do not claim the synthetic improvements generalize to field data.

## 9. Two-layer summary

```text
world/process
  -> recorded signal with target + exogenous disturbance
  -> [V3: representation decomposition]
  -> residual + reference-explained structure
  -> independent T/C/N/O/(A-) evidence channels
  -> [TNOA: decision entitlement]
  -> B/T/N/U
```

Concise interpretation:

> **V3 asks what part of the signal can be explained by a shared disturbance representation. TNOA asks what conclusion the resulting evidence entitles the sensor to make.**

The shared rule is:

> **decompose supported structure, preserve unresolved structure, and never infer a negative biological conclusion from missing positive support.**
