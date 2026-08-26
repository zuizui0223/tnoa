#!/usr/bin/env python3
"""Fail-closed claim scan for the instantiated TNOA Paper-1 draft.

This is a narrow repository guard, not a semantic peer reviewer. It blocks known
priority overclaims and requires internal C-ID provenance tags around the central
locked numerical claims.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "TNOA_P1_DRAFT.md"

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
)

NUMERIC_CLAIM_REQUIREMENTS = {
    "30,625": "C8",
    "5,880,000": "C8",
    "0.2302": "C9",
    "0.4287": "C9",
    "0.0877": "C9",
    "0.2533": "C9",
    "0.02675": "C10",
    "0.22658": "C10",
    "0.3569": "C13",
    "35.69%": "C13",
    "0.04444": "C7",
    "0.0444": "C7",
}

QUALIFICATION_CHECKS = (
    (r"Pi3=0|\\Pi_3=0", "C12", "Pi3 structural result"),
    (r"Pi2\s*~=\s*1|Pi2≈1|\\Pi_2\\approx1|\\Pi_2=1", "C2", "Pi2 ridge result"),
)


def fail(message: str) -> None:
    raise SystemExit(f"TNOA manuscript claim audit failed: {message}")


def paragraphs(text: str) -> list[str]:
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]


def main() -> None:
    if not DRAFT.is_file():
        fail(f"missing manuscript draft: {DRAFT.relative_to(ROOT)}")

    text = DRAFT.read_text(encoding="utf-8")
    lower = text.lower()

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            fail(f"forbidden priority/claim phrase present: {phrase!r}")

    ps = paragraphs(text)

    for token, claim_id in NUMERIC_CLAIM_REQUIREMENTS.items():
        matched = [p for p in ps if token in p]
        if not matched:
            fail(f"expected central numerical claim token missing: {token}")
        for paragraph in matched:
            if claim_id not in paragraph:
                fail(f"numerical claim {token} lacks {claim_id} traceability in its paragraph")

    for pattern, claim_id, label in QUALIFICATION_CHECKS:
        for paragraph in ps:
            if re.search(pattern, paragraph):
                # Method-definition occurrences can be untagged; empirical/result
                # occurrences using directional language must carry the claim ID.
                empirical = any(
                    word in paragraph.lower()
                    for word in ("result", "rate", "failed", "not supported", "surface", "contrast")
                )
                if empirical and claim_id not in paragraph:
                    fail(f"{label} lacks {claim_id} traceability in an empirical paragraph")

    if "not a universal ecological frequency" not in lower and "not a universal" not in lower:
        fail("draft must retain an explicit non-universality qualification")
    if "not a field" not in lower and "field accuracy" not in lower:
        fail("draft must retain the field-validation boundary")
    if "does not claim" not in lower:
        fail("draft must explicitly disclaim component-level novelty")

    print(
        "TNOA manuscript claim scan OK: "
        f"{len(ps)} paragraphs, {len(NUMERIC_CLAIM_REQUIREMENTS)} numeric provenance guards"
    )


if __name__ == "__main__":
    main()
