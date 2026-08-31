#!/usr/bin/env python3
"""Build deterministic double-anonymous reviewer ZIP for active TNOA MEE paper.

The builder verifies pinned upstream checkouts and source blobs, copies the
current manuscript/derived analyses/reusable implementation, sanitizes public
identity-bearing text, generates reviewer figures, and writes a deterministic
ZIP plus an external SHA-256 receipt. It never reruns frozen scientific worlds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
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
TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".bib", ".svg", ".yml", ".yaml", ".toml", ".csv"}

TNOA_DOCS = (
    "docs/CONCEPTUAL_FRAMEWORK.md", "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md", "docs/FINAL_PRIOR_ART_AUDIT.md",
    "docs/NEAREST_NEIGHBOUR_METHODS.md", "docs/REVIEWER_ATTACK_MATRIX.md",
    "docs/TRANSFERABILITY_TABLE.md", "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md", "docs/FIGURE_PLAN.md",
    "docs/MEE_FIGURE_VALIDATION.md", "docs/MEE_SYNTHETIC_CONSEQUENCES.md",
    "docs/STRUCTURAL_RESULT_AUDIT.md", "docs/OBSERVATION_VOCABULARY_ABLATION.md",
    "docs/PREVALENCE_WEIGHTING_SENSITIVITY.md", "docs/REUSABLE_IMPLEMENTATION.md",
    "docs/FIELD_TRANSLATION_PATHWAY.md", "docs/MEE_VOCABULARY_MAP.md",
)
DERIVED = (
    "derived/mee_figure_data.json", "derived/mee_synthetic_consequences.json",
    "derived/structural_axis_audit.json", "derived/observation_vocabulary_ablation.json",
    "derived/prevalence_weighting_sensitivity.json",
)
TNOA_SCRIPTS = (
    "scripts/audit_manuscript_claims.py", "scripts/validate_mee_figure_data.py",
    "scripts/validate_mee_synthetic_consequences.py", "scripts/validate_structural_axis_audit.py",
    "scripts/validate_observation_vocabulary_ablation.py", "scripts/validate_prevalence_weighting_sensitivity.py",
    "scripts/build_mee_figures.py", "scripts/analyze_mee_synthetic_consequences.py",
    "scripts/analyze_structural_axis_audit.py", "scripts/analyze_observation_vocabulary_ablation.py",
    "scripts/analyze_prevalence_weighting_sensitivity.py", "scripts/validate_anonymous_review_bundle.py",
)


def fail(message: str) -> None:
    raise SystemExit(f"anonymous review bundle build failed: {message}")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception as exc:
        fail(f"cannot verify pinned checkout at {root}: {exc}")


def verify_checkout(root: Path, expected: str, label: str) -> None:
    if not root.is_dir():
        fail(f"{label} checkout missing: {root}")
    actual = git_head(root)
    if actual != expected:
        fail(f"{label} checkout drifted: expected {expected}, got {actual}")


def sanitize_text(text: str, literals: tuple[str, ...]) -> str:
    text = GITHUB_URL.sub("[repository URL withheld for double-anonymous review]", text)
    text = EMAIL.sub("[email withheld]", text)
    text = text.replace(OWNER, "[anonymous-owner]")
    for literal in literals:
        if literal:
            text = re.sub(re.escape(literal), "[identity withheld]", text, flags=re.I)
    return text


def write_bytes(stage: Path, relative: str, raw: bytes) -> None:
    path = stage / PurePosixPath(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def write_text(stage: Path, relative: str, text: str) -> None:
    write_bytes(stage, relative, text.encode("utf-8"))


def copy_repo_file(stage: Path, relative: str, literals: tuple[str, ...], exact: bool = False) -> None:
    source = ROOT / relative
    if not source.is_file():
        fail(f"missing repository source file: {relative}")
    raw = source.read_bytes()
    if not exact and source.suffix.lower() in TEXT_SUFFIXES:
        raw = sanitize_text(raw.decode("utf-8"), literals).encode("utf-8")
    write_bytes(stage, relative, raw)


def anonymous_paper_manifest(literals: tuple[str, ...]) -> dict:
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
    return json.loads(sanitize_text(json.dumps(payload), literals))


def neutral_readme() -> str:
    return """# TNOA — anonymous reviewer package

This package supports double-anonymous review of the active MEE-focused TNOA methods paper. Public repository ownership is withheld; immutable scientific run IDs, hashes and artifact digests are retained.

Included materials cover the anonymous manuscript, a parallel C/D-tagged audit source, expanded nearest-neighbour prior-art positioning, frozen/post-freeze derived analyses including the explicitly non-preregistered D3 observation-vocabulary ablation and D4 prevalence/composition-weight sensitivity, reproducible figure inputs/builders, and the minimal reusable API/CLI.

Fast checks:

```bash
python scripts/validate_mee_synthetic_consequences.py
python scripts/validate_observation_vocabulary_ablation.py
python scripts/validate_prevalence_weighting_sensitivity.py
python scripts/validate_structural_axis_audit.py
python scripts/validate_mee_figure_data.py
python scripts/audit_manuscript_claims.py
python -m unittest discover -s tests -p 'test_*.py'
```

The historical full phase-surface generation is intentionally not rerun for routine peer review. D3 and D4 are deterministic post-freeze transformations/sensitivity analyses of the immutable surface and are explicitly not preregistered.
"""


def copy_source_a(stage: Path, root: Path, literals: tuple[str, ...]) -> dict:
    path = root / SOURCE_A_ADAPTER
    if not path.is_file():
        fail("Source A adapter missing")
    raw = path.read_bytes()
    blob = git_blob_sha1(raw)
    if blob != SOURCE_A_ADAPTER_BLOB:
        fail(f"Source A adapter blob mismatch: expected {SOURCE_A_ADAPTER_BLOB}, got {blob}")
    write_bytes(stage, "source_A/target_evidence.py", sanitize_text(raw.decode("utf-8"), literals).encode("utf-8"))
    return {"commit": SOURCE_A_COMMIT, "adapter_git_blob_sha1": blob}


def copy_source_b(stage: Path, root: Path, literals: tuple[str, ...]) -> dict:
    locked_meta: dict[str, dict[str, str]] = {}
    locked_paths: set[Path] = set()
    for relative, expected_blob in LOCKED_B.items():
        path = root / relative
        if not path.is_file():
            fail(f"Source B locked file missing: {relative}")
        raw = path.read_bytes()
        blob = git_blob_sha1(raw)
        if blob != expected_blob:
            fail(f"Source B locked blob mismatch for {relative}: expected {expected_blob}, got {blob}")
        write_bytes(stage, f"source_B/{relative}", raw)
        locked_paths.add(path)
        locked_meta[relative] = {"git_blob_sha1": blob, "sha256": sha256(raw)}

    candidates: set[Path] = set()
    src = root / "src" / "interaction_sensing"
    if src.is_dir():
        candidates.update(src.rglob("*.py"))
    for folder in (root / "scripts", root / "tests"):
        if folder.is_dir():
            candidates.update(p for p in folder.glob("*.py") if "v14" in p.name.lower())
    bench = root / "benchmarks"
    if bench.is_dir():
        candidates.update(bench.glob("v14*.json"))
    for extra in ("pyproject.toml", "requirements.txt"):
        p = root / extra
        if p.is_file():
            candidates.add(p)

    count = 0
    for path in sorted(candidates):
        if path in locked_paths or not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES:
            raw = sanitize_text(raw.decode("utf-8"), literals).encode("utf-8")
        write_bytes(stage, f"source_B/{relative}", raw)
        count += 1
    return {"commit": SOURCE_B_COMMIT, "locked_files": locked_meta, "scientific_snapshot_file_count_excluding_locked": count}


def generate_review_figures(stage: Path) -> None:
    output = stage / "figures" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = "315532800"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_mee_figures.py"), "--output-dir", str(output)], check=True, env=env)
    png = sorted(output.glob("*.png"))
    svg = sorted(output.glob("*.svg"))
    if len(png) != 8 or len(svg) != 8 or not (output / "figure_provenance.json").is_file():
        fail("expected 8 PNG + 8 SVG + figure_provenance.json")
    for path in svg:
        text = re.sub(r"<dc:date>.*?</dc:date>", "<dc:date>1980-01-01T00:00:00</dc:date>", path.read_text(encoding="utf-8"))
        path.write_text(text, encoding="utf-8")


def identity_scan(stage: Path, literals: tuple[str, ...]) -> None:
    tokens = [OWNER.lower(), "github.com/", "raw.githubusercontent.com/"] + [x.lower() for x in literals if x]
    for path in sorted(p for p in stage.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES):
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for token in tokens:
            if token and token in lower:
                fail(f"identity token {token!r} remains in {path.relative_to(stage)}")
        if EMAIL.search(text):
            fail(f"email remains in {path.relative_to(stage)}")


def deterministic_zip(stage: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            relative = path.relative_to(stage).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-a-root", type=Path, required=True)
    parser.add_argument("--source-b-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--forbid-literal", action="append", default=[])
    args = parser.parse_args()
    literals = tuple(x for x in args.forbid_literal if x.strip())

    verify_checkout(args.source_a_root, SOURCE_A_COMMIT, "Source A")
    verify_checkout(args.source_b_root, SOURCE_B_COMMIT, "Source B")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = args.output_dir / "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.zip"
    receipt_path = args.output_dir / "TNOA_MEE_ANONYMOUS_REVIEW_BUNDLE.receipt.json"

    with tempfile.TemporaryDirectory(prefix="tnoa-review-") as tmp:
        stage = Path(tmp) / "bundle"
        stage.mkdir()
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_mee_anonymous_manuscript.py")], check=True)
        reviewer = ROOT / "submission" / "generated" / "MEE_ANONYMOUS_MANUSCRIPT.md"
        if not reviewer.is_file():
            fail("anonymous manuscript output missing")

        write_text(stage, "README.md", neutral_readme())
        for relative in ("LICENSE", "references.bib", "requirements-figures.txt", "requirements-analysis.txt", "pyproject.toml"):
            copy_repo_file(stage, relative, literals)
        write_bytes(stage, "manuscript/MEE_ANONYMOUS_MANUSCRIPT.md", sanitize_text(reviewer.read_text(encoding="utf-8"), literals).encode("utf-8"))
        copy_repo_file(stage, "manuscript/TNOA_MEE_DRAFT.md", literals)
        copy_repo_file(stage, "figures/fig1_tnoa_architecture.svg", literals)
        source_repro = ROOT / "reproduce" / "README.md"
        write_bytes(stage, "reproduce/README_ANONYMOUS.md", sanitize_text(source_repro.read_text(encoding="utf-8"), literals).encode("utf-8"))

        for relative in TNOA_DOCS:
            copy_repo_file(stage, relative, literals)
        for relative in DERIVED:
            copy_repo_file(stage, relative, literals, exact=True)
        for relative in TNOA_SCRIPTS:
            copy_repo_file(stage, relative, literals)
        for relative in ("tnoa/__init__.py", "tnoa/core.py", "tnoa/cli.py", "tests/test_minimal_api.py", "examples/minimal_evidence.csv"):
            copy_repo_file(stage, relative, literals)

        paper = anonymous_paper_manifest(literals)
        write_text(stage, "paper_manifest.json", json.dumps(paper, indent=2) + "\n")
        write_text(stage, "paper_manifest.anonymous.json", json.dumps(paper, indent=2) + "\n")
        generate_review_figures(stage)
        source_meta = {"A": copy_source_a(stage, args.source_a_root, literals), "B": copy_source_b(stage, args.source_b_root, literals)}
        identity_scan(stage, literals)

        files = {path.relative_to(stage).as_posix(): sha256(path.read_bytes()) for path in sorted(p for p in stage.rglob("*") if p.is_file())}
        manifest = {
            "schema": "tnoa-anonymous-review-bundle-v2",
            "paper_generation": "TNOA-P1-MEE",
            "double_anonymous": True,
            "scientific_claim_boundary_unchanged": True,
            "d3_status": "post-freeze/not-preregistered",
            "d4_status": "post-freeze/not-preregistered design sensitivity",
            "source_snapshots": source_meta,
            "files": files,
        }
        write_text(stage, "bundle_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        deterministic_zip(stage, zip_path)

    receipt = {
        "schema": "tnoa-anonymous-review-bundle-receipt-v2",
        "zip_filename": zip_path.name,
        "zip_sha256": sha256(zip_path.read_bytes()),
        "source_A_commit": SOURCE_A_COMMIT,
        "source_B_commit": SOURCE_B_COMMIT,
        "d3_status": "post-freeze/not-preregistered",
        "d4_status": "post-freeze/not-preregistered design sensitivity",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Built anonymous review bundle: {zip_path}")
    print(f"SHA-256: {receipt['zip_sha256']}")


if __name__ == "__main__":
    main()
