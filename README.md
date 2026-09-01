# TNOA

**Target–Nuisance–Observability–Abstention for ecological sensing**

TNOA is a methods-paper repository for a process-preserving observation framework that asks a narrower question than ordinary event classification:

> **What observation state should an ecological sensor preserve before downstream ecological inference?**

The repository isolates the transferable methodological contribution from the source sensing systems used during development. It is not itself a field-accuracy claim or a universal detector package.

## Core object

The minimal observed decision vocabulary is

\[
B + \{T, N, U\},
\]

where:

- **B — baseline:** no marked dynamic deviation requiring target/nuisance adjudication;
- **T — target-supported:** positive evidence for the focal biological process;
- **N — nuisance-supported:** positive evidence for an exogenous observation process that can mimic, mask or corrupt attribution;
- **U — unresolved / abstention:** the available evidence does not justify a unique target/nuisance statement.

T and N are **positive, non-complementary hypotheses**. They may be jointly supported. T+N superposition is therefore not automatically an error state.

The field-facing evidence architecture is richer than the final decision vocabulary:

\[
(T, C, N, O, A^-),
\]

with:

- **T:** direct positive target evidence;
- **C:** target-coupled local response that requires independent attribution before promotion to target evidence;
- **N:** positive evidence for an exogenous nuisance process;
- **O:** measurement-channel observability/support;
- **A−:** independently validated target-absence evidence, if such a channel exists.

Low T is not A−. Good O is not A−. N is not `1 - T`. O is not `1 - N`.

## Main methodological results

The MEE-focused manuscript now leads with C6/C7 and D1/D4 as the two primary evidence blocks, followed by the preregistered C2 negative result.

### 1. A raw threshold lost its operating meaning; the declared error criterion was recalibrated

After the nuisance representation changed, nuisance/non-nuisance ranking remained strong but the inherited raw threshold `0.55` no longer had the intended operating meaning: nuisance recall at that threshold was `0.23125`.

A pooled calibration then produced coupled-negative false nuisance attribution `0.08889`, exceeding the declared `alpha=0.05` family-conditional criterion. The max-over-predeclared-negative-families calibration subsequently produced held-out rates `0/43,200` and `1,920/43,200 = 0.04444`, both within the declared criterion.

These are **closed-world empirical family-conditional checks**, not classical family-wise error-rate control and not a distribution-free finite-sample guarantee. The transferable object in this experiment was the declared error semantics, not the numerical raw-score threshold.

### 2. Binary coarsening destroyed downstream ecological information

Using known latent truth and the frozen observation matrix across a deterministic 3,003-composition simplex:

- median compatible target-prevalence width was about `0.030` with B/T/N/U versus `0.266` after binary coarsening;
- median relative width reduction among non-zero binary widths was about `84.45%`;
- the four-state record was never wider than its binary coarsening, as required structurally by deterministic garbling;
- naive TARGET/not-TARGET estimates were negatively biased in 99.63% of compositions, with median bias about `-0.238`, retained only as a secondary diagnostic.

The D4 stress test showed that the main D1 result is not confined to balanced/high-target compositions. Only `141/3003 = 4.70%` of the simplex has target prevalence `<=0.2`, yet in that subset median compatible width was about `0.000175` with B/T/N/U versus `0.07410` after binary collapse. Under `kappa=10` adversarial reweighting of composition weights, B/T/N/U still removed at least `57.5%` of weighted-mean binary width.

This is a **synthetic target-prevalence information-preservation result**, not a field visit-rate estimate or an ecological prior.

### 3. A preregistered matched-timescale ridge was falsified

The expectation of a narrow ambiguity ridge near \(\Pi_2\approx1\) was not supported. The small final equal-weight contrast is also weighting-sensitive and can change sign within the tested bounded reweighting class. The failed prediction is retained rather than rescued post hoc.

## Supporting self-critical control: finer U splits are not shown to be semantically special

A post-freeze D3 refinement split the frozen generic U column into the two stored V14b U-reason buckets and reduced median target-prevalence width from `0.0299207` to `0.0040780`. A reviewer-motivated D5 control showed that this extra narrowing is **not semantic-specific**: across 500 unlabeled regime-dependent two-way U splits, the median width was `0.0050075`, and `48.0%` of arbitrary splits matched or exceeded the frozen two-reason split. A redundant constant 50:50 split produced no gain, while all 500 unlabeled three-way splits produced full-rank six-regime systems and point identification to numerical tolerance for all five tested estimands.

The safe interpretation is therefore that additional **non-redundant regime-discriminating observation structure** can narrow compatible sets. The present experiment does not demonstrate a special information premium caused by the meanings of the selected U reasons. D3/D5 are supporting controls, not primary evidence for reason semantics.

The frozen V14b surface contains only two aggregated U-reason buckets, whereas the later reusable API exposes four reasons. No one-to-one four-reason empirical validation is claimed.

## Secondary structural results

Under the frozen equal-grid design, unresolved observations were mostly overlap/attribution cases rather than no-supported-evidence cases. That qualitative dominance remained above one half through the tested density-ratio reweighting class to `kappa=10`.

The observation-duration result is deliberately narrower than an earlier non-monotonicity framing. From \(\Pi_1=1\) to \(\Pi_1=3.162\), no-supported-evidence U decreased while overlap/attribution U increased. This is interpreted as **reason substitution**—additional observation can reduce evidence shortage while leaving an attribution/coexistence problem—not as a universal law that longer monitoring increases uncertainty. The pooled total-U shape is not robust to moderate reweighting.

The six registered coordinates also have strongly uneven marginal separation. In particular, five numerical \(\Pi_3\) levels reduce to two distinct marginal B/T/N/U vectors (zero versus positive) in the frozen surface. The 30,625 coordinates and 5.88M worlds therefore describe design coverage and provenance, not six equally effective ecological dimensions or evidence magnitude.

## Minimal reusable implementation

TNOA includes a dependency-free Python API and CSV CLI. The reusable layer starts **after domain-specific calibration**:

```python
from tnoa import Evidence, classify

result = classify(
    Evidence(
        deviation_observed=True,
        target_supported=True,
        nuisance_supported=True,
        observable=True,
    )
)

print(result.decision.value)  # U
print(result.reason.value)    # target_nuisance_overlap
```

See [`docs/REUSABLE_IMPLEMENTATION.md`](docs/REUSABLE_IMPLEMENTATION.md) and [`examples/minimal_evidence.csv`](examples/minimal_evidence.csv).

## Fail-closed field translation

A new sensor domain must not copy synthetic or source-device raw thresholds into the reusable API. The prospective translation sequence is:

1. preserve an interpretable primary scientific record;
2. log raw T/N/O/C diagnostics separately;
3. retain pre-calibration observations as `U / field_calibration_pending` and leave TNOA acquisition control inactive;
4. establish independent biological-event, coupled-response, nuisance and observability truth;
5. calibrate on grouped development data against declared error criteria;
6. freeze the calibration manifest before new days/scenes are scored held-out;
7. only after held-out validation allow reason-specific TNOA states to alter adaptive acquisition.

Camera-trap, passive-acoustic and interaction-camera mappings are given in [`docs/FIELD_TRANSLATION_PATHWAY.md`](docs/FIELD_TRANSLATION_PATHWAY.md).

This pathway is **implementation guidance, not Paper-1 field validation**.

## Dimensionless closed-world formulation

The registered synthetic design uses:

- \(\Pi_1\): observation-window length / target-process timescale;
- \(\Pi_2\): nuisance-response timescale / target timescale;
- \(\Pi_3\): direct target amplitude / nuisance amplitude;
- \(\Pi_4\): target-driven local-response amplitude / nuisance amplitude;
- \(\Pi_5\): nuisance spatial correlation length / target spatial-support width;
- \(\Pi_6\): samples per target timescale.

The final frozen surface contains 30,625 registered coordinate combinations and 5,880,000 synthetic worlds. Equal-grid B/T/N/U rates are retained for reproducibility but are not ecological prevalences.

## Novelty boundary

TNOA does **not** claim to invent:

- abstention / reject options;
- partial or set-valued decisions;
- open-set recognition;
- ignorance / evidence conflict;
- imperfect-detection correction;
- nondetection ≠ absence;
- process/observation separation;
- false-positive/false-negative occupancy modelling;
- sensor fusion;
- adaptive ecological sampling;
- Blackwell information ordering or partial-identification bounds.

The defensible contribution is the integration and testing of:

1. a **process-preserving ecological observation interface** with positive non-complementary T/N, separate O, attribution-gated C and optional independently supported A−;
2. **family-conditional decision calibration** that preserves an explicit error meaning when a score representation changes, without claiming classical FWER;
3. **downstream information preservation**, with the magnitude and prevalence/weight conditions measured against known synthetic truth;
4. a freeze/falsification record that retains failed predictions, invalidated diagnostics and an adverse D5 specificity control rather than rewriting development history.

See [`docs/FINAL_PRIOR_ART_AUDIT.md`](docs/FINAL_PRIOR_ART_AUDIT.md) and [`docs/REVIEWER_ATTACK_MATRIX.md`](docs/REVIEWER_ATTACK_MATRIX.md).

## Paper boundary

Paper 1 is a **closed-world methods paper**, not a field-accuracy paper.

It may claim:

- the process-preserving observation architecture;
- separation of target, nuisance, observability, attribution and optional absence evidence;
- the frozen closed-world threshold-portability/family-conditional calibration result;
- downstream information preservation for a known synthetic target-prevalence estimand and the tested D4 prevalence/weight conditions;
- the preregistered negative Pi2 result;
- D3/D5 as post-freeze self-critical controls showing that finer U subdivision is not demonstrated to be semantic-specific;
- robustness only within explicitly tested weighting classes;
- uneven effective separation of the registered synthetic coordinates;
- a prospective fail-closed pathway for revalidating the architecture in new sensing domains.

It must not claim without later empirical validation:

- field visit-detection accuracy;
- calibrated biological absence;
- field prevalence or visit-rate accuracy;
- universal superiority over existing classifiers;
- universal numerical thresholds;
- classical family-wise error-rate control or a distribution-free risk guarantee;
- quantitative cross-system transfer;
- a semantic-specific information premium for the frozen U reasons;
- greater information per annotation, unit cost or field hour;
- pollination effectiveness.

Later field deployment is external validation, not a prerequisite for the closed-world Paper-1 result.

## Repository map

### Manuscript and submission

- [`manuscript/TNOA_MEE_DRAFT.md`](manuscript/TNOA_MEE_DRAFT.md) — active MEE-focused working draft.
- [`manuscript/TNOA_P1_DRAFT.md`](manuscript/TNOA_P1_DRAFT.md) — retained historical draft.
- [`submission/MEE_FRONT_MATTER.md`](submission/MEE_FRONT_MATTER.md) — numbered MEE abstract and review statements.
- [`submission/MEE_SUBMISSION_CHECKLIST.md`](submission/MEE_SUBMISSION_CHECKLIST.md) — production/upload checklist.
- [`scripts/build_mee_submission_docx.py`](scripts/build_mee_submission_docx.py) — reproducible anonymous Word builder.
- [`scripts/validate_mee_submission_docx.py`](scripts/validate_mee_submission_docx.py) — fail-closed Word XML/format validator.

### Method, transfer and audit

- [`docs/CONCEPTUAL_FRAMEWORK.md`](docs/CONCEPTUAL_FRAMEWORK.md) — definitions and inference logic.
- [`docs/REUSABLE_IMPLEMENTATION.md`](docs/REUSABLE_IMPLEMENTATION.md) — runnable API/CLI.
- [`docs/FIELD_TRANSLATION_PATHWAY.md`](docs/FIELD_TRANSLATION_PATHWAY.md) — fail-closed field calibration/validation sequence.
- [`docs/FINAL_PRIOR_ART_AUDIT.md`](docs/FINAL_PRIOR_ART_AUDIT.md) — targeted prior-art boundary.
- [`docs/REVIEWER_ATTACK_MATRIX.md`](docs/REVIEWER_ATTACK_MATRIX.md) — reviewer objections and required answers.
- [`docs/CLAIM_BOUNDARY.md`](docs/CLAIM_BOUNDARY.md) — allowed and forbidden Paper-1 claims.
- [`docs/CLAIM_TRACEABILITY.md`](docs/CLAIM_TRACEABILITY.md) — C1–C15/D1–D5 claim-to-artifact ledger.
- [`docs/OBSERVATION_VOCABULARY_ABLATION.md`](docs/OBSERVATION_VOCABULARY_ABLATION.md) — D3 vocabulary refinement.
- [`docs/PREVALENCE_WEIGHTING_SENSITIVITY.md`](docs/PREVALENCE_WEIGHTING_SENSITIVITY.md) — D4 prevalence/composition-weight stress test.
- [`docs/REASON_SPLIT_SPECIFICITY_CONTROL.md`](docs/REASON_SPLIT_SPECIFICITY_CONTROL.md) — D5 random-split specificity control.

### Figures and reproducibility

- [`derived/mee_figure_data.json`](derived/mee_figure_data.json) — pinned MEE figure data and provenance.
- [`scripts/build_mee_figures.py`](scripts/build_mee_figures.py) — quantitative component-panel builder.
- [`scripts/build_mee_composite_figures.py`](scripts/build_mee_composite_figures.py) — final Figure 2–4/S2 composition.
- [`scripts/audit_manuscript_claims.py`](scripts/audit_manuscript_claims.py) — manuscript claim/anonymity guard.
- [`scripts/build_anonymous_review_bundle.py`](scripts/build_anonymous_review_bundle.py) — deterministic anonymous reviewer package.
- [`reproduce/README.md`](reproduce/README.md) — reproduction policy.
- [`paper_manifest.json`](paper_manifest.json) — machine-readable scientific source/claim state.

## Current status

**MEE scientific package: no unresolved scientific blockers.** The current package contains the active MEE manuscript, C6/C7 + D1/D4 primary result hierarchy, C2 negative result, D3/D5 self-critical specificity control, known-truth downstream estimand, prevalence/weighting and structural audits, runnable API/CLI, fail-closed field-translation template, reproducible multi-panel figures, deterministic anonymous reviewer bundle, and an automatically generated/validated anonymous MEE DOCX.

Remaining work before actual upload is production/user metadata rather than missing scientific analysis: final human inspection of the generated DOCX/figures/reference rendering, publisher-facing final word-count check, author/title-page/CRediT/acknowledgement/funding/competing-interest metadata, final reviewer ZIP identity-literal scan and private upload, followed by one last claim audit after any text edit.
