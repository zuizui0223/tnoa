# TNOA

**Target–Nuisance–Observability–Abstention for ecological sensing**

TNOA is a methods-paper repository for a process-preserving framework that asks a narrower and safer question than ordinary event classification:

> **When is an ecological sensor entitled to make a biological decision, and when should it retain abstention?**

The framework was developed from the PolliPi/InsePi programme, but this repository is not the Raspberry Pi runtime and is not a classifier package. PolliPi and InsePi remain the implementation/provenance sources; TNOA isolates the transferable methodological contribution and its paper package.

## Core object

The observed decision state is closed as

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
5. **Separate no support from proven information absence.** `no supported evidence` is not automatically proof that the world contained no informative structure.
6. **Risk contracts replace inherited raw thresholds.** Operational boundaries are tied to tolerated false certainty, not score values that happen to work under an earlier representation.
7. **Freeze before measurement.** Definitions, observers, thresholds and claim rules are frozen before one-shot or held-out evaluation.
8. **Negative generations are retained.** Failed hypotheses remain part of the method history and constrain later claims.

## Dimensionless closed-world formulation

The synthetic theory is expressed over dimensionless coordinates rather than absolute scales:

- \(\Pi_1\): observation-window length / target-process timescale;
- \(\Pi_2\): nuisance-response timescale / target timescale;
- \(\Pi_3\): direct target amplitude / nuisance amplitude;
- \(\Pi_4\): target-driven local-response amplitude / nuisance amplitude;
- \(\Pi_5\): nuisance spatial correlation length / target spatial support width;
- \(\Pi_6\): samples per target timescale.

The output is a response surface over this phase space, not a single performance number.

## Locked closed-world result

The frozen V14b/V14c measurement generation evaluated **5,880,000 synthetic worlds** after target and nuisance observers were frozen.

Equal-grid / equal-regime aggregate decision rates were approximately:

- baseline: 0.2302;
- target: 0.4287;
- nuisance: 0.0877;
- abstention: 0.2533.

Most U in the frozen design space was associated with overlap/attribution rather than simple lack of supported evidence. Observation duration did not make U vanish monotonically: longer observation can reveal genuine T+N co-occurrence and therefore increase attribution ambiguity even as the no-support component changes.

The earlier hypothesis that ambiguity should peak narrowly near \(\Pi_2 \approx 1\) was falsified and retired. The sharp \(\Pi_3=0\) versus \(\Pi_3>0\) boundary is explicitly treated as a structural consequence of the frozen synthetic direct-channel rule, not a universal ecological SNR law.

## Relation to PolliPi and InsePi

### PolliPi

PolliPi is the deployable local-first Raspberry Pi observer. Its portable target-evidence adapter exports canonical states as ordinal positive target evidence:

- `no_activity -> 0.0`
- `environmental_noise -> 0.0`
- `uncertain_local_activity -> 0.5`
- `strong_visitation_candidate -> 1.0`

This scale is not a probability and score 0 does not certify biological absence.

### InsePi

InsePi contains the closed-world theory, process-preserving T/N/O logic, risk contracts, phase-space experiments, provenance locks, and the V15 empirical bridge.

### TNOA

TNOA extracts the general method and manuscript package:

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

## Novelty boundary after targeted prior-art audit

TNOA does **not** claim to invent:

- abstention / reject options;
- partial or set-valued decisions;
- open-set recognition;
- ignorance / evidence conflict;
- imperfect-detection correction;
- nondetection ≠ absence;
- process/observation separation;
- false-positive/false-negative occupancy modeling;
- sensor fusion;
- adaptive ecological sampling.

The defensible contribution is the **integrated ecological sensor-decision architecture plus its frozen dimensionless decision geometry**: positive non-complementary T/N, separate O, attribution-gated C, optional independently supported A−, preserved T+N coexistence, reasoned U, process-effect nuisance definitions, false-certainty calibration, and freeze/falsification provenance.

See [`docs/FINAL_PRIOR_ART_AUDIT.md`](docs/FINAL_PRIOR_ART_AUDIT.md).

## Paper boundary

Paper 1 is a **closed-world methods paper**, not a field-accuracy paper.

It may claim:

- the process-preserving observation architecture;
- formal separation of target, nuisance, observability and optional absence evidence;
- locked simulation/benchmark evidence for the resulting decision geometry;
- negative-result-preserving development;
- false-certainty risk contracts;
- downstream information preservation for a known-truth synthetic target-prevalence estimand;
- weighting robustness only within the tested bounded-reweighting class;
- broad conceptual transferability of the architecture.

It must not claim without external validation:

- field visit-detection accuracy;
- calibrated biological absence;
- universal superiority over existing classifiers;
- universal validity of PolliPi thresholds;
- universal ecological significance of the synthetic \(\Pi_3\) boundary;
- quantitative cross-system transfer;
- pollination effectiveness.

Field deployment and V15 empirical validation are external validation, not prerequisites for the closed-world methodological result.

## Repository map

### Manuscript

- [`manuscript/TNOA_MEE_DRAFT.md`](manuscript/TNOA_MEE_DRAFT.md) — active MEE-focused working draft.
- [`manuscript/TNOA_P1_DRAFT.md`](manuscript/TNOA_P1_DRAFT.md) — retained historical Paper-1 draft.
- [`docs/METHOD_PAPER_BLUEPRINT.md`](docs/METHOD_PAPER_BLUEPRINT.md) — manuscript architecture and current figure order.

### Scientific framing and audit

- [`docs/CONCEPTUAL_FRAMEWORK.md`](docs/CONCEPTUAL_FRAMEWORK.md) — definitions and inference logic.
- [`docs/NOVELTY_POSITIONING.md`](docs/NOVELTY_POSITIONING.md) — novelty framing after targeted audit.
- [`docs/LITERATURE_EVIDENCE_MAP.md`](docs/LITERATURE_EVIDENCE_MAP.md) — nearest-method evidence map.
- [`docs/FINAL_PRIOR_ART_AUDIT.md`](docs/FINAL_PRIOR_ART_AUDIT.md) — final targeted prior-art boundary.
- [`docs/REVIEWER_ATTACK_MATRIX.md`](docs/REVIEWER_ATTACK_MATRIX.md) — likely reviewer objections.
- [`docs/TRANSFERABILITY_TABLE.md`](docs/TRANSFERABILITY_TABLE.md) — cross-domain conceptual mapping.
- [`docs/CLAIM_BOUNDARY.md`](docs/CLAIM_BOUNDARY.md) — allowed and forbidden Paper-1 claims.
- [`docs/CLAIM_TRACEABILITY.md`](docs/CLAIM_TRACEABILITY.md) — C1–C15 claim-to-artifact ledger.
- [`docs/FINAL_CLAIM_AUDIT.md`](docs/FINAL_CLAIM_AUDIT.md) — retained audit of the historical draft.

### Figures and reproducibility

- [`docs/FIGURE_PLAN.md`](docs/FIGURE_PLAN.md) — quantitative figure contract.
- [`docs/MEE_FIGURE_VALIDATION.md`](docs/MEE_FIGURE_VALIDATION.md) — active MEE figure provenance and interpretation guard.
- [`derived/mee_figure_data.json`](derived/mee_figure_data.json) — pinned MEE figure values and upstream provenance.
- [`scripts/validate_mee_figure_data.py`](scripts/validate_mee_figure_data.py) — fail-closed MEE figure-data guard.
- [`scripts/build_mee_figures.py`](scripts/build_mee_figures.py) — MEE-priority panel builder.
- [`docs/FIGURE_VALIDATION.md`](docs/FIGURE_VALIDATION.md) and [`scripts/build_paper_figures.py`](scripts/build_paper_figures.py) — retained historical figure package.
- [`scripts/validate_paper_manifest.py`](scripts/validate_paper_manifest.py) — repository manifest guard.
- [`scripts/audit_manuscript_claims.py`](scripts/audit_manuscript_claims.py) — manuscript claim scanner.
- [`reproduce/README.md`](reproduce/README.md) — reproduction policy.
- [`references.bib`](references.bib) — nearest-method bibliography.
- [`paper_manifest.json`](paper_manifest.json) — machine-readable source, claim and submission state.

## Current status

**MEE-focused scientific package assembled and claim-guarded.** The active draft, C1–C15 plus D1–D2 traceability, pinned MEE figure data/builder, runnable observation-state API and post-freeze audits are registered in `paper_manifest.json`, which records **zero unresolved MEE scientific blockers**. The earlier Paper-1 draft and figure package remain in place as historical records.

Remaining work before actual journal upload is editorial/production work: finalize conceptual Figure 1, convert the Markdown draft to journal format, complete authorship/acknowledgement metadata, check final citation style, and rerun the claim audit after any material rewrite.
