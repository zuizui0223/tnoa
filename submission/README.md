# TNOA → Methods in Ecology and Evolution submission assembly

This directory is the production layer for the MEE initial submission. It does not redefine or rerun the TNOA science.

## 1. Validate repository package

From the repository root:

```bash
python scripts/validate_paper_manifest.py
python scripts/audit_manuscript_claims.py
python scripts/validate_mee_submission_package.py
```

## 2. Build anonymous manuscript source

```bash
python scripts/build_mee_anonymous_manuscript.py
```

Expected output:

```text
submission/generated/MEE_ANONYMOUS_MANUSCRIPT.md
```

The builder uses the numbered MEE abstract/front matter and the audited manuscript body, removes internal C-ID HTML comments, and fails on public repository-owner strings or email addresses.

## 3. Convert to journal document

The initial-submission document must be produced from the generated anonymous manuscript and current `references.bib`. The final document should follow the live MEE instructions, including:

- single column;
- double line spacing;
- continuous page numbering;
- continuous line numbering;
- standard MEE section order;
- numbered 1–4 abstract;
- figures/tables with captions;
- current Standard Article word-count limits.

If Pandoc is used, enable citation processing against `references.bib` and then inspect every rendered citation/reference manually. Journal formatting is editorial; it must not change the scientific claim boundary.

## 4. Separate title page

Complete `TITLE_PAGE_TEMPLATE.md` outside the anonymous manuscript and upload it as the separate title-page file requested by MEE.

Do not copy author names, institutions, acknowledgements, ORCIDs or identifying metadata into the anonymous manuscript.

## 5. Reviewer code/data package

Follow `ANONYMOUS_PEER_REVIEW_PACKAGE.md`.

The reviewer package should be private/reviewer-only during double-anonymous review. Preserve scientific hashes and locked result provenance while removing ownership/author identifiers.

## 6. Figures

- Figure 1 conceptual source: `figures/fig1_tnoa_architecture.svg`.
- Quantitative Figures 2–5: generate from the source-guarded builder described in `docs/FIGURE_PLAN.md`.

Do not manually alter quantitative data geometry after generation.

## 7. Final gate before upload

1. Complete all applicable unchecked items in `MEE_SUBMISSION_CHECKLIST.md`.
2. Perform the anonymity scan on the reviewer package.
3. Re-run manuscript claim audit after formatting edits.
4. Re-check the live MEE author guidelines because journal requirements may change.
5. Confirm title page and anonymous manuscript are uploaded as separate files.

## Scientific freeze rule

Formatting, anonymization and submission packaging must not alter:

- locked result hashes;
- T/C/N/O/A− definitions;
- B/T/N/U semantics;
- the no-supported-evidence semantic correction;
- Pi2/Pi3 claim boundaries;
- field-validation exclusions.

Any material scientific edit invalidates the previous final claim audit and requires a new audit before submission.
