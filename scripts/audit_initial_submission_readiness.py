#!/usr/bin/env python3
"""Audit MEE initial-submission readiness that can be checked without author metadata.

The audit is intentionally conservative. It checks the generated anonymous
submission source, citation coverage, a reproducible word-count estimate including
bibliography text, and reviewer-package invariants. It does not replace the
journal's own word counter after conversion to the final upload format.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "submission" / "generated" / "MEE_INITIAL_SUBMISSION_SOURCE.md"
BIB = ROOT / "references.bib"
SUBMISSION = ROOT / "submission" / "submission_manifest.json"
REPORT = ROOT / "submission" / "generated" / "initial_submission_readiness.json"

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*")
CITATION_RE = re.compile(r"@([A-Za-z0-9_:\-.]+)")
BIBKEY_RE = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
MATH_RE = re.compile(r"\\\[.*?\\\]", re.S)
LINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
CITATION_BLOCK_RE = re.compile(r"\[@[^\]]+\]")
BIB_FIELD_RE = re.compile(
    r"=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\")\s*,?",
    re.S,
)

MAX_STANDARD_ARTICLE_WORDS = 8000
GUIDANCE_CHECKED = "2026-08-27"


def fail(message: str) -> None:
    raise SystemExit(f"MEE initial-submission readiness failed: {message}")


def visible_words(text: str) -> int:
    text = COMMENT_RE.sub(" ", text)
    text = CODE_FENCE_RE.sub(" ", text)
    text = MATH_RE.sub(" ", text)
    text = CITATION_BLOCK_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"[`*_#>|]", " ", text)
    return len(WORD_RE.findall(text))


def bibliography_words(text: str) -> int:
    count = 0
    for left, right in BIB_FIELD_RE.findall(text):
        value = left or right
        count += len(WORD_RE.findall(value))
    return count


def main() -> None:
    for path in (SOURCE, BIB, SUBMISSION):
        if not path.is_file():
            fail(f"missing required source: {path.relative_to(ROOT)}")

    source = SOURCE.read_text(encoding="utf-8")
    bib = BIB.read_text(encoding="utf-8")
    submission = json.loads(SUBMISSION.read_text(encoding="utf-8"))

    required_sections = (
        "## Abstract",
        "## Data/Code for peer review statement",
        "## Keywords",
        "## 1. Introduction",
        "## 2. Materials and Methods",
        "## 3. Results",
        "## 4. Discussion",
        "## 5. Conclusions",
        "## Data and code availability",
        "## Figure captions",
    )
    for heading in required_sections:
        if heading not in source:
            fail(f"required manuscript section missing: {heading}")

    for label in ("**1.**", "**2.**", "**3.**", "**4.**"):
        if label not in source:
            fail(f"numbered abstract item missing: {label}")
    for caption in ("**Figure 1.", "**Figure 2.", "**Figure 3.", "**Figure 4.", "**Supplementary Figure S2."):
        if caption not in source:
            fail(f"figure caption missing: {caption}")
    for callout in ("*See Figure 2a–c.*", "*See Figure 3a–b.*", "*See Figure 4a–b.*", "*See Supplementary Figure S2.*"):
        if callout not in source:
            fail(f"figure callout missing: {callout}")

    cited = set(CITATION_RE.findall(source))
    bibkeys = set(BIBKEY_RE.findall(bib))
    missing = sorted(cited - bibkeys)
    if missing:
        fail(f"citation keys missing from references.bib: {missing}")
    unused = sorted(bibkeys - cited)

    source_count = visible_words(source)
    ref_count = bibliography_words(bib)
    estimated_total = source_count + ref_count
    if estimated_total > MAX_STANDARD_ARTICLE_WORDS:
        fail(
            f"estimated Standard Article word count {estimated_total} exceeds "
            f"conservative {MAX_STANDARD_ARTICLE_WORDS}-word ceiling"
        )

    if submission.get("scientific_submission_blockers") != 0:
        fail("scientific submission blockers are not zero")
    peer = submission.get("peer_review_code_data", {})
    if peer.get("status") != "deterministic bundle builder implemented and CI-validated against pinned upstream source checkouts":
        fail("anonymous reviewer bundle is not registered as CI-validated")

    report = {
        "schema": "tnoa-mee-initial-submission-readiness-v1",
        "journal": "Methods in Ecology and Evolution",
        "guidance_checked_date": GUIDANCE_CHECKED,
        "word_count": {
            "assembled_source_visible_words": source_count,
            "bibliography_field_words_estimate": ref_count,
            "estimated_total_including_references": estimated_total,
            "conservative_ceiling": MAX_STANDARD_ARTICLE_WORDS,
            "note": "Final journal-formatted file must be checked again because publisher word-count conventions can differ.",
        },
        "citations": {
            "cited_key_count": len(cited),
            "bibliography_entry_count": len(bibkeys),
            "missing_cited_keys": missing,
            "unused_bibliography_keys": unused,
        },
        "machine_checkable_initial_submission_gates": {
            "numbered_abstract": True,
            "data_code_peer_review_statement": True,
            "standard_sections": True,
            "figure_captions_present": True,
            "figure_callouts_present": True,
            "citation_keys_resolve": True,
            "scientific_submission_blockers_zero": True,
            "anonymous_reviewer_bundle_ci_validated": True,
        },
        "human_only_remaining": [
            "convert to final single-column double-line-spaced upload format with continuous page and line numbering",
            "check final formatted word count under publisher convention",
            "complete separate title page with author metadata, contributions and acknowledgements",
            "build final reviewer ZIP with author/institution literals passed to --forbid-literal and place it in reviewer-only/private location",
            "final visual inspection of multi-panel figure layout and reference style",
        ],
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        "MEE initial-submission readiness OK: "
        f"estimated {estimated_total} words incl. bibliography estimate; "
        f"{len(cited)} cited keys resolved; {len(unused)} unused bibliography entries"
    )


if __name__ == "__main__":
    main()
