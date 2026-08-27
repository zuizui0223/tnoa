# When should an ecological sensor refuse to decide? Target–nuisance–observability–abstention for process-preserving ecological sensing

## Abstract

**1.** Ecological sensors increasingly automate event detection, but weak target evidence can result from true absence, exogenous disturbance, inadequate measurement support, missing attribution, or genuine coexistence of biological and non-biological processes. Existing methods address important parts of this problem, including imperfect detection, reject-option and set-valued prediction, uncertainty representation and observation-process modelling. We develop target–nuisance–observability–abstention (TNOA) as an integrated ecological sensor-decision architecture rather than as a new event classifier.

**2.** TNOA defines target and nuisance as positive, non-complementary process hypotheses; separates direct target evidence, attributed target-coupled response, exogenous nuisance evidence and observability; permits target+nuisance coexistence; and requires an independent channel if target absence is to be certified. We evaluated the resulting decision contract in a closed synthetic world over six dimensionless process/observation coordinates. Observer generations were frozen before one-shot evaluation, failed hypotheses were retained, and nuisance decisions were calibrated against a predeclared false-certainty budget rather than inherited raw-score thresholds.

**3.** The final frozen measurement comprised 30,625 phase-space coordinates and 5,880,000 synthetic worlds with no observer retuning after freeze. Under equal weighting of the registered grid and latent regimes, decision rates were approximately 0.230 baseline, 0.429 target, 0.088 nuisance and 0.253 undetermined. Most undetermined outcomes in that registered design were associated with overlap or attribution rather than the historical no-support category. Longer observation did not monotonically remove abstention because additional information could reveal genuine process coexistence. The registered hypothesis of a narrow ambiguity ridge near equal target and nuisance timescales was not supported.

**4.** TNOA does not claim to introduce abstention, imperfect-detection correction, set-valued prediction or evidence uncertainty individually. Its contribution is the integrated ecological sensor-decision contract and the frozen dimensionless decision geometry induced by that contract. The present study establishes a closed-world methodological result; field accuracy, field absence certification and transfer of quantitative thresholds remain external-validation tasks.

## Keywords

ecological sensing; imperfect detection; abstention; observability; nuisance process; uncertainty; camera monitoring; measurement error

## Data/Code for peer review statement

An anonymized reviewer package containing the manuscript-facing code, paper manifest, claim traceability, figure-generation scripts and the locked result summaries required for review will be supplied either as reviewer-only uploaded files or through a private-for-peer-review archive. The anonymous manuscript will not identify the public repository owner. Permanent public repository/archive links and accession information will be supplied in the Data Availability Statement at acceptance or when journal policy permits de-anonymization.

## Manuscript structure after this front matter

Append, in order, the current audited body from `manuscript/TNOA_P1_DRAFT.md` beginning at `## 1. Introduction`, followed by references, figures/tables and captions. Re-run `scripts/audit_manuscript_claims.py` after the formatted document is materially edited.
