#!/usr/bin/env python3
"""Build a deterministic double-anonymous reviewer ZIP for TNOA Paper 1.

The bundle is a production artifact only. It does not rerun or replace historical
one-shot scientific generations. It verifies the pinned Source-A target adapter and
three locked Source-B JSON artifacts by Git blob SHA-1, copies a reviewer-facing
scientific source snapshot, redacts identity-bearing owner/email/repository URLs,
and writes a deterministic ZIP plus an external SHA-256 receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

SOURCE_A_COMMIT = "f3b266897f3e9139e6c3fe9ce6b645e25371e092"
SOURCE_A_ADAPTER = "packages/analysis/src/pollipi_analysis/target_evidence.py"
SOURCE_A_ADAPTER_BLOB = "4be5f7c88edda1dda3b62e8a95529386d702bb47"
SOURCE_B_COMMIT = "1664a190cec47142e8d14cc5157302a7af18d019"
LOCKED_B = {
    "benchmarks/v14b_frozen_ternary_phase_figure_data.json": "4c8c2935e61c9266697da315b40f58ba13e89f2c",
    "benchmarks/v14b_frozen_ternary_phase_surface_result.json": "feffae4c9457a9defd4f5b640cda781409a6b4ed",
    "benchmarks/v14b_nuisance_familywise_risk_result.json": "19b7432d0551e2526750f7f6cfa09d07421d7c11",
}

OWNER = "zuizui0223"
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
GITHUB_URL = re.compile(r"https?://(?:raw\.)?github(?:usercontent)?\.com/[^\s)\]>'\"]+", re.I)

TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".json", ".bib", ".svg", ".yml", ".yaml", ".toml", ".csv"
}

TNOA_DOCS = (
    "docs/CONCEPTUAL_FRAMEWORK.md",
    "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md",
    "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/TRANSFERABILITY_TABLE.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md",
    "docs/FIGURE_PLAN.md",
    "docs/FIGURE_VALIDATION.md",
    "docs/METHOD_PAPER_BLUEPRINT.md",
)


def fail(message: str) -> None:
    raise SystemExit(f"anonymous review bundle build failed: {message}")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def sanitize_text(text: str) -> str:
    text = GITHUB_URL.sub("[repository URL withheld for double-anonymous review]", text)
    text = EMAIL.sub("[email withheld]", text)
    text = text.replace(OWNER, "[anonymous-owner]")
    return text


def sanitize_bytes(raw: bytes) -> bytes:
    return sanitize_text(raw.decode("utf-8")).encode("utf-8")


def write_bytes(root: Path, relative: str, raw: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def write_text(root: Path, relative: str, text: str) -> None:
    write_bytes(root, relative, text.encode("utf-8"))


def copy_sanitized(root: Path, source: Path, relative: str) -> None:
    if not source.is_file():
        fail(f"missing source file: {source}")
    raw = source.read_bytes()
    if source.suffix.lower() in TEXT_SUFFIXES:
        raw = sanitize_bytes(raw)
    write_bytes(root, relative, raw)


def identity_scan(root: Path) -> None:
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = path.read_bytes()
        lower = raw.lower()
        if OWNER.encode() in lower:
            fail(f"owner identifier remains in {path.relative_to(root)}")
        if b"github.com/" in lower or b"raw.githubusercontent.com/" in lower:
            fail(f"GitHub URL remains in {path.relative_to(root)}")
        if re.search(rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", raw, re.I):
            fail(f"email address remains in {path.relative_to(root)}")


def neutral_readme() -> str:
    return """# TNOA Paper 1 — anonymous reviewer package

This reviewer package supports scientific review of the closed-world TNOA methods paper without exposing public repository ownership.

## What is included

- anonymous MEE manuscript source;
- C-ID-tagged anonymous audit source used by the claim scanner;
- open-source license and bibliography;
- paper-facing framework, claim-boundary, traceability and figure documents;
- source-guarded figure builder;
- pinned target-observer adapter snapshot (Source A);
- pinned closed-world scientific source snapshot and locked result summaries (Source B);
- bundle manifest with SHA-256 for every included payload file.

## Scientific source identity

Repository locations are withheld for double-anonymous review. The exact scientific provenance is retained through immutable commit hashes, workflow/run identifiers, artifact digests and result hashes. Editors can request the identity crosswalk if required.

## Reproduce the paper figures

Install the figure requirements and run:

```bash
python scripts/build_paper_figures.py --insepi-root source_B --output-dir figures/generated
```

The builder fails unless the three locked JSON files match their registered Git blob SHA-1 values.

## Validate the C-ID audit source

```bash
python scripts/audit_manuscript_claims.py
```

The reviewer manuscript itself has internal C-ID comments removed; the parallel `manuscript/TNOA_P1_DRAFT.md` retains them only for provenance auditing.

## Historical one-shot policy

The full 5.88M-world historical scientific generation is not silently rerun or replaced by this bundle. Its prefrozen protocol, pinned code snapshot, immutable result summaries, artifact/run identifiers and hashes constitute the review record. Later reruns cannot replace that locked result.
"""


def anonymous_manifest() -> dict:
    payload = json.loads((ROOT / "paper_manifest.json").read_text(encoding="utf-8"))
    payload["source_repositories"] = {
        "source_A_target_observer": {
            "repository": "withheld for double-anonymous review",
            "pinned_commit": SOURCE_A_COMMIT,
            "target_evidence_adapter_git_blob_sha1": SOURCE_A_ADAPTER_BLOB,
        },
        "source_B_closed_world": {
            "repository": "withheld for double-anonymous review",
            "pinned_commit": SOURCE_B_COMMIT,
        },
    }
    # Production paths should not imply a public source location.
    payload["scope"] = str(payload.get("scope", "")) + "; public source locations withheld during review"
    return payload


def copy_source_a(stage: Path, root: Path) -> dict:
    path = root / SOURCE_A_ADAPTER
    if not path.is_file():
        fail(f"Source A adapter missing: {path}")
    raw = path.read_bytes()
    blob = git_blob_sha1(raw)
    if blob != SOURCE_A_ADAPTER_BLOB:
        fail(f"Source A adapter blob mismatch: expected {SOURCE_A_ADAPTER_BLOB}, got {blob}")
    write_bytes(stage, "source_A/target_evidence.py", sanitize_bytes(raw))
    return {"commit": SOURCE_A_COMMIT, "adapter_git_blob_sha1": blob}


def copy_source_b(stage: Path, root: Path) -> dict:
    locked_meta: dict[str, dict[str, str]] = {}
    for relative, expected_blob in LOCKED_B.items():
        path = root / relative
        if not path.is_file():
            fail(f"locked Source B file missing: {path}")
        raw = path.read_bytes()
        blob = git_blob_sha1(raw)
        if blob != expected_blob:
            fail(f"Source B locked blob mismatch for {relative}: expected {expected_blob}, got {blob}")
        # These authoritative result summaries are retained byte-identically.
        write_bytes(stage, f"source_B/{relative}", raw)
        locked_meta[relative] = {
            "git_blob_sha1": blob,
            "sha256": hashlib.sha256(raw).hexdigest(),
        }

    # Reviewer-facing scientific code snapshot. Text is anonymized only for owner,
    # email and repository URLs; code/protocol semantics are otherwise retained.
    candidates: set[Path] = set()
    src_dir = root / "src" / "interaction_sensing"
    if src_dir.is_dir():
        candidates.update(src_dir.rglob("*.py"))
    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        candidates.update(p for p in scripts_dir.glob("*.py") if "v14" in p.name.lower())
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        candidates.update(p for p in tests_dir.glob("*.py") if "v14" in p.name.lower())
    bench_dir = root / "benchmarks"
    if bench_dir.is_dir():
        candidates.update(bench_dir.glob("v14*.json"))
    for extra in ("pyproject.toml", "requirements.txt"):
        path = root / extra
        if path.is_file():
            candidates.add(path)

    locked_paths = {root / rel for rel in LOCKED_B}
    snapshot_count = 0
    for path in sorted(candidates):
        if path in locked_paths or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES:
            raw = sanitize_bytes(raw)
        write_bytes(stage, f"source_B/{relative}", raw)
        snapshot_count += 1

    return {
        "commit": SOURCE_B_COMMIT,
        "locked_files": locked_meta,
        "scientific_snapshot_file_count_excluding_locked": snapshot_count,
    }


def build_payload(stage: Path, source_a_root: Path, source_b_root: Path) -> dict:
    # Generate the anonymous reviewer manuscript using the already CI-validated builder.
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_mee_anonymous_manuscript.py")], check=True)
    reviewer_manuscript = ROOT / "submission" / "generated" / "MEE_ANONYMOUS_MANUSCRIPT.md"
    if not reviewer_manuscript.is_file():
        fail("anonymous manuscript builder did not produce expected output")

    write_text(stage, "README.md", neutral_readme())
    copy_sanitized(stage, ROOT / "LICENSE", "LICENSE")
    copy_sanitized(stage, ROOT / "references.bib", "references.bib")
    copy_sanitized(stage, ROOT / "requirements-figures.txt", "requirements-figures.txt")
    copy_sanitized(stage, ROOT / "figures" / "fig1_tnoa_architecture.svg", "figures/fig1_tnoa_architecture.svg")
    copy_sanitized(stage, reviewer_manuscript, "manuscript/MEE_ANONYMOUS_MANUSCRIPT.md")

    # Parallel audit source retains C-ID tags but is otherwise identity-sanitized.
    copy_sanitized(stage, ROOT / "manuscript" / "TNOA_P1_DRAFT.md", "manuscript/TNOA_P1_DRAFT.md")
    copy_sanitized(stage, ROOT / "manuscript" / "TNOA_P1_DRAFT.md", "manuscript/TNOA_P1_AUDIT_SOURCE.md")

    for relative in TNOA_DOCS:
        copy_sanitized(stage, ROOT / relative, relative)
    copy_sanitized(stage, ROOT / "reproduce" / "README.md", "reproduce/README.md")
    for relative in (
        "scripts/build_paper_figures.py",
        "scripts/audit_manuscript_claims.py",
        "scripts/validate_anonymous_review_bundle.py",
    ):
        copy_sanitized(stage, ROOT / relative, relative)

    manifest = anonymous_manifest()
    write_text(stage, "paper_manifest.anonymous.json", json.dumps(manifest, indent=2) + "\n")

    source_a_meta = copy_source_a(stage, source_a_root)
    source_b_meta = copy_source_b(stage, source_b_root)
    return {"A": source_a_meta, "B": source_b_meta}


def deterministic_zip(stage: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            relative = path.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-a-root", type=Path, required=True)
    parser.add_argument("--source-b-root", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "submission" / "generated" / "review_bundle",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="tnoa-review-") as tmp:
        stage = Path(tmp) / "TNOA_P1_ANONYMOUS_REVIEW"
        stage.mkdir(parents=True)
        source_meta = build_payload(stage, args.source_a_root, args.source_b_root)

        identity_scan(stage)
        file_hashes = {
            path.relative_to(stage).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(p for p in stage.rglob("*") if p.is_file())
        }
        bundle_manifest = {
            "schema": "tnoa-anonymous-review-bundle-v1",
            "double_anonymous": True,
            "paper_generation": "TNOA-P1",
            "scientific_claim_boundary_unchanged": True,
            "source_snapshots": source_meta,
            "files": file_hashes,
            "identity_policy": {
                "public_owner_identifier_present": False,
                "email_addresses_present": False,
                "github_urls_present": False,
                "repository_identity_crosswalk_withheld": True,
            },
        }
        write_text(stage, "bundle_manifest.json", json.dumps(bundle_manifest, indent=2) + "\n")
        identity_scan(stage)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        zip_path = args.output_dir / "TNOA_P1_ANONYMOUS_REVIEW_BUNDLE.zip"
        deterministic_zip(stage, zip_path)
        zip_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
        receipt = {
            "schema": "tnoa-anonymous-review-bundle-receipt-v1",
            "zip_file": zip_path.name,
            "zip_sha256": zip_sha,
            "zip_size_bytes": zip_path.stat().st_size,
            "payload_file_count": len(file_hashes),
            "source_A_commit": SOURCE_A_COMMIT,
            "source_B_commit": SOURCE_B_COMMIT,
            "scientific_claim_boundary_unchanged": True,
        }
        receipt_path = args.output_dir / "TNOA_P1_ANONYMOUS_REVIEW_BUNDLE.receipt.json"
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    # Re-open and validate the finished ZIP through the standalone validator.
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_anonymous_review_bundle.py"), str(zip_path)],
        check=True,
    )
    print(f"Built anonymous reviewer bundle: {zip_path}")
    print(f"ZIP SHA-256: {zip_sha}")


if __name__ == "__main__":
    main()
