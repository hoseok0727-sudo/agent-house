# Safe Observer Universe — Deterministic laws and the cost of knowing

**Status:** self-contained, formally checkable *toy model* for safe active identification; not a new theorem, not evidence that our universe is simulated, and not an empirical result about real-world safe control.

## Question

Can an observer living inside an unknown deterministic world learn the world's law while guaranteeing its own survival?

Here the world has a hidden constant law `theta` in `{0,1,2,3}`. A safe scan returns the low bit `theta & 1`. An even/odd specialized probe is safe only for a matching parity, and then reveals `theta >> 1`. A mismatched probe destroys the observer.

- With noiseless scans, the minimal robust-safe adaptive experiment has **two steps**: scan, then the matching specialized probe. The included search exhaustively finds this policy.
- Without the scan, no robust-safe identifying strategy exists.
- A **preset** nonadaptive sequence cannot safely identify the law: no probe is safe in every possible initial world.
- With noisy scans, each noise bit is part of a *preselected, deterministic* microstate tape. Probabilities are the observer's uncertainty over those tapes, **not fundamental indeterminism**.
- With any fixed nonzero full-support error rate and a finite number of scans, a robust zero-risk guarantee still forbids a probe. However, repeating scans and using majority vote reduces the probability of destroying the observer.
- Every finite collection of safe noisy scans leaves at least one bit of the law inaccessible: the high bit is never revealed by scanning.

## Run

Python 3 standard library only:

```bash
python experiment.py
```

The script checks finite-state policies, exhaustively enumerates deterministic noise tapes up to 11 scans, and writes `risk_frontier.csv`.

## Contents

- `experiment.py`: implementation, exhaustive check and CSV export.
- `research_note.md`: mathematical model, conditional results, proof sketches, limits, and literature.
- `risk_frontier.csv`: numerical death risk and remaining conditional entropy under an *illustrative* majority-vote strategy.

## Important qualification

The probabilities refer to a Bayesian prior over hidden laws and microstates. The majority-vote curve is *not* claimed globally optimal among all policies with error budgets. The model assumes perfect detection of catastrophe, specified safe action sets, and known candidate law family. Connections to safe system identification and adaptive distinguishing sequences are well studied in the literature; no claim of academic novelty is made.

Research exploration developed with AI assistance, 2026-11-04.