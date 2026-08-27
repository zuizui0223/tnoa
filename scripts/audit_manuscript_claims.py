#!/usr/bin/env python3
"""Fail-closed claim scan for the MEE-focused TNOA draft."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "TNOA_MEE_DRAFT.md"

FORBIDDEN_PHRASES = (
    "tnoa is the first",
    "first abstaining ecological classifier",
    "first framework to separate process and observation",
    "introduces the idea that nondetection is not absence",
    "no previous method separates",
    "uniquely represents ignorance",
    "first method to retain multiple hypotheses",
    "proves that tnoa",
    "proves tnoa",
    "universal ecological snr threshold",
    "field-validated accuracy",
    "field validated accuracy",
    "six-dimensional ecological complexity",
    "tnoa achieves zero false positives",
)

NUMERIC_CLAIM_REQUIREMENTS = {
    "30,625": "C8",
    "5,880,000": "C8",
    "0.55": "C6",
    "0.04444": "C7",
    "3,003": "D1",
    "99.63%": "D1",
    "-0.238": "D1",
    "0.030": "D1",
    "0.266": "D1",
    "84.45%": "D1",
    "0.02675": "C10",
    "0.22658": "C10",
    "0.6431": "D2",
    "0.0214": "D2",
    "0.3569": "C13",
    "0.196125": "C13",
}

QUALIFICATION_CHECKS = (
    (r"Pi3=0|\\Pi_3=0|`Pi3=0`", "C12", "Pi3 structural result"),
    (r"Pi2\s*~=\s*1|Pi2≈1|\\Pi_2\\approx1|`Pi2=1`", "C2", "Pi2 ridge result"),
)

COMMENT_PREFIX = re.compile(r"^<!--\s*([CD]\d+(?:\s+[CD]\d+)*)\s*-->")


def fail(message: str) -> None:
    raise SystemExit(f"TNOA manuscript claim audit failed: {message}")


def paragraphs(text: str) -> list[str]:
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]


def has_claim_tag(ps: list[str], index: int, claim_id: str) -> bool:
    if claim_id in ps[index]:
        return True
    for neighbor in (index - 1, index + 1):
        if neighbor < 0 or neighbor >= len(ps):
            continue
        match = COMMENT_PREFIX.match(ps[neighbor])
        if match and claim_id in match.group(1).split():
            return True
    return False


def main() -> None:
    if not DRAFT.is_file():
        fail(f"missing MEE manuscript: {DRAFT.relative_to(ROOT)}")

    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            fail(f"forbidden priority/claim phrase present: {phrase!r}")

    ps = paragraphs(text)
    for token, claim_id in NUMERIC_CLAIM_REQUIREMENTS.items():
        matched = [i for i, paragraph in enumerate(ps) if token in paragraph]
        if not matched:
            fail(f"expected central numerical claim token missing: {token}")
        for index in matched:
            if not has_claim_tag(ps, index, claim_id):
                fail(f"numerical claim {token} lacks {claim_id} traceability")

    for pattern, claim_id, label in QUALIFICATION_CHECKS:
        for index, paragraph in enumerate(ps):
            if re.search(pattern, paragraph):
                empirical = any(
                    word in paragraph.lower()
                    for word in ("result", "rate", "failed", "not supported", "surface", "contrast", "vector")
                )
                if empirical and not has_claim_tag(ps, index, claim_id):
                    fail(f"{label} lacks {claim_id} traceability")

    required_phrases = (
        "not a field bias estimate",
        "not intrinsic-dimension estimates",
        "not a performance claim",
        "does not claim priority",
        "design coverage and provenance",
    )
    for phrase in required_phrases:
        if phrase not in lower:
            fail(f"required qualification missing: {phrase!r}")

    print(
        "TNOA MEE manuscript claim scan OK: "
        f"{len(ps)} paragraphs, {len(NUMERIC_CLAIM_REQUIREMENTS)} numeric provenance guards"
    )


if __name__ == "__main__":
    main()
