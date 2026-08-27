# TNOA → Methods in Ecology and Evolution submission assembly

This directory is the production layer for the MEE initial submission. It does not redefine or rerun the TNOA science.

## 1. Validate repository package

From the repository root:

```bash
python scripts/validate_paper_manifest.py
python scripts/validate_mee_figure_data.py
python scripts/audit_manuscript_claims.py
python scripts/validate_mee_submission_package.py
```

## 2. Build the canonical anonymous source

```bash
python scripts/build_mee_initial_submission_source.py
python scripts/build_mee_anonymous_manuscript.py
```

Expected Markdown outputs:

```text
submission/generated/MEE_INITIAL_SUBMISSION_SOURCE.md
submission/generated/MEE_ANONYMOUS_MANUSCRIPT.md
```

The builders use the numbered MEE abstract/front matter and the audited manuscript body, normalize the `Materials and Methods` heading, add figure callouts/captions, remove internal C/D provenance comments from the reviewer copy, and fail on public repository-owner strings or email addresses.

## 3. Build and validate the anonymous Word upload candidate

Install the submission dependencies and run the DOCX builder with the pinned CSL parent style recorded in `MEE_FORMATTING_PROVENANCE.md`:

```bash
python -m pip install -r requirements-submission.txt
python scripts/build_mee_submission_docx.py --csl /path/to/pinned/apa.csl
python scripts/validate_mee_submission_docx.py submission/generated/TNOA_MEE_ANONYMOUS_INITIAL_SUBMISSION.docx
```

CI performs the same conversion using the pinned Citation Style Language repository commit and verifies the DOCX XML for:

- single-column manuscript structure;
- double spacing;
- continuous line numbering;
- page numbering;
- rendered citations and References;
- anonymous core metadata;
- the manuscript word-count guard.

The generated DOCX still requires a final visual inspection in Word or a compatible viewer. Formatting is editorial and must not change the scientific claim boundary.

## 4. Separate title page

Complete `TITLE_PAGE_TEMPLATE.md` outside the anonymous manuscript and upload it as the separate title-page file requested by MEE.

The non-author fields already prepared include:

- the synchronized manuscript title;
- the <=45-character running headline;
- Data Availability and Data Sources wording;
- paper-scope ethics wording;
- a synthetic-only submission-stage inclusion statement.

Author names, institutions, corresponding-author details, CRediT assignments, acknowledgements, funding and competing interests remain to be completed from the final authorship information.

Do not copy author names, institutions, acknowledgements, ORCIDs or identifying metadata into the anonymous manuscript.

## 5. Editor-facing positioning

`MEE_EDITORIAL_PITCH.md` contains:

- the one-sentence method pitch;
- why the contribution is more than a workflow linking existing methods;
- the primary simulation/benchmark evidence;
- the cross-sensor transferability argument and closed-world boundary;
- an optional covering-letter draft;
- a short pre-submission-enquiry version.

A covering letter is optional under the author guidance checked on 2026-08-27. Use it only if it adds information relevant to editorial assessment.

## 6. Reviewer code/data package

Follow `ANONYMOUS_PEER_REVIEW_PACKAGE.md`.

The reviewer package should be private/reviewer-only during double-anonymous review. Preserve scientific hashes and locked result provenance while removing ownership/author identifiers. After final authorship metadata are known, rebuild the ZIP with every identifying author/institution literal supplied through repeated `--forbid-literal` flags.

## 7. Figures

- Figure 1 conceptual source: `figures/fig1_tnoa_architecture.svg`.
- Quantitative Figures 2–4 and Supplementary Figure S2 are generated from the pinned MEE figure data.

```bash
python scripts/validate_mee_figure_data.py
python scripts/build_mee_figures.py --output-dir /tmp/tnoa_mee_panels
python scripts/build_mee_composite_figures.py --output-dir /tmp/tnoa_mee_composite
```

Do not manually alter quantitative data geometry after generation. Perform a final visual inspection for typography, label collisions and journal sizing.

## 8. Final gate before upload

1. Complete all applicable unchecked items in `MEE_SUBMISSION_CHECKLIST.md`.
2. Recheck the publisher-facing word count in the generated DOCX/submission system.
3. Perform the final anonymity scan on the reviewer package using all known author/institution literals.
4. Re-run the manuscript claim audit after any material text edit.
5. Re-check the live MEE author guidelines because journal requirements may change.
6. Confirm title page and anonymous manuscript are uploaded as separate files.

## Scientific freeze rule

Formatting, anonymization and submission packaging must not alter:

- locked result hashes;
- T/C/N/O/A− definitions;
- B/T/N/U semantics;
- the no-supported-evidence semantic correction;
- Pi2/Pi3 claim boundaries;
- field-validation exclusions.

Any material scientific edit invalidates the previous final claim audit and requires a new audit before submission.
