from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


class Decision(str, Enum):
    BASELINE = "B"
    TARGET = "T"
    NUISANCE = "N"
    UNDETERMINED = "U"


class Reason(str, Enum):
    BASELINE = "baseline"
    TARGET_SUPPORT = "target_support"
    NUISANCE_SUPPORT = "nuisance_support"
    TARGET_NUISANCE_OVERLAP = "target_nuisance_overlap"
    MISSING_ATTRIBUTION = "missing_attribution"
    INSUFFICIENT_OBSERVABILITY = "insufficient_observability"
    NO_SUPPORTED_EVIDENCE = "no_supported_evidence"


@dataclass(frozen=True)
class Evidence:
    """Already-calibrated positive-support flags for one observation window.

    TNOA deliberately does not define how a raw detector score becomes a support
    flag. That adapter/calibration belongs to the sensor domain and must be
    validated separately.
    """

    deviation_observed: bool
    target_supported: bool
    nuisance_supported: bool
    observable: bool = True
    coupled_response_supported: bool = False
    attribution_supported: bool = False


@dataclass(frozen=True)
class DecisionRecord:
    decision: Decision
    reason: Reason
    target_support_used: bool
    nuisance_support_used: bool
    observable: bool

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        data["reason"] = self.reason.value
        return data


def classify(evidence: Evidence) -> DecisionRecord:
    """Map process-preserving evidence to the minimal B/T/N/U vocabulary.

    Precedence is intentionally conservative:
    - contradictory positive support cannot be silently collapsed to baseline;
    - insufficient observability cannot become baseline/absence;
    - direct T and attribution-gated coupled response are positive target support;
    - simultaneous T and N support is retained as U rather than forced exclusive;
    - an unattributed coupled response remains U even when nuisance is supported;
    - lack of positive support is U, not biological absence.
    """

    if not evidence.deviation_observed and (
        evidence.target_supported
        or evidence.nuisance_supported
        or evidence.coupled_response_supported
        or evidence.attribution_supported
    ):
        raise ValueError(
            "deviation_observed=False is inconsistent with positive target, "
            "nuisance, coupled-response, or attribution support"
        )

    if not evidence.observable:
        return DecisionRecord(
            Decision.UNDETERMINED,
            Reason.INSUFFICIENT_OBSERVABILITY,
            False,
            evidence.nuisance_supported,
            False,
        )

    if not evidence.deviation_observed:
        return DecisionRecord(
            Decision.BASELINE,
            Reason.BASELINE,
            False,
            False,
            True,
        )

    coupled_target = evidence.coupled_response_supported and evidence.attribution_supported
    target = evidence.target_supported or coupled_target
    nuisance = evidence.nuisance_supported

    if target and nuisance:
        return DecisionRecord(
            Decision.UNDETERMINED,
            Reason.TARGET_NUISANCE_OVERLAP,
            True,
            True,
            True,
        )

    if target:
        return DecisionRecord(
            Decision.TARGET,
            Reason.TARGET_SUPPORT,
            True,
            nuisance,
            True,
        )

    if evidence.coupled_response_supported and not evidence.attribution_supported:
        return DecisionRecord(
            Decision.UNDETERMINED,
            Reason.MISSING_ATTRIBUTION,
            False,
            nuisance,
            True,
        )

    if nuisance:
        return DecisionRecord(
            Decision.NUISANCE,
            Reason.NUISANCE_SUPPORT,
            False,
            True,
            True,
        )

    return DecisionRecord(
        Decision.UNDETERMINED,
        Reason.NO_SUPPORTED_EVIDENCE,
        False,
        False,
        True,
    )


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y"}:
        return True
    if text in {"0", "false", "f", "no", "n", "", "none", "na", "nan"}:
        return False
    raise ValueError(f"cannot parse boolean support flag: {value!r}")


def classify_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    deviation: str = "deviation_observed",
    target: str = "target_supported",
    nuisance: str = "nuisance_supported",
    observable: str = "observable",
    coupled: str = "coupled_response_supported",
    attribution: str = "attribution_supported",
) -> list[dict[str, Any]]:
    """Annotate arbitrary row mappings with TNOA decision and reason fields."""

    annotated = []
    for row in rows:
        evidence = Evidence(
            deviation_observed=_bool(row.get(deviation, False)),
            target_supported=_bool(row.get(target, False)),
            nuisance_supported=_bool(row.get(nuisance, False)),
            observable=_bool(row.get(observable, True)),
            coupled_response_supported=_bool(row.get(coupled, False)),
            attribution_supported=_bool(row.get(attribution, False)),
        )
        result = dict(row)
        result.update(classify(evidence).to_dict())
        annotated.append(result)
    return annotated


def summarize(
    rows: Sequence[Mapping[str, Any]],
    *,
    group_by: Sequence[str] = (),
) -> list[dict[str, Any]]:
    """Return B/T/N/U and U-reason rates, optionally by ecological covariates."""

    groups: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row.get(k) for k in group_by)].append(row)

    output = []
    for key, subset in sorted(groups.items(), key=lambda item: tuple(str(x) for x in item[0])):
        n = len(subset)
        decisions = Counter(str(r["decision"]) for r in subset)
        reasons = Counter(str(r["reason"]) for r in subset if str(r["decision"]) == Decision.UNDETERMINED.value)
        rec: dict[str, Any] = {name: value for name, value in zip(group_by, key)}
        rec.update(
            {
                "n": n,
                "baseline_rate": decisions["B"] / n,
                "target_rate": decisions["T"] / n,
                "nuisance_rate": decisions["N"] / n,
                "undetermined_rate": decisions["U"] / n,
                "u_no_supported_evidence_rate": reasons[Reason.NO_SUPPORTED_EVIDENCE.value] / n,
                "u_overlap_rate": reasons[Reason.TARGET_NUISANCE_OVERLAP.value] / n,
                "u_missing_attribution_rate": reasons[Reason.MISSING_ATTRIBUTION.value] / n,
                "u_insufficient_observability_rate": reasons[Reason.INSUFFICIENT_OBSERVABILITY.value] / n,
            }
        )
        output.append(rec)
    return output
