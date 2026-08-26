# TNOA methods-paper blueprint

## Working title

**When should an ecological sensor refuse to decide? Target–nuisance–observability–abstention for process-preserving ecological sensing**

Alternative shorter title:

**Target–nuisance–observability–abstention in ecological sensing**

## One-sentence paper question

> Under what observation conditions can an ecological sensor safely support a target or nuisance interpretation, and when must it retain abstention rather than manufacture false biological certainty?

## Contribution statement

TNOA is not proposed as a new insect classifier. It is a methodological architecture for ecological sensing that:

1. defines target and nuisance as independent positive process hypotheses;
2. preserves legitimate target+nuisance superposition;
3. separates measurement observability from both biological evidence and nuisance burden;
4. forbids low target evidence from serving automatically as target-absence evidence;
5. allows target-coupled responses only when independently attributed;
6. treats abstention as a valid scientific output;
7. calibrates decision boundaries by false-certainty risk rather than inherited raw score thresholds;
8. evaluates resolvability over a dimensionless phase space after observers are frozen.

## Paper boundary

### Paper 1 — TNOA method

Primary evidence:

- closed-world synthetic theory;
- frozen target and nuisance observers;
- dimensionless V14a/V14a2/V14b experiments;
- retained negative results;
- frozen 5.88M-world ternary surface;
- forced-binary comparison;
- semantic correction separating `no supported evidence` from proven information absence;
- risk-contract calibration logic.

Field accuracy is explicitly outside the central claim.

### Paper 2 / external validation

V15 and real PolliPi deployment can later test:

- field calibration of O;
- independent C attribution;
- nuisance effect-risk mapping;
- visit-rate estimation under interpretable exposure;
- real false-certainty / abstention trade-offs.

These results test external validity rather than retroactively defining TNOA.

# Manuscript structure

## Abstract

### Background

Autonomous ecological sensors increasingly decide when an event occurred and when additional recording or review is warranted. Non-detection is difficult to interpret because weak target evidence can arise from true absence, exogenous disturbance, measurement failure, missing attribution, or genuine process overlap.

### Method

Introduce TNOA and the evidence architecture `(T,C,N,O,A−)`. Define final decision vocabulary `B + {T,N,U}` with positive non-complementary T and N. Construct frozen synthetic process worlds over six dimensionless coordinates. Develop target and nuisance observers alternately, retaining failed generations and separating definition, representation, information and coupling contradictions. Freeze both observers and measure the final phase surface.

### Main result

The final frozen closed-world generation contains 5.88M worlds. Abstention remains substantial and is dominated in the registered design space by overlap/attribution rather than simple unsupported evidence. Increasing observation duration does not eliminate abstention monotonically because additional information can expose simultaneous target and nuisance processes. The earlier narrow timescale-collision hypothesis near `Pi2 ~= 1` is falsified. Direct attribution-channel availability strongly structures the frozen surface, with the explicit caveat that the exact `Pi3=0` boundary is a consequence of the synthetic direct-channel rule.

### Interpretation

Ecological sensing should not equate low target evidence with absence or force target and nuisance into mutually exclusive labels. A sensor can be scientifically useful by identifying where it is not entitled to decide.

## 1. Introduction

### 1.1 Ecological observation is a measurement problem

Biological state and measurement process are distinct. Wind, light, occlusion, frame loss and coupled target movement change what can be inferred from a camera without necessarily changing the underlying ecological event.

### 1.2 Why binary event/no-event framing is unsafe

A non-detection can mean:

- no event;
- event present but masked;
- event evidence outside current representation;
- observation channel failed;
- target and nuisance co-occur;
- local response occurred but attribution is missing.

### 1.3 Neighbouring methods solve only parts of this problem

Position relative to:

- reject-option / selective classification;
- uncertainty quantification;
- sensor fusion;
- active learning / disagreement acquisition;
- ecological preferential/adaptive sampling;
- observability / missing-data reasoning.

The literature section must avoid claiming component-level novelty until systematically audited.

### 1.4 TNOA

State the core insight:

> Target evidence, nuisance-process evidence and observability are not complements, and target absence requires its own evidence if it is to be certified.

## 2. Methods

### 2.1 Positive process ontology

Define B, T, N, U.

Explain that latent T and N may coexist and U is epistemic.

### 2.2 Evidence channels

Define T, C, N, O, optional A−.

Formalise:

`C_usable = C_response * C_attribution`.

State forbidden substitutions:

- `N = 1 - T`;
- `O = 1 - N`;
- `A− = low T`;
- `A− = good O + low T`.

### 2.3 Contradiction taxonomy

Four classes:

1. definition defect;
2. representation defect;
3. information absence;
4. process coupling/superposition.

### 2.4 Alternating observer development

Develop one observer at a time while siblings remain frozen. Stop by contradiction-type saturation, not by forcing disagreement to zero.

### 2.5 Dimensionless worlds

Define Pi1–Pi6 and why ratios rather than absolute physical scales are the transferable object.

### 2.6 Registered hypotheses and negative generations

Document:

- short-window information-support hypothesis;
- direct-evidence amplitude/channel hypothesis;
- rejected `Pi2 ~= 1` ambiguity-ridge hypothesis;
- coupled-response rescue hypothesis;
- spatial/sampling refinements Pi5/Pi6.

Retain all failed generations in the method ledger.

### 2.7 Observation-safe representation audit

Explain how truth leakage in an early target diagnostic invalidated that generation and how the corrected audit separated:

- direct-visible representation defect;
- indirect-only essential-attribution ambiguity under the available statistic family.

### 2.8 Target observer freeze

Direct-positive evidence is retained. Indirect-only response is not promoted without attribution. Target absence is not inferred from missing target support.

### 2.9 Nuisance observer and risk contract

Explain why raw threshold 0.55 failed after representation rescaling despite near-perfect ranking. Replace raw-score inheritance with a predeclared false-certainty budget and family-wise calibration.

### 2.10 Frozen ternary measurement generation

No observer, threshold, alpha, grid or estimand changes after freeze.

Report:

- 30,625 phase coordinates;
- six latent regimes;
- 32 repetitions;
- 5,880,000 worlds.

### 2.11 Decision outputs and U decomposition

Use final B/T/N/U outputs.

Distinguish:

- no-supported-evidence U;
- attribution/overlap U.

Do not call all no-support cases true information absence.

### 2.12 Binary-forcing comparator

Quantify the errors introduced when U is forcibly collapsed into target/absence decisions.

### 2.13 Claim boundary

All claims are closed-world methodological claims. Field calibration and ecological rate accuracy remain external validation.

## 3. Results

### 3.1 Negative result: timescale equality is not the main ambiguity boundary

The narrow `Pi2 ~= 1` collision prediction fails in both the original and refined spatiotemporal generations.

### 3.2 Attribution channels dominate a key identifiability transition

Direct-visible T+N is separable under observation-safe representation; indirect-only coupled response remains near chance under the available attribution-free statistic family.

### 3.3 Target observer can preserve direct evidence without inventing target absence

Frozen validation supports direct-visible target worlds and retains indirect-only truth-known target worlds as U when attribution is missing.

### 3.4 Nuisance ranking is not enough: raw score scale is not a decision contract

Show nuisance ranking vs inherited 0.55 failure and the move to family-wise false-certainty calibration.

### 3.5 Final frozen phase surface

Headline aggregate rates in the registered equal-grid / equal-regime design:

- B ~= 0.2302;
- T ~= 0.4287;
- N ~= 0.0877;
- U ~= 0.2533.

### 3.6 U is dominated by attribution/overlap in the frozen design space

Approximate decomposition:

- no-supported-evidence U ~= 0.02675;
- attribution/overlap U ~= 0.22658.

Frame this as a property of the registered design space, not a universal ecological frequency.

### 3.7 More observation does not monotonically eliminate U

Longer windows can reduce unsupported evidence while increasing detection of genuine process overlap. Therefore "observe longer" is not a universal solution to epistemic ambiguity.

### 3.8 Structural Pi3 boundary

Show the `Pi3=0` versus `Pi3>0` transition but explicitly identify it as a structural consequence of the exact-zero synthetic direct-channel rule.

## 4. Discussion

### 4.1 Abstention is part of ecological measurement design

A useful sensor is not one that always answers; it is one that distinguishes evidence sufficient for a claim from evidence that should remain unresolved.

### 4.2 Process preservation matters more than forced classification

T+N superposition is biologically and physically plausible and should survive the decision layer.

### 4.3 Absence is expensive

Without an independently validated A− channel, low target evidence cannot establish absence. Discuss implications for occupancy-like reasoning, interaction rates and adaptive monitoring.

### 4.4 Why this is not just selective classification

U depends on process and observation geometry, not solely model confidence.

### 4.5 Why this is not ordinary sensor fusion

Channels remain separate because their semantics differ and some combinations must remain unresolved rather than fused.

### 4.6 Negative results as method development

The retired Pi2 hypothesis, failed raw nuisance threshold, invalid truth-leaking diagnostic and failed historical disagreement-allocation generations demonstrate a freeze-and-falsify workflow that limits benchmark overfitting.

### 4.7 Transferability

Architecture can transfer, thresholds cannot. Each new sensing domain requires new channel definitions/calibration.

### 4.8 Limitations

Required limitations:

- synthetic closed-world realism;
- structural exact-zero direct-channel rule;
- chosen process families and phase grid;
- no field calibration in Paper 1;
- unresolved distinction between true information absence and unrepresented information for some no-support cases;
- no claim that T/N observer failures are statistically independent;
- no universal optimum abstention level.

## 5. Main figures

### Figure 1 — TNOA architecture

World -> T/C/N/O/A− -> B/T/N/U.

Show forbidden shortcuts (`1-T`, `1-N`, low-T -> absence) as crossed arrows.

### Figure 2 — Development/falsification ledger

Timeline from early dual-observer/disagreement hypothesis through V14b/V14c, retaining negative generations.

### Figure 3 — Dimensionless phase-space design

Six Pi axes and representative worlds showing baseline, direct target, nuisance, coupled response and superposition.

### Figure 4 — Attribution-channel result

Direct-visible vs indirect-only observation-safe separability and the resulting target observer rule.

### Figure 5 — Risk-contract transition

Nuisance score ranking remains strong while inherited raw threshold fails; family-wise alpha calibration controls false certainty.

### Figure 6 — Frozen 5.88M-world ternary surface

Main B/T/N/U response surfaces and U reason decomposition.

### Figure 7 — Forced binary vs abstention

False-certainty cost of collapsing U, with claim boundary and partial-identification interpretation.

## 6. Supplement

- full generation ledger;
- all prefrozen hypotheses;
- all runtime and artifact hashes;
- V14a2 and diagnosis surfaces;
- failed truth-leaking diagnostic provenance;
- target/nuisance freeze receipts;
- exact ternary runner specification;
- sensitivity across Pi axes;
- binary-forcing tables;
- test/CI matrix.

## 7. Target journal logic

Primary target: **Methods in Ecology and Evolution**, provided the literature audit supports methodological distinctiveness and the manuscript emphasises broad ecological-sensing transferability rather than flower-visitor specificity.

Fallback positioning can target ecological informatics / sensor-method journals if reviewers require empirical validation for the stronger methodological framing.

## 8. Submission gate

Do not submit until all are complete:

1. systematic neighbouring-method literature matrix;
2. final paper-specific source/provenance manifest;
3. regenerated paper figures from locked V14b/V14c artifacts only;
4. explicit binary-forcing baseline and ablations in manuscript tables;
5. code-release/reproducibility entry point;
6. claim audit against `CLAIM_BOUNDARY.md`.
