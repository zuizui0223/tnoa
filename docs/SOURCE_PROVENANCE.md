# TNOA source provenance

TNOA is an extraction of a methodological result whose implementation history remains in PolliPi and InsePi. This repository should not rewrite or silently regenerate locked scientific results.

## 1. PolliPi source

Repository:

- `https://github.com/zuizui0223/pollipi`

Current main provenance used when TNOA was seeded:

- main commit: `f3b266897f3e9139e6c3fe9ce6b645e25371e092`
- portable target-evidence adapter: `packages/analysis/src/pollipi_analysis/target_evidence.py`
- adapter Git blob SHA-1: `4be5f7c88edda1dda3b62e8a95529386d702bb47`

Frozen portable mapping:

```text
no_activity                  -> 0.0
environmental_noise          -> 0.0
uncertain_local_activity     -> 0.5
strong_visitation_candidate  -> 1.0
```

Interpretation boundary:

- ordinal evidence, not probability;
- not confirmed visitation;
- `environmental_noise` is not exported as nuisance truth;
- zero evidence does not certify biological absence;
- PolliPi ordinal evidence is not the synthetic dimensionless `Pi3` variable.

## 2. InsePi source

Repository:

- `https://github.com/zuizui0223/insepi`

Current main provenance used when TNOA was seeded:

- main commit: `1664a190cec47142e8d14cc5157302a7af18d019`

This main already contains the historical V6–V14c scientific stack and the V15-v2 fail-closed readiness architecture through the added coupled/operational-calibration gates.

TNOA Paper 1 should cite **locked V14b/V14c artifacts**, not later V15 field-development outputs, unless the paper scope is explicitly changed.

## 3. Key locked scientific generations

### V14a — initial dimensionless closed world

InsePi PR #36.

Core registered results:

- short window increases unsupported inference: supported;
- low direct evidence weakens direct route: supported;
- narrow ambiguity ridge near `Pi2 ~= 1`: not supported;
- high coupled response can rescue target evidence when attribution is available in the synthetic design: supported.

Historical V14a is immutable provenance and should not be rewritten.

### V14b superposition / Pi2 diagnosis

InsePi PR #38.

Key semantic correction:

- target+nuisance superposition is a legitimate process state;
- failure of the narrow Pi2 hypothesis is retained;
- Pi5/Pi6 refinements motivated from spatial/sampling diagnosis.

### V14a2 spatiotemporal closed-world generation

InsePi PR #39.

Locked first scientific run:

- workflow: `32921177706`;
- execution commit: `9d4467c6c93f5b51fe46b250ede4e4e10d3e4bb3`;
- artifact digest: `sha256:11c0409e163183395410271141928777310137711f74fee7e9e0f6e500e32b72`;
- coarse worlds: 612,500;
- focused collision worlds: 32,400.

Registered Pi2×Pi5 collision hypothesis was not supported.

### Failed target-separability diagnosis retained

InsePi PR #40.

The full-signature target LDA conclusion was invalidated because target truth leaked through latent topology/trajectory-derived features. The nuisance score-scale diagnosis remained valid.

This failed generation is important methodological provenance and should appear in the supplement/falsification ledger rather than be erased.

### Corrected observation-safe audit

InsePi PR #41.

Locked run:

- workflow: `32926639089`;
- execution commit: `74eb7aadc2d4b84b771baf9e4ed5a540da94cf47`;
- artifact digest: `sha256:52d7c2602db0eecf826d760cf760ac868c86e02032fbbfe53b469d217fb48075`.

Core result:

- direct-visible T+N worlds were separable under the observation-safe representation;
- low-separability cases concentrated in direct-absent, indirect-only coupled-response worlds;
- this motivated keeping indirect-only evidence unresolved without a new attribution channel.

### Target observer freeze

InsePi PR #42.

Final validation, verified from `benchmarks/v14b_target_observer_direct_first_validation_v2_result.json` on InsePi main:

- workflow: `32928566405`;
- execution commit: `791a58b30bfa2f7ac8acac20e654006ac8d3e0c8`;
- artifact id: `9592413407`;
- artifact digest: `sha256:7caade2a19b21d700cb21cb19b5955e611fcff6c984ecd44d72e9b2e322d0b6e`;
- validation SHA-256: `c863dc123f3d6f7a624043e0626a776af371097814fd84226469139146c4c7eb`;
- runtime: Python 3.11.16 / NumPy 2.4.6.

Scientific boundary:

- direct-visible target support retained;
- nuisance-only target support zero;
- indirect-only coupling not promoted to target support;
- truth-known indirect-only target worlds retained as U;
- target-side contradiction types saturated under that generation.

### Nuisance observer failure and diagnosis

InsePi PR #43 retained a failed nuisance process-scale generation: ranking remained strong but inherited raw threshold 0.55 produced inadequate nuisance coverage.

InsePi PR #44 diagnosed that the inherited raw score threshold had no invariant meaning after score representation changed.

This motivated replacing raw-score inheritance with false-certainty risk calibration.

### Family-wise nuisance risk contract

InsePi PR #46.

Final held-out false-attribution rates under the frozen closed-world risk contract:

- target-only false nuisance attribution: 0;
- target-coupled false nuisance attribution: approximately 0.04444;
- declared alpha: 0.05;
- nuisance coverage on the focused validation design: 1.0;
- new contradiction types: 0.

The nuisance decision contract was frozen after this generation.

### Final frozen ternary phase surface

InsePi PR #47.

Design:

- 30,625 dimensionless coordinates;
- six latent regimes;
- 32 repetitions;
- 5,880,000 worlds.

Approximate registered equal-grid / equal-regime aggregate rates:

```text
B ~= 0.2302
T ~= 0.4287
N ~= 0.0877
U ~= 0.2533
```

Approximate U decomposition:

```text
no-supported-evidence U ~= 0.02675
attribution/overlap U  ~= 0.22658
```

These frequencies describe the registered synthetic design space, not natural ecological frequencies.

### V14c semantic clarification

InsePi PR #49, merged into the V14b science stack before main consolidation.

Clarifications relevant to TNOA:

- historical `INFORMATION_ABSENT` wording is interpreted as `NO_SUPPORTED_EVIDENCE` unless information absence is independently established;
- the legacy `baseline + U` quantity is not strict target-presence partial-identification width;
- without target-absence certification, target-presence upper bound remains 1;
- the sharp synthetic Pi3 boundary is a structural-rule result, not a field SNR law.

## 4. What TNOA may copy

TNOA may copy or restate:

- definitions;
- equations;
- claim boundaries;
- figure specifications;
- locked result summaries;
- provenance hashes/receipts;
- manuscript text derived from those locked results.

## 5. What TNOA must not do

TNOA must not:

- rerun a historical one-shot generation merely to obtain a preferred result;
- alter V14b/V14c observer rules and still call the output the same frozen generation;
- replace failed generations with corrected outputs without retaining the failure history;
- use V15 field-development defaults as evidence for Paper 1;
- silently convert PolliPi target evidence into nuisance or biological absence;
- report a derived number without a source artifact/receipt path.

## 6. Reproducibility work still required in TNOA

Before submission, add a machine-readable paper manifest that records:

- exact source commit for every figure/table;
- artifact digest for every locked result file;
- figure-generation script path;
- manuscript claim linked to result artifact;
- whether each result is historical development, locked failure, frozen validation, or descriptive post-result summary.
