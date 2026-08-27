#!/usr/bin/env python3
"""Validate a built double-anonymous TNOA MEE reviewer ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import PurePosixPath

EMAIL = re.compile(rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
OWNER_TOKEN = (b"zui" + b"zui0223").lower()
GITHUB_TOKEN = b"github" + b".com/"
RAW_GITHUB_TOKEN = b"raw.githubusercontent" + b".com/"
TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".json", ".bib", ".svg", ".yml", ".yaml", ".toml", ".csv"
}
REQUIRED = {
    "README.md",
    "LICENSE",
    "bundle_manifest.json",
    "paper_manifest.json",
    "paper_manifest.anonymous.json",
    "manuscript/MEE_ANONYMOUS_MANUSCRIPT.md",
    "manuscript/TNOA_MEE_DRAFT.md",
    "references.bib",
    "requirements-figures.txt",
    "requirements-analysis.txt",
    "pyproject.toml",
    "docs/CONCEPTUAL_FRAMEWORK.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md",
    "docs/FIGURE_PLAN.md",
    "docs/MEE_FIGURE_VALIDATION.md",
    "docs/MEE_SYNTHETIC_CONSEQUENCES.md",
    "docs/STRUCTURAL_RESULT_AUDIT.md",
    "docs/REUSABLE_IMPLEMENTATION.md",
    "docs/MEE_VOCABULARY_MAP.md",
    "derived/mee_figure_data.json",
    "derived/mee_synthetic_consequences.json",
    "derived/structural_axis_audit.json",
    "scripts/audit_manuscript_claims.py",
    "scripts/validate_mee_figure_data.py",
    "scripts/validate_mee_synthetic_consequences.py",
    "scripts/validate_structural_axis_audit.py",
    "scripts/build_mee_figures.py",
    "scripts/validate_anonymous_review_bundle.py",
    "tnoa/__init__.py",
    "tnoa/core.py",
    "tnoa/cli.py",
    "tests/test_minimal_api.py",
    "examples/minimal_evidence.csv",
    "figures/fig1_tnoa_architecture.svg",
    "figures/generated/figure_provenance.json",
    "source_A/target_evidence.py",
    "source_B/benchmarks/v14b_frozen_ternary_phase_surface_result.json",
    "source_B/benchmarks/v14b_nuisance_observer_process_scale_validation_v1_result.json",
    "source_B/benchmarks/v14b_nuisance_risk_calibration_v1_result.json",
    "source_B/benchmarks/v14b_nuisance_familywise_risk_result.json",
}


def fail(message: str) -> None:
    raise SystemExit(f"anonymous review bundle validation failed: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path")
    parser.add_argument("--forbid-literal", action="append", default=[])
    args = parser.parse_args()
    extra = [x.encode("utf-8").lower() for x in args.forbid_literal if x.strip()]

    with zipfile.ZipFile(args.zip_path, "r") as zf:
        names = set(zf.namelist())
        missing = REQUIRED - names
        if missing:
            fail(f"missing required files: {sorted(missing)}")

        manifest = json.loads(zf.read("bundle_manifest.json").decode("utf-8"))
        if manifest.get("schema") != "tnoa-anonymous-review-bundle-v2":
            fail("unexpected bundle manifest schema")
        if manifest.get("double_anonymous") is not True:
            fail("bundle must be registered as double-anonymous")
        if manifest.get("paper_generation") != "TNOA-P1-MEE":
            fail("bundle paper generation drifted")
        if manifest.get("scientific_claim_boundary_unchanged") is not True:
            fail("bundle cannot change scientific claim boundary")

        recorded = manifest.get("files", {})
        if not isinstance(recorded, dict) or not recorded:
            fail("bundle manifest has no file hash registry")
        for name, expected in recorded.items():
            if name not in names:
                fail(f"manifest-recorded file missing from ZIP: {name}")
            actual = hashlib.sha256(zf.read(name)).hexdigest()
            if actual != expected:
                fail(f"file SHA-256 mismatch for {name}")
        allowed = set(recorded) | {"bundle_manifest.json"}
        extras = names - allowed
        if extras:
            fail(f"unregistered files in ZIP: {sorted(extras)}")

        forbidden = [OWNER_TOKEN, GITHUB_TOKEN, RAW_GITHUB_TOKEN] + extra
        for name in sorted(names):
            if PurePosixPath(name).suffix.lower() not in TEXT_SUFFIXES:
                continue
            raw = zf.read(name)
            lower = raw.lower()
            for token in forbidden:
                if token and token in lower:
                    fail(f"identity-bearing token remains in {name}")
            if EMAIL.search(raw):
                fail(f"email address remains in {name}")

        manuscript = zf.read("manuscript/MEE_ANONYMOUS_MANUSCRIPT.md")
        if b"<!-- C" in manuscript or b"<!-- D" in manuscript:
            fail("reviewer manuscript still contains internal claim-ID comments")
        if b"**1.**" not in manuscript or b"**4.**" not in manuscript:
            fail("reviewer manuscript does not contain numbered 1-4 abstract")

        audit = zf.read("manuscript/TNOA_MEE_DRAFT.md")
        if b"<!-- C" not in audit and b"<!-- D" not in audit:
            fail("parallel audit manuscript lost internal claim provenance tags")

        paper = json.loads(zf.read("paper_manifest.json").decode("utf-8"))
        if paper.get("schema") != "tnoa-paper-manifest-v6" or paper.get("paper_generation") != "TNOA-P1-MEE":
            fail("anonymous paper manifest is not the active MEE manifest")
        if paper.get("submission_blockers") != []:
            fail("anonymous paper manifest reports scientific submission blockers")
        repos = paper.get("source_repositories", {})
        for value in repos.values():
            if value.get("repository") != "withheld for double-anonymous review":
                fail("anonymous paper manifest exposes a source repository identity")

        source_meta = manifest.get("source_snapshots", {})
        if source_meta.get("A", {}).get("commit") != "f3b266897f3e9139e6c3fe9ce6b645e25371e092":
            fail("Source A commit drifted")
        if source_meta.get("B", {}).get("commit") != "1664a190cec47142e8d14cc5157302a7af18d019":
            fail("Source B commit drifted")

        figure_png = [n for n in names if n.startswith("figures/generated/") and n.endswith(".png")]
        figure_svg = [n for n in names if n.startswith("figures/generated/") and n.endswith(".svg")]
        if len(figure_png) != 8 or len(figure_svg) != 8:
            fail(f"expected 8 PNG and 8 SVG review figures, got {len(figure_png)} and {len(figure_svg)}")

        fig_data = json.loads(zf.read("derived/mee_figure_data.json").decode("utf-8"))
        if fig_data.get("schema") != "tnoa-mee-figure-data-v1":
            fail("MEE figure-data schema drifted")
        if fig_data["provenance"]["v14b_phase_surface"]["surface_sha256"] != "1d2c7c1f8f7370aad3cdde4d9d9d47bf318b2a057b6f788d3a48df9ea8d16c34":
            fail("phase-surface scientific provenance drifted")

    print(
        "Anonymous MEE review bundle OK: "
        f"{len(recorded)} registered files, 8+8 figures, identity scan clean, pinned source commits retained"
    )


if __name__ == "__main__":
    main()
