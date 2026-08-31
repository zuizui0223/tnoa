# Structural result audit for MEE positioning

This audit is downstream of the locked V14b/V14c science. It does not rerun or retune an observer. Its purpose is to separate findings that are informative consequences of the experiment from quantities that are largely induced by the registered design.

## 1. Pi1: keep the reason decomposition, demote the total-shape claim

The existing Figure 2 already contains the required decomposition. Across deviation regimes:

| Pi1 | no-supported-evidence U | overlap/attribution U | total U | overlap share of U |
| ---: | ---: | ---: | ---: | ---: |
| 0.1 | 0.0205 | 0.2063 | 0.2268 | 0.910 |
| 0.316 | 0.0391 | 0.2355 | 0.2746 | 0.857 |
| 1 | 0.0539 | 0.2751 | 0.3290 | 0.836 |
| 3.162 | 0.0268 | 0.3190 | 0.3458 | 0.922 |
| 10 | 0.0201 | 0.3236 | 0.3438 | 0.941 |

The components genuinely diverge after `Pi1=1`: from 1 to 3.162, no-support U falls by 0.0271 while overlap/attribution U rises by 0.0439. Thus longer windows can replace evidence shortage with an attribution/coexistence problem.

However, overlap/attribution accounts for about 84–94% of U at every registered Pi1 level. The total-U curve is therefore dominated by overlap, and the post-freeze density-ratio audit showed that the exact total-U shape is not strongly weighting-robust. Paper 1 should **not** headline a generic “non-monotonicity” result. The defensible statement is narrower:

> In the registered design, extending the observation window did not automatically resolve U; after Pi1=1, the no-support component decreased while overlap/attribution continued to increase.

This is a secondary mechanistic illustration, not the primary paper result.

## 2. Six nominal axes do not have six equally effective response dimensions

For each axis, the audit marginalizes equally over the other registered axes and non-baseline latent regimes, computes the mean B/T/N/U decision vector at each level, and reports the maximum total-variation distance between level means. This is a descriptive separability audit, not a causal variance decomposition.

| axis | registered levels | distinct marginal decision vectors | max TV shift | marginal between-level squared fraction |
| --- | ---: | ---: | ---: | ---: |
| Pi1 | 5 | 5 | 0.2665 | 0.0196 |
| Pi2 | 7 | 7 | 0.2402 | 0.0218 |
| Pi3 | 5 | **2** | **0.6431** | **0.1515** |
| Pi4 | 5 | 5 | 0.0728 | 0.00148 |
| Pi5 | 7 | 6 | 0.0214 | 0.000244 |
| Pi6 | 5 | 5 | 0.1608 | 0.00741 |

The important result is not “six-dimensional complexity.” `Pi3` behaves as a structural binary axis: the four registered positive levels are numerically identical after marginalization. `Pi4` and especially `Pi5` are weak marginal separators of the final decision vector in this frozen generation. `Pi1`, `Pi2` and `Pi6` alter decision composition, but their effects are substantially smaller than the structural zero/non-zero `Pi3` split.

Therefore the manuscript should describe the experiment as a **six-coordinate registered design** but should not imply six equally effective dimensions. The 30,625-coordinate and 5.88M-world counts are provenance/design-coverage facts, not evidence strength.

## 3. C13 is a design-compositional diagnostic, not a performance result

The registered forced-binary false-negative rate is 0.3569 among target-present synthetic worlds. Its Pi3 decomposition is:

- `Pi3=0`: false-negative rate = 1.0;
- each positive Pi3 level: false-negative rate = 0.196125.

Because the equal grid gives one fifth of Pi3 mass to zero and four fifths to positive levels,

`0.3569 = 0.2 * 1.0 + 0.8 * 0.196125`.

Thus 0.3569 is strongly determined by the registered grid composition. Likewise, the zero target false-positive rate follows the frozen positive-target observer on the registered non-target regimes and should not be presented as empirical specificity.

C13 remains useful only as an illustration of what the **registered comparator** does when U is collapsed. The prevalence-mixture analyses are the stronger downstream ecological result because they ask how much estimand information is lost across many latent-regime compositions rather than promoting one equal-grid miss rate.

## 4. Final result hierarchy

### Primary

1. **C6 -> C7: representation ranking survived while inherited threshold meaning failed; a predeclared family-conditional false-attribution criterion restored the declared held-out operating meaning.** This is the cleanest non-trivial methodological result because the failure was observed rather than built into the ontology. The historical source files retain the development label `familywise`, but the manuscript does not claim classical FWER or distribution-free control.
2. **D1/D3/D4 downstream information consequence:** progressively coarsening the process-preserving observation record widens the compatible sets for known ecological estimands. D1 establishes the B/T/N/U-versus-binary magnitude, D3 shows additional value in reason-resolved U, and D4 shows that the gain persists in rare-target compositions and under bounded reweighting of the 3,003 composition lattice. Deterministic never-wider ordering remains structural rather than a performance claim.
3. **C2 negative result:** the preregistered narrow `Pi2 ~= 1` ambiguity ridge was not supported and was retired without modifying the generator to rescue it.

### Secondary

4. **U reason composition:** overlap/attribution dominates no-support in the registered design and remains a majority under the tested phase-space density-ratio reweighting family.
5. **Pi1 reason substitution:** longer windows can reduce no-support while increasing overlap/attribution, but the exact pooled total-U curve is weighting-sensitive.
6. **Uneven effective axis separation:** the registered six-coordinate design contains a binary-like Pi3 axis and weak Pi4/Pi5 marginal separation.

### Design/provenance diagnostics, not headline results

- pooled equal-grid B/T/N/U percentages;
- the 5.88M world count;
- exact zero-versus-positive Pi3 boundary;
- C13 `0.3569` forced-binary false-negative rate;
- zero target false-positive rate in the registered closed generator.

## 5. Consequence for the abstract

The abstract should lead with **C6/C7** and then the **D1/D3/D4 downstream information consequence**. The current rare-target sensitivity is useful because only `141/3003` simplex compositions have target prevalence `<=0.2`, yet the information-preservation advantage does not disappear there. The failed Pi2 hypothesis may follow as a credibility constraint. The abstract should not use “non-monotonicity” as a headline result, should not present 0.3569 as method performance, and should treat 5.88M as design provenance rather than evidence magnitude.
