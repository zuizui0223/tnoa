from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestReaderFacingCalibrationWording(unittest.TestCase):
    def test_public_and_submission_figures_do_not_claim_classical_family_wise_control(self) -> None:
        paths = (
            ROOT / "README.md",
            ROOT / "docs" / "FIGURE_PLAN.md",
            ROOT / "docs" / "MEE_FIGURE_VALIDATION.md",
            ROOT / "docs" / "FIELD_TRANSLATION_PATHWAY.md",
            ROOT / "scripts" / "build_mee_figures.py",
            ROOT / "scripts" / "build_mee_composite_figures.py",
        )
        forbidden = (
            "failed family-wise control",
            "preregistered family-wise calibration passed",
            "whereas family-wise calibration passes",
            "nuisance support may use family-wise false-attribution control",
            "Family-wise calibration met",
            '"Family-wise\\ncalibration"',
            '["Pooled", "Family-wise"]',
            "threshold failure -> diagnosis -> family-wise error control",
            "family-wise calibration produced 0.04444 and passed",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                self.assertNotIn(phrase, text, f"stale reader-facing calibration wording in {path}: {phrase}")

    def test_current_semantics_are_explicit(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("family-conditional checks", readme)
        self.assertIn("not classical family-wise error-rate control", readme)

        vocabulary = (ROOT / "docs" / "MEE_VOCABULARY_MAP.md").read_text(encoding="utf-8")
        self.assertIn("predeclared family-conditional false-attribution criterion", vocabulary)
        self.assertIn("historical source labels remain provenance only", vocabulary)

        component_builder = (ROOT / "scripts" / "build_mee_figures.py").read_text(encoding="utf-8")
        composite_builder = (ROOT / "scripts" / "build_mee_composite_figures.py").read_text(encoding="utf-8")
        self.assertIn("Family-conditional", component_builder)
        self.assertIn("Family-conditional", composite_builder)


if __name__ == "__main__":
    unittest.main()
