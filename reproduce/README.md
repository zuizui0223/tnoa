# TNOA Paper-1 reproducibility entry point

TNOA does not rerun locked upstream scientific generations by default. Reproduction is intentionally split into four levels.

## Level 1 — validate the TNOA paper package

From the repository root:

```bash
python scripts/validate_paper_manifest.py
python scripts/validate_mee_synthetic_consequences.py
python scripts/validate_observation_vocabulary_ablation.py
python scripts/validate_structural_axis_audit.py
python scripts/audit_manuscript_claims.py
```

These checks verify that frozen source provenance has not drifted, the post-freeze D1/D2/D3 results remain tied to the immutable V14b surface, D3 remains explicitly literature-audit-motivated and not preregistered, and Paper-1 claim boundaries still forbid field accuracy, formal distribution-free guarantees and primitive-level priority claims.

The same guards run in GitHub Actions.

## Level 2 — verify authoritative external source artifacts

The authoritative frozen scientific results remain in the two pinned source repositories recorded in `paper_manifest.json`. Before final submission packaging:

1. check out the recorded source commits;
2. verify every locked result against its execution commit, artifact digest and result/phase-surface SHA;
3. verify the target-evidence adapter against its pinned Git blob SHA-1;
4. generate manuscript figures only from locked/derived artifacts named in the manifest;
5. do not rerun a historical one-shot generation merely to reproduce a figure if the immutable result artifact already exists.

## Level 3 — reproduce the original MEE post-freeze estimand/weighting audit

Install:

```bash
python -m pip install -r requirements-analysis.txt
```

Download artifact `9593775550` from InsePi workflow `32932634622` and extract `phase_surface.json`. Its SHA-256 must be:

```text
1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34
```

Then run:

```bash
python scripts/analyze_mee_synthetic_consequences.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/mee_synthetic_consequences.json
python scripts/validate_mee_synthetic_consequences.py
```

This derives the original D1 target-prevalence comparison, registered-axis slices and bounded weighting sensitivity. It does not refit observers or change thresholds.

## Level 4 — reproduce the post-freeze observation-vocabulary ablation (D3)

D3 uses the **same immutable phase surface** and 3,003 six-regime simplex mixtures. It was motivated by the expanded prior-art audit after earlier results were inspected, so it is explicitly **not preregistered**.

Run:

```bash
python scripts/analyze_observation_vocabulary_ablation.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/observation_vocabulary_ablation.json
python scripts/validate_observation_vocabulary_ablation.py
```

The analysis compares four nested observation vocabularies across five fixed estimands and all 34 registered single-axis slices. It generates no new synthetic worlds and retunes no observer or threshold. Deterministic never-wider relations are structural; numerical width reductions are post-freeze descriptive results of the frozen emission matrix.

## Reproduction boundary

A rerun and a reproduction are not always the same operation in TNOA. For historical one-shot generations, the scientific record is the prefrozen protocol plus immutable result/receipt. Re-executing a generator under a later runtime may be useful as a software check but must not replace the historical locked result.

Post-freeze derived analyses may transform immutable outputs provided that their source digest, transformation code, temporal status and claim boundary are explicit. D3 therefore remains scientifically usable only with its `post-freeze/not-preregistered` label intact.

## Required final submission bundle

The eventual submission package should contain:

- active manuscript and front matter;
- paper-grade figure scripts and pinned figure data;
- `paper_manifest.json`;
- claim-boundary and claim-traceability documents;
- `derived/mee_synthetic_consequences.json`;
- `derived/structural_axis_audit.json`;
- `derived/observation_vocabulary_ablation.json`;
- expanded prior-art and nearest-neighbour documents;
- `references.bib`;
- release/version identifier and exact source commits/artifact digests.

## Current status

The MEE-focused scientific and reproducibility package is assembled with frozen science, D1/D2 and literature-audit-motivated D3, reusable API/CLI, fail-closed field translation, figures, anonymous DOCX and deterministic reviewer bundle. The expanded prior-art audit explicitly surrenders priority for uncertain ecological observations, continuous-score inference, multilabel abstention, information ordering and partial identification; the residual claim is the tested process-semantic observation contract plus measured information loss under progressive garbling.

Remaining pre-upload work is human-facing: author/title-page metadata, visual inspection, publisher-facing word count, final identity-scanned reviewer ZIP and post-edit audit reruns.
