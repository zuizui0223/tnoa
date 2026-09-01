# Reviewer attack matrix for TNOA Paper 1

This is the pre-submission attack surface for the MEE manuscript. It is not manuscript prose. The purpose is to agree with valid objections early, state the surviving claim narrowly, and point to the evidence that must remain visible.

## 1. “This is just selective classification / reject option.”

**Agree in part.** Abstention and risk–coverage trade-offs are established [@elyaniv2010selective; @hendrickx2024reject]. TNOA does not claim U as a new machine-learning primitive.

**Residual claim:** T/N/O/C/A− are heterogeneous ecological observation propositions rather than one classifier confidence; T and N may coexist, O is measurement support, and C requires attribution.

## 2. “Ecologists already know nondetection is not absence.”

**Agree.** Occupancy and observation models established this long ago [@mackenzie2002occupancy; @roylelink2006occupancy].

**Residual claim:** TNOA acts upstream, deciding what observation record may be emitted before occupancy/state-space inference.

## 3. “Multievent ecology already represents uncertain or equivocal observations.”

**Agree.** Multievent, multistate and partial-observation methods already retain uncertain observations [@pradel2005multievent; @mackenzie2009multistate; @hollanders2022stateuncertainty; @campbellgrant2023partial].

**Residual claim:** TNOA constructs the sensor-side event vocabulary from process evidence rather than claiming a new latent-state model.

## 4. “Rhinehart already avoids binary thresholding.”

**Agree.** Continuous-score occupancy already uses uncertain classifier scores directly [@rhinehart2022continuous], and AI-to-inference workflows already propagate automated model outputs downstream [@cowans2026aiworkflow; @kitzes2026aiworkflow].

**Residual claim:** TNOA preserves heterogeneous process propositions rather than one target-confidence score. D1 tests the information cost of collapsing the core B/T/N/U record to target/not-target.

## 5. “Classification-error models already propagate AI errors.”

**Agree.** Classification confusion and systematic bias can be modelled or audited downstream [@spence2025classification; @santoro2025bias].

**Residual claim:** nuisance, observability and attribution are not necessarily class mistakes. TNOA tries to preserve those distinctions before a confusion-matrix correction would be applied.

## 6. “T+N coexistence is just multilabel prediction.”

**Agree that simultaneous labels are not new.** Multilabel partial abstention already permits coexistence and selective refusal [@nguyen2020partialabstention].

**Residual claim:** T/N/O/C/A− have different semantics and evidence requirements. T+N is physical process coexistence, O is measurement support, C requires attribution and A− requires independent evidence.

## 7. “U is just uncertainty quantification / belief functions.”

**Agree that explicit ignorance/conflict is established** [@denoeux2019belief; @gao2026evidential].

**Residual claim:** TNOA uses U as a fail-closed observation state whose reason provenance can guide measurement design. D5 means the paper must not use D3's identification-width reduction as proof that the selected reason meanings themselves carry a unique information premium.

## 8. “Blackwell makes your never-wider result trivial.”

**Agree.** A deterministic coarsening is a garbling and cannot be more informative [@blackwell1953comparison].

**Required manuscript response:** never-wider is structural, not performance. The empirical D1 result is the **magnitude and conditions** of information loss: target-prevalence median width `0.02992` with B/T/N/U versus `0.26563` after binary collapse, plus the D4 prevalence/weight sensitivity.

## 9. “Identification width is just partial identification.”

**Agree.** Identified-set reasoning is established [@manski2005partial].

**Residual claim:** TNOA uses that established language to evaluate a specific frozen ecological observation contract and its garbling. It does not claim to invent bounds or identification width.

## 10. “Your family-wise error-control claim is statistically overstated.”

**Agree with the terminology objection.** The historical source protocol is named `familywise`, but the manuscript's inferential object is a **predeclared family-conditional false-attribution criterion**. Two negative families were calibrated separately and the maximum calibration boundary was used as one threshold.

**Current evidence:** held-out false nuisance attribution was `0/43,200` and `1,920/43,200 = 0.04444`. The earlier pooled calibration produced `0.08889` in the target-coupled negative family and failed the declared `alpha=0.05` criterion.

**Forbidden response:** do not claim classical FWER or a distribution-free finite-sample guarantee. Formal risk-control methods provide stronger guarantees under their assumptions [@bates2021riskcontrol].

## 11. “The nuisance result is still just threshold tuning.”

**Required response:** representation changed, ranking survived, inherited `0.55` lost its operating meaning, pooled calibration failed, and the predeclared family-conditional calibration passed held-out. No positive held-out world was searched to choose the final threshold.

**Transferable object:** the declared decision error semantics, not the raw threshold value.

## 12. “D3 is post hoc.”

**Agree.** D3 was motivated by the final prior-art audit after the frozen science and original D1 analysis. It is **post-freeze and not preregistered**.

**Why it remains useful:** it reruns no generator, retunes no observer and changes no threshold; it records what happens as the frozen observation matrix gains an additional non-redundant column across all five estimands and 34 axis slices. It is now a refinement/identifiability diagnostic, not evidence that the chosen reason semantics are uniquely informative.

## 13. “You cherry-picked target prevalence for D3.”

**Required response:** all five estimands are reported in `derived/observation_vocabulary_ablation.json`, and D5 repeats the random-split specificity control across all five.

**D5 result:** the fraction of 500 random two-way U splits that were equal to or narrower than the frozen semantic split was `0.480` for target prevalence, `0.488` for nuisance prevalence, `0.488` for T+N co-occurrence, `0.672` for coupled-response prevalence and `0.480` for any-deviation prevalence.

## 14. “Why does reason-resolved U help? Aren’t you just adding categories?”

**Agree with the structural objection.** D5 was added specifically to test it.

- Generic B/T/N/U target-prevalence median width: `0.0299207`.
- Constant 50:50 U split: `0.0299207` — no gain because the added column is redundant.
- 500 unlabeled regime-dependent two-way U splits: median `0.0050075`.
- Frozen two-reason split: `0.0040780`.
- **48.0%** of random two-way splits were equal to or narrower than the frozen semantic split.
- 500 random three-way splits were full rank and point-identified all five estimands to numerical tolerance.

**Required interpretation:** the frozen two-way split is informative, but the size of its gain is not shown to be specific to the reason semantics. Additional non-collinear columns reduce latent-mixture degrees of freedom. State count alone does not determine the exact width, because column orientation relative to the estimand also matters.

**Forbidden response:** do not say D3 demonstrates that `no-support` versus `overlap/attribution` semantics themselves explain the `86.37%` reduction.

## 15. “The U rates and estimand results depend on arbitrary weighting.”

**Agree.** Pooled rates and uniform simplex summaries are design-space summaries, not ecological prevalences.

**Phase-space result:** overlap/attribution remains a majority of U through the tested row-level density-ratio class to `kappa=10`; the exact Pi1 total-U shape and small Pi2 centre contrast are not robust enough for universal claims.

**Composition result:** D4 directly reweights the 3,003 simplex compositions. At `kappa=10`, the worst-case weighted-mean fraction of binary width removed by B/T/N/U remains at least `57.5%`.

**Boundary:** D4's additional finer-split gain must be read with D5; it is not evidence for semantic-specific reason value. Neither bounded class is an ecological prior or arbitrary-distribution robustness guarantee.

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
- D1/D4 core B/T/N/U-versus-binary information-loss magnitude and its prevalence/weight conditions;
- preregistered Pi2 negative result;
- D3/D5 only as a self-critical supporting control showing that finer refinements can narrow identification without demonstrating semantic-specific reason value.

## 21. “Where is the method readers can actually run?”

The repository provides a minimal Python API/CLI that consumes already-calibrated support flags. It deliberately ships no universal raw thresholds.

## 22. “The API starts after calibration. How do ecologists reach those flags?”

Use the fail-closed field translation pathway: preserve the primary record; log raw T/N/O/C diagnostics; remain `U / field_calibration_pending`; establish independent truth; calibrate on grouped development data; freeze; evaluate held-out; only then enable adaptive action. This is implementation guidance, not Paper-1 field validation.

## 23. “Your global simplex median barely represents rare target events.”

**Agree.** The 0.1-step simplex is strongly non-uniform in target prevalence: only `141/3003 = 4.70%` of compositions have known target prevalence `<=0.2`.

**D4 result:** in that rare-target subset, median target-prevalence width is `0.07410` after binary collapse versus `0.000175` with B/T/N/U. The core D1 advantage therefore does not disappear in the rare-target portion of this frozen design.

**Boundary:** this does not estimate how rare field visits actually are and does not make the simplex an ecological prior.

## 24. “A richer vocabulary costs more to annotate and calibrate. Is it still better at fixed budget?”

**Agree that Paper 1 does not answer this.** D1/D3/D4/D5 condition on a frozen, effectively known emission map. That is appropriate for isolating information loss caused by coarsening, but it does not compare information per annotation or per unit calibration cost.

**Required limitation:** with finite calibration data, uncertainty in a richer emission map could offset part of the identification gain under a fixed validation budget.

**Why no new simulation is added here:** a fair fixed-budget comparison would require new choices about annotation allocation, grouped dependence, rare-state sampling, smoothing/regularization and propagation of emission-matrix uncertainty. That is a distinct measurement-design study, not a harmless sensitivity extension of the frozen observer experiment.

## 25. “The frozen paper has two U reasons, but your reusable API has four. Are those four empirically validated by D3?”

**No.** The frozen V14b surface stores only `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`. The latter can arise from simultaneous frozen T+N support or unresolved indirect-only attribution. The current API later separates `target_nuisance_overlap`, `missing_attribution`, `insufficient_observability` and `no_supported_evidence`.

**Required boundary:** there is no one-to-one empirical four-way mapping validated by the frozen D3 surface. `insufficient_observability` has no separate D3 column, and overlap versus attribution cannot be separated from the frozen aggregate rate.

**Residual architectural claim:** the four current reasons encode distinct decision/measurement situations in the reusable contract, but each reason's measurement semantics must be validated in the deployment where it is used.

## Submission gate implied by this matrix

The central scientific attack surface is explicit. The paper should survive valid prior-art and design-dependence objections by **surrendering primitive-level priority**, keeping C6/C7 and D1/D4 as the primary evidence, and presenting D3/D5 as an explicit correction showing that finer observation columns can improve identifiability without proving a semantic-specific reason premium.

Any later textual change must rerun claim, reference, DOCX and reviewer-bundle validation.
