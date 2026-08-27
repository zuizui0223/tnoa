# Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework

## Abstract

**1.** Automated ecological sensors increasingly create detections and non-detections for occupancy, interaction and state-space analyses. Yet a non-detection can represent true absence, inadequate measurement support, nuisance processes, missing attribution or genuine target–nuisance co-occurrence. Collapsing these situations at the sensor interface can irreversibly discard observation-process information before ecological analysis.

**2.** We develop target–nuisance–observability–abstention (TNOA) as an observation-state interface rather than a new event classifier. Target and nuisance are positive, non-complementary supports; measurement support is separate; target-coupled responses require attribution; and biological absence requires independent evidence. Using frozen observer generations, we tested TNOA in a registered six-coordinate synthetic design, calibrated nuisance decisions against a prespecified family-wise false-attribution criterion, and quantified information loss about known latent target prevalence after binary coarsening. A minimal Python API and fail-closed translation sequence support reuse after domain-specific calibration.

**3.** After the nuisance representation changed, ranking was retained but an inherited raw threshold failed its registered coverage rule; family-wise calibration at `alpha=0.05` yielded held-out false nuisance attribution of 0 and approximately 0.0444 in the two registered negative families. Across 3,003 latent-regime compositions, naive binary target prevalence was negatively biased in 99.63% of compositions (median approximately -0.238), while median compatible target-prevalence width was approximately 0.030 with B/T/N/U retained versus 0.266 after binary coarsening. The preregistered matched-timescale ambiguity ridge was not supported; overlap/attribution remained the majority unresolved reason through the tested bounded-reweighting class, whereas the exact observation-duration curve was weighting-sensitive.

**4.** The methodological consequence is upstream of any particular ecological model: preserve observation-process distinctions and calibrate decisions against explicit error criteria rather than inherited score values. In a new sensing system, raw evidence should remain unresolved until independent truth, grouped development calibration and frozen held-out evaluation establish the evidence channels. This is implementation guidance, not field validation. The current quantitative results remain closed-world rather than field-calibrated.

## Keywords

abstention; automated monitoring; ecological sensing; imperfect detection; measurement error; observation model; partial identification; sensor calibration

## Data/Code for peer review statement

An anonymized reviewer package will include the manuscript-facing code, the minimal reusable TNOA Python API and CSV example, paper manifest, claim traceability, derived-analysis summaries and figure-generation scripts. Locked historical results are identified by immutable workflow/artifact hashes. The anonymous manuscript will not identify the public repository owner; permanent public repository/archive links and accession information will be supplied when journal policy permits de-anonymization.

## Manuscript structure after this front matter

Append the MEE-focused body from `manuscript/TNOA_MEE_DRAFT.md` beginning at `## 1. Introduction`, followed by references, figures/tables and captions. Re-run the manuscript claim audit after any material edit.
