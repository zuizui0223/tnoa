# TNOA conceptual framework

## 1. Problem statement

Ecological sensors do not observe biological truth directly. They observe a biological process through a measurement channel that can itself be altered by exogenous processes, limited visibility, finite sampling and coupling between actor and target.

TNOA therefore separates **what is happening biologically** from **what the observation process allows us to infer**.

The central question is not simply whether an event classifier is confident. It is:

> What positive evidence exists for the focal process, what positive evidence exists for observation-distorting processes, was the relevant state observable, and does the available evidence justify a unique decision?

## 2. Closed decision vocabulary

The final decision vocabulary is:

\[
B + \{T,N,U\}.
\]

### B — baseline

No marked dynamic deviation requires target/nuisance adjudication. Baseline is outside the dynamic T/N/U decision problem rather than being equated with negative target truth.

### T — target-supported

Positive evidence supports the focal biological process.

### N — nuisance-supported

Positive evidence supports an exogenous process that changes the observation problem by one or more of the following effects:

1. mimicking target evidence;
2. masking target evidence;
3. corrupting attribution;
4. degrading observation support.

Nuisance is not defined as `not target`.

### U — abstention / undetermined

The current evidence does not justify a unique target/nuisance decision. U may arise for more than one reason and these reasons should remain internally distinguishable.

At minimum:

- **U_no-support:** no sufficient positive decision support was retained;
- **U_attribution/overlap:** multiple process explanations or genuine T+N superposition prevent unique attribution.

`U_no-support` must not automatically be relabelled `information absent`, because observer representation defect and genuine information absence are different possibilities.

## 3. Evidence architecture

The field-facing evidence system is:

\[
(T,C,N,O,A^-).
\]

### T — direct target evidence

Evidence for the focal actor/event itself.

A low T score means only that the target observer did not retain strong positive target evidence. It does not prove biological absence.

### C — target-coupled response

A local response of the biological target can provide indirect evidence only when the response is independently attributable to the focal interaction.

\[
C_{usable}=C_{response}\times C_{attribution}.
\]

Strong local motion with no attribution channel remains non-diagnostic rather than being promoted to target evidence.

### N — exogenous nuisance evidence

N is a separate positive process hypothesis. T and N may coexist:

\[
T=1,\quad N=1
\]

is a legitimate state of the world.

The system therefore preserves superposition rather than forcing one class to erase the other.

### O — observability / measurement support

O asks whether the primary measurement channel preserved enough information to attempt the relevant biological inference.

The current five support dimensions are:

- target-zone coverage;
- target-zone visibility;
- spatial resolution;
- photometric sufficiency;
- temporal continuity.

O is not biological evidence. In particular:

\[
O\text{ good} + T\text{ low} \not\Rightarrow A^-.
\]

### A− — independent target-absence evidence

A− is optional and must be independently validated. It cannot be manufactured from low target evidence, high observability or low nuisance.

Without a validated A− channel, a safe target-presence upper bound remains 1.

## 4. Positive definitions and overlap

TNOA rejects complementary definitions such as:

\[
N=1-T
\]

or

\[
O=1-N.
\]

Each axis answers a different scientific question.

This has three consequences:

1. target and nuisance evidence can be jointly positive;
2. a quiet scene can still be unobservable;
3. a noisy scene can still be observable.

## 5. Contradiction taxonomy

When observations disagree, TNOA classifies the source of the contradiction before modifying the system.

### Definition defect

The ontology or decision rule assigns the wrong meaning to a case. Fix the definition, not the observer.

### Representation defect

Relevant information exists in the observed data but the observer does not represent or use it adequately. Improve that observer while freezing the others.

### Information absence

The observation channel genuinely lacks the information needed for the requested inference. Retain U.

### Process coupling / superposition

More than one process is genuinely active. Preserve multi-process truth rather than forcing a single label.

## 6. Alternating development

Observers with different epistemic roles are developed alternately:

1. freeze all but one subsystem;
2. diagnose contradiction types;
3. modify only the subsystem implicated by the diagnosis;
4. evaluate on a fresh locked generation;
5. retain negative generations;
6. stop when contradiction **types** saturate rather than requiring zero disagreement.

This makes methodological failure informative instead of turning every negative result into a new tuning opportunity.

## 7. Dimensionless formulation

TNOA treats absolute values as implementation-specific and studies the geometry of relative scales.

Current axes:

\[
\Pi_1=\frac{\text{observation-window length}}{\text{target timescale}},
\]

\[
\Pi_2=\frac{\text{nuisance/response timescale}}{\text{target timescale}},
\]

\[
\Pi_3=\frac{\text{direct target amplitude}}{\text{nuisance amplitude}},
\]

\[
\Pi_4=\frac{\text{target-driven local-response amplitude}}{\text{nuisance amplitude}},
\]

\[
\Pi_5=\frac{\text{nuisance spatial correlation length}}{\text{target support width}},
\]

\[
\Pi_6=\text{samples per target timescale}.
\]

The method output is therefore a response surface over \(\Pi\), showing where the observation system resolves T/N and where it must retain U.

## 8. Risk-controlled operational boundaries

Raw score thresholds do not retain meaning when representations change. TNOA therefore separates:

- **representation** — what the observer measures;
- **operational decision calibration** — how evidence is mapped to decision support;
- **claim thresholds** — when held-out uncertainty permits a scientific claim.

The general principle is:

\[
\boxed{\text{choose tolerated false certainty }\alpha\text{, then measure safely resolvable coverage}.}
\]

Abstention is therefore not counted automatically as failure. Unsupported coverage is itself an output.

## 9. Partial identification boundary

Positive-only target evidence does not certify absence. Therefore a decision labelled N does not necessarily prove that T was biologically absent.

Without A−, strict target-presence partial identification is conservative:

\[
P(T)\in[P(\text{target-supported}),1].
\]

Any narrower upper bound requires a separately validated negative-evidence channel.

## 10. Transferability

The framework is intended to transfer at the architectural level, not by copying fitted thresholds. Candidate domains include:

- camera traps;
- pollinator/visitor monitoring;
- nest monitoring;
- phenology imaging;
- feeding/interaction cameras;
- acoustic event sensing;
- edge environmental anomaly sensing.

Transfer requires revalidation of evidence channels and operational calibration in the new system.
