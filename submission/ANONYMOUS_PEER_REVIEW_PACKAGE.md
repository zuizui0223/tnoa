# Anonymous peer-review code/data package

This document defines the reviewer-facing package for the active MEE-focused TNOA paper. It is separate from the public source repository so double-anonymous review does not depend on an owner-identifying URL.

## Current implementation

- `scripts/build_anonymous_review_bundle.py` builds a deterministic ZIP from the current manuscript/package and pinned upstream checkouts.
- `scripts/validate_anonymous_review_bundle.py` verifies the internal hash registry, manifest v9, D3–D5 boundaries, figure count, source commits and recursive identity scan.
- CI builds and validates the ZIP on every relevant pull request.
- The CI artifact is validation only; the final ZIP must be uploaded to the journal's private/reviewer-only location.
- The builder does not rerun the frozen 5.88M-world generation.

D3, D4 and D5 are all post-freeze and not preregistered. D5 is the explicit control preventing D3's extra narrowing from being interpreted as a semantic-specific reason-information premium.

## Build

Pinned source checkouts:

- Source A: `f3b266897f3e9139e6c3fe9ce6b645e25371e092`;
- Source B: `1664a190cec47142e8d14cc5157302a7af18d019`.

```bash
python -m pip install -r requirements-figures.txt
python scripts/build_anonymous_review_bundle.py \
  --source-a-root /path/to/source_A \
  --source-b-root /path/to/source_B \
  --output-dir submission/generated/review_bundle
```

Immediately before journal upload, pass every author/institution literal through the repeatable `--forbid-literal` option. The build fails if a supplied literal survives anywhere in reviewer-facing text.

## Scientific materials included

The ZIP contains the anonymous manuscript plus a C/D-tagged audit source, `paper_manifest.json`, references, figure data/builders, the reusable API/CLI, pinned source snapshots and all current derived controls. In particular it includes:

```text
derived/mee_figure_data.json
scripts/validate_mee_figure_data.py
scripts/build_mee_figures.py
scripts/build_anonymous_review_bundle.py
scripts/validate_anonymous_review_bundle.py
docs/OBSERVATION_VOCABULARY_ABLATION.md
docs/PREVALENCE_WEIGHTING_SENSITIVITY.md
docs/REASON_SPLIT_SPECIFICITY_CONTROL.md
docs/REUSABLE_IMPLEMENTATION.md
derived/observation_vocabulary_ablation.json
derived/prevalence_weighting_sensitivity.json
derived/reason_split_specificity_control.json
scripts/analyze_observation_vocabulary_ablation.py
scripts/validate_observation_vocabulary_ablation.py
scripts/analyze_prevalence_weighting_sensitivity.py
scripts/validate_prevalence_weighting_sensitivity.py
scripts/analyze_reason_split_specificity_control.py
scripts/validate_reason_split_specificity_control.py
```

The derived JSON files are copied byte-identically. Reviewer-facing source is sanitized only for identity-bearing metadata; scientific semantics are retained.

## Reviewer reproduction targets

1. **Package/anonymity:** validate ZIP hashes and identity scan.
2. **Primary science:** validate C6/C7 provenance and D1/D4 information-loss results.
3. **Self-critical refinement control:** validate D3 and then D5. D5 must reproduce target-prevalence random two-way median `0.0050075`, `48.0%` random equal-or-better fraction and the full-rank three-way control.
4. **Reason-vocabulary boundary:** inspect `docs/REUSABLE_IMPLEMENTATION.md`; the frozen surface has two U reason buckets while the current API exposes four, with no one-to-one four-way empirical validation claimed.
5. **Figures/API:** rebuild figures and run API/CLI tests.

The D4/D5 files also expose current limitations: the information comparisons condition on a frozen effectively known emission map and do not establish information per annotation/cost, and D3 does not isolate a semantic-specific advantage of the frozen reason labels.

## Anonymity rules

The reviewer package must not contain author names, emails, institutions, ORCIDs, acknowledgements revealing identity, owner-identifying public repository URLs or commit-author metadata. Neutral Source A / Source B labels replace repository identities while immutable commits, workflow IDs, digests and result hashes remain.

## Final pre-upload procedure

1. Complete the separate title page so all author/institution literals are known.
2. Rebuild with each literal supplied via `--forbid-literal`.
3. Verify the receipt SHA-256.
4. Run `scripts/validate_anonymous_review_bundle.py` on the final ZIP.
5. Upload only to the journal's reviewer-only/private location.

The public CI-generated bundle is not the final delivery location.
