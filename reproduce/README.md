# TNOA Paper-1 reproducibility entry point

TNOA does not rerun locked PolliPi/InsePi scientific generations by default. Reproduction is intentionally split into three levels.

## Level 1 — validate the TNOA paper package

From the TNOA repository root:

```bash
python scripts/validate_paper_manifest.py
python scripts/validate_mee_synthetic_consequences.py
```

These checks verify that:

- required paper/provenance files exist;
- source commits and hashes have valid forms;
- all required locked result IDs are represented;
- the final 30,625-coordinate / 5,880,000-world summary has not drifted;
- the post-freeze MEE ecological-estimand result remains pinned to the immutable V14b surface SHA;
- Paper-1 claim boundaries still forbid field accuracy, field absence certification, a universal Pi3 law and universal optimal abstention;
- the literature evidence map is explicitly labeled as an initial/targeted evidence map rather than a systematic review.

The same guards run in GitHub Actions.

## Level 2 — verify authoritative external source artifacts

The authoritative frozen scientific results remain in:

- `zuizui0223/insepi`;
- `zuizui0223/pollipi` for the portable direct target-evidence contract.

Before final submission packaging:

1. clone both source repositories;
2. check out the commits recorded in `paper_manifest.json` for source-interface provenance;
3. verify each locked InsePi result against the execution commit, artifact digest and result/phase-surface SHA listed in the manifest;
4. verify the PolliPi target-evidence adapter against the pinned Git blob SHA-1;
5. generate manuscript figures only from the locked/derived artifacts named in the manifest;
6. do not rerun a historical one-shot generation merely to reproduce a figure if the immutable result artifact already exists.

## Level 3 — reproduce the MEE post-freeze derivation

The new ecological-estimand and weighting audit is a deterministic transformation of the immutable full V14b surface, not a new observer generation.

Install the analysis dependencies:

```bash
python -m pip install -r requirements-analysis.txt
```

Download GitHub Actions artifact `9593775550` from InsePi workflow `32932634622` and extract `phase_surface.json`. Before analysis its SHA-256 must be:

```text
1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34
```

Then run:

```bash
python scripts/analyze_mee_synthetic_consequences.py \
  --phase-surface /path/to/phase_surface.json \
  --output derived/mee_synthetic_consequences.json
```

The script fails closed on a source-SHA or surface-dimension mismatch. It derives:

- synthetic target-prevalence bias after forced binary collapse;
- B/T/N/U versus binary partial-identification widths over the six-regime simplex;
- registered-axis slice sensitivity;
- density-ratio weighting sensitivity for U composition, Pi1 monotonicity and the Pi2 local contrast.

It does **not** refit target/nuisance observers, change alpha, alter the registered grid or replace the frozen V14b result.

## Reproduction boundary

A rerun and a reproduction are not always the same operation in TNOA.

For historical one-shot generations, the scientific record is the prefrozen protocol plus immutable result/receipt. Re-executing the generator under a later software/runtime environment may be useful as a software check, but it must not replace the historical locked result.

Post-freeze derived analyses may transform immutable outputs provided that their source digest, transformation code and claim boundary are recorded explicitly.

## Required final submission bundle

The eventual submission tag should contain:

- manuscript source;
- paper-grade figure scripts;
- figure/table manifest mapping each output to locked or explicitly derived result IDs;
- `paper_manifest.json`;
- `docs/CLAIM_TRACEABILITY.md`;
- `derived/mee_synthetic_consequences.json`;
- `references.bib`;
- a release/version identifier for TNOA;
- exact source repository commits/artifact digests used for every figure and table.

## Current status

The frozen scientific source stack, quantitative figure builder, claim guards and post-freeze MEE ecological-estimand/weighting analysis are implemented. Remaining MEE-specific work is to package a minimal reusable user-facing implementation, translate manuscript terminology toward ecological observation-model language, and integrate the new estimand result into the main figure/manuscript order.
