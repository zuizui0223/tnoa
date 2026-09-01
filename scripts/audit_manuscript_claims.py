#!/usr/bin/env python3
"""Fail-closed claim scan for the MEE-focused TNOA draft."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "TNOA_MEE_DRAFT.md"

FORBIDDEN_PHRASES = (
    "tnoa is the first",
    "no previous method separates",
    "uniquely represents ignorance",
    "proves that tnoa",
    "proves tnoa",
    "universal ecological snr threshold",
    "field-validated accuracy",
    "field validated accuracy",
    "field translation pathway is validated",
    "validated field translation",
    "field-calibrated tnoa",
    "six-dimensional ecological complexity",
    "tnoa achieves zero false positives",
    "distribution-free guarantee provided by tnoa",
    "d3 was preregistered",
    "d4 was preregistered",
    "d5 was preregistered",
    "reason provenance was not merely diagnostic metadata",
    "reason provenance retained information about latent",
    "supports reason provenance as part of the observation contract rather than as logging metadata alone",
    "pollipi",
    "insepi",
)

NUMERIC_CLAIM_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "30,625": ("C8",),
    "5,880,000": ("C8",),
    "0.55": ("C6",),
    "0.04444": ("C7",),
    "43,200": ("C7",),
    "1,920": ("C7",),
    "3,003": ("D1", "D3", "D4"),
    "99.63%": ("D1",),
    "-0.238": ("D1",),
    "`0.030`": ("D1",),
    "`0.266`": ("D1",),
    "84.45%": ("D1",),
    "`0.00408`": ("D3",),
    "`0.01484`": ("D3",),
    "141/3003": ("D4",),
    "4.70%": ("D4",),
    "`0.07410`": ("D4",),
    "`0.000175`": ("D4",),
    "57.5%": ("D4",),
    "`0.0050075`": ("D5",),
    "48.0%": ("D5",),
    "0.02675": ("C10",),
    "0.22658": ("C10",),
    "0.6431": ("D2",),
    "0.0214": ("D2",),
    "0.3569": ("C13",),
    "0.196125": ("C13",),
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
            fail(f"forbidden priority/claim/anonymity phrase present: {phrase!r}")

    ps = paragraphs(text)
    for token, claim_ids in NUMERIC_CLAIM_REQUIREMENTS.items():
        matched = [i for i, paragraph in enumerate(ps) if token in paragraph]
        if not matched:
            fail(f"expected central numerical claim token missing: {token}")
        for index in matched:
            if not any(has_claim_tag(ps, index, claim_id) for claim_id in claim_ids):
                allowed = "/".join(claim_ids)
                fail(f"numerical claim {token} lacks {allowed} traceability")

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
        "performance claim",
        "does not claim priority",
        "design coverage and provenance",
        "we do not estimate field flower-visitor accuracy",
        "do not transfer automatically to another device",
        "implementation guidance, not field validation",
        "no field result from such a deployment is used as evidence in paper 1",
        "deterministic coarsening cannot make the retained record more informative",
        "the empirical result is the size of the information loss",
        "post-freeze and not preregistered",
        "not a distribution-free finite-sample guarantee",
        "continuous-score occupancy already shows",
        "multievent or partial-observation models already preserve uncertain ecological events",
        "fixed validation budget",
        "do not claim greater information per annotation",
        "not specific to the reason semantics",
        "does not attribute that extra narrowing to reason semantics",
        "contains only two aggregated u-reason buckets",
        "reusable api later exposes four u reasons",
    )
    for phrase in required_phrases:
        if phrase not in lower:
            fail(f"required qualification missing: {phrase!r}")

    results = text.split("## 3. Results", 1)[-1].split("## 4. Discussion", 1)[0]
    first = results.find("### 3.1")
    second = results.find("### 3.2")
    third = results.find("### 3.3")
    if not (0 <= first < second < third):
        fail("Results 3.1-3.3 ordering is malformed")
    if "inherited raw threshold" not in results[first:second].lower():
        fail("Results 3.1 must lead with the inherited-threshold failure")
    section32 = results[second:third].lower()
    if "target-prevalence" not in section32 and "target prevalence" not in section32:
        fail("Results 3.2 must lead with the downstream ecological estimand")
    if "the empirical result is the size of the information loss" not in section32:
        fail("Results 3.2 must distinguish structural garbling from empirical loss magnitude")
    if "post-freeze vocabulary ablation" not in section32 or "<!-- d3 -->" not in section32:
        fail("Results 3.2 must retain the D3 post-freeze refinement")
    if "not specific to the reason semantics" not in section32 or "500 unlabeled" not in section32:
        fail("Results 3.2 must retain D5 semantic-specificity control")
    if "rare-target subset" not in section32 or "adversarially" not in section32:
        fail("Results 3.2 must retain D4 prevalence/composition-weight sensitivity")
    if section32.find("`0.030`") > section32.find("99.63%"):
        fail("Results 3.2 must lead with identification-width magnitude before the secondary naive-bias diagnostic")
    if "not supported" not in results[third:].lower() or "pi2" not in results[third:].lower():
        fail("Results 3.3 must retain the preregistered Pi2 negative result")

    section31 = results[first:second].lower()
    if "predeclared family-conditional" not in section31:
        fail("Results 3.1 must use family-conditional calibration semantics")
    if "distribution-free" not in section31:
        fail("Results 3.1 must deny distribution-free guarantee")

    discussion = text.split("## 4. Discussion", 1)[-1]
    if "current experiment does not show that the size of that gain is specific to the selected reason semantics" not in discussion.lower():
        fail("Conclusions must demote semantic-specific D3 interpretation")

    print(
        "TNOA MEE manuscript claim scan OK: "
        f"{len(ps)} paragraphs, {len(NUMERIC_CLAIM_REQUIREMENTS)} numeric provenance guards, D3-D5 controls enforced"
    )


if __name__ == "__main__":
    main()
