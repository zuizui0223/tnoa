import unittest

from tnoa import Decision, Evidence, Reason, classify, classify_rows, summarize


class DecisionTests(unittest.TestCase):
    def test_baseline_requires_observability(self):
        self.assertEqual(classify(Evidence(False, False, False)).decision, Decision.BASELINE)
        result = classify(Evidence(False, False, False, observable=False))
        self.assertEqual(result.decision, Decision.UNDETERMINED)
        self.assertEqual(result.reason, Reason.INSUFFICIENT_OBSERVABILITY)

    def test_positive_support_cannot_silently_become_baseline(self):
        contradictory = (
            Evidence(False, True, False),
            Evidence(False, False, True),
            Evidence(False, False, False, coupled_response_supported=True),
        )
        for evidence in contradictory:
            with self.subTest(evidence=evidence):
                with self.assertRaisesRegex(ValueError, "deviation_observed=False"):
                    classify(evidence)

    def test_positive_target_and_nuisance_are_not_complements(self):
        target = classify(Evidence(True, True, False))
        nuisance = classify(Evidence(True, False, True))
        overlap = classify(Evidence(True, True, True))
        self.assertEqual(target.decision, Decision.TARGET)
        self.assertEqual(nuisance.decision, Decision.NUISANCE)
        self.assertEqual(overlap.decision, Decision.UNDETERMINED)
        self.assertEqual(overlap.reason, Reason.TARGET_NUISANCE_OVERLAP)

    def test_coupled_response_requires_attribution(self):
        unresolved = classify(Evidence(True, False, False, coupled_response_supported=True))
        resolved = classify(
            Evidence(
                True,
                False,
                False,
                coupled_response_supported=True,
                attribution_supported=True,
            )
        )
        self.assertEqual(unresolved.decision, Decision.UNDETERMINED)
        self.assertEqual(unresolved.reason, Reason.MISSING_ATTRIBUTION)
        self.assertEqual(resolved.decision, Decision.TARGET)

    def test_no_support_is_not_absence(self):
        result = classify(Evidence(True, False, False))
        self.assertEqual(result.decision, Decision.UNDETERMINED)
        self.assertEqual(result.reason, Reason.NO_SUPPORTED_EVIDENCE)

    def test_rows_and_group_summary(self):
        rows = [
            {"site": "A", "deviation_observed": 0, "target_supported": 0, "nuisance_supported": 0},
            {"site": "A", "deviation_observed": 1, "target_supported": 1, "nuisance_supported": 0},
            {"site": "A", "deviation_observed": 1, "target_supported": 1, "nuisance_supported": 1},
            {"site": "B", "deviation_observed": 1, "target_supported": 0, "nuisance_supported": 1},
        ]
        annotated = classify_rows(rows)
        summary = summarize(annotated, group_by=["site"])
        by_site = {row["site"]: row for row in summary}
        self.assertAlmostEqual(by_site["A"]["baseline_rate"], 1 / 3)
        self.assertAlmostEqual(by_site["A"]["target_rate"], 1 / 3)
        self.assertAlmostEqual(by_site["A"]["undetermined_rate"], 1 / 3)
        self.assertEqual(by_site["B"]["nuisance_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
