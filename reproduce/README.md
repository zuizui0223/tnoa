# TNOA Paper-1 reproducibility entry point

TNOA does not rerun locked PolliPi/InsePi scientific generations by default. Reproduction is intentionally split into two levels.

## Level 1 — validate the TNOA paper package

From the TNOA repository root:

```bash
python scripts/validate_paper_manifest.py
```

This verifies that:

- required paper/provenance files exist;
- source commits and hashes have valid forms;
- all required locked result IDs are represented;
- the final 30,625-coordinate / 5,880,000-world summary has not drifted;
- Paper-1 claim boundaries still forbid field accuracy, field absence certification, a universal Pi3 law and universal optimal abstention;
- the literature evidence map is explicitly labeled as an initial evidence map rather than a systematic review.

The same check runs in GitHub Actions.

## Level 2 — verify authoritative external source artifacts

The authoritative scientific results remain in:

- `zuizui0223/insepi`;
- `zuizui0223/pollipi` for the portable direct target-evidence contract.

Before final submission packaging:

1. clone both source repositories;
2. check out the commits recorded in `paper_manifest.json` for source-interface provenance;
3. verify each locked InsePi result against the execution commit, artifact digest and result/phase-surface SHA listed in the manifest;
4. verify the PolliPi target-evidence adapter against the pinned Git blob SHA-1;
5. generate manuscript figures only from the locked artifacts named in `paper_manifest.json`;
6. do not rerun a historical one-shot generation merely to reproduce a figure if the immutable result artifact already exists.

## Reproduction boundary

A rerun and a reproduction are not always the same operation in TNOA.

For historical one-shot generations, the scientific record is the prefrozen protocol plus immutable result/receipt. Re-executing the generator under a later software/runtime environment may be useful as a software check, but it must not replace the historical locked result.

## Required final submission bundle

The eventual submission tag should contain:

- manuscript source;
- paper-grade figure scripts;
- figure/table manifest mapping each output to locked result IDs;
- `paper_manifest.json`;
- `docs/CLAIM_TRACEABILITY.md`;
- `references.bib`;
- a release/version identifier for TNOA;
- exact source repository commits used for every figure/table.

## Current status

The repository-level manifest validator and claim traceability are implemented. Paper-grade figure generation and the final external source-verification pass remain before submission.
