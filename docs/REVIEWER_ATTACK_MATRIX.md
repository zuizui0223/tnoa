# Reviewer attack matrix for TNOA Paper 1

This file converts the nearest-method literature and the MEE-facing stress test into explicit reviewer objections and response boundaries. It is not manuscript prose; it is a pre-submission attack surface.

## Objection 1 — “This is just selective classification / reject option.”

### Why the objection is plausible
Selective classification already formalizes abstention and risk–coverage trade-offs.

### Required response
TNOA must not claim novelty for abstention itself. The distinction is structural:

- T and N are independent positive hypotheses and may coexist;
- O is an independent measurement-support property, not classifier confidence;
- low T is not certified absence;
- A- is a separate optional evidence channel;
- C requires independent attribution;
- U can arise from recognized T+N coexistence/attribution ambiguity, not only low predictive confidence.

### Evidence the manuscript must show
Figure 1 and Methods must include a case with strong T and strong N that remains a legitimate superposition, and a case with low T but adequate O that still cannot become certified absence without A-.

## Objection 2 — “Ecologists already know non-detection is not absence; occupancy models solved this.”

### Why the objection is plausible
MacKenzie et al. and the imperfect-detection literature explicitly separate occupancy and detection.

### Required response
Agree with the premise. TNOA acts upstream of occupancy: it governs whether a sensor window can safely be emitted as target evidence, nuisance evidence, unresolved, or censored before detection/non-detection observations enter a population model.

The MEE synthetic-estimand analysis should make this connection operational: when the frozen observation process is collapsed to binary, target prevalence becomes less identifiable or is naively underestimated across most synthetic regime mixtures.

### Evidence the manuscript must show
A schematic should place TNOA before occupancy/state-space inference and state that TNOA is complementary, not a replacement. The downstream synthetic prevalence comparison should use known latent truth and remain explicitly non-field-calibrated.

## Objection 3 — “State-space models already separate process and observation error.”

### Required response
Agree. TNOA does not claim to invent process/observation separation. It specializes the sensor-decision layer where multiple positive processes can coexist and where the main object is decision entitlement for one observation window.

### Evidence the manuscript must show
The contribution statement must use “process-preserving sensing architecture” rather than “first separation of process and observation.”

## Objection 4 — “This is just sensor fusion.”

### Required response
Conventional fusion generally aims to combine channels into a better estimate of a latent state. TNOA can terminate without fusion into a unique state. It preserves T and N jointly and permits U when attribution is not justified.

### Evidence the manuscript must show
An explicit contrast between “fusion to sharpen a state estimate” and “channel preservation until a statement is licensed.”

## Objection 5 — “U is just uncertainty quantification.”

### Required response
U is not a scalar uncertainty estimate. It is a decision state produced by missing or competing evidential structure. TNOA distinguishes at least no-supported-evidence from overlap/attribution U, and V14c forbids calling all no-support cases information absence.

### Evidence the manuscript must show
The main result should report the U decomposition and the semantic correction from historical `information_absent` to `no_supported_evidence`.

## Objection 6 — “The method is flower-visitor specific.”

### Required response
The locked synthetic generator is visit-oriented, but the ontology is process-level. The paper must demonstrate mappings to multiple sensor domains without claiming quantitative transfer.

### Minimum transfer table
For each of the following, define T, C, N, O and optional A-:

- camera-trap animal event;
- acoustic call/event sensor;
- nest/feeding interaction monitor;
- phenology or remote camera anomaly/event monitor.

If a domain has no meaningful C or A-, mark that channel absent rather than forcing an analogy.

## Objection 7 — “The method is a workflow that strings together existing ideas.”

### Why this matters
MEE explicitly notes that workflows linking existing methods are generally not considered new methods.

### Required response
The paper must center the new formal object and experimentally tested consequences:

- non-complementary positive T/N hypotheses;
- separate O and optional A-;
- process-preserving B/T/N/U decision map;
- dimensionless phase-space measurement;
- false-certainty risk contract;
- frozen-generation contradiction protocol;
- downstream information loss when B/T/N/U is coarsened before ecological estimation.

PolliPi and InsePi implementations are examples/provenance, not the novelty claim by themselves.

## Objection 8 — “The strong Pi3 boundary is tautological because direct evidence is defined structurally.”

### Required response
Agree in part. V14c already restricts the claim: the Pi3=0 versus Pi3>0 split is a structural result of the closed-world direct-channel rule, not a universal SNR law.

### Evidence the manuscript must show
Do not write “direct signal amplitude above zero is biologically sufficient.” Write that the frozen structural observer exposes channel availability as a dominant axis in this synthetic decision geometry. The downstream slice analysis should retain the weak `Pi3=0` case rather than hiding it: median prevalence-identification width remains about 0.897 even with B/T/N/U retained.

## Objection 9 — “The U rates are arbitrary because the phase-space weighting is arbitrary.”

### Required response
The global B/T/N/U fractions are properties of the prefrozen equal-grid/equal-regime design, not estimated ecological prevalences. This is no longer answered only by a disclaimer.

A post-freeze density-ratio sensitivity analysis now asks which qualitative results survive bounded reweighting of the immutable rows.

### Current evidence

- The overlap/attribution share of U remains above 0.5 through the tested `kappa=10` class; its worst-case share is about 0.520 at `kappa=10`.
- Pi1 nonmonotonicity is not robust enough to remain a headline: a monotone non-increasing U curve is infeasible through `kappa=1.5` but becomes feasible at `kappa=1.6`.
- The small pooled Pi2=1 contrast is highly weight-sensitive: at `kappa=1.25` its admissible range already crosses zero.

### Evidence the manuscript must show
Global percentages should be secondary descriptive summaries. The robust headline should be the overlap/attribution composition result within its explicit reweighting class. Pi1 nonmonotonicity and the Pi2 pooled contrast must be presented as conditional design-space properties, not prior-free laws.

## Objection 10 — “Why not minimize U?”

### Required response
Because U is not automatically error. Forcing a binary decision can create false certainty and can destroy information used by downstream ecological estimands.

### Evidence the manuscript must show
Retain the forced-binary false-negative comparison, but do not stop there. Add the synthetic prevalence result: across the 3,003 regime-mixture lattice, naive binary prevalence is negatively biased in 99.63% of compositions, while calibrated B/T/N/U retention produces substantially narrower partial-identification sets than binary coarsening in almost all compositions.

## Objection 11 — “Your nuisance result is just threshold tuning.”

### Required response
The development history directly addresses this. A raw threshold inherited across score representations failed; the response was not post-hoc threshold search on positives, but a prefrozen family-wise false-certainty calibration on negative families with held-out validation.

### Evidence the manuscript must show
Retain PR #43 failure, PR #44 diagnosis and PR #46 family-wise risk freeze in the method-generation ledger.

## Objection 12 — “The method was over-developed on the benchmark.”

### Required response
The manuscript must make the frozen-generation protocol visible: negative generations are retained, truth-leakage diagnostics are invalidated rather than hidden, alternating development freezes one observer while changing the other, and the final surface is measured only after both sides are frozen.

The new MEE analysis is post-freeze and must remain a deterministic transformation of the immutable phase surface. It cannot alter observer thresholds or regenerate a preferred surface.

### Evidence the manuscript must show
Include a concise generation timeline with FAIL / DIAGNOSIS / FREEZE / MEASUREMENT / POST-FREEZE DERIVATION labels and immutable source hashes in the supplement.

## Objection 13 — “What ecological quantity becomes better identified by keeping these states?”

### Why this matters
Without a downstream ecological estimand, the paper can be read as a decision-ontology exercise rather than a method that changes ecological inference.

### Required response
Use synthetic target prevalence as the known-truth ecological estimand. For each regime composition, treat the frozen regime-by-B/T/N/U matrix as the observation process and compare the set of latent target prevalences compatible with:

1. full B/T/N/U observations;
2. the binary coarsening TARGET/not-TARGET.

Do not claim a field estimator. The point is information loss under coarsening.

### Current evidence
Across the deterministic 0.1 six-regime simplex (3,003 compositions):

- median naive forced-binary bias = about `-0.238` prevalence units;
- negative naive bias occurs in 99.63% of compositions;
- median TNOA-compatible width = about `0.030`;
- median binary-compatible width = about `0.266`;
- median relative width reduction where binary width is non-zero = about 84.45%;
- TNOA is never wider than binary, as expected from retaining a refinement of the same observation.

The 34 registered-axis slice audit preserves the “never wider” property, while also showing honest boundary cases where binary calibration already suffices or both encodings remain weak.

### Evidence the manuscript must show
A main-text figure or table should show naive bias plus identification-width comparison, and the Methods must define the latent prevalence estimand and partial-identification construction in ecological observation-model language.

## Submission gate implied by this matrix

Paper 1 should not be submitted to MEE until each objection above has a direct manuscript location (section, figure, table or supplement) rather than being answerable only from repository history.

The downstream estimand and weighting analyses are now implemented and locked. Remaining MEE-specific blockers are the minimal reusable implementation/API, the main-text vocabulary translation, and integration of these new results into the final manuscript/figure package.
