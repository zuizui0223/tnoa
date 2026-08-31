#!/usr/bin/env python3
"""Build the anonymous MEE initial-submission Markdown source.

This is an editorial assembly step. It does not alter scientific results. The
output combines the numbered abstract/front matter with the active MEE body,
normalizes the journal-standard section name, removes internal provenance tags,
adds figure callouts, and appends figure captions.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
BODY = ROOT / "manuscript" / "TNOA_MEE_DRAFT.md"
OUT = ROOT / "submission" / "generated" / "MEE_INITIAL_SUBMISSION_SOURCE.md"

C_TAG = re.compile(r"\s*<!--\s*[CD]\d+(?:\s+[CD]\d+)*\s*-->")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
FORBIDDEN = ("zuizui0223", "github.com/zuizui0223", "raw.githubusercontent.com/zuizui0223")

CAPTIONS = r"""
## Figure captions

**Figure 1. TNOA observation-state interface.** Conceptual separation of the world/process layer, evidence channels, B/T/N/U observation states and development safeguards. Target and nuisance are positive, non-complementary supports; measurement support is separate; target-coupled response requires attribution; and unresolved observations are retained rather than converted automatically to biological absence.

**Figure 2. A raw nuisance-score threshold did not retain its operating meaning after the score representation changed.** (a) Nuisance ranking against both registered negative families remained strong while recall at the inherited threshold 0.55 fell to 0.23125. (b) Pass rates of spatial, temporal and combined nuisance components across registered Pi5 values at the inherited 0.55 boundary show that the numerical threshold no longer represented a stable process boundary. (c) A pooled false-attribution calibration exceeded the predeclared alpha=0.05 criterion for the coupled negative family, whereas the max-over-predeclared-families calibration reduced held-out false nuisance attribution to approximately 0.04444 while retaining nuisance coverage. All values are closed-world empirical validation results, not distribution-free guarantees or field false-positive rates. <!-- C6 C7 -->

**Figure 3. Information about synthetic latent target prevalence retained by the four-state observation record.** (a) Quantiles of the bias obtained when the TARGET observation proportion is used naively as a binary estimate of known latent target prevalence across 3,003 registered regime compositions. (b) Quantiles of partial-identification width when B/T/N/U are retained versus after deterministic coarsening to TARGET/not-TARGET. The composition lattice is a sensitivity design, not an ecological prior, and the result is not a field prevalence estimate. <!-- D1 -->

**Figure 4. Composition and robustness of unresolved observations.** (a) Equal-weight no-supported-evidence U, overlap/attribution U and total U across registered Pi1 values. After Pi1=1, no-support decreases while overlap/attribution continues to increase; overlap/attribution dominates total U throughout the registered Pi1 levels. (b) Worst-case overlap/attribution share of U under the tested bounded density-ratio reweighting class. The robustness statement applies only to that explicit weighting class. <!-- C10 C11 D1 D2 -->

**Supplementary Figure S2. Uneven marginal separation across the six registered synthetic coordinates.** For each coordinate, the panel reports the maximum total-variation distance between marginal level-mean B/T/N/U distributions. These values describe the frozen registered design and are not estimates of intrinsic ecological dimensionality. <!-- D2 -->
""".strip()


def fail(message: str) -> None:
    raise SystemExit(f"MEE initial-submission source build failed: {message}")


def main() -> None:
    if not FRONT.is_file() or not BODY.is_file():
        fail("front matter or active MEE body missing")
    front = FRONT.read_text(encoding="utf-8")
    body = BODY.read_text(encoding="utf-8")
    if "## 1. Introduction" not in body:
        fail("active MEE body lacks Introduction marker")

    front = front.split("## Manuscript structure after this front matter", 1)[0].rstrip()
    body = "## 1. Introduction" + body.split("## 1. Introduction", 1)[1]
    body = body.replace("## 2. Methods", "## 2. Materials and Methods", 1)
    body = C_TAG.sub("", body)

    callouts = {
        "### 3.1 An inherited raw threshold failed even when nuisance ranking was retained": "### 3.1 An inherited raw threshold failed even when nuisance ranking was retained\n\n*See Figure 2a–c.*",
        "### 3.2 Progressive coarsening discarded information about downstream ecological estimands": "### 3.2 Progressive coarsening discarded information about downstream ecological estimands\n\n*See Figure 3a–b.*\n\nThe post-freeze reason-resolved vocabulary ablation is reported in the text and supplementary analysis files; Figure 3 retains the frozen B/T/N/U-versus-binary target-prevalence comparison.",
        "### 3.4 Unresolved observations were dominated by overlap/attribution, but observation duration is secondary": "### 3.4 Unresolved observations were dominated by overlap/attribution, but observation duration is secondary\n\n*See Figure 4a–b.*",
        "### 3.5 The six registered coordinates had strongly uneven effective separation": "### 3.5 The six registered coordinates had strongly uneven effective separation\n\n*See Supplementary Figure S2.*",
    }
    for old, new in callouts.items():
        if old not in body:
            fail(f"expected result heading missing: {old}")
        body = body.replace(old, new, 1)

    output = front + "\n\n---\n\n" + body.rstrip() + "\n\n" + C_TAG.sub("", CAPTIONS) + "\n"
    lower = output.lower()
    for literal in FORBIDDEN:
        if literal.lower() in lower:
            fail(f"identity-bearing public repository literal remains: {literal}")
    if EMAIL.search(output):
        fail("email address remains in anonymous initial-submission source")
    if "<!-- C" in output or "<!-- D" in output:
        fail("internal provenance comments remain in initial-submission source")
    if "## 2. Materials and Methods" not in output:
        fail("journal-standard Materials and Methods heading was not produced")
    if "## Figure captions" not in output:
        fail("figure captions missing")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(output, encoding="utf-8")
    print(f"Built MEE initial-submission source: {OUT}")


if __name__ == "__main__":
    main()
