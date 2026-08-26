# TNOA

**Target–Nuisance–Observability–Abstention for ecological sensing**

TNOA is a methods-paper repository for a process-preserving framework that asks a narrower and safer question than ordinary event classification:

> **When is an ecological sensor entitled to make a biological decision, and when should it retain abstention?**

The framework was developed from the PolliPi/InsePi programme, but this repository is not the Raspberry Pi runtime and is not a classifier package. PolliPi and InsePi remain the implementation/provenance sources; TNOA isolates the transferable methodological contribution.

## Core object

The observed state is closed as

\[
B + \{T, N, U\},
\]

where:

- **B — baseline:** no marked dynamic deviation requiring target/nuisance adjudication;
- **T — target-supported:** positive evidence for the focal biological process;
- **N — nuisance-supported:** positive evidence for an exogenous observation process that can mimic, mask, or corrupt attribution;
- **U — abstention / undetermined:** the current evidence does not justify a unique T/N decision.

T and N are **positive, non-complementary hypotheses**. They may be jointly supported. T+N superposition is therefore not automatically an error state.

The field-facing evidence architecture is richer than the final decision vocabulary:

\[
(T, C, N, O, A^-),
\]

with:

- **T:** direct positive target evidence;
- **C:** target-coupled local response with independent attribution;
- **N:** exogenous nuisance-process evidence;
- **O:** measurement-channel observability/support;
- **A−:** independently validated target-absence evidence, if such a channel exists.

Low T is not A−. Good O is not A−. N is not `1 - T`. O is not `1 - N`.

## Methodological principles

1. **Positive definitions, not complements.** Target and nuisance are defined by what supports them, not by mutual negation.
2. **Process types, not cause lists.** Nuisance is defined by effects on inference—mimic, mask, corrupt attribution, degrade support—rather than an open-ended catalogue of wind, shadow, blur, etc.
3. **Preserve superposition.** Real biological and exogenous processes can co-occur.
4. **Abstention is an output, not a defect.** U is retained whenever evidence cannot safely support a unique conclusion.
5. **Separate information absence from representation defect.** `no supported evidence` is not automatically proof that the world contained no informative structure.
6. **Risk contracts replace inherited raw thresholds.** Operational boundaries are tied to tolerated false certainty, not score values that happen to work under an earlier representation.
7. **Freeze before measurement.** Definitions, observers, thresholds and claim rules are frozen before one-shot or held-out evaluation.
8. **Negative generations are retained.** Failed hypotheses remain part of the method history and constrain later claims.

## Dimensionless closed-world formulation

The synthetic theory is expressed over dimensionless coordinates rather than absolute scales. The current core axes are:

- \(\Pi_1\): observation-window length / target-process timescale;
- \(\Pi_2\): nuisance-response timescale / target timescale;
- \(\Pi_3\): direct target amplitude / nuisance amplitude;
- \(\Pi_4\): target-driven local-response amplitude / nuisance amplitude;
- \(\Pi_5\): nuisance spatial correlation length / target spatial support width;
- \(\Pi_6\): samples per target timescale.

The output is a response surface over this phase space, not a single performance number.

## Locked closed-world result currently motivating the paper

The frozen V14b/V14c measurement generation evaluated **5,880,000 synthetic worlds** after target and nuisance observers were frozen.

Equal-grid / equal-regime aggregate decision rates were approximately:

- baseline: 0.2302;
- target: 0.4287;
- nuisance: 0.0877;
- abstention: 0.2533.

Most U in the frozen design space was associated with overlap/attribution rather than simple lack of supported evidence. Observation duration did not make U vanish monotonically: longer observation can reveal genuine T+N co-occurrence and therefore increase attribution ambiguity even as raw information shortage decreases.

The earlier hypothesis that ambiguity should peak narrowly near \(\Pi_2 \approx 1\) was falsified and retired. A stronger current interpretation is that identifiability depends on **attribution-channel availability and evidence geometry**, not timescale equality alone.

The sharp \(\Pi_3=0\) versus \(\Pi_3>0\) boundary must be interpreted as a structural consequence of the frozen synthetic direct-channel rule, not as a universal ecological SNR law.

## Relation to PolliPi and InsePi

### PolliPi

PolliPi is the deployable local-first Raspberry Pi observer. Its portable target-evidence adapter currently exports the canonical states as ordinal positive target evidence:

- `no_activity -> 0.0`
- `environmental_noise -> 0.0`
- `uncertain_local_activity -> 0.5`
- `strong_visitation_candidate -> 1.0`

This scale is not a probability and score 0 does not certify biological absence.

### InsePi

InsePi contains the closed-world theory, process-preserving T/N/O logic, risk contracts, phase-space experiments, provenance locks, and the V15 empirical bridge.

### TNOA

TNOA extracts the general method from those implementations:

```text
world
  ↓
independent evidence channels T / C / N / O / optional A−
  ↓
process-preserving inference
  ↓
B / T / N / U
  ↓
false-certainty-controlled claims
```

## Paper boundary

The first TNOA paper is intended to be a **methods paper**, not a field-accuracy paper.

It may claim:

- a process-preserving observation ontology;
- a formal separation of target, nuisance, observability and optional absence evidence;
- a principled role for abstention;
- locked simulation/benchmark evidence for the resulting phase geometry;
- negative-result-preserving development and false-certainty risk contracts;
- a reusable architecture for ecological sensing systems.

It must not claim, without field validation:

- field visit-detection accuracy;
- calibrated biological absence;
- universal superiority over existing classifiers;
- universal validity of PolliPi thresholds;
- universal ecological significance of the synthetic \(\Pi_3\) boundary;
- pollination effectiveness.

Field deployment and V15 empirical validation are external validation, not prerequisites for the closed-world methodological result.

## Repository map

- [`docs/CONCEPTUAL_FRAMEWORK.md`](docs/CONCEPTUAL_FRAMEWORK.md) — definitions and inference logic.
- [`docs/NOVELTY_POSITIONING.md`](docs/NOVELTY_POSITIONING.md) — internal novelty framing.
- [`docs/LITERATURE_EVIDENCE_MAP.md`](docs/LITERATURE_EVIDENCE_MAP.md) — evidence-backed comparison with selective classification, imperfect detection, state-space models, camera-trap detectability, adaptive sampling and sensor fusion.
- [`docs/REVIEWER_ATTACK_MATRIX.md`](docs/REVIEWER_ATTACK_MATRIX.md) — likely reviewer objections and the manuscript evidence required to answer them.
- [`docs/METHOD_PAPER_BLUEPRINT.md`](docs/METHOD_PAPER_BLUEPRINT.md) — manuscript architecture.
- [`docs/CLAIM_BOUNDARY.md`](docs/CLAIM_BOUNDARY.md) — allowed, conditional and forbidden claims.
- [`docs/SOURCE_PROVENANCE.md`](docs/SOURCE_PROVENANCE.md) — implementation/result provenance to PolliPi and InsePi.
- [`references.bib`](references.bib) — initial nearest-method bibliography.
- [`paper_manifest.json`](paper_manifest.json) — machine-readable source and submission state.

## Current status

**Methods-paper extraction + initial literature positioning completed.** The central novelty is now framed as the integrated ecological sensing architecture and its tested decision geometry, not abstention, imperfect-detection correction, sensor fusion or adaptive sampling individually. Remaining submission work is paper-grade figure assembly, claim-to-artifact traceability, reproducibility entry point, transferability table, citation-completeness audit and final manuscript claim audit.
