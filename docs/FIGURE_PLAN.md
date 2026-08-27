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

B. Score-scale diagnosis across registered Pi5 levels: spatial, temporal and combined components do not share a stable boundary at the inherited threshold.

C. Error-control comparison: pooled calibration fails the coupled-negative `alpha=0.05` gate, whereas family-wise calibration passes it.

### Main message

The reusable object is the prespecified operating error criterion, not a numerical score threshold copied across representations.

### Boundary

Closed-world validation only; no field threshold or field false-positive-rate claim.

## Figure 3 — Binary coarsening loses information about a downstream ecological estimand

Primary quantitative result from `derived/mee_synthetic_consequences.json` and its locked source surface.

### Panels

A. Distribution or ECDF of naive binary target-prevalence bias across the 3,003 registered latent-regime compositions.

B. Paired distribution of compatible target-prevalence widths with full B/T/N/U versus target/not-target coarsening.

### Main message

Preserving observation-process states constrains the downstream known-truth target-prevalence estimand more tightly than binary coarsening in the registered synthetic experiment.

### Boundary

The composition lattice is a deterministic sensitivity design, not an ecological prior, and the result is not a field visit-rate estimator.

## Figure 4 — What unresolved observations mean

Secondary quantitative result.

### Panels

A. Pi1 reason decomposition: no-support peaks at Pi1=1 and then declines while overlap/attribution continues to increase.

B. Bounded-reweighting sensitivity: minimum possible overlap/attribution share of U as `kappa` increases.

### Main message

Unresolved observations are dominated by coexistence/attribution in the registered design and within the tested weighting class. Extending the observation window can exchange evidence shortage for attribution ambiguity; the exact pooled total-U curve is not a headline result.

## Supplementary Figure S2 — Uneven effective separation of registered axes

Plot the post-freeze marginal axis-separation audit:

- Pi3 maximum total-variation shift about 0.6431 with only two distinct marginal decision vectors across five registered levels;
- Pi1 about 0.2665;
- Pi2 about 0.2402;
- Pi6 about 0.1608;
- Pi4 about 0.0728;
- Pi5 about 0.0214.

This is not an intrinsic-dimension estimate.

The preregistered Pi2 negative result, structural Pi3/C13 diagnostic and method-generation falsification ledger remain in the manuscript-facing audit documents and may be presented as supplementary tables or text. They are not outputs of the current eight-panel MEE figure builder.

## Rendering and provenance rules

- Every quantitative panel must be generated in code from pinned artifacts or pinned derived results.
- Primary archival/vector format: SVG; submission raster: 300-dpi PNG from the same script.
- Do not manually change plotted data geometry after generation.
- Design-space counts and pooled rates are provenance/descriptive information, not visual emphasis.
- Every generated set must carry source artifact hashes and claim/derived-analysis identifiers.
