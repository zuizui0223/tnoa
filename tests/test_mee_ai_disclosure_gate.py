from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "submission" / "submission_manifest.json"
TEMPLATE = ROOT / "submission" / "MEE_AI_DISCLOSURE_TEMPLATE.md"


def test_mee_ai_disclosure_is_explicit_human_finalization_gate() -> None:
    assert TEMPLATE.exists()
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ai = payload["ai_assistance"]
    assert ai["live_mee_policy_checked_date"] == "2026-09-12"
    assert ai["template"] == "submission/MEE_AI_DISCLOSURE_TEMPLATE.md"
    assert ai["methods_statement_required_for_substantive_llm_use"] is True
    assert ai["application_name_and_version_required"] is True
    assert ai["human_author_responsibility_required"] is True
    assert ai["finalized"] is False
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "OpenAI ChatGPT" in text
    assert "confirm exact application/model version(s)" in text
    assert "take full responsibility" in text
    remaining = "\n".join(payload["remaining_initial_upload_tasks"])
    assert "exact ChatGPT application/model version(s)" in remaining
    assert "Materials and Methods" in remaining
