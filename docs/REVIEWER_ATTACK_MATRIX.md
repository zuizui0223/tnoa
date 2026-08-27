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

### Required response
Agree with the premise. TNOA acts upstream of occupancy: it governs whether a sensor window can safely be emitted as target evidence, nuisance evidence, unresolved, or censored before detection/non-detection observations enter a population model.

The MEE synthetic-estimand analysis makes this connection operational: when the frozen observation process is collapsed to binary, target prevalence becomes less identifiable or is naively underestimated across most synthetic regime mixtures.

### Evidence the manuscript must show
A schematic should place TNOA before occupancy/state-space inference and state that TNOA is complementary, not a replacement. The downstream synthetic prevalence comparison must use known latent truth and remain explicitly non-field-calibrated.

## Objection 3 — “State-space models already separate process and observation error.”

### Required response
Agree. TNOA does not claim to invent process/observation separation. It specializes the sensor-decision layer where multiple positive processes can coexist and where the main object is the observation state handed to downstream ecological inference.

## Objection 4 — “This is just sensor fusion.”

### Required response
Conventional fusion generally aims to combine channels into a better estimate of a latent state. TNOA can terminate without fusion into a unique state. It preserves T and N jointly and permits U when attribution is not justified.

## Objection 5 — “U is just uncertainty quantification.”

### Required response
U is not a scalar uncertainty estimate. It is a decision state produced by missing or competing evidential structure. TNOA distinguishes no-supported-evidence from overlap/attribution U, and the semantic clarification forbids calling all no-support cases information absence.

## Objection 6 — “The method is flower-visitor specific.”

### Required response
The locked synthetic generator is visit-oriented, but the ontology is process-level. Show mappings to camera traps, passive acoustics, nest/feeding monitors and phenology cameras without claiming numerical transfer. If a domain has no meaningful C or A-, mark that channel absent rather than forcing an analogy.

## Objection 7 — “The method is a workflow that strings together existing ideas.”

### Why this matters
MEE explicitly notes that workflows linking existing methods are generally not considered new methods.

### Required response
Center experimentally tested consequences rather than repository plumbing:

- non-complementary positive T/N hypotheses;
- separate O and optional A-;
- process-preserving B/T/N/U observation map;
- prespecified false-attribution/error criterion;
- frozen-generation contradiction protocol;
- downstream information loss when B/T/N/U is coarsened before ecological estimation.

Upstream source repositories are provenance and implementation sources, not the novelty claim by themselves.

## Objection 8 — “The strong Pi3 boundary is tautological because direct evidence is defined structurally.”

### Required response
Agree. The boundary is a structural result, not a performance discovery. The post-freeze effective-axis audit makes the limitation explicit: five registered Pi3 values produce only **two** distinct marginal B/T/N/U vectors, zero versus positive.

### Evidence the manuscript must show
Do not write that positive signal amplitude is biologically sufficient. Treat Pi3 primarily as a structural channel-availability axis in this generation.

## Objection 9 — “The U rates are arbitrary because the phase-space weighting is arbitrary.”

### Required response
The global B/T/N/U fractions are properties of the prefrozen equal-grid/equal-regime design, not estimated ecological prevalences. A post-freeze density-ratio sensitivity analysis now asks which qualitative results survive bounded reweighting of the immutable rows.

### Current evidence

- overlap/attribution remains a majority of U through the tested `kappa=10` class; worst-case share is about 0.520;
- the exact Pi1 pooled total-U shape is not robust enough for a headline; a monotone non-increasing curve becomes feasible at about `kappa=1.6`;
- the small pooled Pi2=1 contrast already admits either sign at `kappa=1.25`.

### Evidence the manuscript must show
Global percentages are secondary. Weighting-robust statements must name their tested weighting class.

## Objection 10 — “Why not minimize U?”

### Required response
Because U is not automatically error. Forcing a binary decision can create false certainty and destroy information used by downstream ecological estimands.

### Evidence the manuscript must show
The synthetic prevalence analysis is the main answer. Across the 3,003 registered regime-mixture compositions, binary coarsening discards information that the four-state observation preserves. C13 is only a design diagnostic and should not carry this argument by itself.

## Objection 11 — “Your nuisance result is just threshold tuning.”

### Required response
This is the strongest development result. A redefined nuisance representation retained ranking while the inherited raw threshold failed its coverage rule. The repair was not post-hoc threshold search on positive test cases: a prefrozen family-wise false-attribution criterion was calibrated on negative families and then evaluated held-out. A pooled quantile had itself failed family-wise control before family-specific calibration passed.

### Evidence the manuscript must show
Promote the failure → diagnosis → pooled-calibration failure → family-wise calibration pass sequence to a primary result, with the failure retained rather than rewritten away.

## Objection 12 — “The method was over-developed on the benchmark.”

### Required response
Make the frozen-generation protocol visible: negative generations are retained, truth-leakage diagnostics are invalidated rather than hidden, alternating development freezes one observer while changing the other, and the final surface is measured only after both sides are frozen. Post-freeze analyses may transform only the immutable surface and cannot retune observers.

## Objection 13 — “What ecological quantity becomes better identified by keeping these states?”

### Required response
Use synthetic target prevalence as the known-truth ecological estimand. For each regime composition, treat the frozen regime-by-B/T/N/U matrix as the observation process and compare the set of latent target prevalences compatible with full B/T/N/U versus TARGET/not-TARGET.

### Current evidence
Across the deterministic 0.1 six-regime simplex (3,003 compositions):

- median naive forced-binary bias = about `-0.238` prevalence units;
- negative naive bias occurs in 99.63% of compositions;
- median TNOA-compatible width = about `0.030`;
- median binary-compatible width = about `0.266`;
- median relative width reduction where binary width is non-zero = about 84.45%;
- TNOA is never wider than binary, as expected from retaining a refinement of the same observation.

The 34 registered-axis slice audit preserves the “never wider” property while exposing boundary cases where both encodings are weak or the coarsening loses little.

## Objection 14 — “You call this a six-dimensional phase space, but how many axes actually distinguish outcomes?”

### Why the objection is serious
A large nominal grid can create the impression of complexity without corresponding effective response dimensionality. The exact-zero Pi3 rule is especially vulnerable because four positive Pi3 levels collapse.

### Required response
Report marginal axis separation rather than implying six equally effective dimensions. In the frozen deviation design, maximum total-variation shifts between level-mean B/T/N/U vectors are approximately:

- Pi3: `0.6431` with only **2** distinct marginal decision vectors across 5 registered levels;
- Pi1: `0.2665`;
- Pi2: `0.2402`;
- Pi6: `0.1608`;
- Pi4: `0.0728`;
- Pi5: `0.0214`.

These are descriptive marginal summaries, not intrinsic-dimension estimates. The correct claim is that the **six-coordinate registered design has strongly uneven effective separation**.

### Evidence the manuscript must show
Describe 30,625 coordinates and 5.88M worlds as design coverage/provenance, not evidence magnitude. Explicitly state that Pi3 behaves as a binary structural axis and Pi4/Pi5 weakly separate the final marginal decision vector in this generation.

## Objection 15 — “Your 35.69% forced-binary miss rate and zero false-positive rate are built into the design.”

### Required response
Agree and demote C13. The exact decomposition is:

- `FN(Pi3=0) = 1.0`;
- `FN(Pi3>0) = 0.196125` at every registered positive level;
- equal-grid `FN = 0.2*1 + 0.8*0.196125 = 0.3569`.

The zero target false-positive rate likewise follows the frozen positive-target observer on the registered non-target regimes. These quantities are not transferable performance metrics.

### Evidence the manuscript must show
Keep C13 only as a transparent comparator diagnostic. The downstream prevalence-mixture analysis, not 0.3569, must carry the claim that binary coarsening can damage ecological inference.

## Objection 16 — “Where is the method readers can actually run?”

### Required response
TNOA includes a minimal reusable Python API and CSV CLI. It accepts **already-calibrated positive-support flags**, maps them to B/T/N/U with reason provenance, and summarizes U rates by user-supplied ecological covariates. It deliberately does not ship universal raw-score thresholds.

### Evidence the manuscript must show
The code/data statement and repository documentation should point to `tnoa/`, `docs/REUSABLE_IMPLEMENTATION.md`, `examples/minimal_evidence.csv`, and tests. The Methods should separate domain-specific support calibration from the reusable process-preserving decision layer.

## Objection 17 — “The API starts after calibration. How does a real ecologist get to those support flags without circularity?”

### Why this objection matters
A reusable decision function is not operationally useful if the paper leaves the most dangerous step—turning raw sensor outputs into T/N/O/C support—implicit. Copying synthetic or source-device thresholds would contradict the paper's own portability result.

### Required response
Provide a prospective **fail-closed field translation pathway**, not field-validation claims:

1. keep an interpretable primary scientific record;
2. log raw target, nuisance, observability and coupled-response diagnostics separately;
3. before calibration, retain those windows as unresolved (`field_calibration_pending`) and leave TNOA acquisition actions inactive;
4. establish independent biological-event, coupled-response, nuisance and observability truth, using a separate reference channel when the primary stream cannot resolve hidden presence/absence;
5. blind annotators to algorithm scores/states;
6. calibrate on recording-day × scene/individual × block development groups against declared error criteria;
7. freeze the calibration manifest before held-out days/scenes are scored;
8. enable reason-specific adaptive acquisition only after held-out observation semantics are validated.

### Evidence the manuscript must show
Methods must include the sequence at a concise level and Discussion must show camera-trap/acoustic/interaction examples. `docs/FIELD_TRANSLATION_PATHWAY.md` should provide the implementation detail. The manuscript must explicitly state that this is guidance, not Paper-1 empirical field evidence.

## Submission gate implied by this matrix

Each objection above now has a direct manuscript location, figure, quantitative audit, runnable code path or implementation document. The previous MEE-specific blockers—downstream ecological consequence, weighting sensitivity, structural-axis audit, reusable implementation and ecological-statistical vocabulary—are resolved in the current package.

Remaining pre-upload work is production/user metadata rather than a missing scientific answer: validate the final formatted DOCX after any text change, complete author/title-page metadata, perform final human figure/reference rendering inspection, rebuild the final reviewer ZIP with author/institution literals in the identity scanner, and rerun the claim audit after material revision.
