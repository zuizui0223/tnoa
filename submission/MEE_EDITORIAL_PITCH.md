# MEE editorial pitch — TNOA

This document is editorial preparation, not manuscript evidence. It is written to match the current Methods in Ecology and Evolution scope: the methodological gap should be independent of a focal organism, the contribution must be more than a workflow linking existing methods, computational methods should be tested by simulation/benchmarking, broad applicability should be clear, and code should be usable by readers.

## One-sentence pitch

TNOA is an observation-state interface for automated ecological sensing that prevents unresolved, nuisance-dominated and poorly observed records from being irreversibly collapsed into biological non-detections before downstream ecological models are fitted.

## Why this is a methods paper rather than a workflow

The contribution is not the sequence of software components used during development. The tested methodological objects are:

1. positive, non-complementary target and nuisance support;
2. separate measurement observability and attribution-gated coupled response;
3. preservation of B/T/N/U observation states before ecological inference;
4. calibration against a declared false-attribution criterion rather than inherited raw thresholds;
5. a frozen-generation falsification protocol that retains failed hypotheses and invalidated diagnostics;
6. a known-truth downstream experiment showing information loss caused by binary coarsening.

## Main evidence for an editor

- A changed nuisance representation retained ranking while an inherited raw threshold lost its registered operating meaning.
- A prespecified family-wise false-attribution criterion subsequently achieved the declared held-out control in the frozen synthetic benchmark.
- Across 3,003 known-truth latent-regime compositions, binary coarsening substantially widened the set of target prevalences compatible with the observation relative to retaining B/T/N/U.
- A preregistered matched-timescale ambiguity-ridge prediction failed and is reported as a negative result rather than rescued post hoc.
- The repository contains a minimal reusable Python API/CLI and a fail-closed field-translation template showing how another sensing system can reach the calibrated support flags consumed by the decision layer.

## Breadth beyond the motivating sensing system

The architecture is process-level rather than taxon-specific. A wildlife camera can instantiate T as focal-species support, N as independently measured masking/mimic processes and O as measurement adequacy. Passive acoustics can use focal-call support, overlapping/masking acoustic processes and microphone/temporal support. Interaction cameras can additionally use a local target-coupled response when independent attribution is available. Numerical thresholds do not transfer across these systems; the logical interface and calibration sequence do.

## Scope boundary to state proactively

The current quantitative evidence is closed-world. The manuscript does not claim field accuracy, field prevalence, biological-absence certification, universal score thresholds or quantitative cross-system transfer. Field implementation is provided as a prospective fail-closed translation pathway: preserve raw evidence, remain unresolved while uncalibrated, obtain independent truth, calibrate on grouped development data, freeze, evaluate held-out, and only then permit adaptive action.

## Optional covering-letter draft

Dear Editors,

Please consider our manuscript, “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework,” as a Standard Article for Methods in Ecology and Evolution.

Automated sensors increasingly create the observation records subsequently analysed by occupancy, interaction and state-space models. We address a methodological gap that arises before those models are fitted: target absence, inadequate observability, nuisance processes and unresolved target–nuisance coexistence can all be collapsed into the same binary non-detection. TNOA provides a process-preserving observation-state interface in which target and nuisance are positive non-complementary supports, measurement support and attribution are retained separately, and unresolved observations remain explicit rather than being converted to absence.

The paper is centred on method evaluation rather than a case study. In frozen synthetic experiments, we show that an inherited raw nuisance threshold can lose its operating meaning after a representation change even when ranking is retained; a prespecified family-wise false-attribution criterion restores the declared held-out control. We then use known latent truth across 3,003 regime compositions to show that binary coarsening discards information about downstream target prevalence that is preserved by the richer observation record. A preregistered matched-timescale ambiguity prediction is retained as a negative result. The manuscript includes a reusable Python implementation and a sensor-agnostic, fail-closed pathway for recalibrating the evidence channels in other ecological sensing systems.

We believe the manuscript fits MEE because the methodological problem is independent of a focal taxon, the central contribution is more than a software workflow, the method is evaluated by simulation/benchmarking, and the architecture can be instantiated across camera, acoustic and interaction-monitoring systems without claiming numerical threshold transfer.

The manuscript is prepared for double-anonymous review, and anonymized code/data and reproducibility materials are available in a reviewer-only package. The quantitative claims are explicitly closed-world; no field-accuracy or field-prevalence result is asserted.

Thank you for considering the manuscript.

Sincerely,

[Corresponding author]

## Short pre-submission-enquiry version

We are preparing a Standard Article entitled “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework.” The method addresses an upstream observation-process problem: automated sensors often collapse inadequate observability, nuisance-dominated windows and unresolved target–nuisance coexistence into the same biological non-detection before occupancy or other ecological models are fitted. TNOA retains positive target and nuisance support, observability, attribution and unresolved states as a reusable observation interface. Frozen synthetic benchmarking shows (i) why raw score thresholds need not transfer across representation changes even when ranking is preserved and (ii) that binary coarsening can discard substantial information about a known downstream target-prevalence estimand. A minimal Python implementation and fail-closed cross-sensor translation pathway are included. The current quantitative evidence is deliberately closed-world; field accuracy and numerical cross-system threshold transfer are not claimed. We would welcome advice on whether this methodological framing is suitable for MEE as a Standard Article.
