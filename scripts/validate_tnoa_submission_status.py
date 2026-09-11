#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "submission" / "TNOA_SUBMISSION_STATUS_2026-09-11.json"
MANIFEST = ROOT / "submission" / "submission_manifest.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha1(value: str) -> None:
    assert isinstance(value, str) and len(value) == 40
    int(value, 16)


def _sha256_digest(value: str) -> None:
    assert value.startswith("sha256:")
    digest = value.split(":", 1)[1]
    assert len(digest) == 64
    int(digest, 16)


def main() -> None:
    status = _load(STATUS)
    manifest = _load(MANIFEST)

    assert status["paper"] == "TNOA"
    assert status["target_journal"] == "Methods in Ecology and Evolution"
    assert status["status"] == "science-complete-production-validated-human-input-open"
    assert status["scientific_source_manifest"] == "paper_manifest.json"
    assert status["submission_manifest"] == "submission/submission_manifest.json"
    assert status["canonical_manuscript"] == "manuscript/TNOA_MEE_DRAFT.md"
    assert status["scientific_submission_blockers"] == 0
    assert status["science_blocker"] is False
    _sha1(status["validated_source_sha"])

    run = status["validation_run"]
    assert run["workflow"] == "validate-paper-package"
    assert run["run_id"] == 34564310098
    assert run["conclusion"] == "success"

    expected = {
        "anonymous_docx": 10185463934,
        "anonymous_reviewer_bundle": 10185463162,
        "initial_submission_readiness": 10185463542,
        "composite_figures": 10185464425,
    }
    assert set(status["validated_artifacts"]) == set(expected)
    for key, artifact_id in expected.items():
        row = status["validated_artifacts"][key]
        assert row["artifact_id"] == artifact_id
        _sha256_digest(row["digest"])

    production = status["production_state"]
    for required in (
        "anonymous_docx_built_and_validated",
        "double_spacing",
        "continuous_line_numbering",
        "page_numbering",
        "citations_and_references_rendered",
        "anonymous_reviewer_bundle_built_and_validated",
        "figure_1_to_4_and_supplementary_s2_code_assembled",
    ):
        assert production[required] is True
    assert production["open_source_license"] == "MIT"
    assert production["final_human_visual_inspection_required"] is True

    assert manifest["scientific_submission_blockers"] == 0
    assert manifest["scientific_claim_boundary_unchanged"] is True
    assert manifest["formatted_docx"]["ci_validation_required"] is True
    assert "human" in status["next_mainline"].lower()
    assert "no new scientific analysis" in status["next_mainline"].lower()

    print("TNOA_SUBMISSION_STATUS PASS")


if __name__ == "__main__":
    main()
