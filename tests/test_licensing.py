from tnoa.core import Evidence, classify
from tnoa.licensing import (
    ReportClaim,
    license_report_claim,
    licensed_claims,
)


def test_target_record_licenses_target_only_not_absence():
    record = classify(Evidence(True, True, False))
    assert license_report_claim(record, ReportClaim.TARGET_ATTRIBUTION).licensed
    assert not license_report_claim(
        record, ReportClaim.BIOLOGICAL_ABSENCE, independent_absence_supported=True
    ).licensed


def test_baseline_does_not_license_biological_absence():
    record = classify(Evidence(False, False, False))
    assert license_report_claim(record, ReportClaim.BASELINE_RECORD).licensed
    assert not license_report_claim(record, ReportClaim.BIOLOGICAL_ABSENCE).licensed


def test_independent_absence_channel_is_separate():
    record = classify(Evidence(True, False, False))
    assert license_report_claim(
        record, ReportClaim.BIOLOGICAL_ABSENCE, independent_absence_supported=True
    ).licensed


def test_overlap_withholds_target_and_nuisance_attribution():
    record = classify(Evidence(True, True, True))
    assert not license_report_claim(record, ReportClaim.TARGET_ATTRIBUTION).licensed
    assert not license_report_claim(record, ReportClaim.NUISANCE_ATTRIBUTION).licensed
    assert licensed_claims(record) == ()
