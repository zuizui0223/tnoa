# Anonymous peer-review code/data package

This document defines the reviewer-facing package for the active MEE-focused TNOA paper. It is intentionally separate from the public source repository so that double-anonymous review does not depend on an author-identifying repository URL.

## Current implementation

The reviewer package is now executable rather than a manual checklist:

- `scripts/build_anonymous_review_bundle.py` builds a deterministic ZIP from the current MEE manuscript/package plus pinned upstream scientific source checkouts;
- `scripts/validate_anonymous_review_bundle.py` verifies the internal hash registry, current MEE schemas, figure count, source commits and recursive identity scan;
- CI checks out the two pinned upstream source commits and builds/validates the ZIP on every relevant pull request;
- the CI artifact is a validation artifact only. The final reviewer ZIP must still be placed in the journal's private/reviewer-only location.

The builder does **not** rerun the frozen 5.88M-world scientific generation.

## Build command

Provide local checkouts at the exact registered commits:

- Source A: `f3b266897f3e9139e6c3fe9ce6b645e25371e092`;
- Source B: `1664a190cec47142e8d14cc5157302a7af18d019`.

Then run:

```bash
python -m pip install -r requirements-figures.txt
python scripts/build_anonymous_review_bundle.py \
  --source-a-root /path/to/source_A \
  --source-b-root /path/to/source_B \
  --output-dir submission/generated/review_bundle
```

Immediately before journal upload, add every author/institution literal that must not survive anonymization:

```bash
python scripts/build_anonymous_review_bundle.py \
  --source-a-root /path/to/source_A \
  --source-b-root /path/to/source_B \
  --forbid-literal "AUTHOR NAME" \
  --forbid-literal "INSTITUTION NAME" \
  --output-dir submission/generated/review_bundle
```

`--forbid-literal` is repeatable. The build fails if a supplied literal survives anywhere in reviewer-facing text.

## Bundle contents

The v2 ZIP contains, at minimum:

```text
README.md
LICENSE
paper_manifest.json
paper_manifest.anonymous.json
references.bib
requirements-figures.txt
requirements-analysis.txt
pyproject.toml
manuscript/
  MEE_ANONYMOUS_MANUSCRIPT.md
  TNOA_MEE_DRAFT.md              # parallel C/D-tagged audit source
docs/
  CONCEPTUAL_FRAMEWORK.md
  CLAIM_BOUNDARY.md
  CLAIM_TRACEABILITY.md
  FIGURE_PLAN.md
  MEE_FIGURE_VALIDATION.md
  MEE_SYNTHETIC_CONSEQUENCES.md
  STRUCTURAL_RESULT_AUDIT.md
  REUSABLE_IMPLEMENTATION.md
  MEE_VOCABULARY_MAP.md
derived/
  mee_figure_data.json
  mee_synthetic_consequences.json
  structural_axis_audit.json
scripts/
  audit_manuscript_claims.py
  validate_mee_figure_data.py
  validate_mee_synthetic_consequences.py
  validate_structural_axis_audit.py
  build_mee_figures.py
  validate_anonymous_review_bundle.py
tnoa/
  __init__.py
  core.py
  cli.py
tests/
  test_minimal_api.py
examples/
  minimal_evidence.csv
figures/
  fig1_tnoa_architecture.svg
  generated/                    # 8 PNG + 8 SVG + figure_provenance.json
source_A/
  target_evidence.py
source_B/
  benchmarks/                   # pinned locked result summaries
  src/, scripts/, tests/        # anonymized scientific source snapshot
bundle_manifest.json
```

The three `derived` files are copied byte-identically from the source-guarded TNOA repository. Pinned Source-B locked result summaries are also copied byte-identically after Git-blob verification. Reviewer-facing source code is sanitized only for identity-bearing owner/email/repository metadata; scientific code and parameter semantics are retained.

## Remove or replace for anonymity

The package must not contain:

- public repository owner/user names;
- author names or initials that reveal identity;
- author email addresses;
- institutional names/addresses;
- ORCID identifiers;
- acknowledgements that identify the authors;
- public GitHub URLs that expose ownership;
- Git commit author metadata exported into the review package.

Repository identities in the anonymous manifest are replaced by neutral `Source A` / `Source B` labels while immutable commits, workflow/run IDs, artifact digests and result hashes are retained.

## Reviewer reproduction targets

The bundle supports three levels of checking without requiring a network connection:

1. **Package integrity and anonymity:** validate the ZIP hash registry and identity scan.
2. **Paper-result validation:** run the three derived-result/figure validators and the manuscript claim scanner.
3. **Figure and API reproduction:** rebuild the MEE figures from the included pinned derived data and run the reusable `tnoa` API tests/CSV example.

The package is not required to reproduce the full historical 5.88M-world computation during routine peer review unless editors specifically request it. That generation remains defined by its prefrozen protocol plus immutable result/receipt and hashes.

## Final pre-upload procedure

1. Complete the separate title page first so the full author/institution literal set is known.
2. Rebuild the bundle with each identifying literal passed through `--forbid-literal`.
3. Confirm the generated `.receipt.json` SHA-256 and ZIP size.
4. Run `scripts/validate_anonymous_review_bundle.py` on the final ZIP.
5. Upload the ZIP only to the private/reviewer-only location required by the journal.

The public CI-generated bundle must not be treated as the final reviewer delivery location.
