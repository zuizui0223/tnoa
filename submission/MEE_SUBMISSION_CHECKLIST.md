# Methods in Ecology and Evolution submission checklist

This checklist translates the current MEE author guidance into concrete TNOA upload items. It is a production checklist, not a scientific result.

## Manuscript package

- [x] Working paper is a Standard Article-scale methods manuscript rather than an Applications/Practical Tools note.
- [x] Scientific scope is closed-world methods; field validation remains external.
- [x] Active MEE working draft exists at `manuscript/TNOA_MEE_DRAFT.md`.
- [x] The earlier `manuscript/TNOA_P1_DRAFT.md` remains unchanged as the historical draft.
- [x] Numbered 1–4 abstract text is prepared in `submission/MEE_FRONT_MATTER.md`.
- [x] The numbered abstract was compressed from about 391 repository-counted words to below the journal's 350-word target, and `scripts/validate_mee_submission_package.py` now fails if the abstract exceeds 350 words.
- [x] Eight keywords are prepared, unique and alphabetized; `tests/test_submission_front_matter.py` enforces the maximum-eight and alphabetical-order rules.
- [x] Data/Code for peer review statement is prepared.
- [x] `scripts/build_mee_initial_submission_source.py` assembles one anonymous source with the standard `Materials and Methods` heading, figure callouts and Figure 1–4/S2 captions.
- [x] `scripts/audit_initial_submission_readiness.py` checks structure, citation-key completeness and a conservative word-count estimate including bibliography text in CI.
- [x] CI run `33039903388` estimated 4,953 words including a conservative bibliography-field estimate; all 12 cited bibliography keys resolved with zero missing citations. Six unused bibliography entries remain non-blocking and do not represent missing citations.
- [x] `scripts/build_mee_submission_docx.py` converts the canonical anonymous source to a single-column Word upload candidate with citeproc-rendered references, double spacing, continuous line numbering, page numbering and anonymous document metadata.
- [x] `scripts/validate_mee_submission_docx.py` inspects the Word XML fail-closed for title/section content, rendered citations/references, anonymity, double spacing, continuous line numbering and page numbering. The CSL parent style is pinned and hash-checked in CI.
- [ ] Recheck the final publisher-facing word count, including references, in the generated DOCX/submission system. The repository counts remain guards, not the publisher's final count.
- [ ] Open the generated DOCX in Word or a compatible viewer and confirm equation rendering, page/line numbering, typography, page breaks and figure-caption placement.

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

- [x] Manuscript title is synchronized with the active MEE manuscript.
- [x] Running headline is prepared as `Preserving unresolved observations` and is within the journal's 45-character limit.
- [x] Initial-submission Data Availability Statement is prepared, with permanent DOI/accession wording reserved for acceptance.
- [x] Data sources statement is prepared and explicitly limits quantitative evidence to the locked synthetic/post-freeze record.
- [x] Paper-scope ethics wording is prepared and states that this manuscript does not report a new organismal, human-subject or field-site experiment.
- [x] A submission-stage inclusion statement is prepared for the synthetic-only methodological scope, explicitly noting that no region-specific field sampling or stakeholder-derived data are reported.
- [ ] Full author names.
- [ ] Institutions and addresses.
- [ ] Corresponding-author information required by the submission system.
- [ ] Author contributions / CRediT statement.
- [ ] Acknowledgements.
- [ ] Funding statement.
- [ ] Conflict of interest / competing interests statement.

## Editor-facing positioning

- [x] `submission/MEE_EDITORIAL_PITCH.md` prepares an optional cover-letter draft and a short pre-submission-enquiry version.
- [x] The pitch leads with a methodological gap independent of the motivating taxon/system.
- [x] The pitch distinguishes the tested methodological contribution from a workflow that merely links existing tools.
- [x] Simulation/benchmark evidence, broad cross-sensor applicability, usable code and the closed-world field boundary are explicit.
- [ ] Decide at submission whether to use the optional covering letter and/or send a pre-submission enquiry.

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

- [x] Quantitative Figure 2–4 component panels and Supplementary Figure S2 have pinned data, a fail-closed validator and a CI smoke-tested builder.
- [x] `scripts/build_mee_composite_figures.py` assembles final Figure 2 (3 panels), Figure 3 (2 panels), Figure 4 (2 panels) and Supplementary Figure S2 directly from the same pinned figure data.
- [x] Composite output includes SVG + 300-dpi PNG and a provenance sidecar; no manual data-geometry editing is required.
- [x] Conceptual Figure 1 source is stored as `figures/fig1_tnoa_architecture.svg`.
- [x] Figure 1–4 and Supplementary Figure S2 captions are assembled into the canonical anonymous submission source.
- [ ] Final human visual inspection of Figure 1 and the code-assembled multi-panel figures for typography, label collisions and journal sizing; do not alter data geometry manually.

## References

- [x] Every citation key used by the active MEE submission source resolves in `references.bib` (12 cited keys, zero missing in CI run `33039903388`).
- [x] Six BibTeX entries are currently unused by the active manuscript; they are retained because `references.bib` also supports the broader prior-art audit and are not missing-reference errors.
- [x] DOCX conversion renders citations and the References section through Pandoc citeproc using the pinned APA parent CSL recorded in `submission/MEE_FORMATTING_PROVENANCE.md`.
- [ ] Final publisher-style visual inspection of rendered references in the generated DOCX.

## Scientific claim gate

- [x] Final targeted prior-art audit completed.
- [x] Final manuscript claim audit completed for the current working draft.
- [x] No field-accuracy, field-prevalence, calibrated-absence or universal-Pi3 claim is licensed.
- [ ] Re-run claim audit after any material manuscript revision or formatting change that changes text.

## Final upload gate

Do not upload until all unchecked items above that apply to the initial submission have been completed.

## Journal guidance checked

This checklist was aligned to the MEE author guidance retrieved on 2026-08-27. Current guidance requires a single-column, double-line-spaced Standard Article within the 7000–8000-word range/ceiling (including references), continuous line and page numbering, a separate title page, a running headline of no more than 45 characters, a numbered 1–4 abstract aiming not to exceed 350 words, at most eight keywords in alphabetical order, anonymized code/data available for peer review, and an inclusion statement during submission. Re-check the live author guidelines immediately before upload.
