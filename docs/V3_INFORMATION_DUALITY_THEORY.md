# V3–TNOA information duality — companion theory note

Status: **companion theory only. This does not alter TNOA Paper 1, its frozen quantitative results, or its submission claim.**

## 1. Purpose

The V3 sister-method line and TNOA can now be related by an exact information-order duality rather than only by verbal symmetry.

TNOA asks:

> Given retained evidence, what semantic conclusion is licensed?

The V3/reference line asks:

> Can independent reference information refine the observation before that semantic question is asked?

The shared principle is:

> **increase retained information upstream when justified, and avoid irreversible semantic coarsening downstream before entitlement.**

## 2. Compatible-world formulation

Let `Ω` be the latent-world set. For any observation `X`, define

\[
\mathcal C_X(x)=\{\omega:X(\omega)=x\},
\]

and for any estimand `theta`,

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

These sets make the sister-method relation exact.

## 3. Reference refinement

For primary observation `Y` and additional reference `R`,

\[
\mathcal C_{(Y,R)}(y,r)\subseteq\mathcal C_Y(y),
\]

hence

\[
\boxed{\mathcal I_{(Y,R)}(y,r)\subseteq\mathcal I_Y(y).}
\]

Adding a retained reference can therefore only preserve or improve identification at the information level. It may fail to add useful information, but it cannot enlarge the set of worlds compatible with the richer retained record.

This statement concerns retained information, not the performance of a particular correction algorithm.

## 4. Semantic coarsening

Let `E` be a process-preserving evidence record and `C=c(E)` a deterministic coarsening. Then

\[
\mathcal C_E(e)\subseteq\mathcal C_C(c(e)),
\]

and therefore

\[
\boxed{\mathcal I_E(e)\subseteq\mathcal I_C(c(e)).}
\]

Thus deterministic coarsening cannot improve identification. This is the general mathematical form behind TNOA's information-preservation result.

## 5. Exact duality

The two directions are:

\[
\sigma(Y)\subseteq\sigma(Y,R)
\]

for upstream reference augmentation, and

\[
\sigma(c(E))\subseteq\sigma(E)
\]

for downstream semantic coarsening.

So the sister methods occupy opposite directions in the same information partial order:

- **V3/reference acquisition:** refine the observation partition;
- **TNOA:** resist unnecessary quotienting of the evidence partition.

The symmetry is therefore a symmetry of epistemic role, not a requirement that the two methods use the same empirical validation strategy.

## 6. Why a reference does not automatically license correction

Suppose a reference-derived orthogonal projector `P` is applied to

\[
Y=S+N.
\]

Define

\[
a_S=\frac{\|PS\|^2}{\|S\|^2},\qquad
 a_N=\frac{\|PN\|^2}{\|N\|^2}.
\]

After projection, the target-to-nuisance energy-ratio gain is

\[
\boxed{\frac{1-a_S}{1-a_N}}.
\]

Therefore projection improves this ratio exactly when

\[
\boxed{a_N>a_S.}
\]

Reference activity alone does not imply this inequality.

A nonzero projector also always has some nonzero target vector in its range, so over an unrestricted target class there exists a target that the projection erases completely. This is why representation entitlement and semantic entitlement must remain distinct.

## 7. Information-safe V3/TNOA interface

The mathematically safer generic interface is not to replace the observation by a residual.

Instead retain

\[
A=(Y,R,\hat N,Z),
\]

where

\[
\hat N=PY,\qquad Z=(I-P)Y.
\]

Because `Y` and `R` remain explicitly present and the other components are deterministic functions of them,

\[
\boxed{\sigma(A)=\sigma(Y,R).}
\]

Thus the decomposition does not destroy retained information.

The downstream TNOA layer may then use calibrated target/nuisance/observability evidence derived from raw and decomposed channels while retaining U when unique attribution is not licensed.

This yields a stronger interface rule:

> **V3 should augment measurement evidence, not overwrite the measurement record.**

## 8. TNOA-side consequence

The existing TNOA rule remains unchanged:

- low target support is not target absence;
- positive nuisance support is not `not target`;
- target and nuisance may coexist;
- overlap or insufficient support may remain U;
- A− requires an independently validated negative-evidence channel.

The V3 decomposition therefore cannot create TNOA semantics by itself. Residual quietness cannot create A−, and reference-explained variation cannot directly create N without calibration.

## 9. Structural result versus empirical result

The following are structural and do not require field data once their assumptions are stated:

1. reference augmentation weakly shrinks identified sets;
2. deterministic semantic coarsening weakly expands identified sets;
3. additive target/nuisance decomposition is non-identifiable from the sum alone without restrictions;
4. projection improves energy SNR iff `a_N > a_S`;
5. nonzero projection cannot universally preserve an unrestricted target class;
6. raw-retaining augmentation avoids representation-level information loss;
7. positive-only evidence cannot certify absence when target-present compatible worlds remain.

The following remain empirical:

- whether a physical reference is usefully coupled to nuisance;
- whether nuisance capture exceeds target capture in a domain;
- finite-sample stability of the learned/reference-derived subspace;
- downstream observer performance;
- transfer across applications.

## 10. Relationship to TNOA Paper 1

This note does **not** add V3 to the frozen Paper-1 novelty claim.

TNOA Paper 1 remains independently supported by its own closed-world theory, process-preserving evidence architecture, partial-identification boundary, and synthetic consequences.

The V3 duality provides a sister-method conceptual extension:

\[
\boxed{\text{refine before interpretation; preserve before conclusion.}}
\]

A future joint paper may test the two-layer architecture empirically, but the mathematical duality itself is not contingent on that field validation.
