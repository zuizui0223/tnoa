#!/usr/bin/env python3
"""Build a deterministic double-anonymous reviewer ZIP for the active TNOA MEE paper.

This is a production/review artifact. It does not rerun or replace the frozen
scientific generations. It verifies pinned upstream source checkouts, retains the
current MEE manuscript/derived analyses/figure package and reusable API, removes
identity-bearing repository metadata, and writes a deterministic ZIP plus receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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
    "benchmarks/v14b_nuisance_observer_process_scale_validation_v1_result.json": "589225b146c6466fabafe6f8503995a5861ddece",
    "benchmarks/v14b_nuisance_risk_calibration_v1_result.json": "d29407b18382b63424c296e2dadb6aad38015c8c",
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
    "docs/REVIEWER_ATTACK_MATRIX.md",
    "docs/TRANSFERABILITY_TABLE.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md",
    "docs/FIGURE_PLAN.md",
    "docs/MEE_FIGURE_VALIDATION.md",
    "docs/MEE_SYNTHETIC_CONSEQUENCES.md",
    "docs/STRUCTURAL_RESULT_AUDIT.md",
    "docs/REUSABLE_IMPLEMENTATION.md",
    "docs/MEE_VOCABULARY_MAP.md",
)

DERIVED = (
    "derived/mee_figure_data.json",
    "derived/mee_synthetic_consequences.json",
    "derived/structural_axis_audit.json",
)

TNOA_SCRIPTS = (
    "scripts/audit_manuscript_claims.py",
    "scripts/validate_mee_figure_data.py",
    "scripts/validate_mee_synthetic_consequences.py",
    "scripts/validate_structural_axis_audit.py",
    "scripts/build_mee_figures.py",
    "scripts/analyze_mee_synthetic_consequences.py",
    "scripts/analyze_structural_axis_audit.py",
    "scripts/validate_anonymous_review_bundle.py",
)


def fail(message: str) -> None:
    raise SystemExit(f"anonymous review bundle build failed: {message}")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(f"cannot verify pinned checkout at {root}: {exc}")


def verify_checkout(root: Path, expected: str, label: str) -> None:
    if not root.is_dir():
        fail(f"{label} checkout missing: {root}")
    actual = git_head(root)
    if actual != expected:
        fail(f"{label} checkout drifted: expected {expected}, got {actual}")


def sanitize_text(text: str, extra_literals: tuple[str, ...]) -> str:
    text = GITHUB_URL.sub("[repository URL withheld for double-anonymous review]", text)
    text = EMAIL.sub("[email withheld]", text)
    text = text.replace(OWNER, "[anonymous-owner]")
    for literal in extra_literals:
        if literal:
            text = re.sub(re.escape(literal), "[identity withheld]", text, flags=re.I)
    return text


def sanitized_bytes(raw: bytes, extra_literals: tuple[str, ...]) -> bytes:
    return sanitize_text(raw.decode("utf-8"), extra_literals).encode("utf-8")


def write_bytes(root: Path, relative: str, raw: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def write_text(root: Path, relative: str, text: str) -> None:
    write_bytes(root, relative, text.encode("utf-8"))


def copy_sanitized(stage: Path, source: Path, relative: str, extra_literals: tuple[str, ...]) -> None:
    if not source.is_file():
        fail(f"missing source file: {source}")
    raw = source.read_bytes()
    if source.suffix.lower() in TEXT_SUFFIXES:
        raw = sanitized_bytes(raw, extra_literals)
    write_bytes(stage, relative, raw)


def copy_exact(stage: Path, source: Path, relative: str) -> None:
    if not source.is_file():
        fail(f"missing exact source file: {source}")
    write_bytes(stage, relative, source.read_bytes())


def identity_scan(root: Path, extra_literals: tuple[str, ...]) -> None:
    forbidden = [OWNER.lower(), "github.com/", "raw.githubusercontent.com/"]
    forbidden.extend(x.lower() for x in extra_literals if x)
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        lower = text.lower()
        for token in forbidden:
            if token in lower:
                fail(f"identity-bearing token {token!r} remains in {path.relative_to(root)}")
        if EMAIL.search(text):
            fail(f"email address remains in {path.relative_to(root)}")


def neutral_readme() -> str:
    return """# TNOA — anonymous reviewer package

This package supports double-anonymous review of the active MEE-focused TNOA methods paper.
Public repository ownership is withheld; immutable scientific run IDs, hashes and artifact digests are retained.

## Included review targets

- anonymous numbered-abstract manuscript plus a parallel C/D-tagged audit source;
- current claim, framework, figure, robustness and implementation documentation;
- byte-identical post-freeze derived JSON used by the MEE manuscript;
- source-guarded MEE figure data/builder and generated reviewer figures;
- minimal reusable `tnoa` Python API/CLI example;
- pinned target-observer adapter (Source A);
- pinned closed-world result summaries and anonymized scientific source snapshot (Source B);
- deterministic bundle manifest and external ZIP receipt.

## Fast checks

```bash
python scripts/validate_mee_synthetic_consequences.py
python scripts/validate_structural_axis_audit.py
python scripts/validate_mee_figure_data.py
python scripts/audit_manuscript_claims.py
python -m unittest discover -s tests -p 'test_*.py'
```

Rebuild the quantitative panels with:

```bash
python -m pip install -r requirements-figures.txt
python scripts/build_mee_figures.py --output-dir figures/rebuilt
```

The historical full phase-surface generation is intentionally not rerun for routine peer review. Its frozen protocol/results and immutable provenance define that scientific record.
"""


def anonymous_manifest(extra_literals: tuple[str, ...]) -> dict:
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
    payload["scope"] = str(payload.get("scope", "")) + "; public source locations withheld during review"
    # Round-trip through the same sanitizer so future identity-bearing prose cannot leak.
    return json.loads(sanitize_text(json.dumps(payload), extra_literals))


def copy_source_a(stage: Path, root: Path, extra_literals: tuple[str, ...]) -> dict:
    path = root / SOURCE_A_ADAPTER
    raw = path.read_bytes()
    blob = git_blob_sha1(raw)
    if blob != SOURCE_A_ADAPTER_BLOB:
        fail(f"Source A adapter blob mismatch: expected {SOURCE_A_ADAPTER_BLOB}, got {blob}")
    write_bytes(stage, "source_A/target_evidence.py", sanitized_bytes(raw, extra_literals))
    return {"commit": SOURCE_A_COMMIT, "adapter_git_blob_sha1": blob}


def copy_source_b(stage: Path, root: Path, extra_literals: tuple[str, ...]) -> dict:
    locked_meta: dict[str, dict[str, str]] = {}
    locked_paths: set[Path] = set()
    for relative, expected_blob in LOCKED_B.items():
        path = root / relative
        raw = path.read_bytes()
        blob = git_blob_sha1(raw)
        if blob != expected_blob:
            fail(f"Source B locked blob mismatch for {relative}: expected {expected_blob}, got {blob}")
        write_bytes(stage, f"source_B/{relative}", raw)
        locked_paths.add(path)
        locked_meta[relative] = {"git_blob_sha1": blob, "sha256": sha256(raw)}

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
        p = root / extra
        if p.is_file():
            candidates.add(p)

    snapshot_count = 0
    for path in sorted(candidates):
        if path in locked_paths or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES:
            raw = sanitized_bytes(raw, extra_literals)
        write_bytes(stage, f"source_B/{relative}", raw)
        snapshot_count += 1

    return {
        "commit": SOURCE_B_COMMIT,
        "locked_files": locked_meta,
        "scientific_snapshot_file_count_excluding_locked": snapshot_count,
    }


def generate_review_figures(stage: Path) -> None:
    output = stage / "figures" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = "315532800"  # 1980-01-01 for stable SVG metadata where supported.
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_mee_figures.py"), "--output-dir", str(output)],
        check=True,
        env=env,
    )
    png = sorted(output.glob("*.png"))
    svg = sorted(output.glob("*.svg"))
    if len(png) != 8 or len(svg) != 8 or not (output / "figure_provenance.json").is_file():
        fail("MEE figure builder did not produce the expected 8 PNG + 8 SVG + provenance files")
    # Matplotlib SVG may retain a date element; normalize it for deterministic bundle bytes.
    for path in svg:
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"<dc:date>.*?</dc:date>", "<dc:date>1980-01-01T00:00:00</dc:date>", text)
        path.write_text(text, encoding="utf-8")


def build_payload(stage: Path, source_a_root: Path, source_b_root: Path, extra_literals: tuple[str, ...]) -> dict:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_mee_anonymous_manuscript.py")], check=True)
    reviewer_manuscript = ROOT / "submission" / "generated" / "MEE_ANONYMOUS_MANUSCRIPT.md"
    if not reviewer_manuscript.is_file():
        fail("anonymous manuscript builder did not produce expected output")

    write_text(stage, "README.md", neutral_readme())
    for relative in ("LICENSE", "references.bib", "requirements-figures.txt", "requirements-analysis.txt", "pyproject.toml"):
        copy_sanitized(stage, ROOT / relative, relative, extra_literals)
    copy_sanitized(stage, ROOT / "figures" / "fig1_tnoa_architecture.svg", "figures/fig1_tnoa_architecture.svg", extra_literals)
    copy_sanitized(stage, reviewer_manuscript, "manuscript/MEE_ANONYMOUS_MANUSCRIPT.md", extra_literals)
    copy_sanitized(stage, ROOT / "manuscript" / "TNOA_MEE_DRAFT.md", "manuscript/TNOA_MEE_DRAFT.md", extra_literals)

    for relative in TNOA_DOCS:
        copy_sanitized(stage, ROOT / relative, relative, extra_literals)
    copy_sanitized(stage, ROOT / "reproduce" / "README.md", "reproduce/README_ANONYMOUS.md", extra_literals)
    for relative in DERIVED:
        copy_exact(stage, ROOT / relative, relative)
    for relative in TNOA_SCRIPTS:
        copy_sanitized(stage, ROOT / relative, relative, extra_literals)
    for relative in ("tnoa/__init__.py", "tnoa/core.py", "tnoa/cli.py", "tests/test_minimal_api.py", "examples/minimal_evidence.csv"):
        copy_sanitized(stage, ROOT / relative, relative, extra_literals)

    manifest = anonymous_manifest(extra_literals)
    write_text(stage, "paper_manifest.json", json.dumps(manifest, indent=2) + "\n")
    write_text(stage, "paper_manifest.anonymous.json", json.dumps(manifest, indent=2) + "\n")

    generate_review_figures(stage)
    source_a_meta = copy_source_a(stage, source_a_root, extra_literals)
    source_b_meta = copy_source_b(stage, source_b_root, extra_literals)
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
    parser.add_argument("--forbid-literal", action="append", default=[], help="Additional author/institution literal to remove and reject (repeatable)")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "submission" / "generated" / "review_bundle")
    args = parser.parse_args()
    extra_literals = tuple(x.strip() for x in args.forbid_literal if x.strip())

    verify_checkout(args.source_a_root, SOURCE_A_COMMIT, "Source A")
    verify_checkout(args.source_b_root, SOURCE_B_COMMIT, "Source B")

    with tempfile.TemporaryDirectory(prefix="tnoa-review-") as tmp:
        stage = Path(tmp) / "TNOA_MEE_ANONYMOUS_REVIEW"
        stage.mkdir(parents=True)
        source_meta = build_payload(stage, args.source_a_root, args.source_b_root, extra_literals)
        identity_scan(stage, extra_literals)

        file_hashes = {
            path.relative_to(stage).as_posix(): sha256(path.read_bytes())
            for path in sorted(p for p in stage.rglob("*") if p.is_file())
        }
        bundle_manifest = {
            "schema": "tnoa-anonymous-review-bundle-v2",
            "double_anonymous": True,
            "paper_generation": "TNOA-P1-MEE",
            "scientific_claim_boundary_unchanged": True,
            "source_snapshots": source_meta,
            "files": file_hashes,
            "identity_policy": {
                "public_owner_identifier_present": False,
                "email_addresses_present": False,
                "github_urls_present": False,
                "additional_forbidden_literals": len(extra_literals),
                "repository_identity_crosswalk_withheld": True,
            },
        }
        write_text(stage, "bundle_manifest.json", json.dumps(bundle_manifest, indent=2) + "\n")
        identity_scan(stage, extra_literals)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        zip_path = args.output_dir / "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.zip"
        deterministic_zip(stage, zip_path)
        zip_sha = sha256(zip_path.read_bytes())
        receipt = {
            "schema": "tnoa-anonymous-review-bundle-receipt-v2",
            "zip_file": zip_path.name,
            "zip_sha256": zip_sha,
            "zip_size_bytes": zip_path.stat().st_size,
            "payload_file_count": len(file_hashes),
            "source_A_commit": SOURCE_A_COMMIT,
            "source_B_commit": SOURCE_B_COMMIT,
            "paper_generation": "TNOA-P1-MEE",
            "scientific_claim_boundary_unchanged": True,
        }
        receipt_path = args.output_dir / "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.receipt.json"
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    cmd = [sys.executable, str(ROOT / "scripts" / "validate_anonymous_review_bundle.py"), str(zip_path)]
    for literal in extra_literals:
        cmd.extend(["--forbid-literal", literal])
    subprocess.run(cmd, check=True)
    print(f"Built anonymous reviewer bundle: {zip_path}")
    print(f"ZIP SHA-256: {zip_sha}")


if __name__ == "__main__":
    main()
