# Preserving unresolved observations in automated ecological sensing: a target–nuisance–observability framework

## Abstract

**1.** Automated ecological sensors increasingly emit detections and non-detections that feed downstream occupancy, interaction and state-space analyses. Yet a non-detection can combine true absence, inadequate measurement support, exogenous disturbance, missing attribution and genuine co-occurrence of target and nuisance processes. Collapsing these observation situations before ecological analysis can destroy information that later models cannot recover.

**2.** We develop target–nuisance–observability–abstention (TNOA) as an observation-state interface rather than a new event classifier. Target and nuisance are positive, non-complementary supports; measurement support is separate; target-coupled responses require attribution; and biological absence requires independent evidence. Observer generations were frozen before evaluation. We tested the framework in a registered six-coordinate synthetic design, calibrated nuisance decisions against a prespecified family-wise false-attribution criterion, and quantified how much information about known latent target prevalence is lost when B/T/N/U observations are coarsened to target/not-target. A minimal Python API and CSV interface implement the reusable observation mapping from domain-calibrated support flags, and a fail-closed translation sequence specifies how a new sensing system can move from raw evidence to independently calibrated support without treating pre-calibration output as biological absence.

**3.** A revised nuisance representation retained ranking but an inherited raw threshold failed its registered coverage rule; family-wise calibration at `alpha=0.05` subsequently yielded held-out false nuisance attribution of 0 and approximately 0.0444 in the two registered negative families. Across 3,003 synthetic latent-regime compositions, naive binary target prevalence was negatively biased in 99.63% of compositions (median bias approximately -0.238). The median range of target prevalences compatible with the observation was approximately 0.030 when B/T/N/U were retained versus 0.266 after binary coarsening. The preregistered prediction of a narrow ambiguity ridge near matched target and nuisance timescales was not supported. Overlap/attribution remained the majority reason for unresolved observations through the tested bounded-reweighting class, whereas the exact observation-duration curve was weighting-sensitive.

**4.** The main methodological consequence is upstream of any particular ecological model: preserve observation-process distinctions before fitting the downstream model, and calibrate operational decisions against explicit error criteria rather than inherited score values. For transfer to a new sensor, raw evidence should remain unresolved until independent truth, grouped development calibration and a frozen held-out evaluation establish the meaning of the evidence channels; adaptive control is a later step. This sequence is implementation guidance, not field validation. TNOA does not claim to introduce abstention, imperfect-detection correction or observation-process modelling individually, and the current quantitative results remain closed-world rather than field-calibrated.

## Keywords

ecological sensing; observation model; imperfect detection; measurement error; partial identification; abstention; sensor calibration; automated monitoring

## Data/Code for peer review statement

An anonymized reviewer package will include the manuscript-facing code, the minimal reusable TNOA Python API and CSV example, paper manifest, claim traceability, derived-analysis summaries and figure-generation scripts. Locked historical results are identified by immutable workflow/artifact hashes. The anonymous manuscript will not identify the public repository owner; permanent public repository/archive links and accession information will be supplied when journal policy permits de-anonymization.

## Manuscript structure after this front matter

Append the MEE-focused body from `manuscript/TNOA_MEE_DRAFT.md` beginning at `## 1. Introduction`, followed by references, figures/tables and captions. Re-run the manuscript claim audit after any material edit.
