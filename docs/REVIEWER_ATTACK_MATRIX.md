# Reviewer attack matrix for TNOA Paper 1

This is the pre-submission attack surface for the MEE manuscript. It is not manuscript prose. The purpose is to agree with valid prior-art objections early, state the surviving claim narrowly, and point to the evidence that must remain visible.

## 1. “This is just selective classification / reject option.”

**Agree in part.** Abstention and risk–coverage trade-offs are established [@elyaniv2010selective; @hendrickx2024reject]. TNOA does not claim U as a new machine-learning primitive.

**Residual claim:** T/N/O/C/A− are heterogeneous ecological observation propositions rather than one classifier confidence; T and N may coexist, O is measurement support, and C requires attribution.

## 2. “Ecologists already know nondetection is not absence.”

**Agree.** Occupancy and observation models established this long ago [@mackenzie2002occupancy; @roylelink2006occupancy].

**Residual claim:** TNOA acts upstream, deciding what observation record may be emitted before occupancy/state-space inference.

## 3. “Multievent ecology already represents uncertain or equivocal observations.”

**Agree.** Multievent, multistate and partial-observation methods already retain uncertain observations [@pradel2005multievent; @mackenzie2009multistate; @hollanders2022stateuncertainty; @campbellgrant2023partial].

**Residual claim:** TNOA constructs the sensor-side event vocabulary from process evidence rather than claiming a new latent-state model. D3 asks whether its specific reason provenance carries additional downstream identifying information.

## 4. “Rhinehart already avoids binary thresholding.”

**Agree.** Continuous-score occupancy already uses uncertain classifier scores directly [@rhinehart2022continuous], and AI-to-inference workflows already propagate automated model outputs downstream [@cowans2026aiworkflow; @kitzes2026aiworkflow].

**Residual claim:** TNOA preserves heterogeneous propositions, not one target-confidence score. The progressive vocabulary ablation directly tests the information value of target/nuisance structure and U reason provenance.

## 5. “Classification-error models already propagate AI errors.”

**Agree.** Classification confusion and systematic bias can be modelled or audited downstream [@spence2025classification; @santoro2025bias].

**Residual claim:** nuisance, observability and attribution are not necessarily class mistakes. TNOA tries to preserve those distinctions before a confusion-matrix correction would be applied.

## 6. “T+N coexistence is just multilabel prediction.”

**Agree that simultaneous labels are not new.** Multilabel partial abstention already permits coexistence and selective refusal [@nguyen2020partialabstention].

**Residual claim:** T/N/O/C/A− have different semantics and evidence requirements. T+N is physical process coexistence, O is measurement support, C requires attribution and A− requires independent evidence.

## 7. “U is just uncertainty quantification / belief functions.”

**Agree that explicit ignorance/conflict is established** [@denoeux2019belief; @gao2026evidential].

**Residual claim:** TNOA U has process-semantic reason provenance. D3 shows, in the frozen experiment, that separating no-support U from overlap/attribution U substantially narrows compatible ecological estimands.

## 8. “Blackwell makes your never-wider result trivial.”

**Agree.** A deterministic coarsening is a garbling and cannot be more informative [@blackwell1953comparison].

**Required manuscript response:** never-wider is structural, not performance. The empirical result is the **magnitude and conditions** of information loss: target-prevalence median width `0.02992` versus `0.26563` for generic B/T/N/U versus binary, `0.00408` when U reason is retained, plus the D4 prevalence/weight sensitivity.

## 9. “Identification width is just partial identification.”

**Agree.** Identified-set reasoning is established [@manski2005partial].

**Residual claim:** TNOA uses that established language to evaluate a specific frozen ecological observation contract and its progressive garblings. It does not claim to invent bounds or identification width.

## 10. “Your family-wise error-control claim is statistically overstated.”

**Agree with the terminology objection.** The historical source protocol is named `familywise`, but the manuscript's inferential object is a **predeclared family-conditional false-attribution criterion**. Two negative families were calibrated separately and the maximum calibration boundary was used as one threshold.

**Current evidence:** held-out false nuisance attribution was `0/43,200` and `1,920/43,200 = 0.04444`. The earlier pooled calibration produced `0.08889` in the target-coupled negative family and failed the declared `alpha=0.05` criterion.

**Forbidden response:** do not claim classical FWER or a distribution-free finite-sample guarantee. Formal risk-control methods provide stronger guarantees under their assumptions [@bates2021riskcontrol].

## 11. “The nuisance result is still just threshold tuning.”

**Required response:** representation changed, ranking survived, inherited `0.55` lost its operating meaning, pooled calibration failed, and the predeclared family-conditional calibration passed held-out. No positive held-out world was searched to choose the final threshold.

**Transferable object:** the declared decision error semantics, not the raw threshold value.

## 12. “D3 is post hoc.”

**Agree.** D3 was motivated by the final prior-art audit after the frozen science and original D1 analysis. It is **post-freeze and not preregistered**.

**Why it remains useful:** it reruns no generator, retunes no observer and changes no threshold; it reports four nested vocabularies, all five fixed estimands and all 34 registered-axis slices. It is a transparent deterministic ablation, not confirmatory preregistered evidence.

## 13. “You cherry-picked target prevalence for D3.”

**Required response:** all five estimands are reported in `derived/observation_vocabulary_ablation.json`: target prevalence, nuisance prevalence, T+N co-occurrence, coupled-response prevalence and any-deviation prevalence.

Reason-resolved U was never wider than generic U in all 34 registered slices for all five estimands; strict median improvement occurred in 27/34 target slices and 29/34 slices for each other estimand.

## 14. “Why does reason-resolved U help? Aren’t you just adding categories?”

**Required response:** the non-worsening direction is structural for any deterministic refinement. The empirical question is magnitude and semantic usefulness. In the frozen design, target-prevalence median width fell `0.02992 -> 0.00408` and T+N co-occurrence `0.10494 -> 0.01484` when U reasons were retained.

**Boundary:** this does not prove that arbitrary extra categories help. The added fields must have defensible measurement semantics.

## 15. “The U rates and estimand results depend on arbitrary weighting.”

**Agree.** Pooled rates and uniform simplex summaries are design-space summaries, not ecological prevalences.

**Phase-space result:** overlap/attribution remains a majority of U through the tested row-level density-ratio class to `kappa=10`; the exact Pi1 total-U shape and small Pi2 centre contrast are not robust enough for universal claims.

**Composition result:** D4 directly reweights the 3,003 simplex compositions. At `kappa=10`, the worst-case weighted-mean fraction of binary width removed by B/T/N/U remains at least `57.5%`, and the additional reason-resolved-U gain remains at least `40.0%` of generic-U width.

**Boundary:** neither bounded class is an ecological prior or arbitrary-distribution robustness guarantee.

## 16. “The strong Pi3 boundary is built in.”

**Agree.** Five numeric Pi3 levels collapse to two marginal decision vectors: zero versus positive. Treat this as structural channel availability, not a field SNR law.

## 17. “Your 35.69% miss rate and zero FP are built into the design.”

**Agree and demote.** `0.3569 = 0.2*1 + 0.8*0.196125`; zero FP likewise follows the frozen target observer on registered non-target regimes. C13 is a design diagnostic, not performance evidence.

## 18. “The six-dimensional phase space overstates effective dimensionality.”

**Agree that registered coordinates are not six equally effective dimensions.** Maximum marginal TV shifts are about Pi3 `0.6431`, Pi1 `0.2665`, Pi2 `0.2402`, Pi6 `0.1608`, Pi4 `0.0728`, Pi5 `0.0214`.

## 19. “The method is flower-visitor specific.”

**Required response:** quantitative validation is flower-visitor-like and closed-world; generality is architectural only. Camera, acoustic and interaction-monitoring mappings require fresh evidence adapters and calibration. No numerical threshold transfers.

## 20. “The method is only a workflow connecting existing ideas.”

**Required response:** do not rely on repository plumbing or a conjunction-of-components priority claim. Lead with tested consequences:

- C6/C7 representation-change threshold failure and corrected family-conditional decision semantics;
- D1/D3/D4 empirical information-loss magnitude and its prevalence/weight conditions;
- preregistered Pi2 negative result.

## 21. “Where is the method readers can actually run?”

The repository provides a minimal Python API/CLI that consumes already-calibrated support flags. It deliberately ships no universal raw thresholds.

## 22. “The API starts after calibration. How do ecologists reach those flags?”

Use the fail-closed field translation pathway: preserve the primary record; log raw T/N/O/C diagnostics; remain `U / field_calibration_pending`; establish independent truth; calibrate on grouped development data; freeze; evaluate held-out; only then enable adaptive action. This is implementation guidance, not Paper-1 field validation.

## 23. “Your global simplex median barely represents rare target events.”

**Agree.** The 0.1-step simplex is strongly non-uniform in target prevalence: only `141/3003 = 4.70%` of compositions have known target prevalence `<=0.2`.

**D4 result:** in that rare-target subset, median target-prevalence width is `0.07410` for binary target/not-target, `0.07386` for target/nuisance/other, `0.000175` for B/T/N/U and `0.0` to numerical tolerance for reason-resolved U. The advantage therefore does not disappear in the rare-target portion of this frozen design.

**Boundary:** this does not estimate how rare field visits actually are and does not make the simplex an ecological prior.

## 24. “A richer vocabulary costs more to annotate and calibrate. Is it still better at fixed budget?”

**Agree that Paper 1 does not answer this.** D1/D3/D4 condition on a frozen, effectively known emission map. That is appropriate for isolating information loss caused by coarsening, but it does not compare information per annotation or per unit calibration cost.

**Required limitation:** with finite calibration data, uncertainty in a richer emission map could offset part of the identification gain under a fixed validation budget.

**Why no new simulation is added here:** a fair fixed-budget comparison would require new choices about annotation allocation, grouped dependence, rare-state sampling, smoothing/regularization and propagation of emission-matrix uncertainty. That is a distinct measurement-design study, not a harmless sensitivity extension of the frozen observer experiment.

## Submission gate implied by this matrix

The central scientific attack surface is explicit. The paper should survive valid prior-art and design-dependence objections by **surrendering primitive-level priority**, keeping C6/C7 as the first primary result, and defending the measured D1/D3/D4 information consequence with explicit prevalence and weighting boundaries.

Any later textual change must rerun claim, reference, DOCX and reviewer-bundle validation.
