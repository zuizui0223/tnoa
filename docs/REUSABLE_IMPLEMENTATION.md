# Minimal reusable implementation

TNOA includes a small, dependency-free Python decision layer so the paper is not only a manuscript/provenance package.

The implementation intentionally starts **after domain-specific score calibration**. It does not claim that a raw detector score of a particular value means target or nuisance support. Users supply already-calibrated positive-support flags from their own camera, acoustic, classifier or rule-based system.

## Install

```bash
pip install -e .
```

## Python API

```python
from tnoa import Evidence, classify

result = classify(
    Evidence(
        deviation_observed=True,
        target_supported=True,
        nuisance_supported=True,
        observable=True,
    )
)

print(result.decision.value)  # U
print(result.reason.value)    # target_nuisance_overlap
```

The minimal evidence contract is:

- `deviation_observed`: a dynamic observation requires adjudication;
- `target_supported`: independently calibrated positive target support;
- `nuisance_supported`: independently calibrated positive nuisance support;
- `observable`: the measurement channel is adequate for the focal inference;
- `coupled_response_supported`: a local response potentially caused by the target;
- `attribution_supported`: independent support attributing that coupled response to the target.

The decision mapping preserves the manuscript guardrails:

- an unobservable window cannot silently become baseline or absence;
- target and nuisance are positive non-complementary supports;
- simultaneous T and N support becomes U under the minimal exclusive-decision contract rather than being forced to one side;
- coupled response is promoted to target support only when attribution is supported;
- lack of positive evidence becomes U/no-supported-evidence, not biological absence.

## Important: the reusable U-reason vocabulary is not the frozen V14b D3 vocabulary

The reusable API emits four unresolved reasons:

- `target_nuisance_overlap`;
- `missing_attribution`;
- `insufficient_observability`;
- `no_supported_evidence`.

The frozen V14b phase surface used by D3/D5 contains only **two** unresolved-reason columns. The source decision code defines them as `INFORMATION_ABSENT` and `OVERLAP_OR_ATTRIBUTION`; manuscript-facing text relabels the first conservatively as `no-supported-evidence`.

There is no one-to-one empirical four-way mapping from the frozen surface to the current API:

| reusable API reason | frozen V14b D3 representation | what is supported |
| --- | --- | --- |
| `no_supported_evidence` | historical `INFORMATION_ABSENT` / reported `no-supported-evidence` | closest semantic continuation, but the API is a later implementation contract |
| `target_nuisance_overlap` | included inside frozen `OVERLAP_OR_ATTRIBUTION` when both frozen T and N were supported | not separately recoverable from the frozen reason-rate column |
| `missing_attribution` | included inside frozen `OVERLAP_OR_ATTRIBUTION` for unresolved indirect-only target response | not separately recoverable from the frozen reason-rate column |
| `insufficient_observability` | **no separate frozen D3 column** | current API refinement only; not empirically isolated by the frozen surface |

The frozen V14b source therefore supports a two-bucket decomposition, not validation of the current four-reason implementation. In particular, D3's two-way split must not be cited as evidence that each current API reason has an independently demonstrated information value. The D5 random-split control further shows that D3's identification-width reduction is not specific to the semantics of the two frozen reason labels.

## CSV CLI

Input CSV columns can use the defaults above or arbitrary column names supplied with command-line flags.

```bash
tnoa examples/minimal_evidence.csv annotated.csv \
  --summary summary.json \
  --group-by site,condition
```

The annotated CSV receives:

- `decision`: `B`, `T`, `N` or `U`;
- `reason`: provenance for the decision;
- the support flags actually used by the decision layer.

The summary JSON returns B/T/N/U rates and reason-resolved U rates by the requested ecological covariates.

## Field translation begins before this API

A real sensor cannot jump directly from raw detector outputs to the calibrated flags consumed above. The field-facing implementation should therefore be staged and fail closed:

1. preserve an interpretable primary scientific record;
2. log raw T/N/O/C diagnostics separately while calibrated support remains unavailable;
3. retain those pre-calibration windows as `U / field_calibration_pending` and do not let TNOA alter capture behaviour;
4. establish independent biological-event, coupled-response, nuisance and observability truth without exposing algorithm scores to annotators;
5. calibrate on grouped development data against declared error criteria;
6. freeze the calibration manifest before held-out days/scenes are scored;
7. only after held-out validation allow reason-specific TNOA states to influence adaptive acquisition.

The complete sensor-agnostic sequence, including camera-trap, acoustic and interaction-camera mappings, is documented in `docs/FIELD_TRANSLATION_PATHWAY.md`.

## What this implementation does not do

It does not:

- calibrate target or nuisance scores;
- choose a universal threshold;
- infer biological absence from low target support;
- reproduce the historical V14b phase-surface generator;
- validate the current four U reasons from the frozen two-reason D3 surface;
- claim that finer reason labels provide a semantic-specific information premium;
- claim field validation;
- replace occupancy, state-space or other downstream ecological models.

Its role is narrower: **preserve the observation states before downstream ecological inference instead of forcing them into a target/absence binary, while exposing reason provenance whose semantics must be validated in each implementation.**
