# Evidence-admissible report transitions

TNOA already preserves B/T/N/U rather than forcing every observation into target/not-target. This extension makes the next semantic transition explicit:

```text
TNOA decision record
        |
        v
requested report claim
        |
        v
licensed / withheld
```

This is a **scientific reportability rule**, not an implementation of human informed consent and not a claim about research-participant ethics.

## Core rule

A downstream semantic statement must not outrun the process evidence retained by the TNOA record.

The implementation is `tnoa/licensing.py`.

Four report claims are currently distinguished:

```text
baseline_record
target_attribution
nuisance_attribution
biological_absence
```

The first three are licensed only by their corresponding TNOA decisions. An unresolved `U` therefore does not silently become either target or nuisance.

## Absence remains separate

TNOA's existing conceptual rule remains unchanged:

```text
low T != A-
good O != A-
N != A-
baseline != biological absence.
```

`biological_absence` is licensed only when a separately validated `independent_absence_supported` channel is supplied and there is no positive target-support contradiction in the TNOA record.

The Boolean argument is deliberately not inferred by `classify()`. A sensor/domain adapter must establish that channel independently.

## Why add this layer?

The original B/T/N/U vocabulary protects the observation record. The new layer protects the **transition from record to claim**. These are related but distinct objects:

```text
observation-state preservation
!=
report licensing.
```

This makes a fail-closed pipeline possible without changing the original minimal classifier.

## Tests

```bash
pytest -q tests/test_licensing.py
```

The tests check that target evidence licenses target attribution but not absence, baseline does not imply biological absence, a separate A- channel can license absence, and T+N overlap withholds both unique attributions.
