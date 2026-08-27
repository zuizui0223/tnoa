# MEE vocabulary map

This file fixes the language used in the MEE manuscript. The mathematical object does not change; the reader-facing vocabulary moves closer to ecological observation models and imperfect-detection practice.

| Internal / development term | Preferred MEE wording | Why |
| --- | --- | --- |
| decision entitlement | observation-state support / whether an observation supports a biological statement | avoids legal/philosophical tone |
| sensor-decision contract | observation-state mapping / observation model interface | connects to ecological observation models |
| false certainty | false positive process attribution / unsupported positive attribution | makes the error type concrete |
| risk contract | prespecified error-rate criterion | familiar statistical wording |
| target-supported T | positive target-evidence observation | separates evidence from latent truth |
| nuisance-supported N | positive nuisance-process observation | avoids treating nuisance as `not target` |
| U / abstention | unresolved observation state | reads as an observation category rather than classifier reluctance |
| no-supported-evidence U | unresolved because neither positive process is sufficiently supported | avoids claiming information absence |
| overlap/attribution U | unresolved because processes coexist or attribution is insufficient | exposes observation-process reason |
| T+N superposition | co-occurring target and nuisance processes | ecological wording |
| O / observability | measurement support / observation quality sufficient for the focal inference | connects to detection-process language |
| A− | independently validated absence evidence | keeps absence distinct from non-detection |
| phase-space frequency | registered design-space proportion | never ecological prevalence |
| six-dimensional phase space | six-coordinate registered synthetic design | avoids implying six effective dimensions |
| forced-binary comparator | binary coarsening of the observation record | emphasizes information loss |
| false-negative rate 0.3569 | equal-grid comparator diagnostic | not performance |
| partial-identification width | range of latent target prevalences compatible with the retained observation categories | gives ecological estimand first |
| latent regime mixture | synthetic composition of ecological/observation regimes | closer to population composition |
| representation change | change in nuisance-score representation | concrete wording |
| inherited raw threshold | threshold copied from an earlier score scale | makes failure mechanism explicit |
| family-wise false-certainty budget | prespecified family-wise false-attribution rate | statistical wording |

## Manuscript framing rules

1. Start from the downstream ecological problem: automated sensors emit observations that later feed occupancy, interaction-rate or other ecological models.
2. Describe B/T/N/U as **observation states**, not natural classes.
3. Use `unresolved observation` before `abstention`; reserve `abstention` for connection to machine-learning literature.
4. Introduce the error-rate calibration as a prespecified false-attribution criterion before using the internal phrase `risk contract`.
5. Present the known-truth prevalence analysis as an observation-model coarsening experiment: retaining four observation states versus collapsing them to target/not-target.
6. Treat the six Pi axes as experimental coordinates. Do not imply equal importance or intrinsic dimensionality.
7. Treat the 30,625-coordinate / 5.88M count as reproducibility and design-coverage information, not a headline result.
8. C13 is not a performance claim. If reported, immediately give its Pi3 composition identity.
9. The Pi1 result is reason substitution, not generic non-monotonicity: after Pi1=1, no-support U declines while overlap/attribution rises.
10. The strongest result order is: nuisance threshold-scale failure and prespecified error control -> downstream ecological estimand information loss -> preregistered Pi2 negative result -> robust U reason composition.
