# V3 reversible-decomposition corollary for the TNOA companion interface

Status: **companion mathematics only; no change to TNOA Paper 1.**

For a reference-derived linear operator `P`, write

\[
E=PY,\qquad Z=(I-P)Y.
\]

Then

\[
\boxed{Y=E+Z.}
\]

Therefore the pair `(E,Z)` is an injective representation of the original primary observation `Y`. If both channels are retained losslessly, decomposition itself does not discard primary information.

The destructive operation is residual-only replacement:

\[
Y\mapsto Z=(I-P)Y.
\]

Whenever `P` has nonzero range this map is non-injective. Distinct observations differing only by a vector in `range(P)` collapse to the same residual.

## Consequence for representation entitlement

Representation entitlement is not mathematically required merely to **compute** the decomposition. It is required before an irreversible or semantically loaded use, such as:

- discarding the explained component;
- suppressing raw evidence because the explained component is called nuisance;
- treating explained variation as calibrated nuisance support;
- treating residual quietness as absence evidence;
- triggering an irreversible live action.

Thus the safer generic interface is

\[
(Y,R)\rightarrow(R,E,Z,\text{raw audit})\rightarrow\text{calibrated T/C/N/O/(A-)}\rightarrow B/T/N/U.
\]

Raw `Y` is mathematically reconstructible from `(E,Z)` but remains useful as an audit/provenance copy.

## Decision-risk corollary

For any fixed decision problem and loss function, adding retained reference information cannot worsen the **best achievable** decision risk because a decision rule may ignore the new channel:

\[
R^*(Y,R)\le R^*(Y).
\]

Conversely, if `C=c(Evidence)` is a deterministic semantic coarsening, then every rule based on `C` is already available from the richer evidence, so

\[
R^*(Evidence)\le R^*(C).
\]

The two sister directions are therefore exact:

- reference refinement expands the available decision-rule class;
- semantic coarsening contracts it.

A particular V3 algorithm may still perform worse if it forces an inappropriate use of the reference. That is an algorithmic restriction, not a property of retaining the information itself.

## Revised sister-method principle

> **Decompose without discarding; interpret without forcing.**

This is the compact mathematical bridge between upstream V3-style information refinement and downstream TNOA uncertainty preservation.
