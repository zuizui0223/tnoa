# Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework

## Abstract

See `submission/MEE_FRONT_MATTER.md` for the numbered MEE abstract used in the anonymous submission build.

---

## 1. Introduction

### 1.1 Automated sensors produce observations, not ecological truth

Camera traps, acoustic recorders and other automated sensors increasingly convert physical records into ecological data. Those data are subsequently used to estimate occurrence, activity, interaction rates and other ecological quantities. The statistical ecology literature has long recognized that an ecological process and the process by which it is observed are different objects [@mackenzie2002occupancy; @roylelink2006occupancy; @royle2008hierarchical; @augermethe2021statespace]. Camera-trap studies likewise show that geometry, environment, device settings and behaviour can alter detection independently of the ecological state of interest [@hofmeester2019framing; @findlay2020detection].

A practical problem occurs before those downstream models are fitted. An automated sensor must decide what observation record to emit. A weak target signal can mean that the target was absent, that it was present but poorly observed, that a non-target process masked or mimicked it, or that target and nuisance processes occurred together. If these situations are collapsed at the sensor interface into `target` versus `not target`, a later occupancy, interaction or state-space model cannot recover distinctions that were discarded upstream.

We address this observation-interface problem. Our aim is not to replace imperfect-detection models, nor to introduce abstention as a machine-learning concept. Instead, we ask which observation states should be retained when positive target evidence, positive nuisance evidence, measurement support and attribution are not logical complements.

### 1.2 Why binary coarsening can be ecologically consequential

Suppose an automated flower camera emits a non-detection whenever direct insect evidence is absent. That same non-detection may contain at least four different observation situations: a quiet and well-supported baseline, a nuisance-dominated window, an unresolved window with insufficient positive evidence, or a window in which target and nuisance evidence coexist but cannot be uniquely attributed. Treating all four as biological absence makes a strong assumption at data creation rather than at ecological analysis.

This distinction is closely related to the familiar principle that non-detection is not absence, but it applies one stage earlier. Occupancy and observation models can account for imperfect detection only if the data record preserves enough information to represent the observation process. We therefore treat the sensor output as an observation state rather than a natural class label.

### 1.3 Relation to reject options, uncertainty and observation models

Selective classification, reject-option methods, set-valued prediction, open-set recognition and evidential approaches already provide mature ways to withhold or broaden predictions [@elyaniv2010selective; @geifman2017selective; @geifman2019selectivenet; @hendrickx2024reject; @geng2021openset; @denoeux2019belief]. TNOA does not claim priority for these ideas. Ecological hierarchical models likewise already separate ecological and observation processes.

The narrower contribution here is an observation-state interface tailored to ecological sensing. Target and nuisance are represented as positive, non-complementary process supports; measurement support is represented separately; a target-coupled response requires independent attribution before it is promoted to target evidence; and biological absence requires evidence distinct from low target support. When available evidence does not support a unique observation statement, the record remains unresolved rather than being coerced to absence.

Accordingly, we evaluate TNOA as a tested method rather than as a conceptual workflow. One operational experiment asks whether a nuisance decision can retain a declared error meaning after its numerical score representation changes. A second asks how much downstream information about a known ecological estimand is lost when the process-preserving observation record is deterministically coarsened to target/not-target. Falsified predictions and post-freeze sensitivity analyses then constrain, rather than expand, those methodological claims.

### 1.4 Questions

We evaluate four questions. First, can an operational nuisance decision remain meaningful when the numerical representation of nuisance changes, or must the decision boundary be tied to a prespecified error criterion rather than an inherited raw threshold? Second, does preserving the richer observation record retain information about a downstream ecological estimand that is lost under binary coarsening? Third, does the preregistered prediction of a narrow ambiguity ridge at matched target and nuisance timescales survive a frozen synthetic test? Fourth, which features of the resulting unresolved observations are robust to alternative weighting of the registered design?

---

## 2. Methods

### 2.1 Observation states and evidence channels

The field-facing evidence layer is

\[
(T,C,N,O,A^-),
\]

where `T` is direct positive target evidence, `C` is a target-coupled local response, `N` is positive evidence for an exogenous nuisance process, `O` is measurement support for the focal inference, and `A-` is optional independently validated evidence of target absence.

These channels support different propositions. In particular,

\[
N \neq 1-T,
\]

and low `T` does not create `A-`. A coupled response is usable as target evidence only when attribution is independently supported. Target and nuisance processes may coexist.

The minimal observation vocabulary is baseline (`B`), target-supported (`T`), nuisance-supported (`N`) and unresolved (`U`). These are observation states, not four mutually exclusive ecological states. Baseline indicates that no marked dynamic deviation requires target/nuisance adjudication. `U` indicates that the available observation does not support a unique target/nuisance statement. We retain reason provenance for unresolved observations, especially no-supported-evidence and overlap/attribution cases. <!-- C1 C4 C14 -->

### 2.2 Reusable decision layer

The repository includes a minimal Python API and CSV command-line interface that maps already-calibrated positive-support flags to B/T/N/U and reports reason-resolved U rates by user-specified ecological covariates. The reusable layer begins **after** domain-specific calibration: it does not define a universal detector threshold or convert a raw score to target/nuisance support.

This separation is deliberate. A camera, acoustic model or rule-based observer may produce very different raw score scales. The reusable object is the process-preserving observation mapping, while score calibration remains a domain-specific measurement problem. An unobservable window cannot silently become baseline; simultaneous positive target and nuisance support is retained as unresolved under the minimal exclusive-decision output; and a local coupled response without attribution remains unresolved. The implementation and example input are documented in `docs/REUSABLE_IMPLEMENTATION.md`.

### 2.3 Fail-closed field translation sequence

A real sensor should not move directly from uncalibrated detector scores to the calibrated support flags consumed by the reusable layer. We therefore separate measurement acquisition, field calibration and decision/control. During a pre-calibration deployment, the system may log raw direct-target, nuisance, observability and coupled-response diagnostics, but the corresponding calibrated-support fields remain unavailable. These windows stay unresolved with explicit calibration-pending provenance, and the TNOA layer does not alter the primary acquisition schedule. A detector's generic `noise` or `not-target` output is not automatically converted to positive nuisance support, and a local response does not become target evidence without independent attribution.

Field calibration then requires truth that is defined independently of the algorithm under calibration. For event-sensing systems we distinguish biological-event truth, target-coupled-response truth, exogenous nuisance truth and primary-stream observability truth. If the primary stream cannot resolve hidden presence or absence, a separate reference channel is needed for truth establishment and is not supplied to the tested observer. Reference truth that remains unresolved is retained as unresolved rather than converted to absence.

Calibration and validation should also respect the dependence structure of the data. Consecutive frames from one observation block are not independent replicates, so development and held-out material should be separated at a grouping level such as recording day × focal scene or individual × recording block. Evidence channels are calibrated on development groups against declared error criteria, the calibration manifest is frozen, and new days/scenes are then scored held-out. Only after those semantics are validated should reason-specific TNOA states be allowed to change adaptive acquisition. This sequence is implementation guidance; no field result from such a deployment is used as evidence in Paper 1. The complete sensor-agnostic pathway is documented in `docs/FIELD_TRANSLATION_PATHWAY.md`.

### 2.4 Registered synthetic design

We evaluated the observation mapping in a closed synthetic design defined by six dimensionless coordinates:

\[
\Pi_1=\frac{\text{observation-window duration}}{\text{target-process timescale}},
\]

\[
\Pi_2=\frac{\text{nuisance-response timescale}}{\text{target timescale}},
\]

\[
\Pi_3=\frac{\text{direct target amplitude}}{\text{reference nuisance amplitude}},
\]

\[
\Pi_4=\frac{\text{target-driven local-response amplitude}}{\text{reference nuisance amplitude}},
\]

\[
\Pi_5=\frac{\text{nuisance spatial correlation length}}{\text{target spatial-support width}},
\]

and

\[
\Pi_6=\text{samples per target timescale}.
\]

The registered latent regimes were baseline, target only, nuisance only, target plus coupled response, target+nuisance superposition, and target+nuisance with coupling. Target was represented as a localized entry/dwell/exit process. Nuisance was a temporally correlated exogenous process whose shared component decayed across reference regions according to `Pi5`. Coupled response was local to the focal target support. `Pi6` changed actual temporal sampling rather than only a post-hoc feature.

The final frozen surface covered 30,625 registered coordinate combinations and 5,880,000 synthetic worlds. <!-- C8 --> These counts describe design coverage and provenance; they are not used as evidence magnitude.

### 2.5 Freeze, falsification and retained failures

Development was separated into generations. Definitions, observers and decision criteria were frozen before each one-shot or held-out evaluation. Failed hypotheses were retained rather than overwritten.

A preregistered expectation that unresolved observations would form a narrow ridge near matched target and nuisance timescales (`Pi2` approximately 1) was not supported in the earlier or refined synthetic generations. <!-- C2 --> A target-separability diagnostic was invalidated after code audit identified latent truth leakage; the corrected observation-safe audit excluded those features. Direct-visible target+nuisance worlds remained separable under the corrected representation, while indirect-only coupled-response worlds without an attribution channel remained unresolved. <!-- C3 C4 -->

### 2.6 From nuisance score ranking to a prespecified error-rate criterion

Nuisance development exposed a different failure mode. A revised nuisance representation retained strong ordering between nuisance and non-nuisance worlds, but the historical raw threshold `0.55` no longer produced the intended positive coverage. <!-- C6 --> The problem was therefore not simply loss of nuisance information; the numerical meaning of the score boundary had changed with the representation.

Rather than search post hoc for a threshold on the final positive evaluation set, we specified a family-wise false-attribution criterion of `alpha=0.05`. Negative calibration families were treated separately because a pooled quantile failed to control the error within each family. The resulting frozen rule was then evaluated held-out. It produced false nuisance attribution of `0` in the target-only negative family and approximately `0.04444` in the target+nuisance+coupling negative family, both within the prespecified criterion. <!-- C7 --> These are closed-world validation rates, not field false-positive rates.

### 2.7 Frozen observation surface and weighting sensitivity

After target and nuisance rules were frozen, the final measurement emitted B/T/N/U together with unresolved-reason provenance. Equal-grid/equal-regime summaries are retained for reproducibility, but they are not interpreted as ecological prevalence.

To assess dependence on design weighting, we performed a post-freeze density-ratio sensitivity analysis on the immutable rows. Relative to the equal-grid/equal-regime design, each row weight could vary within `1/kappa` and `kappa`, subject to the mean weight remaining one. No observer or threshold was changed. We used this class to ask whether the dominance of overlap/attribution U, the `Pi1` total-U shape and the small `Pi2=1` contrast could be reversed by bounded reweighting. <!-- C2 D1 -->

### 2.8 Downstream synthetic target-prevalence estimand

We next asked whether preserving B/T/N/U changes what can be inferred about a downstream ecological quantity. The estimand was the known latent target prevalence across the six registered synthetic regimes.

Let `p` be a six-element vector of latent-regime proportions and let `M` be the frozen six-by-four emission matrix whose columns are B/T/N/U probabilities. The observed four-state distribution is

\[
q=pM.
\]

Let `z=(0,1,0,1,1,1)` indicate which registered regimes contain the target. The known-truth target prevalence is

\[
\theta=pz.
\]

For the four-state observation, we computed the minimum and maximum `theta` over all non-negative regime mixtures summing to one that reproduce the retained B/T/N/U distribution. For the binary coarsening, only TARGET versus not-TARGET was retained and the same compatible-mixture calculation was repeated. The difference between the upper and lower compatible `theta` values is the identification width.

Because the binary record is a deterministic function of B/T/N/U, every latent mixture compatible with the four-state record is also compatible with the binary record. The four-state compatible set is therefore nested within the binary compatible set, so its identification interval cannot be wider. This nesting is a mathematical property of the two representations, not an empirical performance result. The registered experiment estimates the **magnitude** of the information lost under coarsening: how much wider the binary-compatible interval becomes over the tested latent-regime compositions and axis slices. <!-- D1 -->

We evaluated a deterministic simplex lattice with regime proportions in increments of 0.1, giving 3,003 synthetic compositions. The lattice is a design for sensitivity analysis, not an ecological prior. We also repeated the width comparison within all 34 registered single-axis slices. As a deliberately naive secondary comparator, we treated the TARGET observation proportion itself as a binary estimate of latent target prevalence. <!-- D1 -->

### 2.9 Structural interpretation audit

A second post-freeze audit asked how strongly the six registered coordinates separate the final observation distribution. For each coordinate, we averaged B/T/N/U over the remaining axes and non-baseline latent regimes, counted distinct marginal decision vectors at numerical tolerance `1e-10`, and calculated the maximum total-variation distance between level-mean observation distributions. These summaries describe this frozen design; they are not estimates of intrinsic ecological dimensionality. <!-- D2 -->

The same audit decomposed the historical forced-binary false-negative summary by `Pi3` to determine how much of that number is determined by the registered grid composition. <!-- C13 D2 -->

### 2.10 Scope and claim boundary

All numerical results in this paper are closed-world methodological results. We do not estimate field flower-visitor accuracy, field nuisance rates, field target prevalence, biological absence or pollination effectiveness. Numerical score thresholds, the exact `Pi3` boundary and the synthetic emission matrix do not transfer automatically to another device, site, taxon or sensor domain. The field question is whether real evidence channels can be measured and calibrated without changing the logical distinctions preserved here.

---

## 3. Results

### 3.1 An inherited raw threshold failed even when nuisance ranking was retained

The nuisance-development sequence separated representation quality from decision calibration. After the nuisance representation changed, discrimination remained strong, but carrying forward the historical raw threshold failed the registered positive-coverage rule. <!-- C6 --> Thus a threshold value that had operational meaning under one score representation did not retain that meaning under another.

The prespecified family-wise false-attribution criterion resolved this closed-world decision-scale problem. Under `alpha=0.05`, held-out false nuisance attribution was `0` for target-only negative worlds and approximately `0.04444` for the second registered negative family. <!-- C7 --> A pooled calibration had failed family-wise control before the family-specific calibration passed. The transferable methodological object in this experiment was therefore the declared error criterion, not the numerical raw-score threshold.

### 3.2 Binary coarsening discarded information about synthetic target prevalence

The non-worsening direction is fixed by construction: because TARGET/not-TARGET is a deterministic coarsening of B/T/N/U, retaining the four-state record cannot produce a wider compatible set than discarding distinctions. The empirical result is the size of that advantage in the registered observation process. Across the 3,003 registered regime compositions, the median identification width was approximately `0.030` with B/T/N/U retained versus `0.266` after binary coarsening. Among compositions with non-zero binary width, the median relative reduction was approximately `84.45%`. <!-- D1 --> The same nesting relation held across all 34 registered single-axis slices, while the amount of narrowing varied with the slice.

As a secondary diagnostic, the deliberately naive TARGET/not-TARGET prevalence estimate underestimated known latent target prevalence in `99.63%` of compositions, with median bias approximately `-0.238` prevalence units. <!-- D1 --> This is not a field bias estimate and is not the main information-preservation claim; it describes the registered synthetic emission process and comparator.

This result changes the interpretation of unresolved observations. Their value is not that every U should later be converted into a target event. Their value is that retaining observation-process distinctions prevents the sensor from destroying potentially useful information before an ecological model is fitted.

### 3.3 The preregistered matched-timescale ambiguity ridge was not supported

The expectation that unresolved observations would form a narrow critical band near `Pi2=1` failed in both the earlier dimensionless experiment and the refined spatiotemporal generation. <!-- C2 --> In the final surface, the equal-weight total-U contrast near `Pi2=1` was shallow rather than dominant, and post-freeze reweighting showed that the small centre-versus-neighbour contrast could change sign within the tested `kappa=1.25` class. <!-- D1 --> We therefore retain the failed prediction as a negative result rather than rescuing it through post-hoc changes to the generator.

### 3.4 Unresolved observations were dominated by overlap/attribution, but observation duration is secondary

Under equal weighting of the registered design, no-supported-evidence U was approximately `0.02675`, whereas overlap/attribution U was approximately `0.22658`. <!-- C10 --> The composition result was substantially more robust than the pooled U rate itself: overlap/attribution remained more than half of U throughout the tested density-ratio class through `kappa=10`, with a worst-case share of about `0.52`. <!-- D1 -->

The `Pi1` reason decomposition gives a narrower mechanistic illustration. From `Pi1=1` to `Pi1=3.162`, no-supported-evidence U decreased from about `0.0539` to `0.0268`, while overlap/attribution U increased from about `0.2751` to `0.3190`. <!-- C11 D2 --> Thus extending the observation window can reduce evidence shortage while leaving or increasing an attribution/coexistence problem. However, overlap/attribution already accounts for roughly 84–94% of U across the registered `Pi1` levels, and the exact pooled total-U shape is weighting-sensitive. We therefore treat the reason substitution, not generic non-monotonicity, as the relevant observation-process result.

### 3.5 The six registered coordinates had strongly uneven effective separation

The final experiment used six coordinates, but they did not behave as six equally effective response dimensions. `Pi3` had five registered numerical levels but only two distinct marginal B/T/N/U vectors: zero and positive. Its maximum total-variation shift between level means was `0.6431`. <!-- C12 D2 --> Corresponding maximum shifts were about `0.2665` for `Pi1`, `0.2402` for `Pi2`, `0.1608` for `Pi6`, `0.0728` for `Pi4` and `0.0214` for `Pi5`. <!-- D2 -->

These results are descriptive marginal separations, not intrinsic-dimension estimates. They show why the number of simulated coordinates should be treated as design coverage rather than as evidence that all six registered coordinates are equally informative ecological dimensions.

### 3.6 The historical forced-binary miss rate is a design diagnostic, not performance

The registered equal-grid comparator reports a target-present false-negative rate of `0.3569`. <!-- C12 C13 --> The structural audit shows that this number is exactly reconstructed from the `Pi3` composition: false-negative rate is `1.0` at `Pi3=0` and `0.196125` at every registered positive `Pi3` level, so

\[
0.3569=0.2\times1.0+0.8\times0.196125.
\]

<!-- C13 D2 -->

The registered zero target false-positive rate likewise follows the frozen positive-target observer on the non-target regimes. We therefore do not use either quantity as a performance claim. The prevalence-mixture analysis in Section 3.2 is the stronger ecological consequence of binary coarsening because it evaluates information loss across many synthetic regime compositions rather than elevating one equal-grid rate.

---

## 4. Discussion

### 4.1 Preserve observation-process information before ecological modelling

The main practical result is upstream of any particular occupancy, interaction or abundance model. Automated sensors create the observation record that downstream models receive. If a sensor stores unresolved, nuisance-dominated and baseline windows as the same biological non-detection, the downstream analyst cannot reconstruct the original observation process from the binary record alone.

The direction of the information comparison is structural, not a discovered performance advantage: a deterministic coarsening cannot make the retained observation more informative than the record from which it was derived. What the known-truth experiment contributes is the scale of the consequence in the registered observation process. Median compatible target-prevalence width increased from about `0.030` with B/T/N/U retained to `0.266` after binary coarsening, while some boundary slices remained weak under both representations. <!-- D1 --> This is the ecological use case for TNOA: not “more abstention” for its own sake, but avoiding a quantitatively large irreversible coarsening before ecological inference in conditions where the discarded distinctions matter.

### 4.2 Error criteria transfer more naturally than raw score thresholds

The nuisance sequence provides a second practical lesson. A detector or feature representation may change while retaining useful ranking. In that situation, copying the old numerical threshold can silently change the operating error rate. The frozen development history shows this failure directly: the representation retained ordering, the inherited threshold failed, a pooled calibration failed family-wise control, and a prespecified family-wise false-attribution criterion subsequently passed held-out.

This does not establish that `alpha=0.05` is universally appropriate. The transferable principle is to specify the tolerated observation error at the decision level and calibrate the current score representation to that criterion, rather than treating a raw threshold as an invariant property of the ecological problem.

### 4.3 Unresolved states can identify what additional measurement is missing

An unresolved observation is not a single type of uncertainty. No-supported-evidence U and overlap/attribution U imply different measurement problems. More sampling or improved observability may help the first. The second may require a new attribution channel because target and nuisance can be simultaneously supported.

The `Pi1` decomposition illustrates the distinction without supporting a universal observation-duration law. After `Pi1=1`, the no-support component declined while overlap/attribution continued to rise. Simply extending the same observation can therefore reveal that multiple processes coexist without making their attribution unique.

### 4.4 Negative results constrain the method

Two failures are particularly informative. First, the preregistered `Pi2` matched-timescale ridge was not supported. Second, a target diagnostic was discarded after truth leakage was found. These failures were retained because a methods paper is stronger when its development history distinguishes a failed hypothesis, a representation defect and a successful calibration from one another.

The structural-axis audit adds another constraint. The frozen `Pi3` result is largely a zero-versus-positive channel-availability rule, and `Pi4`/`Pi5` weakly separate the marginal decision distribution. The paper therefore does not use the nominal size of the grid as a substitute for effective experimental variation.

### 4.5 What is reusable, what must be recalibrated and how to transfer it

The repository separates a reusable observation-state layer from domain-specific observers. The Python API accepts calibrated support flags and returns B/T/N/U plus unresolved-reason provenance. This makes the method directly runnable without pretending that source-system raw thresholds or the synthetic nuisance representation are universal.

Operationally, a new deployment should begin in shadow mode rather than with TNOA controlling the sensor. The primary record is preserved, raw evidence channels are logged separately, and pre-calibration windows remain unresolved. Independent truth is then collected without exposing algorithm outputs to annotators, channel-specific error criteria are calibrated on grouped development data, and the resulting calibration manifest is frozen before new days/scenes are scored. Adaptive actions become a later layer, enabled only after the observation semantics themselves have held up under held-out validation. This ordering prevents the capture policy from changing the evidence-generating process before the meaning of its observation states has been established.

A camera-trap application might define T as positive focal-species evidence, N as positive evidence for motion or visibility processes that mimic or mask detection, and O as adequate camera geometry and image support. A passive-acoustic application could define T as focal-call support, N as masking or overlapping non-target sound and O as sufficient microphone/temporal support. An interaction camera can additionally retain a local biological response as C until independent attribution supports a target link. The raw features and calibration rules change across systems, but the fail-closed sequence does not. Each application must validate its own evidence adapters and error criteria.

### 4.6 Limitations

Paper 1 remains a closed-world methods study. The synthetic generator was built to expose observation-process distinctions, not to reproduce all natural camera scenes. The downstream target-prevalence result uses the frozen synthetic emission matrix and a deterministic composition lattice; it is not an empirical estimator of visitation rate. The bounded weighting analysis explores a defined sensitivity class rather than an ecological prior distribution. The staged field-translation pathway is implementation guidance, not field validation.

The exact zero/positive `Pi3` split is structural. The six registered coordinates have uneven effective separation, and the historical C13 comparator rate is design-compositional. No independently validated target-absence channel is assumed. Finally, the prior-art review is targeted rather than systematic. Accordingly, we claim an integrated observation interface and experimentally documented consequences, not historical priority for abstention, imperfect detection, sensor fusion or uncertainty representation.

---

## 5. Conclusions

Automated ecological sensors should not be required to manufacture biological absence from unresolved observations. TNOA separates positive target support, positive nuisance support, measurement support and attribution before an observation is passed downstream. In the frozen synthetic study, the strongest evidence was not the size of the phase-space sweep or a single forced-binary miss rate. It was that an inherited raw threshold lost its operating meaning after a representation change, that a prespecified family-wise false-attribution criterion restored the declared control, and that binary coarsening discarded substantial information about a known downstream target-prevalence estimand. <!-- C6 C7 D1 -->

The broader methodological recommendation is therefore practical: calibrate observation decisions against explicit error criteria, preserve unresolved observation states and their reasons, and let downstream ecological models decide how those states should contribute to inference rather than destroying them at the sensor interface.

---

## Data and code availability

The repository contains the manuscript-facing provenance package, immutable result identifiers, post-freeze derived analyses, figure scripts, claim guards and a minimal reusable Python implementation. The reusable API and CSV CLI are documented in `docs/REUSABLE_IMPLEMENTATION.md` and demonstrated with `examples/minimal_evidence.csv`; the fail-closed sensor-to-field calibration sequence is documented in `docs/FIELD_TRANSLATION_PATHWAY.md`. Historical one-shot results remain tied to their original workflow runs and artifact hashes; later software checks do not replace the frozen scientific record.

## Author contributions

To be completed at submission.

## Acknowledgements

To be completed at submission.

## References

Bibliography source: `references.bib`.
