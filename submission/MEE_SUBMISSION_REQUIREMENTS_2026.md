# Methods in Ecology and Evolution submission requirements — checked 2026-08-27

Authoritative sources checked for the current TNOA Paper-1 packaging:

- Author Guidelines: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/author-guidelines
- Aims and Scope: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/aims-and-scope/read-full-aims-and-scope
- Code policy: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/policyonpublishingcode.html

## Research Article fit

Current guidance states that Research Articles describe new methods in ecology and evolution and how they may be used. New computational methods normally should be tested using simulations or benchmark datasets. The journal prioritises methods that are broadly applicable across taxa or systems and generally does not treat a workflow that merely links existing methods as a new method.

TNOA therefore remains positioned as a new sensor-decision architecture plus its tested closed-world decision geometry, not as a workflow combining PolliPi and InsePi.

## Initial-submission structure

The current checklist requires:

- single-column manuscript;
- double line spacing;
- continuous line and page numbering;
- approximately 7,000–8,000 words maximum for a Research Article, including references, tables, figure captions and statements;
- separate title-page file;
- abstract numbered 1–4 and normally no more than 350 words;
- Data/Code for peer review statement;
- Keywords;
- Introduction;
- Materials and Methods;
- Results;
- Discussion;
- Figures and Tables with captions.

The main text and supporting information should avoid obvious author identification. Author names, affiliations, acknowledgements and contribution statements belong in the separate title page.

## Code/data requirement

Code and/or data must be available for peer review, either uploaded for reviewers or supplied through a suitable private peer-review repository/link. Code submitted with the paper must carry an open-source software licence. TNOA therefore uses the MIT licence in the repository.

For blinded review, the public repository URL should not be inserted into the anonymised manuscript if it identifies the authors. Use the journal's peer-review code/data mechanism or an anonymised/private reviewer link.

## TNOA package mapping

| MEE requirement | TNOA file/status |
| --- | --- |
| Research Article method | `manuscript/TNOA_P1_DRAFT.md` |
| numbered 1–4 abstract | `submission/MEE_ABSTRACT_AND_STATEMENTS.md` |
| title page | `submission/MEE_TITLE_PAGE_TEMPLATE.md` |
| data/code statement | `submission/MEE_ABSTRACT_AND_STATEMENTS.md` |
| open-source licence | `LICENSE` |
| paper provenance | `paper_manifest.json` |
| claim audit | `docs/FINAL_CLAIM_AUDIT.md` |
| prior-art boundary | `docs/FINAL_PRIOR_ART_AUDIT.md` |
| quantitative figures | `scripts/build_paper_figures.py`, `docs/FIGURE_PLAN.md` |
| conceptual Figure 1 | `figures/fig1_tnoa_architecture.svg` |

## Remaining non-scientific upload tasks

- fill author names, affiliations and correspondence metadata;
- fill acknowledgements, contributions and conflict statement;
- place final anonymised peer-review code/data link;
- convert Markdown to a double-spaced line-numbered submission document;
- perform a final word-count and reference-style pass;
- rerun the claim audit after any substantive manuscript editing.
