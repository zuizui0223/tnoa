from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "submission" / "MEE_SUBMISSION_CHECKLIST.md"


class TestSubmissionChecklistStatus(unittest.TestCase):
    def test_stale_pre_d5_status_is_absent(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        for token in (
            "33039903388",
            "4,953 words",
            "all 12 cited bibliography keys",
            "three derived analyses",
            "Six BibTeX entries are currently unused",
            "retrieved on 2026-08-27",
        ):
            self.assertNotIn(token, text, f"stale checklist status remains: {token}")

    def test_current_validated_status_is_recorded(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        for token in (
            "302 repository-counted words",
            "7,712 visible words",
            "24 active-paper citation entries",
            "9 prior-art-only entries",
            "0 orphan bibliography entries",
            "D1–D5",
            "2026-09-01",
            "classical-FWER",
            "semantic-specific-reason-premium",
        ):
            self.assertIn(token, text, f"current checklist invariant missing: {token}")


if __name__ == "__main__":
    unittest.main()
