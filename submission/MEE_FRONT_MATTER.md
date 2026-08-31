# Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework

## Abstract

**1.** Automated ecological sensors increasingly create detections and non-detections for occupancy, interaction and state-space analyses. Yet a non-detection can represent true absence, inadequate measurement support, nuisance processes, missing attribution or genuine target–nuisance co-occurrence. Collapsing these situations at the sensor interface can irreversibly discard observation-process information before ecological analysis.

**2.** We develop target–nuisance–observability–abstention (TNOA) as an upstream observation contract rather than a new event classifier or uncertainty calculus. Target and nuisance are positive, non-complementary supports; measurement support is separate; target-coupled responses require attribution; and biological absence requires independent evidence. Using frozen observer generations, we tested TNOA in a registered six-coordinate synthetic design and quantified information loss under progressively coarser observation vocabularies. A minimal Python API and fail-closed translation sequence support reuse after domain-specific calibration.

**3.** After the nuisance representation changed, ranking was retained but an inherited raw threshold failed its registered coverage rule. A predeclared family-conditional false-attribution criterion at `alpha=0.05` yielded held-out false nuisance attribution of `0/43,200` and `1,920/43,200` (`0.0444`) in the two negative families. Across 3,003 latent-regime compositions, median compatible target-prevalence width was `0.2656` for target/not-target, `0.1886` for target/nuisance/other, `0.0299` for B/T/N/U and `0.00408` when unresolved reasons were retained. The latter ablation was post-freeze and not preregistered. The preregistered matched-timescale ambiguity ridge was not supported.

**4.** TNOA's contribution is therefore process-semantic rather than priority for abstention, uncertain ecological events or continuous classifier scores: preserve target, nuisance, observability and attribution provenance before downstream inference, and calibrate process-support decisions against explicit error criteria rather than inherited score values. Current quantitative results are closed-world; field translation requires independent truth, grouped development calibration and frozen held-out evaluation.

## Keywords

abstention; automated monitoring; ecological sensing; imperfect detection; measurement error; observation model; partial identification; sensor calibration

## Data/Code for peer review statement

An anonymized reviewer package will include the manuscript-facing code, the minimal reusable TNOA Python API and CSV example, paper manifest, claim traceability, derived-analysis summaries and figure-generation scripts. Locked historical results are identified by immutable workflow/artifact hashes. The anonymous manuscript will not identify the public repository owner; permanent public repository/archive links and accession information will be supplied when journal policy permits de-anonymization.

## Manuscript structure after this front matter

Append the MEE-focused body from `manuscript/TNOA_MEE_DRAFT.md` beginning at `## 1. Introduction`, followed by references, figures/tables and captions. Re-run the manuscript claim audit after any material edit.
