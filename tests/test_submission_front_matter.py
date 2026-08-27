from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*")


class TestMEESubmissionFrontMatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = FRONT.read_text(encoding="utf-8")

    def test_numbered_abstract_is_within_350_word_guard(self) -> None:
        self.assertIn("## Abstract", self.text)
        self.assertIn("## Keywords", self.text)
        abstract = self.text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
        for label in ("**1.**", "**2.**", "**3.**", "**4.**"):
            self.assertEqual(abstract.count(label), 1, label)
        words = WORD_RE.findall(abstract)
        self.assertLessEqual(len(words), 350, f"abstract has {len(words)} words")

    def test_keywords_are_unique_alphabetical_and_at_most_eight(self) -> None:
        self.assertIn("## Data/Code for peer review statement", self.text)
        block = self.text.split("## Keywords", 1)[1].split("## Data/Code for peer review statement", 1)[0].strip()
        keywords = [item.strip() for item in block.split(";") if item.strip()]
        self.assertGreater(len(keywords), 0)
        self.assertLessEqual(len(keywords), 8)
        self.assertEqual(len(keywords), len(set(item.casefold() for item in keywords)))
        self.assertEqual(
            [item.casefold() for item in keywords],
            sorted(item.casefold() for item in keywords),
        )


if __name__ == "__main__":
    unittest.main()
