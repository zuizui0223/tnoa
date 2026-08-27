# MEE front matter for anonymised main manuscript

## Abstract

**1.** Ecological sensors increasingly automate event detection, but weak target evidence can reflect true absence, exogenous disturbance, poor measurement support, missing attribution, representation failure, or genuine coexistence of target and nuisance processes. Existing methods address important parts of this problem, including imperfect detection, reject-option and set-valued prediction, open-set recognition, evidence uncertainty, and observation-process modelling. We develop target–nuisance–observability–abstention (TNOA) as an integrated ecological sensor-decision architecture that asks when an observation licenses a biological decision and when abstention should be retained.

**2.** TNOA treats target and nuisance as positive, non-complementary process hypotheses; separates direct target evidence, attribution-gated target-coupled response, exogenous nuisance evidence and measurement observability; and requires an independent channel if target absence is to be certified. We evaluated the architecture in closed synthetic worlds spanning six dimensionless process and observation coordinates. Observer rules were frozen before held-out measurement, failed generations were retained, and nuisance decisions were calibrated against a predeclared false-certainty budget rather than inherited raw-score thresholds.

**3.** The final frozen measurement comprised 30,625 phase-space coordinates and 5,880,000 synthetic worlds with no observer retuning after freeze. Under equal weighting of the registered grid and latent regimes, decision rates were approximately 0.230 baseline, 0.429 target, 0.088 nuisance and 0.253 undetermined. Most undetermined outcomes in that design arose from overlap or attribution rather than the historical no-support category. Longer observation did not monotonically remove abstention, and the preregistered hypothesis of a narrow ambiguity ridge near equal target and nuisance timescales was not supported.

**4.** TNOA does not claim priority for abstention, imperfect-detection correction, set-valued prediction or evidence uncertainty. Its contribution is the integrated ecological sensor-decision contract and the frozen dimensionless decision geometry induced by that contract. The present study establishes a closed-world methodological result; field accuracy, field absence certification and transfer of quantitative thresholds remain external-validation tasks.

## Keywords

ecological sensing; imperfect detection; abstention; observability; nuisance process; uncertainty; camera monitoring; measurement error

## Data/Code for peer review

Code, synthetic benchmark summaries, result provenance and figure-generation scripts required to evaluate the submitted method will be made available to editors and reviewers through the journal's reviewer-facing upload mechanism or an anonymised/private peer-review repository. The peer-review package will preserve the immutable workflow/run/hash provenance recorded in `paper_manifest.json` while avoiding author-identifying public links in the blinded manuscript.

## Main-text anonymity guard

Do not place author names, institutional affiliations, acknowledgements, personal repository-owner names, or author-identifying phrases such as “in our previous study” in the blinded manuscript. The separate title page contains author-identifying metadata.
