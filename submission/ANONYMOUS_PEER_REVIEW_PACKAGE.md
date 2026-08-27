# Anonymous peer-review code/data package

This document defines the reviewer-facing package for TNOA Paper 1. It is intentionally separate from the public source repository so that double-anonymous review does not depend on an author-identifying repository URL.

## Include

Create a reviewer ZIP/private archive containing, at minimum:

```text
README.md
LICENSE
paper_manifest.anonymous.json
references.bib
manuscript/
  MEE_ANONYMOUS_MANUSCRIPT.*
docs/
  CONCEPTUAL_FRAMEWORK.md
  CLAIM_BOUNDARY.md
  CLAIM_TRACEABILITY_ANONYMOUS.md
  FIGURE_PLAN.md
  MEE_FIGURE_VALIDATION.md
derived/
  mee_figure_data.json
  mee_synthetic_consequences.json
  structural_axis_audit.json
reproduce/
  README_ANONYMOUS.md
scripts/
  validate_paper_manifest.py
  audit_manuscript_claims.py
  validate_mee_figure_data.py
  validate_mee_synthetic_consequences.py
  validate_structural_axis_audit.py
  build_mee_figures.py
figures/
  submission figure files
```

The three `derived` files must be byte-identical to the source-guarded repository versions. Their provenance records the immutable upstream workflow, artifact and result hashes. Do not rebuild the 5.88M-world scientific generation simply to create the reviewer package.

## Remove or replace for anonymity

Before upload, the reviewer package must not contain:

- public repository owner/user names;
- author names or initials that reveal identity;
- author email addresses;
- institutional names/addresses;
- ORCID identifiers;
- acknowledgements that identify the authors;
- public GitHub URLs that expose ownership;
- Git commit author metadata exported into the review package.

Repository identifiers in prose should be replaced with neutral labels such as `Source repository A (target observer implementation)` and `Source repository B (closed-world implementation/provenance)` where the identity is not needed for scientific review.

## Preserve despite anonymization

Do not anonymize away scientific provenance. Retain:

- workflow/run IDs where they do not identify an author;
- execution/result hashes;
- artifact digests;
- phase-surface SHA-256;
- exact locked numerical results;
- failed-generation status and claim boundaries;
- code and parameter semantics.

If a particular external identifier would expose authorship, map it to a neutral reviewer-package identifier while retaining an internal crosswalk outside the anonymous package.

## Reviewer reproduction target

The reviewer package should support two levels of checking:

1. **Paper-package validation:** validate manifest structure, claim boundaries, source hashes and manuscript provenance tags without network access.
2. **Figure reproduction:** regenerate the quantitative figures from the included locked JSON sources without refitting observers or rerunning historical one-shot experiments.

The package is not required to reproduce the full historical 5.88M-world computation during routine peer review unless editors specifically request it; the scientific record for that one-shot generation is the prefrozen protocol plus immutable result/receipt and hashes.

## Final pre-upload anonymity scan

Search the entire reviewer directory recursively for:

- the public repository owner's username;
- `github.com/` URLs;
- email-address patterns;
- author/institution strings supplied on the separate title page.

Any match must be reviewed before upload. Generic references to GitHub as a software platform are acceptable only if they do not expose ownership.
