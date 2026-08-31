# Literature evidence map for TNOA Paper 1

Status: **expanded targeted evidence map complete; not a systematic review**. The adversarial synthesis is in `FINAL_PRIOR_ART_AUDIT.md`; the compact comparison is in `NEAREST_NEIGHBOUR_METHODS.md`.

The purpose is to identify the method families most likely to collapse a TNOA novelty claim and state precisely what remains after those overlaps are conceded.

## 1. Ecological uncertain-event and multievent models

Multievent capture–recapture explicitly handles uncertain state assignment [@pradel2005multievent]. Multistate occupancy models allow multiple states and imperfect state detection [@mackenzie2009multistate]. Later ecological models explicitly retain state uncertainty, ambiguous/equivocal events or partial observations [@hollanders2022stateuncertainty; @campbellgrant2023partial].

**Shared ground:** uncertain ecological observations need not be forced to a fully observed latent state.

**TNOA difference:** these methods model latent ecological states from an observation/event record. TNOA operates one stage earlier and specifies what process-semantic event record the sensor is entitled to emit.

**Claim surrendered:** TNOA is not the first ecological method to retain uncertainty, ambiguity or partial observations.

## 2. Continuous-score and AI-assisted ecological inference

Continuous-score occupancy uses classifier score distributions directly rather than thresholding them to detections [@rhinehart2022continuous]. Broader AI-to-inference workflows describe how automated classifier confidence should connect to ecological models [@cowans2026aiworkflow; @kitzes2026aiworkflow]. Classification-error models and camera-trap audits show that classifier confusion or systematic bias can alter ecological estimates [@spence2025classification; @santoro2025bias].

**Shared ground:** binary thresholding is not required and classifier error can propagate downstream.

**TNOA difference:** TNOA does not retain one target-confidence score. It retains heterogeneous propositions: positive T, positive N, separate O, attribution-gated C and optional independently supported A−, plus unresolved-reason provenance.

**Claim surrendered:** TNOA is not the first non-binary or continuous-score ecological use of machine-learning output.

## 3. Imperfect detection and process/observation models

Occupancy and hierarchical/state-space models already separate ecological state from observation [@mackenzie2002occupancy; @roylelink2006occupancy; @royle2008hierarchical; @augermethe2021statespace]. Camera-trap work decomposes encounter, triggering, registration and image-quality processes [@hofmeester2019framing; @findlay2020detection].

**TNOA difference:** its object is the upstream observation contract handed to these downstream models, not a replacement latent-state model.

**Claim surrendered:** nondetection-is-not-absence and process/observation separation are established ecology.

## 4. Selective, reject and partial-abstention methods

Selective classification and reject options formalize refusal [@elyaniv2010selective; @geifman2017selective; @geifman2019selectivenet; @hendrickx2024reject]. Partial/set-valued and multilabel abstention allow non-singleton decisions and selective refusal [@karlsson2024partialreject; @nguyen2020partialabstention]. Conformal reject methods add formal guarantees under their assumptions [@garciagalindo2024conformalreject; @szabadvary2025reject].

**TNOA difference:** T/N/O/C/A− are not exchangeable labels. They make different propositions and can require different evidence. T+N is physical coexistence, O is measurement support, and C requires attribution.

**Claim surrendered:** abstention, coexistence of labels and partial refusal are not new.

## 5. Open-set and evidential uncertainty

Open-set recognition handles unknown classes [@geng2021openset]. Belief-function and evidential approaches represent ignorance, conflict and non-singleton belief [@denoeux2019belief; @gao2026evidential].

**TNOA difference:** U need not be an unknown class or a scalar uncertainty state. It can arise from known processes whose evidence does not license one ecological statement; reason provenance is retained.

**Claim surrendered:** explicit ignorance/conflict is prior art.

## 6. Calibration and formal risk control

Confidence calibration changes with model representation [@guo2017calibration], and uncertainty can degrade under dataset shift [@ovadia2019shift]. Risk-controlling prediction sets provide stronger formal guarantees under specified assumptions [@bates2021riskcontrol].

**TNOA difference:** the frozen development history documents an ecological nuisance representation change where ranking survived but the inherited raw threshold lost its operating meaning. The repair transfers a declared **family-conditional decision error** rather than the raw score value.

**Boundary:** the current `0/43,200` and `1,920/43,200` held-out rates are closed-world empirical checks. They are not classical family-wise error-rate control and not distribution-free finite-sample guarantees.

## 7. Information ordering and partial identification

Blackwell comparison formalizes garbling of statistical experiments [@blackwell1953comparison]. Partial-identification theory formalizes compatible identified sets when data do not point-identify an estimand [@manski2005partial].

**Shared ground:** a deterministic coarsening cannot be more informative than the record from which it is derived, and identification width is established statistical language.

**TNOA difference:** the empirical contribution is the magnitude of information loss for a frozen ecological sensing experiment and the observation semantics responsible for retaining it.

The post-freeze D3 ablation makes this explicit across four nested records: target/not-target; target/nuisance/other; B/T/N/U; and reason-resolved B/T/N/U.

## 8. Adaptive ecological sampling

Adaptive and preferential sampling already treat data-dependent effort as an inferential-design problem [@henrys2024adaptive; @pescott2025adaptive].

TNOA Paper 1 is upstream of adaptive control. Its field translation requires shadow-mode calibration before reason-specific acquisition can change sampling effort.

## 9. Residual novelty after the expanded audit

The defensible contribution is not a conjunction-of-components priority claim. It is a tested **upstream process-semantic ecological observation contract** that:

1. separates positive target and nuisance process support;
2. preserves T+N coexistence;
3. keeps measurement support O semantically separate;
4. requires attribution before C is promoted to target evidence;
5. requires independent evidence for certified absence;
6. preserves unresolved-reason provenance;
7. calibrates process-support decisions to predeclared family-conditional error semantics rather than inherited raw thresholds;
8. quantifies under frozen known truth how much downstream ecological identification is lost when the record is progressively garbled.

## 10. D3 prior-art-motivated test

Because prior ecology already preserves uncertain observations and continuous classifier scores, the key residual empirical question is whether TNOA-specific **reason provenance** carries additional information.

The literature-audit-motivated D3 analysis is explicitly post-freeze and not preregistered. Median target-prevalence width across the four nested vocabularies was `0.2656`, `0.1886`, `0.02992`, `0.00408`; T+N co-occurrence width was `0.7231`, `0.5136`, `0.10494`, `0.01484`. Reason-resolved U was never wider than generic U in all 34 registered single-axis slices for all five fixed estimands and strictly reduced the slice median in most slices.

The nesting direction is structural. The numerical reduction is the post-freeze result.

## 11. MEE positioning

The intended MEE framing is therefore:

> TNOA contributes a tested upstream ecological observation contract and a frozen known-truth experiment quantifying the ecological information destroyed by coarsening that contract.

It is not framed as the first abstaining classifier, first uncertain ecological-event model, first continuous-score inference method, first multilabel method, first calibration method, or first use of partial identification.

Quantitative transfer beyond the frozen synthetic generator remains unclaimed; field validation is external to Paper 1.
