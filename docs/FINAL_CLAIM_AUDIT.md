# Final claim audit for TNOA Paper 1

Status: **repository manuscript draft audited against the locked claim boundary**.

Audited manuscript:

- `manuscript/TNOA_P1_DRAFT.md`

This audit is the final scientific-language gate for the current repository draft. It must be repeated if the manuscript is materially rewritten before journal submission.

## 1. Audit rules

The manuscript was checked against:

- `docs/CLAIM_BOUNDARY.md`;
- `docs/CLAIM_TRACEABILITY.md`;
- `docs/FINAL_PRIOR_ART_AUDIT.md`;
- `paper_manifest.json`;
- the locked V14b/V14c result and receipt paths listed in the manifest.

The audit specifically checks:

1. every central numerical/directional result remains a closed-world claim;
2. no field accuracy, prevalence or absence-certification claim is imported from V15 development;
3. the historical `information_absent` source label is not presented as proven information absence;
4. the historical `baseline + U` metric is not called strict target-presence partial-identification width;
5. the Pi3 zero/positive contrast is explicitly structural and synthetic;
6. Pi2≈1 is reported as a rejected narrow-ridge hypothesis, not as a universal negative law;
7. T/N coexistence is not described as statistical independence;
8. low T is never converted to A−;
9. component-level priority claims are absent after the final prior-art audit;
10. central numerical claims retain C-ID provenance tags during drafting.

## 2. Claim-by-claim audit

| ID | Audit result | Manuscript status | Required qualification retained |
| --- | --- | --- | --- |
| C1 | PASS | T and N are described as positive non-complementary process hypotheses and legitimate coexistence is retained. | No claim of statistically independent failures. |
| C2 | PASS | The narrow Pi2≈1 ridge is reported as not supported in the registered synthetic experiments. | Manuscript explicitly says timescale ratios may matter elsewhere. |
| C3 | PASS | Corrected observation-safe direct-visible separability is used only as a locked diagnostic. | No field accuracy/general separability claim. |
| C4 | PASS | Indirect-only C is not promoted without attribution. | Manuscript explicitly avoids “all indirect evidence is useless”. |
| C5 | PASS | Frozen target validation rates are described only under registered closed-world worlds. | No probability or prevalence interpretation. |
| C6 | PASS | Historical nuisance failure is localized to score/decision-scale inheritance. | Representation itself is not falsely declared failed. |
| C7 | PASS | Family-wise alpha=0.05 false-certainty result is reported with its two registered held-out negative-family rates. | Explicitly not a field threshold/FPR. |
| C8 | PASS | 30,625 coordinates and 5,880,000 worlds appear with C8 provenance. | No ecological-frequency interpretation. |
| C9 | PASS | B/T/N/U aggregate rates appear with C9 provenance. | Explicitly equal-grid/equal-regime design-space rates. |
| C10 | PASS | U decomposition uses `no-supported-evidence`, not unconditional information absence. | Explicitly design-space composition, not ecological prevalence. |
| C11 | PASS | Longer Pi1 is reported as not monotonically removing U in the frozen design. | No universal sensor law. |
| C12 | PASS | Pi3=0 versus Pi3>0 is labeled a structural consequence of the exact-zero synthetic direct-channel rule. | No continuous field SNR claim. |
| C13 | PASS | Forced-binary false-negative rate 0.3569 / 35.69% is tied to the registered synthetic comparator. | Explicitly not a field miss rate. |
| C14 | PASS | U is distinguished from low classifier confidence. | Manuscript does not claim invention of abstention/ignorance. |
| C15 | PASS | PolliPi 0/0.5/1 is described as ordinal positive target evidence only. | Score 0 never certifies absence. |

## 3. Prior-art language audit

The instantiated draft does not claim that TNOA invented:

- abstention or reject options;
- set-valued/partial decisions;
- open-set recognition;
- ignorance or evidence conflict;
- imperfect-detection correction;
- nondetection/absence separation;
- false-positive/false-negative occupancy modeling;
- ecological process/observation separation;
- sensor fusion;
- adaptive ecological sampling.

The novelty statement is restricted to **integrated ecological sensing architecture plus frozen dimensionless decision geometry**.

### Prohibited phrases

The following priority formulations are prohibited by repository policy and are absent from the current draft:

- `TNOA is the first ...`;
- `No previous method separates ...`;
- `first framework to separate process and observation`;
- `introduces the idea that nondetection is not absence`;
- `uniquely represents ignorance`;
- `first method to retain multiple hypotheses`.

## 4. Information-status audit

### Historical source terminology

The frozen V14b source contains the field name:

- `undetermined_information_absent_rate`

The manuscript does **not** expose that source name as a scientific interpretation. It consistently uses:

- `no-supported-evidence U`

and states that true information absence requires an independent diagnostic.

Status: **PASS**.

### Partial-identification terminology

The historical source field `visit_presence_partial_identification_width` is not treated as a strict target-presence partial-identification width in the manuscript. The draft explains that N does not certify target absence and that the historical `baseline + U` quantity is therefore only a descriptive non-target-decision width.

Status: **PASS**.

## 5. Field-boundary audit

The manuscript explicitly excludes from Paper 1:

- field visit-detection accuracy;
- field nuisance FPR;
- field prevalence;
- calibrated field absence;
- transfer of the alpha-derived raw nuisance threshold;
- pollination effectiveness;
- universal Pi3 threshold interpretation.

V15 appears only as external validation / empirical next step.

Status: **PASS**.

## 6. Figure-claim audit

The current quantitative figure package is consistent with the manuscript:

- Figure 2: C10/C11, U composition over Pi1;
- Figure 3: C2, absence of the registered narrow Pi2 ridge;
- Figure 4: C12/C13, structural registered Pi3 zero/positive contrast and binary cost;
- Figure 5: C7, family-wise nuisance false-certainty contract.

Figure 4 was specifically changed from symlog geometry to equal-spaced registered Pi3 categories after visual audit so that the figure does not imply a continuous field SNR law.

Status: **PASS**.

## 7. Mechanical scanner

`scripts/audit_manuscript_claims.py` now checks:

- known forbidden absolute-priority phrases;
- C-ID presence in paragraphs containing the central registered numerical values;
- Pi2/Pi3 empirical qualification tags;
- explicit non-universality and field-boundary language.

A local execution attempt in the current ChatGPT execution environment could not clone GitHub because external DNS resolution for `github.com` failed before repository code was reached. This is an environment/network limitation, not a failed manuscript scan. The scanner is added to repository CI so it will execute when GitHub Actions run generation is available for this repository.

## 8. Scientific submission status

For the current repository draft, the following scientific preparation gates are complete:

- conceptual framework;
- locked result provenance;
- targeted final prior-art audit;
- integration-level novelty boundary;
- cross-domain conceptual transfer map;
- claim-to-artifact traceability;
- paper-grade quantitative figure builder and render audit;
- instantiated full manuscript draft;
- final claim audit against that draft.

No unresolved **scientific** blocker is identified in the repository package at this stage.

Remaining work before actual journal upload is editorial/production work:

- finalize the conceptual Figure 1 artwork;
- convert the working Markdown draft to the target journal format;
- complete author contributions / acknowledgements / metadata;
- perform a final citation-style and reference-completeness pass after formatting;
- rerun this claim audit after any material manuscript revision.

## 9. Re-audit trigger

This audit is invalidated and must be repeated if any of the following occur:

- locked result source or artifact hashes change;
- a new quantitative result is added;
- Paper 1 scope expands to field validation;
- T/C/N/O/A− definitions change;
- the manuscript adds a new novelty/priority claim;
- quantitative figure geometry changes;
- the manuscript is substantially rewritten.
