# Reviewer attack matrix for TNOA Paper 1

This file converts the nearest-method literature into explicit reviewer objections and response boundaries. It is not manuscript prose; it is a pre-submission stress test.

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

### Evidence the manuscript must show
A schematic should place TNOA before occupancy/state-space inference and state that TNOA is complementary, not a replacement.

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
The paper must center the new formal object and experimentally tested geometry:

- non-complementary positive T/N hypotheses;
- separate O and optional A-;
- process-preserving B/T/N/U decision map;
- dimensionless phase-space measurement;
- false-certainty risk contract;
- frozen-generation contradiction protocol.

PolliPi and InsePi implementations are examples/provenance, not the novelty claim by themselves.

## Objection 8 — “The strong Pi3 boundary is tautological because direct evidence is defined structurally.”

### Required response
Agree in part. V14c already restricts the claim: the Pi3=0 versus Pi3>0 split is a structural result of the closed-world direct-channel rule, not a universal SNR law.

### Evidence the manuscript must show
Do not write “direct signal amplitude above zero is biologically sufficient.” Write that the frozen structural observer exposes channel availability as a dominant axis in this synthetic decision geometry.

## Objection 9 — “The U rates are arbitrary because the phase-space weighting is arbitrary.”

### Required response
The global B/T/N/U fractions are properties of the prefrozen equal-grid/equal-regime design, not estimated ecological prevalences.

### Evidence the manuscript must show
Every global rate should be labeled as a design-space summary. Claims should rely more strongly on response surfaces, contrasts and structural changes than on the pooled percentage itself.

## Objection 10 — “Why not minimize U?”

### Required response
Because U is not automatically error. Forcing a binary decision can create false certainty. The method optimizes/controls false certainty subject to coverage rather than treating abstention as a defect to eliminate.

### Evidence the manuscript must show
Include the forced-binary comparator and explain why its false-negative behavior is informative even though the closed generator produced no false-positive target calls under the registered rule.

## Objection 11 — “Your nuisance result is just threshold tuning.”

### Required response
The development history directly addresses this. A raw threshold inherited across score representations failed; the response was not post-hoc threshold search on positives, but a prefrozen family-wise false-certainty calibration on negative families with held-out validation.

### Evidence the manuscript must show
Retain PR #43 failure, PR #44 diagnosis and PR #46 family-wise risk freeze in the method-generation ledger.

## Objection 12 — “The method was over-developed on the benchmark.”

### Required response
The manuscript must make the frozen-generation protocol visible: negative generations are retained, truth-leakage diagnostics are invalidated rather than hidden, alternating development freezes one observer while changing the other, and the final surface is measured only after both sides are frozen.

### Evidence the manuscript must show
Include a concise generation timeline with FAIL / DIAGNOSIS / FREEZE / MEASUREMENT labels and immutable source hashes in the supplement.

## Submission gate implied by this matrix

Paper 1 should not be submitted until each objection above has a direct manuscript location (section, figure, table or supplement) rather than being answerable only from repository history.
