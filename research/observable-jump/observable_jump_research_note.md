# Query-Selective Exact Acceleration of Nonlinear Dynamics

Exploratory research concept, 2026-11-04. **Not a claimed first discovery.** Closely related to Koopman invariant subspaces, algebraic program analysis, and C-finite recurrences.

## Problem and bottleneck

For a nonlinear deterministic update `F`, evaluating `F^T(s)` by simulation takes `T` steps. The central research question is whether one can compute **only a requested observable** `g(F^T(s))` without evolving the entire state. A generic state may not have a finite small polynomial lifting, yet a useful observable can.

## Certificate theorem

Let `F : K^n -> K^n`. Assume symbolic functions `g_1,...,g_k`, with `g_1` the requested output, and a constant matrix `A` satisfy the identities

`g_i(F(s)) = sum_j A[i,j] g_j(s)`, for every `s` and each `i`.

Then writing `G=(g_1,...,g_k)^T`, one has exactly

`G(F^T(s)) = A^T G(s)`,

where the exponent on the right is matrix exponentiation. Proof is induction using `G(F(s))=A G(s)`. Exponentiation by squaring requires `O(k^3 log T)` field operations for a generic dense `k x k` matrix. Evaluating and certifying the `g_i` also costs time. For polynomial `F,g_i`, the identities can be checked by symbolic polynomial subtraction; a zero polynomial is a deterministic algebraic certificate.

## Automatic toy discovery

Define rational polynomial updates:

```
y_next = y*y + 1
x_next = 3*x - 3*y*y + 1 + (y*y+1)**2
```

The `y` subsystem has iterates of degree `2^T` (over characteristic zero). So the polynomial observables `y, y∘F, y∘F^2, ...` are linearly independent: **no finite-dimensional polynomial Koopman-invariant subspace containing `y` exists** for this map.

Search a restricted family `g(x,y) = x + c*y*y + d*y` with undetermined coefficients and require `g(F)=a*g+b`. Matching polynomial coefficients and solving produces

```
c = -1, d = 0, a = 3, b = 1
```

Thus `g=x-y**2` and **the exact identity for every input** is

`g(F(x,y)) = 3*g(x,y)+1`.

The entire observable's future follows a 2D affine update, despite the unrelated coordinate's exponentially increasing symbolic degree. For any integer `T>=0`:

`g_T = 3**T * g_0 + (3**T-1)/2`.

This formula holds over the rationals. For computation modulo odd prime `p`, use modular exponentiation and the modular inverse of `2`.

## Reproduced test

The accompanying script automatically discovers the coefficients with SymPy, checks the identity has exactly zero residual, then compares direct modular simulation to jump-ahead for four initial states and 500,000 iterations each, under prime `1,000,000,007`. All four outputs match. Example observed timings on the execution environment: `0.436619 s` total direct vs `0.000020 s` total jump, or about `21,897x` as measured. These values are microbenchmarks of an intentionally solvable toy, not a general speedup result and depend on timing overhead and implementation. It further calculates `T=10**12` giving `g_T=927280765` for `(x,y)=(713,97)`, verified by an independent split-composition check (the polynomial identity is the real correctness certificate).

## Research direction and novelty boundary

The relevant mathematical idea is *not new*: Koopman finite-dimensional invariant subspaces and polynomial recurrence analysis exist. The novel **research goal, to be investigated**, is a **query-selective certified jump compiler** which:

1. Searches only for observables needed to answer a given query, not a full-state representation.
2. Discovers polynomial combinations with cancellation, not merely a monomial-closure basis.
3. Issues independently checkable symbolic identities as a proof-carrying acceleration certificate.
4. Rejects candidates for which the certificate is unavailable, instead of returning approximate predictions as exact.
5. Quantifies resource limits, such as search complexity and the tradeoff between basis size and certificate size.

The difficult bottleneck is the combinatorial explosion of candidate observables and polynomial substitutions. A small successful toy does not imply that these can be handled at scale. Strong evaluation would require representative open loop/program benchmarks and comparison with existing program acceleration and Koopman/recurrence-finding methods.

## Related work (initial references, not an exhaustive novelty review)

- Brunton et al. (2016), *Koopman Invariant Subspaces and Finite Linear Representations of Nonlinear Dynamical Systems for Control*, PLOS ONE: https://pmc.ncbi.nlm.nih.gov/articles/PMC4769143/
- Wang & Lin (CAV 2024), *On Polynomial Expressions with C-Finite Recurrences in Loops with Nested Nondeterministic Branches*.
- Bayarmagnai, Mohammadi & Prébet (2026), *Algebraic and algorithmic methods for computing polynomial loop invariants*, Journal of Symbolic Computation: https://doi.org/10.1016/j.jsc.2025.102551
- Yang et al. (2026), *Discrete-time dynamical systems characterization via invariance and approximation of Koopman operators and operator-valued kernels*: https://doi.org/10.1007/s11071-026-12317-x

## Run

```bash
pip install sympy
python observable_jump_research.py
```