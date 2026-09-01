# MEE editorial pitch — TNOA

This is editorial preparation, not manuscript evidence. The intended positioning is a tested ecological method rather than a workflow or a priority claim for abstention.

## One-sentence pitch

TNOA is a tested upstream observation contract for automated ecological sensing that preserves core process-semantic observation distinctions before downstream inference and quantifies the information lost when B/T/N/U is collapsed to target/not-target.

## Why this is a methods paper rather than a workflow

The contribution is not the sequence of software components and not historical priority for uncertain observations, continuous classifier scores, multilabel prediction, abstention, Blackwell ordering or partial identification. The tested objects are:

1. a process-semantic sensor-to-inference record in which target and nuisance are positive non-complements and observability/attribution remain separate;
2. C6/C7, an observed representation-change failure showing that a raw threshold need not preserve its operating meaning, followed by predeclared family-conditional calibration;
3. D1/D4, known-truth downstream experiments measuring the magnitude and prevalence/weight conditions of information loss when core B/T/N/U is garbled to binary;
4. transparent falsification and post-freeze controls, including D5, which retract an initially attractive semantic interpretation when an unlabeled rank control explains the effect.

## Nearest prior art and what we do not claim

Continuous-score occupancy already avoids binary thresholding [@rhinehart2022continuous]. Multievent and partial-observation models already preserve uncertain events [@pradel2005multievent; @campbellgrant2023partial]. Multilabel partial abstention already permits coexistence/refusal [@nguyen2020partialabstention]. Blackwell comparison and partial-identification theory already supply the information-ordering language [@blackwell1953comparison; @manski2005partial].

The residual contribution is the tested **upstream process-semantic observation contract**, the observed calibration failure/recovery, and the measured ecological information cost of collapsing the core record before downstream modelling.

## Main evidence for an editor

- A changed nuisance representation retained ranking while an inherited raw threshold lost its registered operating meaning.
- A predeclared family-conditional false-attribution criterion subsequently produced held-out rates `0/43,200` and `1,920/43,200 = 0.04444` in the two negative families. These are closed-world empirical checks, not distribution-free guarantees.
- **Across 3,003 known-truth latent-regime compositions**, median compatible target-prevalence width was about `0.0299` with B/T/N/U versus `0.2656` after binary coarsening. The non-worsening direction is structural; the empirical evidence is the magnitude.
- Only `141/3003 = 4.70%` of the simplex compositions had target prevalence `<=0.2`, yet median width in that subset remained `0.000175` with B/T/N/U versus `0.07410` after binary collapse. Under `kappa=10` adversarial composition weighting, B/T/N/U still removed at least `57.5%` of weighted-mean binary width.
- A post-freeze D3 refinement narrowed target-prevalence width from `0.02992` to `0.00408`, but a reviewer-motivated D5 control showed this was **not a semantic-specific reason effect**: among 500 unlabeled regime-dependent two-way U splits, the median width was `0.0050075` and `48%` matched or exceeded the frozen two-reason split. All 500 random three-way splits were full rank and point-identified all five estimands. D3/D5 are supporting self-controls, not primary evidence for reason semantics.
- A preregistered matched-timescale ambiguity-ridge prediction failed and remains a negative result.
- The repository includes a runnable minimal API/CLI and fail-closed field-translation template.

## Breadth beyond the motivating sensing system

The architecture is process-level rather than taxon-specific. Wildlife cameras, passive acoustics and interaction sensors can instantiate different T/N/O/C evidence adapters, but each system must validate its own measurement semantics and error criteria. Numerical thresholds and the synthetic emission matrix do not transfer.

The current reusable API exposes four U reasons, while the frozen D3/D5 surface contains only two aggregated U buckets. The paper explicitly does **not** claim a one-to-one four-reason empirical validation from the frozen experiment.

## Scope boundary to state proactively

The quantitative evidence is **closed-world**. The manuscript does not claim field accuracy, field prevalence, biological-absence certification, universal score thresholds, distribution-free risk control, arbitrary ecological-weight robustness or quantitative cross-system transfer.

D3–D5 are post-freeze/not-preregistered. D5 specifically prevents the paper from treating finer reason categories as intrinsically or semantically informative merely because they increase observation rank. All information comparisons also condition on a frozen effectively known emission map, so no information-per-annotation, cost or field-hour advantage is claimed.

## Optional covering-letter draft

Dear Editors,

Please consider our manuscript, “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework,” as a Standard Article for Methods in Ecology and Evolution.

Automated sensors create the observation records subsequently analysed by occupancy, interaction and state-space models. Existing methods already represent uncertain events and can propagate continuous classifier scores downstream. We address a distinct upstream problem: what observation record should a sensor preserve before those models are fitted?

The manuscript centres on two tested consequences. First, after a nuisance-score representation changed, ranking remained useful but the inherited raw threshold lost its registered operating meaning; a predeclared family-conditional false-attribution calibration then satisfied the held-out criterion in both negative families. Second, across 3,003 known-truth latent-regime compositions, median compatible target-prevalence width was about 0.0299 with B/T/N/U retained versus 0.2656 after binary coarsening. The gain remained large in the underrepresented rare-target subset and under ten-fold bounded composition reweighting.

We also report a deliberately adverse post-freeze control. A finer two-way split of U initially appeared to provide a large additional information gain, but 48% of 500 unlabeled regime-dependent random splits matched or exceeded that frozen semantic split. We therefore demote that result and state explicitly that the experiment supports additional non-redundant observation structure, not a semantic-specific information premium for the chosen reason labels. The frozen experiment also has two U-reason buckets whereas the reusable API exposes four, and no one-to-one empirical validation is claimed.

We believe this self-critical structure fits MEE: the methodological gap is taxon-independent, the central evidence is simulation/known-truth method evaluation rather than a case study, nearby prior art is explicitly acknowledged, and runnable code plus an anonymized reviewer package are provided. Quantitative claims remain closed-world; field accuracy, numerical threshold transfer, distribution-free risk guarantees and annotation-budget efficiency are not asserted.

Thank you for considering the manuscript.

Sincerely,

[Corresponding author]

## Short pre-submission-enquiry version

We are preparing a Standard Article entitled “Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework.” TNOA addresses the upstream sensor-interface problem of which observation-process distinctions should be preserved before downstream ecological inference. Frozen known-truth benchmarking documents a score-threshold portability failure and a large information cost of binary coarsening (median target-prevalence compatible width 0.0299 with B/T/N/U versus 0.2656 after target/not-target collapse), with the advantage persisting in rare-target and bounded composition-weight stress tests. A post-freeze random-split control further shows that an apparent extra gain from splitting U is not semantic-specific, so the paper explicitly demotes that interpretation rather than claiming that additional reason labels are intrinsically informative. A minimal Python implementation and fail-closed cross-sensor translation pathway are included. The evidence is closed-world and does not claim field accuracy or threshold transfer.
