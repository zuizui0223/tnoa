# TNOA MEE figure plan

The main figures follow the revised result hierarchy. The historical phase-surface figures remain reproducible but are demoted to supplementary/design diagnostics where appropriate.

## Figure 1 — Observation states before downstream ecological inference

Conceptual figure.

### Panels

A. Latent ecological/observation processes: baseline, target, nuisance and co-occurrence.

B. Measurement evidence: direct target support, attribution-gated coupled response, nuisance support, measurement support and optional independent absence evidence.

C. Retained observation record: B / T / N / unresolved U with reason provenance.

D. Downstream interface: occupancy, interaction-rate, state-space or other ecological models receive the retained observation states rather than a prematurely forced target/absence record.

### Main message

TNOA is an observation-model interface upstream of ecological estimation, not merely a reject option attached to a classifier.

## Figure 2 — Raw score thresholds are not invariant decision criteria

Primary quantitative result: C6 -> C7.

### Panels

A. Development failure: the revised nuisance representation retains ranking while the inherited raw threshold `0.55` fails the registered coverage rule.

B. Diagnosis: a pooled false-attribution calibration fails family-wise control.

C. Frozen result: family-wise calibration at `alpha=0.05`, showing held-out false nuisance attribution for each registered negative family and the prespecified error-rate line.

### Main message

The reusable object is the prespecified operating error criterion, not a numerical score threshold copied across representations.

### Boundary

Closed-world validation only; no field threshold or field false-positive-rate claim.

## Figure 3 — Binary coarsening loses information about a downstream ecological estimand

Primary quantitative result from `derived/mee_synthetic_consequences.json` and its locked source surface.

### Panels

A. Distribution or ECDF of naive binary target-prevalence bias across the 3,003 registered latent-regime compositions.

B. Paired distribution of compatible target-prevalence widths with full B/T/N/U versus target/not-target coarsening.

C. Optional axis-slice summary showing where the four-state record remains informative and where both encodings are weak, including the Pi3=0 boundary.

### Main message

Preserving observation-process states constrains the downstream known-truth target-prevalence estimand more tightly than binary coarsening in the registered synthetic experiment.

### Boundary

The composition lattice is a deterministic sensitivity design, not an ecological prior, and the result is not a field visit-rate estimator.

## Figure 4 — What unresolved observations mean

Secondary quantitative result.

### Panels

A. U composition under equal weighting: no-supported-evidence versus overlap/attribution.

B. Bounded-reweighting sensitivity: minimum possible overlap/attribution share of U as `kappa` increases.

C. Pi1 reason decomposition: no-support peaks at Pi1=1 and then declines while overlap/attribution continues to increase.

### Main message

Unresolved observations are dominated by coexistence/attribution in the registered design and within the tested weighting class. Extending the observation window can exchange evidence shortage for attribution ambiguity; the exact pooled total-U curve is not a headline result.

## Supplementary Figure S1 — Preregistered Pi2 hypothesis and its rejection

Retain the Pi1×Pi2 surface and the registered contrast. Emphasize that the narrow matched-timescale ridge was not supported and that the small pooled Pi2=1 contrast is weighting-sensitive.

## Supplementary Figure S2 — Uneven effective separation of registered axes

Plot the post-freeze marginal axis-separation audit:

- Pi3 maximum total-variation shift about 0.6431 with only two distinct marginal decision vectors across five registered levels;
- Pi1 about 0.2665;
- Pi2 about 0.2402;
- Pi6 about 0.1608;
- Pi4 about 0.0728;
- Pi5 about 0.0214.

This is not an intrinsic-dimension estimate.

## Supplementary Figure S3 — Structural Pi3/C13 diagnostic

Retain the historical Pi3 plot only as a design diagnostic. Explicitly show

`0.3569 = 0.2 * 1.0 + 0.8 * 0.196125`.

Do not use zero false positives or 0.3569 as performance evidence.

## Supplementary Figure S4 — Method-generation falsification ledger

Include:

- Pi2 narrow-ridge prediction: not supported;
- target diagnostic: invalidated after truth-leakage audit;
- corrected observation-safe audit;
- target freeze;
- nuisance inherited-threshold failure;
- score-scale diagnosis;
- pooled family-wise calibration failure;
- family-wise risk freeze;
- final frozen phase-surface measurement;
- post-freeze estimand/weighting audit;
- post-freeze structural-axis audit.

## Rendering and provenance rules

- Every quantitative panel must be generated in code from pinned artifacts or pinned derived results.
- Primary archival/vector format: SVG; submission raster: 300-dpi PNG from the same script.
- Do not manually change plotted data geometry after generation.
- Design-space counts and pooled rates are provenance/descriptive information, not visual emphasis.
- Every generated set must carry source artifact hashes and claim/derived-analysis identifiers.
