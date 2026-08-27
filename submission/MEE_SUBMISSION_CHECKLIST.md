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
- [x] `scripts/build_mee_initial_submission_source.py` assembles one anonymous source with the standard `Materials and Methods` heading, figure callouts and Figure 1–4/S2 captions.
- [x] `scripts/audit_initial_submission_readiness.py` checks structure, citation-key completeness and a conservative word-count estimate including bibliography text in CI.
- [ ] Convert the assembled source to a single-column, double-line-spaced upload document with continuous page and line numbering.
- [ ] Recheck the final publisher-facing word count, including references, after conversion. The CI estimate is a guard, not the publisher's final count.
- [ ] Confirm figure/table caption placement after conversion to the final upload format.

## Double-anonymous review

- [x] Author-identifying material is separated into `submission/TITLE_PAGE_TEMPLATE.md`.
- [x] Anonymous code/data-review instructions are separated into `submission/ANONYMOUS_PEER_REVIEW_PACKAGE.md`.
- [x] Deterministic anonymous reviewer-bundle builder and standalone validator are implemented.
- [x] CI builds the bundle from the active MEE package plus pinned Source-A/Source-B checkouts and runs the recursive identity/hash checks.
- [x] The reviewer manuscript and initial-submission manuscript are assembled from the same canonical anonymous source.
- [ ] After the title page is complete, rebuild the final ZIP with every author/institution identifying literal supplied through repeated `--forbid-literal` arguments.
- [ ] Review any remaining ORCID, acknowledgement or file-metadata identifiers that are not representable as simple text literals.
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
- [x] Anonymous reviewer ZIP construction is automated by `scripts/build_anonymous_review_bundle.py`.
- [x] The bundle contains the active anonymous manuscript, C/D-tagged audit source, three derived analyses, current figure data/builder, reusable API/CLI, pinned upstream result summaries, scientific source snapshot, README and license.
- [x] `scripts/validate_anonymous_review_bundle.py` verifies file hashes, active MEE schemas, source commits, figure inventory and identity leakage.
- [ ] Build the final reviewer ZIP after all author/title-page metadata are known and retain its external receipt SHA-256.
- [ ] Upload that final validated ZIP to the journal's reviewer-only/private location. The public CI artifact is validation only.
- [ ] At acceptance, replace private review locations with a permanent archive carrying a persistent identifier/DOI; do not rely solely on a mutable source-code host.

## Figures

- [x] Quantitative Figures 2–4 and Supplementary Figure S2 have pinned data, a fail-closed validator and a CI smoke-tested builder.
- [x] Conceptual Figure 1 source is stored as `figures/fig1_tnoa_architecture.svg`.
- [x] Figure 1–4 and Supplementary Figure S2 captions are assembled into the canonical anonymous submission source.
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

This checklist was aligned to the MEE author guidance retrieved on 2026-08-27. Current guidance requires a single-column, double-line-spaced Standard Article within the 7000–8000-word range/ceiling (including references), continuous line and page numbering, a separate title page, a numbered 1–4 abstract, and anonymized code/data available for peer review. Re-check the live author guidelines immediately before upload.
