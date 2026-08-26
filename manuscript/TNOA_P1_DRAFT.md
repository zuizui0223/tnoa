# When should an ecological sensor refuse to decide? Target–nuisance–observability–abstention for process-preserving ecological sensing

## Abstract

Ecological sensors increasingly automate event detection, but a weak event signal can arise from several different situations: true absence, exogenous disturbance, poor measurement support, missing attribution, or genuine coexistence of biological and non-biological processes. Established methods address important parts of this problem, including imperfect detection, reject-option classification, set-valued decisions, uncertainty representation and observation-process modeling. Here we introduce **target–nuisance–observability–abstention (TNOA)** as an integrated sensor-decision architecture for ecological observation. TNOA defines target and nuisance as positive, non-complementary process hypotheses; separates direct target evidence, attributed target-coupled response, exogenous nuisance evidence and observability; permits target+nuisance coexistence; and requires independent evidence if target absence is to be certified. The resulting decision vocabulary closes as baseline plus target, nuisance or undetermined, with abstention retained whenever the available evidence channels do not license a unique biological statement.

We developed the framework in a closed synthetic world over six dimensionless process and observation coordinates. Observer generations were frozen before one-shot evaluation, failed hypotheses were retained, and operational nuisance decisions were calibrated against a predeclared false-certainty budget rather than an inherited raw score. The final frozen measurement comprised 30,625 phase-space coordinates and 5,880,000 synthetic worlds, with no observer retuning after freeze. <!-- C8 --> Under equal weighting of the registered grid and latent regimes, decision rates were approximately 0.230 baseline, 0.429 target, 0.088 nuisance and 0.253 undetermined. <!-- C9 --> Most undetermined outcomes in that design were associated with overlap or attribution rather than the historical no-support category. <!-- C10 --> Longer observation did not monotonically eliminate abstention because recognition of process coexistence could increase even as simple evidence shortage changed. <!-- C11 --> The originally registered hypothesis of a narrow ambiguity ridge near equal target and nuisance timescales was not supported. <!-- C2 -->

TNOA does not claim to invent abstention, imperfect-detection correction, set-valued prediction or evidence uncertainty. Its contribution is the integrated ecological sensor-decision contract and the frozen dimensionless geometry induced by that contract. The present study establishes a closed-world methodological result; field accuracy, field absence certification and transfer of quantitative thresholds remain external validation tasks.

**Keywords:** ecological sensing; imperfect detection; abstention; observability; nuisance process; uncertainty; camera monitoring; measurement error

---

## 1. Introduction

### 1.1 Ecological observation is not biological truth

Automated cameras, acoustic recorders and other ecological sensors do not observe ecological state directly. They observe a physical scene through a measurement channel. The same biological event can therefore generate different records under different illumination, occlusion, camera geometry, motion, noise or temporal sampling conditions. Conversely, non-target processes can resemble biological events or obscure them. Camera-trap research has made this measurement dependence explicit by decomposing detection into component processes and documenting animal-, environment-, camera- and setup-dependent failures [@hofmeester2019framing; @findlay2020detection]. Hierarchical and state-space ecological models likewise distinguish ecological process from observation process [@royle2008hierarchical; @augermethe2021statespace].

A foundational consequence is that nondetection cannot generally be equated with absence. Occupancy models formalized this point by estimating occurrence under imperfect detection [@mackenzie2002occupancy], and later extensions allowed both false-negative and false-positive observation errors [@roylelink2006occupancy]. TNOA begins from the same broad measurement principle, but addresses an earlier stage of the inferential pipeline. Before an automated sensor emits a detection or nondetection datum for later ecological analysis, what biological statement is that individual observation window entitled to support?

### 1.2 Why binary target/no-target decisions are insufficient

Consider a camera monitoring a focal flower. A low target score can arise because no insect entered the relevant interaction zone, because an insect was occluded, because image quality was inadequate, because a target-driven flower response occurred without direct visual evidence, or because the representation used by the observer failed to encode available information. Strong target evidence can also coexist with wind or background motion. Thus a binary target/no-target classifier collapses several distinct questions:

1. Is there positive evidence for the focal biological process?
2. Is there positive evidence for an exogenous process that can mimic, mask or corrupt attribution?
3. Did the measurement channel preserve enough information to attempt the biological inference?
4. If a local target response occurred, is it attributable to the focal interaction?
5. Is there any independent evidence for biological absence?

These questions are not logical complements. A quiet scene is not automatically observable; a noisy scene is not automatically unobservable; weak target evidence is not negative target evidence; and a target event can occur while nuisance is also present.

### 1.3 Neighbouring methods solve important parts of the problem

Several established method families motivate, but do not individually define, the architecture considered here. Selective classification and reject-option methods allow a predictor to abstain when predictive risk is too high [@elyaniv2010selective; @geifman2017selective; @geifman2019selectivenet; @hendrickx2024reject], and conformal reject methods can add formal error guarantees under their assumptions [@garciagalindo2024conformalreject; @szabadvary2025reject]. Partial-reject methods can retain non-singleton class sets [@karlsson2024partialreject], while open-set recognition permits rejection of samples outside the known class taxonomy [@geng2021openset]. Belief-function and evidential approaches explicitly represent ignorance, conflict and incomplete evidence [@denoeux2019belief; @gao2026evidential].

These methods establish that abstention, multiple hypotheses, unknown conditions and evidence conflict are not new ideas. Likewise, ecological imperfect-detection and state-space models already separate biological and observation processes. The methodological question for TNOA is narrower: can these concerns be organized into an explicit **ecological sensor-decision contract** in which target, nuisance and observability retain distinct positive semantics, target and nuisance may coexist, coupled responses require attribution, and absence cannot be inferred by negating target support?

### 1.4 TNOA

We call this architecture **target–nuisance–observability–abstention (TNOA)**. Its field-facing evidence layer is

\[
(T, C, N, O, A^-),
\]

where \(T\) is direct positive target evidence, \(C\) is target-coupled response usable only with independent attribution, \(N\) is positive exogenous nuisance-process evidence, \(O\) is positive measurement support or observability, and \(A^-\) is optional independently validated target-absence evidence. The final closed decision vocabulary is

\[
B + \{T, N, U\},
\]

where \(B\) is baseline and \(U\) is undetermined/abstention. Target and nuisance are not mutually exclusive natural classes; target+nuisance coexistence is a legitimate process configuration. <!-- C1 -->

Our contribution is not a new insect classifier or a claim of priority for abstention, imperfect detection or uncertainty representation. It is the integration of these constraints into a process-preserving ecological sensing architecture, together with a controlled experiment that measures its resolvability geometry over a frozen dimensionless process space.

We ask four questions. First, does ambiguity form the narrow timescale-collision ridge originally hypothesized, or is it structured by other evidence geometry? Second, can target evidence be preserved without turning missing target support into biological absence? Third, can nuisance decisions be calibrated by tolerated false certainty rather than raw score inheritance? Fourth, after both observers are frozen, where in process space does the architecture support target, nuisance or abstention?

---

## 2. Methods

### 2.1 Positive process ontology

TNOA distinguishes latent/process structure from final decision vocabulary. A world can contain no marked dynamic deviation, a focal target process, an exogenous nuisance process, target-driven coupled response, or combinations of these processes. The decision layer is intentionally smaller.

**Baseline (B)** is the unmarked state in which no dynamic target/nuisance adjudication is required. For marked dynamic windows, the sensor may retain positive support for target, nuisance, or no unique decision. Importantly,

\[
N \neq 1-T,
\]

and target+nuisance support may coexist. The final `T` or `N` decision therefore means that the corresponding positive evidence is sufficient for the registered decision contract, not that the competing latent process is logically impossible.

### 2.2 Evidence channels T, C, N, O and A−

The evidence channels are defined independently because each supports a different proposition.

**Direct target evidence (T).** This channel supports the focal biological actor or event itself. In the PolliPi implementation that motivated the field bridge, portable target evidence is ordinal rather than probabilistic: `no_activity` and `environmental_noise` map to 0, `uncertain_local_activity` to 0.5 and `strong_visitation_candidate` to 1. <!-- C15 --> A score of 0 means only that strong positive target evidence was not retained; it is not biological absence.

**Target-coupled response (C).** A local biological response can provide useful information, but only if it can be attributed to the focal interaction. We therefore define

\[
C_{usable}=C_{response}\,C_{attribution}.
\]

A local flower movement with no independent attribution channel cannot be promoted to target evidence merely because it is spatially local. In the frozen target observer, indirect-only coupled response was retained as U rather than promoted to target support. <!-- C4 -->

**Nuisance evidence (N).** Nuisance is defined by a finite vocabulary of effects on inference rather than an open-ended list of physical causes. The relevant effects are processes that can mimic target evidence, mask a target, corrupt attribution, or degrade observation support. Wind, illumination changes and camera motion are examples of possible causes, not the definition itself.

**Observability (O).** O is a positive property of the measurement channel: whether relevant geometry, visibility, spatial resolution, photometry and temporal continuity are sufficient to attempt the focal inference. It is not the complement of N. A scene may be noisy but observable or quiet but unobservable.

**Independent absence evidence (A−).** TNOA permits a target-absence channel only if absence is independently supported. Neither `low T` nor `good O + low T` is defined as A−. In the current field-bridge generation, no validated A− channel is assumed; consequently the safe upper bound on target presence remains 1 when absence is not independently certified.

### 2.3 Undetermined outcomes and reason provenance

U is an epistemic output, not a natural third process. We distinguish at least two operational reasons:

1. **no-supported-evidence U**, in which available observers do not provide sufficient positive support for a unique target or nuisance decision;
2. **overlap/attribution U**, in which evidence coexistence or missing attribution prevents a unique statement.

The first category is deliberately not called true information absence. Information may exist in the world but remain unrepresented by the current observer. This semantic distinction was introduced after the frozen V14b measurement and is retained as V14c interpretation rather than used to alter the locked result.

### 2.4 Contradiction-guided development

Method development used disagreements and failures diagnostically rather than assuming that disagreement itself was an optimal acquisition score. Four contradiction types were distinguished:

1. **definition defect:** the ontology or decision contract is internally wrong;
2. **representation defect:** the required information exists but the observer fails to encode it;
3. **no-support / unresolved information status:** available evidence does not justify a unique decision;
4. **process coupling/superposition:** multiple processes are genuinely active.

Observer development alternated. When the target side was modified, the nuisance side was held fixed, and vice versa. Development stopped by contradiction-type saturation rather than by forcing disagreement or abstention to zero.

### 2.5 Dimensionless synthetic worlds

The closed-world generator was parameterized by six dimensionless coordinates:

\[
\Pi_1 = \frac{\text{observation-window duration}}{\text{target-process timescale}},
\]

\[
\Pi_2 = \frac{\text{nuisance-response timescale}}{\text{target timescale}},
\]

\[
\Pi_3 = \frac{\text{direct target amplitude}}{\text{nuisance amplitude}},
\]

\[
\Pi_4 = \frac{\text{target-driven local-response amplitude}}{\text{nuisance amplitude}},
\]

\[
\Pi_5 = \frac{\text{nuisance spatial correlation length}}{\text{target spatial-support width}},
\]

and

\[
\Pi_6 = \text{samples per target timescale}.
\]

Using ratios rather than absolute physical units makes the synthetic object a response surface over process geometry rather than a benchmark tied to one camera frame rate or one organismal timescale.

### 2.6 Registered hypotheses and retained negative generations

The development history was preserved rather than rewritten as a monotonic success story. Early experiments registered the expectation that ambiguity could become maximal when nuisance and target timescales approached equality, \(\Pi_2\approx1\). The refined spatiotemporal experiment added explicit spatial and sampling dimensions and again tested this collision hypothesis.

The registered narrow-ridge hypothesis was not supported in either the original or refined generations. <!-- C2 --> Rather than modifying the generator to recover the expected result, the hypothesis was retired and later interpretation shifted toward attribution-channel availability and evidence geometry.

A separate target-separability diagnostic was invalidated when a code audit found that latent target topology and ideal actor trajectory leaked into diagnostic features. That generation is retained as a failed diagnostic and is not used as evidence for target separability. A corrected observation-safe audit then excluded the leaking features.

### 2.7 Observation-safe target diagnosis and freeze

Under the corrected observation-safe representation, direct-visible target+nuisance worlds were strongly separable in the registered diagnostic, whereas direct-absent indirect-only coupled worlds remained near chance under the available attribution-free statistic family. <!-- C3 --> The interpretation was therefore asymmetric: direct target information existed and the previous target route had a representation defect, while indirect-only evidence remained unresolved without a new attribution channel.

The target observer was then frozen. In its validation, nuisance-only worlds produced no target support; direct-visible target+nuisance and direct-visible coupled worlds retained target support; and indirect-only target-present worlds were retained as U rather than promoted without attribution. <!-- C4 C5 --> This freeze does not imply field calibration or a universal rule that indirect evidence is uninformative.

### 2.8 Nuisance observer and false-certainty contract

Nuisance development exposed a distinct problem. A revised nuisance representation preserved excellent ordering between nuisance and non-nuisance worlds, but an inherited raw threshold of 0.55 produced poor positive coverage. <!-- C6 --> The failure therefore concerned decision-scale inheritance rather than loss of nuisance information.

The final nuisance decision rule was calibrated against a predeclared family-wise false-certainty budget \(\alpha=0.05\). Negative calibration families were treated separately rather than pooled because a pooled quantile had failed to control error within each family. The resulting frozen contract yielded held-out false nuisance attribution of 0 for target-only negative worlds and 0.04444 for target+nuisance+coupling negative worlds, within the registered 0.05 budget. <!-- C7 --> These are closed-world validation rates and are not field false-positive rates.

### 2.9 Final frozen ternary measurement

After target and nuisance rules were frozen, the final measurement generation evaluated 30,625 phase-space coordinates, six latent regimes and 32 repetitions, totaling 5,880,000 synthetic worlds. <!-- C8 --> No observer was retuned after the freeze.

The final outputs were baseline, target, nuisance and U, together with reason-resolved U summaries and a forced-binary comparator. The source generation retained historical field names that were later semantically clarified without changing the underlying counts.

### 2.10 Forced-binary comparator

To quantify what is hidden when abstention is disallowed, a prefrozen binary comparator collapsed unresolved cases into a target/absence decision. In the registered closed generator, this rule produced no false target positives but missed 35.69% of latent target-present worlds under the equal-grid/equal-regime weighting. <!-- C13 --> This number is a property of the synthetic design and comparator; it is not a field miss rate.

The historical summary also included a quantity named `visit_presence_partial_identification_width`. Subsequent semantic audit showed that, because N does not certify target absence, the historical `baseline + U` quantity is not a strict target-presence partial-identification width. Paper 1 therefore treats it only as a descriptive non-target-decision width.

### 2.11 Reproducibility and claim control

Scientific generations are linked to immutable workflow runs, execution commits, artifact digests and result hashes. Failed generations remain in provenance. Paper figures are generated only from locked JSON artifacts pinned by Git blob SHA and the final phase-surface SHA. Manuscript result sentences are linked internally to claim IDs in `CLAIM_TRACEABILITY.md`.

### 2.12 Paper boundary

All quantitative claims in Paper 1 are closed-world methodological claims. We do not infer field prevalence, field detection accuracy, field nuisance false-positive rate, calibrated biological absence or pollination effectiveness. A separate empirical bridge is being developed to test whether real systems can be calibrated and located on the synthetic decision geometry without changing the locked Paper-1 result.

---

## 3. Results

### 3.1 The registered narrow timescale-collision hypothesis was not supported

The original expectation that ambiguity would form a narrow critical band near \(\Pi_2=1\) failed in both the earlier dimensionless generation and the refined spatiotemporal generation. <!-- C2 --> In the final frozen surface, total U showed only a broad and shallow non-monotonic pattern over \(\Pi_2\), rather than a dominant narrow ridge (Fig. 3). This result rejects the registered narrow-ridge hypothesis for the present closed generator; it does not imply that timescale ratios are irrelevant in other sensing systems.

### 3.2 Attribution-channel availability structured a key target transition

The corrected observation-safe diagnostic showed strong separation for direct-visible target+nuisance worlds, while indirect-only coupled-response worlds without a direct channel remained near chance under the available statistic family. <!-- C3 --> The target observer therefore retained direct-positive evidence and refused to promote indirect-only response without independent attribution. In the subsequent frozen validation, nuisance-only target support was zero and direct-visible target support was one under the registered worlds, while indirect-only target-present worlds remained U. <!-- C4 C5 -->

The final phase surface preserves the same structural consequence. For target-present worlds at the registered \(\Pi_3=0\) level, target decision rate was zero and U was high; all registered positive \(\Pi_3\) levels produced nearly identical target and U rates (Fig. 4). <!-- C12 --> We interpret this as a consequence of the frozen exact-zero direct-channel rule, not as evidence for a universal ecological signal-to-noise threshold.

### 3.3 Nuisance ranking and nuisance decision scale were different problems

The nuisance-development sequence showed that strong discrimination did not justify carrying a historical raw threshold into a redefined score representation. <!-- C6 --> The initial nuisance process-scale generation preserved ranking but failed its positive-coverage rule under the inherited threshold. A subsequent diagnosis localized the issue to decision-scale meaning rather than observer information.

Replacing raw-score inheritance with a family-wise false-certainty contract resolved this specific closed-world decision problem. With \(\alpha=0.05\), held-out false nuisance attribution was 0 for target-only negative worlds and approximately 0.0444 for target+nuisance+coupling negative worlds (Fig. 5). <!-- C7 --> The calibration is not proposed as a field threshold; its methodological role is to tie the operational boundary to a declared cost of false certainty.

### 3.4 Final frozen decision surface

The final frozen experiment comprised 30,625 dimensionless coordinates and 5,880,000 worlds. <!-- C8 --> Under equal weighting across the registered grid and latent regimes, the aggregate decision rates were approximately

\[
B=0.2302,\qquad T=0.4287,\qquad N=0.0877,\qquad U=0.2533.
\]

<!-- C9 --> These are design-space frequencies, not ecological prevalences.

### 3.5 Most U in the registered design was associated with overlap or attribution

The historical final result separated U into a source field originally called `information_absent` and an overlap/attribution category. V14c semantic audit established that the first label was too strong; without an independent information-availability diagnostic, it is more accurately described as **no-supported-evidence U**.

Using that corrected terminology, aggregate no-supported-evidence U was approximately 0.02675, whereas overlap/attribution U was approximately 0.22658. <!-- C10 --> Thus most U in the registered equal-weight synthetic design arose from recognized coexistence or missing attribution rather than the no-support category. This composition is a property of the registered design, not a universal ecological frequency.

### 3.6 Longer observation did not monotonically eliminate abstention

Across the registered \(\Pi_1\) levels, total U increased from short observation windows and then remained high rather than declining monotonically (Fig. 2). <!-- C11 --> The reason decomposition shows why: no-supported-evidence U and overlap/attribution U moved differently. Longer windows can reveal more of the scene while simultaneously exposing that target and nuisance processes coexist, making attribution rather than raw information availability the limiting problem.

Thus “observe longer” is not, by itself, a universal solution to sensor ambiguity in the TNOA architecture.

### 3.7 Forced binary decisions hid target-present worlds

The prefrozen forced-binary comparator produced a false-negative rate of 0.3569 among latent target-present worlds under the registered equal-grid/equal-regime weighting. <!-- C13 --> The comparison is not intended to show that abstention is universally optimal. It shows that, in this frozen design, forcing every unresolved window into a binary decision can conceal substantial target-present structure that the process-preserving system keeps unresolved.

---

## 4. Discussion

### 4.1 Decision entitlement is an ecological measurement problem

TNOA reframes automated sensing from “which class should this window receive?” to “which biological statement does the available evidence license?” This shift is modest in one sense: ecology already has a mature literature on imperfect detection, observation models and measurement error [@mackenzie2002occupancy; @roylelink2006occupancy; @royle2008hierarchical; @augermethe2021statespace]. It is nevertheless operationally consequential at the sensor interface. A downstream occupancy or interaction model cannot recover distinctions that an edge system has already collapsed—for example, if an unobservable window has been stored as a biological absence.

TNOA therefore complements rather than replaces imperfect-detection models. Its intended output is a provenance-rich observation record that preserves which evidence channels were available and why an event was supported, a nuisance process was supported, or a decision remained U.

### 4.2 Abstention is not the novelty; reasoned abstention is part of the architecture

Reject-option methods establish a well-developed theory of abstention and risk–coverage trade-offs [@elyaniv2010selective; @hendrickx2024reject]. Partial-reject approaches allow sets of candidate labels [@karlsson2024partialreject], conformal methods can add error guarantees [@garciagalindo2024conformalreject; @szabadvary2025reject], open-set methods recognize unknown conditions [@geng2021openset], and belief/evidential frameworks can represent ignorance and conflict [@denoeux2019belief; @gao2026evidential].

Accordingly, TNOA does not claim novelty for refusing a decision, retaining multiple hypotheses or representing ignorance. Its contribution lies in deciding **which ecological propositions are kept distinct before abstention is computed**. T, C, N, O and A− have different semantics and forbidden substitutions. The final U reason can therefore expose a missing measurement channel or genuine process coexistence rather than merely low confidence.

### 4.3 Target and nuisance should not be forced into complementary labels

A biologically interesting event and an exogenous disturbance can occur simultaneously. In the TNOA ontology, target+nuisance is therefore a legitimate latent/process state. <!-- C1 --> This differs from a conventional target-versus-noise classifier in which increasing confidence in one class necessarily reduces the other.

Preserving coexistence changes what additional sensing can accomplish. If U is caused by insufficient evidence, more observation may resolve it. If U is caused by known T+N coexistence without an attribution channel, simply extending the same observation can reveal more evidence without licensing a unique interpretation. The Pi1 result illustrates this distinction in the registered synthetic design. <!-- C11 -->

### 4.4 Certified absence requires distinct evidence

The strongest safety rule in TNOA is simple:

\[
\text{low }T \not\Rightarrow A^-.
\]

Good observability plus low target evidence still does not, by definition, create an independent absence channel. This rule is consistent with the ecological lesson that nondetection does not imply absence [@mackenzie2002occupancy], but applies it at the sensor-decision layer. In systems where certified absence matters, an A− channel must be justified independently. Where such a channel does not exist, the appropriate scientific output may remain unresolved.

This restriction is intentionally conservative. Whether its cost is worthwhile in real field monitoring is an empirical question for the V15 bridge, not a result of the present simulation.

### 4.5 False-certainty contracts are more portable than inherited raw scores

The nuisance development sequence demonstrates a common methodological trap: a score threshold can appear meaningful only because of a particular representation scale. <!-- C6 --> Once the score definition changed, the inherited numerical threshold no longer represented the intended risk even though ranking remained strong.

TNOA therefore treats the tolerable false-certainty rate as the decision-level quantity of interest and lets a development calibration map that risk contract onto the current score representation. The successful family-wise \(\alpha=0.05\) generation provides one closed-world example. <!-- C7 --> We do not claim that \(\alpha=0.05\) or its resulting score threshold should transfer to field systems. The transferable object is the distinction between **risk contract** and **raw score scale**.

### 4.6 Negative generations are part of the method

Several of the most informative steps were failures. The expected narrow \(\Pi_2\) collision ridge was not supported. <!-- C2 --> A target diagnostic was invalidated by truth leakage. A nuisance representation retained ranking while its inherited threshold failed. A pooled false-certainty calibration failed family-wise control before the family-wise contract succeeded.

These failures are retained because they constrain the final interpretation. The framework is therefore not presented as the result of one optimization run. Definitions, protocols and one-shot evaluations were frozen at generation boundaries so that negative evidence could change the method without silently rewriting previous outcomes.

### 4.7 Transferability is architectural, not numerical

The TNOA channels can be mapped conceptually to other sensor domains. In a camera trap, T could be direct evidence for a focal species, N could represent exogenous processes that mimic or mask detection, and O could capture camera geometry and image support. In passive acoustics, T could be vocalization evidence, N could include overlapping non-target sound and masking, and O could include microphone saturation or temporal coverage. Similar mappings are possible for nest cameras, feeding monitors and phenology systems.

What does **not** transfer automatically is the numerical observer, threshold, nuisance feature set or phase-space frequency. Each domain requires its own definitions and calibration. The current quantitative result is therefore evidence that the architecture can be studied as a controlled decision geometry, not evidence that its flower-visitor parameterization is universally optimal.

### 4.8 Limitations

The primary limitation is that Paper 1 is a closed-world methods study. The synthetic processes are designed to expose identifiable measurement relationships, not to reproduce the full complexity of natural camera scenes. Field calibration is absent, and the present results do not establish real visit-detection accuracy or ecological rates.

Second, the strong \(\Pi_3=0\) versus positive-\(\Pi_3\) contrast follows an exact-zero direct-channel rule in the frozen generator. <!-- C12 --> It should not be interpreted as a universal continuous signal-to-noise law.

Third, no-supported-evidence remains epistemically ambiguous in some worlds. The system cannot always distinguish true lack of informative structure from information that exists but is missing from the current representation. We therefore avoid calling the entire no-support category “information absence.”

Fourth, TNOA does not establish statistical independence between target and nuisance observer failures, nor does it identify a universal optimal abstention rate. Finally, the targeted prior-art audit is not systematic. We therefore make an integration-level novelty claim rather than an absolute historical-priority claim.

### 4.9 Empirical next step

The next stage is to connect the frozen architecture to real devices without changing the Paper-1 result. The V15 bridge separates field measurement of direct T, attribution-gated C, exogenous N and O, freezes sampling and truth-annotation protocols before held-out evaluation, and retains no A− assumption unless an independent absence channel is validated. The empirical question is not whether field results can rescue the closed-world method, but where real systems lie relative to its decision geometry and what new contradiction types appear.

---

## 5. Conclusions

TNOA provides a process-preserving contract for ecological sensor decisions. It keeps target and nuisance as positive non-complementary hypotheses, keeps observability separate from both, requires attribution for coupled response, and refuses to create absence by negating target support. The final frozen synthetic experiment shows that these constraints produce a non-trivial decision geometry in which abstention is often associated with attribution and process coexistence rather than simple no-support, and in which longer observation does not necessarily eliminate unresolved decisions. <!-- C8 C9 C10 C11 -->

The broader methodological point is not that ecological sensors should always abstain more. It is that an automated observer should expose the conditions under which its biological statement is justified—and should preserve unresolved evidence when those conditions are not met.

---

## Data and code availability

The TNOA paper package records claim-to-artifact provenance, figure-generation guards and the source commits for locked PolliPi/InsePi results. Quantitative paper figures are generated from source JSON artifacts whose Git blob SHA values and phase-surface SHA are pinned in `paper_manifest.json`. Historical one-shot results are treated as immutable scientific records; later reruns do not replace them.

The present manuscript is a working draft and should be converted to the final journal format only after the repository-level claim audit remains green against the instantiated text.

## Author contributions

To be completed at submission.

## Acknowledgements

To be completed at submission.

## References

Bibliography source: `references.bib`.
