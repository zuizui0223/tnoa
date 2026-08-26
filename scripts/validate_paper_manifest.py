#!/usr/bin/env python3
"""Validate TNOA Paper-1 manifest and repository-level provenance contracts.

This script checks only information committed inside the TNOA repository. It does
not silently fetch or rerun PolliPi/InsePi scientific generations. External source
verification remains an explicit reproduction step documented in reproduce/README.md.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "paper_manifest.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_REPO_FILES = (
    "README.md",
    "paper_manifest.json",
    "references.bib",
    "docs/CONCEPTUAL_FRAMEWORK.md",
    "docs/NOVELTY_POSITIONING.md",
    "docs/LITERATURE_EVIDENCE_MAP.md",
    "docs/REVIEWER_ATTACK_MATRIX.md",
    "docs/TRANSFERABILITY_TABLE.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/CLAIM_TRACEABILITY.md",
    "docs/SOURCE_PROVENANCE.md",
    "docs/METHOD_PAPER_BLUEPRINT.md",
)

REQUIRED_LOCKED_IDS = {
    "v14a2_first_spatiotemporal_sweep",
    "v14a2_corrected_observation_safe_audit",
    "v14b_target_observer_freeze",
    "v14b_nuisance_familywise_risk_freeze",
    "v14b_final_ternary_phase_surface",
}


def fail(message: str) -> None:
    raise SystemExit(f"TNOA manifest validation failed: {message}")


def main() -> None:
    for relative in REQUIRED_REPO_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing required repository file: {relative}")

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("paper_generation") != "TNOA-P1":
        fail("paper_generation must be TNOA-P1")
    if "closed-world methods paper" not in str(payload.get("scope", "")):
        fail("scope must retain the closed-world Paper-1 boundary")

    repos = payload.get("source_repositories", {})
    for repo_name in ("pollipi", "insepi"):
        if repo_name not in repos:
            fail(f"missing source repository: {repo_name}")
    if not HEX40.fullmatch(repos["pollipi"].get("main_commit_at_seed", "")):
        fail("PolliPi source commit must be 40-hex")
    if not HEX40.fullmatch(repos["insepi"].get("main_commit_at_seed", "")):
        fail("InsePi source commit must be 40-hex")
    if not HEX40.fullmatch(repos["pollipi"].get("target_evidence_adapter_git_blob_sha1", "")):
        fail("PolliPi target adapter blob must be 40-hex")

    locked = payload.get("locked_results")
    if not isinstance(locked, list) or not locked:
        fail("locked_results must be a non-empty list")
    ids = [row.get("id") for row in locked]
    if len(ids) != len(set(ids)):
        fail("locked result IDs must be unique")
    missing_ids = REQUIRED_LOCKED_IDS - set(ids)
    if missing_ids:
        fail(f"missing required locked result IDs: {sorted(missing_ids)}")

    by_id = {row["id"]: row for row in locked}
    for result_id, row in by_id.items():
        if not HEX40.fullmatch(str(row.get("execution_commit", ""))):
            fail(f"{result_id}: execution_commit must be 40-hex")
        if not SHA256.fullmatch(str(row.get("artifact_digest", ""))):
            fail(f"{result_id}: artifact_digest must be sha256: + 64-hex")
        result_sha = row.get("result_sha256")
        if result_sha is not None and not HEX64.fullmatch(str(result_sha)):
            fail(f"{result_id}: result_sha256 must be 64-hex when present")
        source_path = str(row.get("source_path", ""))
        if not source_path.startswith("benchmarks/"):
            fail(f"{result_id}: source_path must point to an InsePi benchmark artifact")

    final = by_id["v14b_final_ternary_phase_surface"]
    summary = final.get("registered_summary", {})
    if summary.get("coordinate_count") != 30625:
        fail("final coordinate_count must remain 30625")
    if summary.get("world_count") != 5880000:
        fail("final world_count must remain 5880000")
    if summary.get("observer_retuned") is not False:
        fail("final observer_retuned must remain false")

    boundary = payload.get("paper_claim_boundary", {})
    required_false = (
        "field_accuracy",
        "field_absence_certification",
        "universal_pi3_law",
        "universal_optimal_abstention",
    )
    for key in required_false:
        if boundary.get(key) is not False:
            fail(f"claim boundary {key} must remain false for Paper 1")
    if boundary.get("closed_world_method_claims") is not True:
        fail("closed_world_method_claims must remain true")

    literature = payload.get("literature_positioning", {})
    if literature.get("status") != "initial_evidence_map_complete_not_systematic_review":
        fail("literature positioning must not be mislabeled as a systematic review")
    for key in ("evidence_map", "reviewer_attack_matrix", "bibliography", "transferability_map"):
        path = literature.get(key)
        if not path or not (ROOT / path).is_file():
            fail(f"literature positioning path missing or invalid: {key}")

    blockers = payload.get("submission_blockers")
    if not isinstance(blockers, list):
        fail("submission_blockers must be a list")

    print(
        "TNOA manifest OK: "
        f"{len(locked)} locked results, "
        f"{len(payload.get('retained_failures', []))} retained failures, "
        f"{len(blockers)} submission blockers"
    )


if __name__ == "__main__":
    main()
