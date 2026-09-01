# Nearest-neighbour methods matrix

Status: targeted adversarial positioning aid for TNOA Paper 1; **not a systematic review**.

| Method family | What prior work already solves | Priority claim TNOA surrenders | Residual TNOA distinction |
| --- | --- | --- | --- |
| Continuous-score ecological inference [@rhinehart2022continuous] | Uses classifier scores directly in occupancy inference | First non-binary ecological classifier output | TNOA retains heterogeneous process propositions rather than one target-confidence stream |
| AI-to-inference workflows [@cowans2026aiworkflow; @kitzes2026aiworkflow] | Connects sensors, AI confidence and downstream ecology | First end-to-end AI/ecology workflow | TNOA is an upstream observation contract, not an end-to-end workflow |
| Classification-error models [@spence2025classification; @santoro2025bias] | Propagates confusion/bias into ecological inference | First recognition of classifier-error propagation | TNOA distinguishes nuisance, observability and attribution from ordinary class mistakes |
| Multievent / uncertain-state ecology [@pradel2005multievent; @mackenzie2009multistate; @hollanders2022stateuncertainty; @campbellgrant2023partial] | Represents uncertain or partially observed events | First ecological unresolved observation | TNOA constructs the sensor-side event record before downstream latent-state inference |
| Multilabel partial abstention [@nguyen2020partialabstention] | Allows simultaneous labels and partial refusal | First coexistence/partial abstention | T/N/O/C/A− are heterogeneous propositions with different evidence requirements |
| Reject/selective/risk-control methods [@elyaniv2010selective; @hendrickx2024reject; @bates2021riskcontrol] | Abstains and may control formal risks | First abstention/error-controlled rejection | TNOA specifies ecological process-support semantics; its current calibration is closed-world empirical control |
| Calibration and dataset shift [@guo2017calibration; @ovadia2019shift] | Shows confidence semantics can change with representation/shift | First raw-score non-invariance observation | TNOA documents a concrete nuisance-score representation change and recalibrates a declared decision-level error criterion |
| Blackwell information ordering [@blackwell1953comparison] | Formalizes garbling/information ordering | Discovery of never-wider under deterministic coarsening | TNOA measures the ecological magnitude of information loss for a frozen observation contract |
| Partial identification [@manski2005partial] | Provides identified sets/bounds | Invention of identification widths | TNOA uses them to quantify target-prevalence information lost under sensor-record coarsening |
| Belief/evidential uncertainty [@denoeux2019belief; @gao2026evidential] | Represents ignorance/conflict | First explicit ignorance/conflict representation | TNOA fixes ecological process and measurement propositions upstream |
| Imperfect detection / observation models [@mackenzie2002occupancy; @roylelink2006occupancy; @augermethe2021statespace] | Separates latent ecology from observation | Nondetection-is-not-absence | TNOA operates one stage earlier, deciding what observation record those models receive |

## Strongest residual novelty statement

> **TNOA contributes a tested upstream ecological observation contract that separates positive target support, positive nuisance support, measurement observability, attribution-gated coupled response and independently supported absence; calibrates process-support decisions against predeclared family-conditional error semantics; and quantifies under frozen known truth the identifying information lost when the core B/T/N/U record is garbled to binary.**

## D3/D5 qualification

D3's finer frozen U split narrows identified sets numerically, but D5 shows that comparable narrowing is commonly obtained from arbitrary regime-dependent splits. For target prevalence, `48.0%` of 500 random two-way splits are equal to or narrower than the frozen two-reason split. Therefore **the current experiment does not isolate a semantic-specific information advantage of the selected U-reason labels**.

This does not invalidate the architectural choice to retain reason provenance when the reasons are scientifically measurable. It means that D3 cannot be used as quantitative evidence that those meanings, rather than generic extra regime-discriminating structure, caused the additional narrowing.

## Consequence for manuscript language

The paper should defend the tested process-semantic observation contract, C6/C7 calibration result and D1/D4 core B/T/N/U-versus-binary information consequence. D3/D5 belongs as a self-critical supporting diagnostic. Historical priority for abstention, uncertain events, continuous scores, multilabel coexistence, information ordering, partial identification or reason-specific information value is not claimed.
