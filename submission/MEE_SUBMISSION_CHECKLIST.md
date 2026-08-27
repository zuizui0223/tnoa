# Methods in Ecology and Evolution submission checklist

This checklist translates the current MEE author guidance into concrete TNOA upload items. It is a production checklist, not a scientific result.

## Manuscript package

- [x] Working paper is a Standard Article-scale methods manuscript rather than an Applications/Practical Tools note.
- [x] Scientific scope is closed-world methods; V15 field validation remains external.
- [x] Active MEE working draft exists at `manuscript/TNOA_MEE_DRAFT.md`.
- [x] The earlier `manuscript/TNOA_P1_DRAFT.md` remains unchanged as the historical draft.
- [x] Numbered 1–4 abstract text is prepared in `submission/MEE_FRONT_MATTER.md`.
- [x] Keywords are prepared.
- [x] Data/Code for peer review statement is prepared.
- [ ] Convert final manuscript to single-column, double-line-spaced document with continuous page and line numbering.
- [ ] Confirm final Standard Article word count, including references, remains within the journal's current 7000–8000-word guidance.
- [ ] Put all figure/table captions in the manuscript in the journal-required location/order.

## Double-anonymous review

- [x] Author-identifying material is separated into `submission/TITLE_PAGE_TEMPLATE.md`.
- [x] Anonymous code/data-review instructions are separated into `submission/ANONYMOUS_PEER_REVIEW_PACKAGE.md`.
- [ ] Before upload, remove author names, institutions, acknowledgements, repository-owner names, email addresses, ORCIDs and identifying file metadata from the anonymous reviewer package.
- [ ] Use a private-for-peer-review archive/link or reviewer-only uploaded ZIP, not the public owner-identifying repository URL in the anonymous manuscript.

## Title page — separate upload

Complete only in the separate title-page file:

- [ ] manuscript title;
- [ ] full author names;
- [ ] institutions and addresses;
- [ ] acknowledgements;
- [ ] author contributions / CRediT statement;
- [ ] data availability statement;
- [ ] data sources statement where appropriate;
- [ ] corresponding-author information required by the submission system.

## Code and data

- [x] Open-source `LICENSE` is present in the TNOA repository.
- [x] Locked scientific results are pinned by execution commit, artifact digest and result hash in `paper_manifest.json`.
- [x] Claim-to-artifact traceability exists.
- [x] MEE-priority figure data, validation, generation code and source guards exist.
- [x] Reproduction entry point exists in `reproduce/README.md`.
- [ ] Prepare anonymized reviewer ZIP/private archive containing the manuscript-facing code, manifest, required locked JSON artifacts or reviewer-accessible equivalents, README and license.
- [ ] Verify the review package contains every script/file needed to reproduce the paper figures and manuscript inferences that are claimed reproducible from archived artifacts.
- [ ] At acceptance, replace private review locations with permanent public archival accession/DOI(s).

## Figures

- [x] Quantitative Figures 2–4 and Supplementary Figure S2 have pinned data, a fail-closed validator and a CI smoke-tested builder.
- [x] Conceptual Figure 1 source is stored as `figures/fig1_tnoa_architecture.svg`.
- [ ] Final editorial pass on Figure 1 typography only; do not alter its scientific semantics without re-audit.
- [ ] Visually inspect and assemble the final MEE multi-panel layouts without changing plotted data geometry.
- [ ] Generate final submission-resolution raster/vector files from authoritative sources.

## Scientific claim gate

- [x] Final targeted prior-art audit completed.
- [x] Final manuscript claim audit completed for the current working draft.
- [x] No field-accuracy, field-prevalence, calibrated-absence or universal-Pi3 claim is licensed.
- [ ] Re-run claim audit after any material manuscript revision or journal-format rewrite.

## Final upload gate

Do not upload until all unchecked items above that apply to the initial submission have been completed.

## Journal guidance checked

This checklist was aligned to the MEE author guidance retrieved on 2026-08-27. Journal requirements can change; re-check the live author guidelines immediately before upload.
