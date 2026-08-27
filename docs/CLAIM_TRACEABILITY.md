# Claim-to-artifact traceability for TNOA Paper 1

Every central Paper-1 claim must resolve to a locked source generation. This table is the manuscript-level guard against turning development intuition into a result claim.

| ID | Paper claim | Primary locked source | Supporting source / semantic guard | Status | Forbidden extension |
| --- | --- | --- | --- | --- | --- |
| C1 | Target and nuisance are non-complementary positive hypotheses; a target+nuisance state may be legitimate superposition. | InsePi V14b superposition generation / PR #38 | V14b final ternary surface | supported as architecture + closed-world behavior | “T and N are statistically independent” |
| C2 | A narrow ambiguity ridge at Pi2 ≈ 1 is not supported by the registered synthetic experiments. | V14a/V14a2 locked sweeps; `v14a2_first_scientific_sweep_receipt.json` | final surface Pi2 descriptives + weighting sensitivity | locked negative result | “timescale matching never matters” |
| C3 | Direct-visible target+nuisance worlds retained strong target separability under the corrected observation-safe representation. | `v14a2_plateau_diagnosis_observation_safe_result.json`; workflow 32926639089 | target observer freeze | locked diagnostic | field target accuracy |
| C4 | Indirect-only coupled response was not promoted to target support without an independent attribution channel. | `v14b_target_observer_direct_first_validation_v2_result.json`; workflow 32928566405 | V14c semantic clarification | frozen validation | “all indirect evidence is useless” |
| C5 | The target-side frozen validation retained nuisance-only target support at zero and direct-visible target support at one under its registered closed-world design. | `v14b_target_observer_direct_first_validation_v2_result.json` | exact artifact digest in `paper_manifest.json` | frozen validation / structural observer behavior | probability calibration or field prevalence |
| C6 | Inherited raw nuisance thresholds were not invariant across score-representation changes. | retained failed PR #43 + PR #44 diagnosis | family-wise risk freeze | supported development/falsification claim | “the nuisance representation itself failed” |
| C7 | A family-wise alpha=0.05 nuisance decision contract passed its frozen held-out closed-world false-attribution gates. | `v14b_nuisance_familywise_risk_result.json`; workflow 32931223272 | `paper_manifest.json` | frozen validation | field nuisance threshold or field FPR |
| C8 | The final frozen phase surface contains 30,625 coordinates and 5,880,000 synthetic worlds with observers not retuned after freeze. | `v14b_frozen_ternary_phase_surface_result.json`; workflow 32932634622 | artifact digest + phase-surface SHA in manifest | design/provenance fact | evidence strength or ecological frequency estimate |
| C9 | Under equal-grid/equal-regime weighting, the final design-space summary is approximately B=0.2302, T=0.4287, N=0.0877, U=0.2533. | `v14b_frozen_ternary_phase_surface_result.json` | V14c semantic clarification + weighting audit | descriptive locked result | natural prevalence or field decision rate |
| C10 | Most U in that frozen design-space summary is overlap/attribution U rather than the historical no-support category. | final ternary surface | V14c semantic clarification + bounded reweighting audit | descriptive result robust within tested weighting class | universal cause of ecological uncertainty |
| C11 | In the registered Pi1 decomposition, no-support U peaks at Pi1=1 and then declines while overlap/attribution U continues to rise; extending the window therefore does not automatically resolve U. | final ternary surface Pi1 descriptives | `derived/structural_axis_audit.json`; weighting audit | secondary mechanistic illustration | generic non-monotonicity or universal observation-duration law |
| C12 | The sharp Pi3=0 versus Pi3>0 contrast is a structural result of the frozen direct-channel rule; the four positive Pi3 levels collapse to one marginal decision vector. | final ternary surface Pi3 descriptives | V14c semantic clarification + `derived/structural_axis_audit.json` | structural/design result | universal ecological SNR threshold |
| C13 | The registered forced-binary comparator reports target-present false-negative rate 0.3569, but that rate is design-compositional across Pi3 levels and is retained only as a comparator diagnostic. | final ternary surface | `derived/structural_axis_audit.json` + claim boundary | demoted design diagnostic | classifier performance, field miss rate, or general safety effect size |
| C14 | TNOA abstention is not synonymous with low model confidence: U can encode no support, attribution failure or recognized process coexistence. | TNOA framework + final U decomposition | selective-classification comparison in `LITERATURE_EVIDENCE_MAP.md` | conceptual contribution grounded by locked result | novelty claim for abstention itself |
| C15 | PolliPi’s portable 0/0.5/1 output is ordinal positive target evidence, not visit truth, nuisance truth or calibrated probability. | PolliPi `target_evidence.py` pinned in `paper_manifest.json` | TNOA source provenance | frozen interface claim | target absence from score 0 |

## Post-freeze derived analyses

These analyses do not change C1–C15 or the frozen observers. They qualify how the locked results may be interpreted.

- `derived/mee_synthetic_consequences.json`: known-truth synthetic target-prevalence consequence and bounded weighting sensitivity.
- `derived/structural_axis_audit.json`: Pi1 U-reason decomposition, marginal axis-separation audit, and C13 Pi3 composition identity.

The downstream prevalence result is stronger than C13 as an ecological consequence of binary coarsening because it evaluates information loss across 3,003 latent-regime compositions rather than elevating one equal-grid comparator rate.

## Manuscript rule

A sentence that asserts an empirical/simulation result must cite at least one C-ID internally during drafting or point explicitly to a registered post-freeze derived analysis. Conceptual framing can cite framework sections, but if it contains a number, direction of effect, pass/fail statement or claim of observed structure it must map to a locked C-ID or pinned derived result.

## Results that must remain in the supplement or development ledger

- the PR #40 target-separability diagnostic invalidated by truth leakage;
- PR #43 nuisance v1 failure;
- any V15 development calibration or field result unless Paper 1 scope is explicitly revised.

## Claim audit rule

Before submission, scan the manuscript for the following terms and require a traceability entry or qualification wherever they appear:

- `shows`, `demonstrates`, `proves`, `supports`, `falsifies`, `improves`, `reduces`, `increases`;
- percentages, rates, thresholds and world counts;
- `field`, `general`, `universal`, `optimal`, `absence`, `probability`, `performance`, `dimension`.
