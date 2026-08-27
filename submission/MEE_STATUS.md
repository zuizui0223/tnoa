# TNOA Paper 1 — MEE submission status

Status after journal-specific packaging pass: **scientific package complete; upload package structurally prepared; author metadata and final document conversion remain.**

## Completed

- Research Article scope checked against current Methods in Ecology and Evolution guidance.
- Closed-world simulations/benchmark positioning retained; V15 field validation remains external.
- Final targeted prior-art audit and final claim audit complete.
- Full working manuscript draft instantiated with C1–C15 provenance tags.
- Quantitative figure builder locked to authoritative InsePi artifacts and visually audited.
- Conceptual Figure 1 implemented as `figures/fig1_tnoa_architecture.svg`.
- Numbered 1–4 abstract prepared.
- Data/Code for peer review statement prepared.
- Keywords prepared.
- Separate title-page template prepared.
- Cover-letter draft prepared.
- MIT open-source licence added for the TNOA code package.
- Reproducible assembler added for an anonymised MEE-facing main-text Markdown file.
- CI definition includes manifest, claim-boundary and MEE package structural checks.

## Still requires author-side metadata

- author names and final author order;
- affiliations and correspondence details;
- CRediT contribution assignments;
- acknowledgements/funding;
- conflict-of-interest statement confirmation;
- ORCID identifiers where applicable.

These cannot be safely inferred from the scientific repository and must be filled before upload.

## Still requires final production

- run `python scripts/assemble_mee_main.py` in a normal checkout;
- convert the assembled Markdown to the journal-upload document format;
- apply double line spacing, continuous line numbering and page numbering;
- place figures/captions according to the chosen upload route;
- provide the anonymised/private reviewer-facing code/data link;
- perform the final 7,000–8,000-word count including references, captions and statements;
- rerun `validate_paper_manifest.py`, `audit_manuscript_claims.py` and `check_mee_submission.py` after any material edit.

## Known infrastructure issue

GitHub Actions has not been generating runs in the TNOA repository during this preparation session. The workflow definitions are committed, but automatic execution has therefore not been observed. This is tracked as an execution/infrastructure issue, not as an unresolved scientific result.
