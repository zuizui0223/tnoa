# Literature evidence map for TNOA Paper 1

Status: **expanded targeted evidence map complete; not a systematic review**. The adversarial synthesis is in `FINAL_PRIOR_ART_AUDIT.md`; the compact comparison is in `NEAREST_NEIGHBOUR_METHODS.md`.

The purpose is to identify neighbouring method families that constrain TNOA's novelty claim and to state what remains after those overlaps are conceded.

## 1. Ecological uncertain-event and multievent models

Multievent capture–recapture accommodates uncertain state assignment [@pradel2005multievent]. Multistate occupancy allows imperfect state detection [@mackenzie2009multistate]. Later ecological models retain uncertain, equivocal or partial observations [@hollanders2022stateuncertainty; @campbellgrant2023partial].

**Shared ground:** uncertain ecological observations need not be forced to fully observed states.

**TNOA difference:** it acts one stage earlier and specifies what process-semantic record the sensor may emit.

**Claim surrendered:** TNOA is not the first ecological method to retain uncertainty or ambiguous observations.

## 2. Continuous-score and AI-assisted ecological inference

Continuous-score occupancy can use classifier-score distributions without thresholding them to detections [@rhinehart2022continuous]. AI-to-inference workflows connect automated confidence/error to ecological analysis [@cowans2026aiworkflow; @kitzes2026aiworkflow]. Classification-error models show that classifier confusion/bias alters ecological inference [@spence2025classification; @santoro2025bias].

**Shared ground:** binary thresholding is not required and automated-classifier error can propagate downstream.

**TNOA difference:** TNOA retains heterogeneous propositions—positive T, positive N, separate O, attribution-gated C and optional independently supported A−—rather than one target-confidence stream.

**Claim surrendered:** TNOA is not the first non-binary or continuous-score ecological use of machine-learning output.

## 3. Imperfect detection and process/observation models

Occupancy and hierarchical/state-space models already separate ecological state from observation [@mackenzie2002occupancy; @roylelink2006occupancy; @royle2008hierarchical; @augermethe2021statespace]. Camera-trap work decomposes encounter, trigger, registration and image-quality processes [@hofmeester2019framing; @findlay2020detection].

**TNOA difference:** its object is the upstream observation contract handed to these models.

**Claim surrendered:** nondetection-is-not-absence and process/observation separation are established ecology.

## 4. Selective, reject and partial-abstention methods

Selective classification/reject options formalize refusal [@elyaniv2010selective; @hendrickx2024reject]. Multilabel partial abstention permits coexistence and selective refusal [@nguyen2020partialabstention]. Formal risk-control methods can offer stronger guarantees under stated assumptions [@bates2021riskcontrol].

**TNOA difference:** T/N/O/C/A− are not exchangeable class labels; they make different process/measurement propositions.

**Claim surrendered:** abstention, coexistence and partial refusal are not new.

## 5. Open-set and evidential uncertainty

Open-set recognition handles unknown classes [@geng2021openset]. Belief/evidential approaches represent ignorance and conflict [@denoeux2019belief; @gao2026evidential].

**TNOA difference:** U may arise among known processes because available evidence does not license one observation statement.

**Claim surrendered:** explicit ignorance/conflict is prior art.

## 6. Calibration and formal risk control

Calibration depends on representation [@guo2017calibration] and can degrade under dataset shift [@ovadia2019shift]. Risk-controlling prediction sets provide stronger formal guarantees under their assumptions [@bates2021riskcontrol].

**TNOA contribution:** the frozen nuisance history documents a representation change where ranking survived but an inherited raw threshold lost its operating meaning; a **predeclared family-conditional false-attribution criterion** was then recalibrated and checked held-out.

**Boundary:** the `0/43,200` and `1,920/43,200` held-out rates are closed-world empirical checks, not classical FWER or distribution-free finite-sample guarantees.

## 7. Information ordering and partial identification

Blackwell comparison formalizes garbling [@blackwell1953comparison]. Partial-identification theory formalizes compatible identified sets [@manski2005partial].

**Shared ground:** deterministic coarsening cannot be more informative, and identification width is established statistical language.

**TNOA contribution:** D1 quantifies the magnitude of ecological target-prevalence information lost when the frozen core B/T/N/U record is coarsened to target/not-target. D4 maps how that magnitude behaves across target prevalence and bounded composition reweighting.

For the primary comparison, median target-prevalence width is approximately `0.0299` with B/T/N/U versus `0.2656` after binary coarsening. This is the core downstream information result.

## 8. D3 and D5: refinement is informative, semantic specificity is not demonstrated

D3, motivated after the prior-art audit, split the frozen generic U column into two observed reason buckets and found large additional numerical narrowing (`0.02992 -> 0.00408` for target prevalence).

D5 was added as the required control. A constant 50:50 split of U gives no gain, but 500 arbitrary regime-dependent two-way splits have median target-prevalence width `0.0050075`; `48.0%` are equal to or narrower than the frozen two-reason split. Across all five estimands, random equal-or-better fractions range from `0.480` to `0.672`. Random three-way splits generically make the six-regime constraint system full rank.

Therefore D3 shows the value of adding **non-redundant observation structure**, not an isolated information premium caused by the meanings of the two frozen reason labels. Exact width at a fixed rank still depends on column orientation, so state count/rank does not alone determine every effect size.

The frozen D3/D5 surface also has only two U reason buckets, whereas the later reusable API exposes four U reasons. The frozen analysis does not validate a one-to-one four-reason API decomposition.

## 9. Adaptive ecological sampling

Adaptive and preferential sampling already treat data-dependent effort as an inferential-design problem [@henrys2024adaptive; @pescott2025adaptive]. TNOA Paper 1 is upstream of adaptive control; field translation begins in shadow mode and requires fresh calibration.

## 10. Residual novelty after the expanded audit and D5 control

The defensible contribution is a tested **upstream process-semantic ecological observation contract** that:

1. keeps positive target and nuisance support non-complementary;
2. permits T+N coexistence;
3. separates measurement support O;
4. requires attribution before C is promoted to target evidence;
5. requires independent evidence for certified absence;
6. calibrates operational support decisions to declared family-conditional error semantics rather than inherited raw thresholds;
7. quantifies under frozen known truth how much downstream ecological identification is lost when the **core B/T/N/U record** is garbled to binary;
8. reports finer reason refinements only with the explicit D5 qualification that their semantic-specific information value is not isolated.

## 11. MEE positioning

> TNOA contributes a tested upstream ecological observation contract, a frozen operational calibration failure/recovery, and a known-truth experiment quantifying the ecological information destroyed by binary coarsening of core observation-process states.

D3/D5 is a self-critical supporting diagnostic, not a reason-semantics novelty claim. Quantitative transfer beyond the frozen generator remains unclaimed; field validation is external to Paper 1.
