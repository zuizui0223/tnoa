"""Fail-closed report-transition licensing for TNOA decision records.

This module is not an informed-consent implementation and makes no human-
subjects ethics claim. It operationalises the narrower scientific rule that a
semantic report must not outrun the evidence state preserved by TNOA.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .core import Decision, DecisionRecord


class ReportClaim(str, Enum):
    BASELINE_RECORD = "baseline_record"
    TARGET_ATTRIBUTION = "target_attribution"
    NUISANCE_ATTRIBUTION = "nuisance_attribution"
    BIOLOGICAL_ABSENCE = "biological_absence"


class LicenseStatus(str, Enum):
    LICENSED = "licensed"
    WITHHELD = "withheld"


@dataclass(frozen=True)
class ReportLicense:
    claim: ReportClaim
    status: LicenseStatus
    reason: str

    @property
    def licensed(self) -> bool:
        return self.status is LicenseStatus.LICENSED


def license_report_claim(
    record: DecisionRecord,
    claim: ReportClaim,
    *,
    independent_absence_supported: bool = False,
) -> ReportLicense:
    """Evaluate whether one report transition is supported by the record.

    ``independent_absence_supported`` represents a separately validated A-
    channel. It is never inferred from baseline, observability, nuisance, or
    lack of target support.
    """
    if claim is ReportClaim.BASELINE_RECORD:
        ok = record.decision is Decision.BASELINE
        return ReportLicense(
            claim,
            LicenseStatus.LICENSED if ok else LicenseStatus.WITHHELD,
            "baseline_decision" if ok else "record_is_not_baseline",
        )

    if claim is ReportClaim.TARGET_ATTRIBUTION:
        ok = record.decision is Decision.TARGET
        return ReportLicense(
            claim,
            LicenseStatus.LICENSED if ok else LicenseStatus.WITHHELD,
            "target_supported" if ok else "target_not_uniquely_supported",
        )

    if claim is ReportClaim.NUISANCE_ATTRIBUTION:
        ok = record.decision is Decision.NUISANCE
        return ReportLicense(
            claim,
            LicenseStatus.LICENSED if ok else LicenseStatus.WITHHELD,
            "nuisance_supported" if ok else "nuisance_not_uniquely_supported",
        )

    if claim is ReportClaim.BIOLOGICAL_ABSENCE:
        contradiction = record.target_support_used or record.decision is Decision.TARGET
        ok = independent_absence_supported and not contradiction
        reason = (
            "independent_absence_channel"
            if ok
            else "target_support_conflicts_with_absence"
            if contradiction
            else "independent_absence_not_supported"
        )
        return ReportLicense(
            claim,
            LicenseStatus.LICENSED if ok else LicenseStatus.WITHHELD,
            reason,
        )

    raise ValueError(f"unsupported report claim: {claim!r}")


def licensed_claims(
    record: DecisionRecord,
    *,
    independent_absence_supported: bool = False,
) -> tuple[ReportClaim, ...]:
    return tuple(
        claim
        for claim in ReportClaim
        if license_report_claim(
            record,
            claim,
            independent_absence_supported=independent_absence_supported,
        ).licensed
    )
