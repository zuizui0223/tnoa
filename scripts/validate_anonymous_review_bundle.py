#!/usr/bin/env python3
"""Validate a built anonymous TNOA reviewer ZIP.

The validator checks deterministic package structure, file hashes recorded in the
internal bundle manifest, and a narrow identity-leak policy. Scientific project
names may remain where method semantics require them, but public owner identifiers,
email addresses and GitHub URLs are forbidden in the reviewer archive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import PurePosixPath

EMAIL = re.compile(rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
FORBIDDEN_BYTES = (
    b"zuizui0223",
    b"github.com/",
    b"raw.githubusercontent.com/",
)
TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".json", ".bib", ".svg", ".yml", ".yaml", ".toml", ".csv"
}
REQUIRED = {
    "README.md",
    "LICENSE",
    "bundle_manifest.json",
    "manuscript/MEE_ANONYMOUS_MANUSCRIPT.md",
    "manuscript/TNOA_P1_AUDIT_SOURCE.md",
    "references.bib",
    "requirements-figures.txt",
    "figures/fig1_tnoa_architecture.svg",
    "scripts/build_paper_figures.py",
    "scripts/audit_manuscript_claims.py",
    "source_A/target_evidence.py",
    "source_B/benchmarks/v14b_frozen_ternary_phase_figure_data.json",
    "source_B/benchmarks/v14b_frozen_ternary_phase_surface_result.json",
    "source_B/benchmarks/v14b_nuisance_familywise_risk_result.json",
}


def fail(message: str) -> None:
    raise SystemExit(f"anonymous review bundle validation failed: {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path")
    args = parser.parse_args()

    with zipfile.ZipFile(args.zip_path, "r") as zf:
        names = set(zf.namelist())
        missing = REQUIRED - names
        if missing:
            fail(f"missing required files: {sorted(missing)}")

        manifest = json.loads(zf.read("bundle_manifest.json").decode("utf-8"))
        if manifest.get("schema") != "tnoa-anonymous-review-bundle-v1":
            fail("unexpected bundle manifest schema")
        if manifest.get("double_anonymous") is not True:
            fail("bundle must be registered as double-anonymous")

        recorded = manifest.get("files", {})
        if not isinstance(recorded, dict) or not recorded:
            fail("bundle manifest has no file hash registry")

        for name, expected in recorded.items():
            if name not in names:
                fail(f"manifest-recorded file missing from ZIP: {name}")
            raw = zf.read(name)
            actual = hashlib.sha256(raw).hexdigest()
            if actual != expected:
                fail(f"file SHA-256 mismatch for {name}")

        # No unregistered payload files apart from the manifest itself.
        allowed = set(recorded) | {"bundle_manifest.json"}
        extras = names - allowed
        if extras:
            fail(f"unregistered files in ZIP: {sorted(extras)}")

        for name in sorted(names):
            suffix = PurePosixPath(name).suffix.lower()
            if suffix not in TEXT_SUFFIXES:
                continue
            raw = zf.read(name)
            lower = raw.lower()
            for token in FORBIDDEN_BYTES:
                if token in lower:
                    fail(f"identity-bearing token {token.decode()} remains in {name}")
            if EMAIL.search(raw):
                fail(f"email address remains in {name}")

        manuscript = zf.read("manuscript/MEE_ANONYMOUS_MANUSCRIPT.md")
        if b"<!-- C" in manuscript:
            fail("reviewer manuscript still contains internal C-ID comments")
        if b"**1.**" not in manuscript or b"**4.**" not in manuscript:
            fail("reviewer manuscript does not contain numbered 1-4 abstract")

        source_meta = manifest.get("source_snapshots", {})
        if source_meta.get("A", {}).get("commit") != "f3b266897f3e9139e6c3fe9ce6b645e25371e092":
            fail("Source A commit drifted")
        if source_meta.get("B", {}).get("commit") != "1664a190cec47142e8d14cc5157302a7af18d019":
            fail("Source B commit drifted")

    print(
        "Anonymous review bundle OK: "
        f"{len(recorded)} registered files, identity scan clean, locked source commits retained"
    )


if __name__ == "__main__":
    main()
