# MEE editorial pitch — TNOA

This document is editorial preparation, not manuscript evidence. It is written to match the current Methods in Ecology and Evolution scope: the methodological gap should be independent of a focal organism, the contribution must be more than a workflow linking existing methods, computational methods should be tested by simulation/benchmarking, broad applicability should be clear, and code should be usable by readers.

## One-sentence pitch

TNOA is a tested upstream observation contract for automated ecological sensing that preserves process-semantic target, nuisance, observability and attribution provenance before downstream ecological inference and quantifies what is lost when that record is coarsened.

## Why this is a methods paper rather than a workflow

The contribution is not the sequence of software components used during development, and it is not priority for abstention, uncertain ecological observations or continuous classifier scores. Those already have substantial prior art. The tested methodological objects are:

1. positive, non-complementary target and nuisance support as process propositions rather than alternative class labels;
2. separate measurement observability and attribution-gated coupled response;
3. preservation of B/T/N/U and unresolved-reason provenance before ecological inference;
4. calibration against a declared family-conditional false-attribution criterion rather than inherited raw thresholds;
5. a frozen-generation falsification protocol that retains failed hypotheses and invalidated diagnostics;
6. known-truth downstream experiments quantifying the magnitude of information lost under progressively coarser observation vocabularies.

## Nearest prior art and what we do not claim

Continuous-score occupancy already uses uncertain machine-learning scores without binary thresholding [@rhinehart2022continuous]. Multievent and partial-observation ecological models already preserve uncertain or equivocal events [@pradel2005multievent; @campbellgrant2023partial]. Multilabel partial abstention already permits coexistence and selective refusal [@nguyen2020partialabstention]. Blackwell comparison and partial-identification theory already provide the language for garbling and identified sets [@blackwell1953comparison; @manski2005partial]. TNOA therefore does not claim historical priority for any of those ideas.

The residual contribution is a process-semantic **sensor-to-inference observation contract** and an ecological experiment measuring the information lost when that contract is garbled before downstream inference.

## Main evidence for an editor

- A changed nuisance representation retained ranking while an inherited raw threshold lost its registered operating meaning.
- A predeclared family-conditional false-attribution criterion subsequently produced held-out rates `0/43,200` and `1,920/43,200 = 0.04444` in the two negative families. These are closed-world empirical checks, not a distribution-free guarantee.
- Across 3,003 known-truth latent-regime compositions, target/not-target is a deterministic coarsening of B/T/N/U, so the non-worsening direction is structural. The empirical magnitude was large: median target-prevalence compatible width was about `0.030` with B/T/N/U versus `0.266` after binary coarsening.
- A literature-audit-motivated post-freeze vocabulary ablation showed that U reason provenance retained additional information: target-prevalence median width fell from `0.02992` with generic U to `0.00408` with no-support versus overlap/attribution U separated; T+N co-occurrence width fell from `0.10494` to `0.01484`. This analysis is explicitly not preregistered.
- A preregistered matched-timescale ambiguity-ridge prediction failed and is reported as a negative result rather than rescued post hoc.
- The repository contains a minimal reusable Python API/CLI and a fail-closed field-translation template showing how another sensing system can reach the calibrated support flags consumed by the decision layer.

## Breadth beyond the motivating sensing system

The architecture is process-level rather than taxon-specific. A wildlife camera can instantiate T as focal-species support, N as independently measured masking/mimic processes and O as measurement adequacy. Passive acoustics can use focal-call support, overlapping/masking acoustic processes and microphone/temporal support. Interaction cameras can additionally use a local target-coupled response when independent attribution is available. Numerical thresholds do not transfer across these systems; the logical interface and calibration sequence do.

## Scope boundary to state proactively

The current quantitative evidence is closed-world. The manuscript does not claim field accuracy, field prevalence, biological-absence certification, universal score thresholds, distribution-free risk control or quantitative cross-system transfer. D3 is a post-freeze literature-audit-motivated analysis rather than a preregistered prediction. Field implementation remains a prospective fail-closed translation pathway: preserve raw evidence, remain unresolved while uncalibrated, obtain independent truth, calibrate on grouped development data, freeze, evaluate held-out, and only then permit adaptive action.

## Optional covering-letter draft

Dear Editors,

Please consider our manuscript, “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework,” as a Standard Article for Methods in Ecology and Evolution.

Automated sensors increasingly create the observation records subsequently analysed by occupancy, interaction and state-space models. Existing ecological methods already accommodate uncertain observations and can propagate continuous classifier scores or classification error downstream. We address a distinct upstream problem: what process-semantic record should an automated sensor emit before those downstream models are fitted? TNOA separates positive target and nuisance support, measurement observability, attribution-gated coupled response and independently supported absence, while unresolved observations and their reasons remain explicit rather than being converted to biological non-detections.

The paper is centred on method evaluation rather than a case study. In frozen synthetic experiments, an inherited raw nuisance threshold lost its operating meaning after a representation change even though ranking was retained; a predeclared family-conditional false-attribution calibration then satisfied the declared held-out criterion in both negative families. We use known latent truth across 3,003 regime compositions to quantify the downstream consequence of observation garbling. Median compatible target-prevalence width was about 0.030 with B/T/N/U retained versus 0.266 after binary coarsening. A clearly labelled post-freeze vocabulary ablation further showed that retaining unresolved-reason provenance narrowed the median target-prevalence width from 0.02992 to 0.00408 and the target+nuisance co-occurrence width from 0.10494 to 0.01484. A preregistered matched-timescale ambiguity prediction is retained as a negative result.

We believe the manuscript fits MEE because the methodological problem is independent of a focal taxon, the central contribution is more than a software workflow, the method is evaluated against frozen known truth, the closest prior methods and surrendered priority claims are explicit, and the architecture can be instantiated across camera, acoustic and interaction-monitoring systems without claiming numerical threshold transfer.

The manuscript includes reusable Python code and a sensor-agnostic fail-closed translation pathway. It is prepared for double-anonymous review, with anonymized reproducibility materials available in a reviewer-only package. The quantitative claims are explicitly closed-world; no field-accuracy, field-prevalence or formal distribution-free risk guarantee is asserted.

Thank you for considering the manuscript.

Sincerely,

[Corresponding author]

## Short pre-submission-enquiry version

We are preparing a Standard Article entitled “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework.” Existing ecological methods already retain uncertain events and can incorporate continuous classifier scores; our method addresses the upstream sensor-interface problem of what process-semantic observation should be emitted before downstream inference. TNOA retains positive target and nuisance support, observability, attribution and unresolved-reason provenance. Frozen known-truth benchmarking documents score-threshold portability failure and quantifies information lost under progressive observation coarsening (target-prevalence median compatible width 0.030 with B/T/N/U versus 0.266 after binary coarsening; 0.00408 when U reasons are additionally retained in a clearly labelled post-freeze ablation). A minimal Python implementation and fail-closed cross-sensor translation pathway are included. The current quantitative evidence is deliberately closed-world; field accuracy and numerical threshold transfer are not claimed. We would welcome advice on whether this methodological framing is suitable for MEE as a Standard Article.
