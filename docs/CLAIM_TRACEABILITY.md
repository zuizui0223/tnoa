# Claim-to-artifact traceability for TNOA Paper 1

Every empirical or simulation claim must resolve to a locked C-source or an explicitly labelled post-freeze D-analysis. Post-freeze controls qualify the interpretation of frozen results; they do not rewrite the frozen observers.

## Frozen claims C1–C15

| ID | Supported paper claim | Primary source | Status / required boundary |
| --- | --- | --- | --- |
| C1 | T and N are positive, non-complementary supports and may coexist. | frozen TNOA/V14b decision architecture | architecture + closed-world behavior; not statistical independence |
| C2 | The preregistered narrow ambiguity ridge near Pi2≈1 was not supported. | V14a/V14a2 locked sweeps | locked negative result; not “timescale matching never matters” |
| C3 | Direct-visible target+nuisance remained separable under corrected observation-safe representation. | V14a2 corrected audit, workflow 32926639089 | closed-world diagnostic only |
| C4 | Indirect-only coupled response was not promoted to T without attribution. | V14b target freeze, workflow 32928566405 | frozen validation; not “indirect evidence is useless” |
| C5 | Frozen target observer behavior on registered target/non-target regimes. | V14b target freeze | structural observer behavior, not probability calibration |
| C6 | Inherited nuisance raw threshold was not invariant after score-representation change. | retained failed/diagnostic development sequence | primary methodological failure |
| C7 | A **predeclared family-conditional** `alpha=0.05` false-attribution criterion passed held-out negative families (`0/43,200`, `1,920/43,200`). | historically named `v14b_nuisance_familywise_risk_result.json`, workflow 32931223272 | primary frozen validation; **not** classical FWER, distribution-free guarantee, field threshold or field FPR |
| C8 | Final surface has 30,625 coordinates and 5,880,000 worlds with no post-freeze retuning. | V14b final surface, workflow 32932634622 | design/provenance fact, not evidence strength |
| C9 | Equal-grid pooled B/T/N/U rates. | V14b final surface | descriptive design-space summary, not ecological prevalence |
| C10 | Frozen U is mainly the combined overlap/attribution bucket under the registered design. | V14b final surface | stronger statement only within tested row-level reweighting class |
| C11 | After Pi1=1, frozen no-support U decreases while combined overlap/attribution U increases. | V14b final surface | secondary reason-substitution illustration; not universal non-monotonicity |
| C12 | Pi3 zero/positive boundary is structural in the frozen direct-channel rule. | V14b final surface | not a field SNR law |
| C13 | Forced-binary miss `0.3569` is design-compositional: `0.2*1 + 0.8*0.196125`. | V14b final surface + D2 | demoted design diagnostic, not classifier performance |
| C14 | U need not mean low confidence; unresolvedness can have different process/measurement causes. | framework + frozen decomposition | conceptual contribution; abstention itself is prior art |
| C15 | Source adapter 0/0.5/1 is ordinal positive target evidence, not visit truth/probability/absence. | pinned Source-A adapter | frozen interface claim |

## Post-freeze derived analyses

### D1 — downstream synthetic consequence

`derived/mee_synthetic_consequences.json`

Known-truth target-prevalence partial identification under the frozen six-regime emission map. The binary record is a deterministic garbling of B/T/N/U, so never-wider is structural. The empirical result is the magnitude of information loss, including median B/T/N/U `0.0299207` versus binary `0.2656306`.

### D2 — structural interpretation audit

`derived/structural_axis_audit.json`

Pi1 reason substitution, uneven marginal axis separation and the C13 Pi3 composition identity. Descriptive frozen-design diagnostics only.

### D3 — observation-vocabulary refinement

`derived/observation_vocabulary_ablation.json`

Literature-audit-motivated, post-freeze, not preregistered. It records numerical narrowing across four nested vocabularies and five estimands. The final two-way frozen U split is informative, but **D3 does not demonstrate semantic specificity**. Its interpretation is controlled by D5.

### D4 — prevalence/composition-weight sensitivity

`derived/prevalence_weighting_sensitivity.json`

Reviewer-motivated, post-freeze, not preregistered. It stress-tests the **core D1 B/T/N/U-versus-binary result** by target prevalence and direct composition weighting. Key allowed results include `141/3003 = 4.70%` compositions at θ≤0.2, rare-target median `0.000175` B/T/N/U versus `0.07410` binary, and κ=10 worst-case ≥`57.5%` weighted-mean binary width removal.

D4 does not convert the simplex into an ecological prior and does not rescue a semantic interpretation of D3.

### D5 — random-split semantic-specificity control

`derived/reason_split_specificity_control.json`

Reviewer-motivated, post-freeze, not preregistered. It tests whether D3's final narrowing is specific to the meanings of the two frozen reason buckets.

Target-prevalence control:

- generic B/T/N/U: `0.0299207`;
- constant 50:50 U split: `0.0299207`;
- 500 unlabeled regime-dependent two-way splits, median: `0.0050075`;
- frozen two-reason split: `0.0040780`;
- random equal-or-narrower fraction: `0.480`.

Across all five estimands, random equal-or-better fractions range `0.480–0.672`. All 500 random three-way splits are full rank for the six-regime constraint system and point-identify all five estimands to numerical tolerance.

**Required interpretation:** additional non-redundant observation columns can sharply improve identification in the six-regime design, but the current experiment does not isolate an information advantage caused by the selected reason semantics. Exact width depends on the added column's orientation as well as rank/state count.

## Frozen reason vocabulary versus reusable API

The frozen V14b D3/D5 surface stores two U reason buckets: historical `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`. The later `tnoa/core.py` exposes four U reasons: no-supported-evidence, target+nuisance overlap, missing attribution and insufficient observability.

The frozen `OVERLAP_OR_ATTRIBUTION` bucket includes both simultaneous T+N and unresolved indirect-only attribution in the source decision code. `insufficient_observability` has no separate frozen D3 column. Therefore **D3/D5 do not empirically validate a one-to-one four-reason API decomposition**.

## Final result hierarchy

1. **C6/C7** — observed threshold-meaning failure and family-conditional calibration recovery.
2. **D1 + D4** — core B/T/N/U-versus-binary information-loss magnitude and prevalence/composition-weight conditions.
3. **C2** — preregistered negative ridge result.
4. **D3 + D5** — supporting self-critical refinement diagnostic: additional columns improve identifiability, but semantic-specific reason value is not isolated.
5. C10/C11/D2 — secondary mechanism/design interpretation. C13 remains diagnostic only.

## Manuscript rule

A numerical direction, pass/fail statement or observed structure must carry its C/D provenance internally during drafting. D3–D5 must always retain their post-freeze/not-preregistered status. `0.00408` may not appear as evidence of a semantic-specific reason premium unless D5 is stated in the same interpretive context.

## Results outside Paper 1

- the PR #40 target-separability diagnostic invalidated by truth leakage;
- later field/V15 calibration unless scope is explicitly revised;
- any fixed-annotation-budget information-efficiency claim without a separate frozen measurement-design specification.
