# Methods in Ecology and Evolution submission checklist

This checklist translates the current MEE author guidance into concrete TNOA upload items. It is a production checklist, not a scientific result.

## Manuscript package

- [x] Working paper is a Research Article / Standard Article-scale methods manuscript rather than an Applications/Practical Tools note.
- [x] Scientific scope is closed-world methods; field validation remains external.
- [x] Active MEE working draft exists at `manuscript/TNOA_MEE_DRAFT.md`.
- [x] The earlier `manuscript/TNOA_P1_DRAFT.md` remains unchanged as the historical draft.
- [x] Numbered 1–4 abstract text is prepared in `submission/MEE_FRONT_MATTER.md`.
- [x] The current numbered abstract is **302 repository-counted words**, below the journal's 350-word target; `scripts/validate_mee_submission_package.py` fails if it exceeds 350 words.
- [x] Eight keywords are prepared, unique and alphabetized; `tests/test_submission_front_matter.py` enforces the maximum-eight and alphabetical-order rules.
- [x] Data/Code for peer review statement is prepared.
- [x] `scripts/build_mee_initial_submission_source.py` assembles one anonymous source with the standard `Materials and Methods` heading, figure callouts and Figure 1–4/S2 captions.
- [x] `scripts/audit_initial_submission_readiness.py` checks structure, citation-key completeness and a conservative word-count estimate including bibliography text in CI.
- [x] The latest validated package is within the repository's 8,000-word guard. The generated anonymous DOCX reports **7,712 visible words**; this is a production check, not the publisher submission system's final count.
- [x] Current reference-scope audit reports **24 active-paper citation entries, 9 prior-art-only entries and 0 orphan bibliography entries**.
- [x] `scripts/build_mee_submission_docx.py` converts the canonical anonymous source to a single-column Word upload candidate with citeproc-rendered references, double spacing, continuous line numbering, page numbering and anonymous document metadata.
- [x] `scripts/validate_mee_submission_docx.py` inspects the Word XML fail-closed for title/section content, rendered citations/references, anonymity, double spacing, continuous line numbering and page numbering. The CSL parent style is pinned and hash-checked in CI.
- [ ] Recheck the final publisher-facing word count, including references, in the generated DOCX/submission system. The 7,712-word validated DOCX count remains a repository guard, not the publisher's authoritative count.
- [ ] Open the generated DOCX in Word or a compatible viewer and confirm equation rendering, page/line numbering, typography, page breaks and figure-caption placement.

## Double-anonymous review

- [x] Author-identifying material is separated into `submission/TITLE_PAGE_TEMPLATE.md`.
- [x] Anonymous code/data-review instructions are separated into `submission/ANONYMOUS_PEER_REVIEW_PACKAGE.md`.
- [x] Deterministic anonymous reviewer-bundle builder and standalone validator are implemented.
- [x] CI builds the bundle from the active MEE package plus pinned Source-A/Source-B checkouts and runs the recursive identity/hash checks.
- [x] The reviewer manuscript and initial-submission manuscript are assembled from the same canonical anonymous source.
- [x] The reviewer package includes the current D1–D5 derived analyses/controls, structural and figure-data audits, reusable API/CLI, pinned upstream scientific snapshots, claim documentation, README and license.
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
- [x] D5 is presented as an adverse/self-critical specificity control rather than as evidence for a semantic-specific U-reason information premium.
- [ ] Decide at submission whether to use the optional covering letter and/or send a pre-submission enquiry.

## Code and data

- [x] Open-source `LICENSE` is present in the TNOA repository.
- [x] Locked scientific results are pinned by execution commit, artifact digest and result hash in `paper_manifest.json`.
- [x] Claim-to-artifact traceability exists through C1–C15 and D1–D5.
- [x] MEE-priority figure data, validation, generation code and source guards exist.
- [x] Reproduction entry point exists in `reproduce/README.md`.
- [x] Anonymous reviewer ZIP construction is automated by `scripts/build_anonymous_review_bundle.py`.
- [x] The bundle contains the active anonymous manuscript, C/D-tagged audit source, current D1–D5 derived analyses/controls, current figure data/builders, reusable API/CLI, pinned upstream result summaries/scientific source snapshots, claim/prior-art documents, README and license.
- [x] `scripts/validate_anonymous_review_bundle.py` verifies file hashes, manifest v9 and D3–D5 boundaries, pinned source commits, figure inventory, frozen-two-reason/current-four-reason API boundary and identity leakage.
- [ ] Build the final reviewer ZIP after all author/title-page metadata are known and retain its external receipt SHA-256.
- [ ] Upload that final validated ZIP to the journal's reviewer-only/private location. The public CI artifact is validation only.
- [ ] At acceptance, replace private review locations with a permanent archive carrying a persistent identifier/DOI; do not rely solely on a mutable source-code host.

## Figures

- [x] Quantitative Figure 2–4 component panels and Supplementary Figure S2 have pinned data, a fail-closed validator and a CI smoke-tested builder.
- [x] `scripts/build_mee_composite_figures.py` assembles final Figure 2 (3 panels), Figure 3 (2 panels), Figure 4 (2 panels) and Supplementary Figure S2 directly from the same pinned figure data.
- [x] Figure 2 reader-facing calibration wording is family-conditional; historical `familywise` artifact/data identifiers remain provenance only and are not presented as classical FWER.
- [x] Composite output includes SVG + 300-dpi PNG and a provenance sidecar; no manual data-geometry editing is required.
- [x] Conceptual Figure 1 source is stored as `figures/fig1_tnoa_architecture.svg`.
- [x] Figure 1–4 and Supplementary Figure S2 captions are assembled into the canonical anonymous submission source.
- [ ] Final human visual inspection of Figure 1 and the code-assembled multi-panel figures for typography, label collisions and journal sizing; do not alter data geometry manually.

## References

- [x] Every citation key used by the active MEE submission source resolves in `references.bib`; the current audit reports **24 active-paper entries and zero missing/orphan active citations**.
- [x] **9 entries are prior-art-only rather than active-manuscript citations**. They are intentionally retained because `references.bib` also supports the targeted adversarial prior-art audit; reference-scope CI distinguishes them from orphan entries.
- [x] DOCX conversion renders citations and the References section through Pandoc citeproc using the pinned APA parent CSL recorded in `submission/MEE_FORMATTING_PROVENANCE.md`.
- [ ] Final publisher-style visual inspection of rendered references in the generated DOCX.

## Scientific claim gate

- [x] Final targeted prior-art audit completed.
- [x] Final manuscript claim audit completed for the current working draft.
- [x] C6/C7 + D1/D4 are the primary evidence blocks; C2 is the preregistered negative result; D3/D5 are supporting self-critical controls.
- [x] No field-accuracy, field-prevalence, calibrated-absence, universal-Pi3, classical-FWER, distribution-free-risk, semantic-specific-reason-premium or annotation-efficiency claim is licensed.
- [ ] Re-run claim audit after any material manuscript revision or formatting change that changes text.

## Final upload gate

Do not upload until all unchecked items above that apply to the initial submission have been completed.

## Journal guidance checked

- [x] Live MEE author/scope guidance rechecked on **2026-09-01** before this production sync.

Current guidance supports the present Research Article / Standard Article-scale package: a new ecological method or methodological approach should be central rather than a focal-system result; new computational methods should normally be tested through simulation/benchmarking; broad applicability and usable/open code are expected; a workflow that merely links existing methods is not enough. Initial-submission guidance also calls for a single-column, double-line-spaced manuscript within the journal's approximately 7,000–8,000-word article range/ceiling including references/captions/statements, continuous line and page numbering, a separate title page, a running headline of no more than 45 characters, a numbered 1–4 abstract aiming not to exceed 350 words, at most eight keywords in alphabetical order, anonymized code/data available for peer review and a submission-stage inclusion statement.

Re-check the live author guidance once more immediately before the actual journal upload in case publisher requirements change.
