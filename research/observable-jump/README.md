# Proof-Carrying Observable Jump-Ahead (Research Prototype)

**Status:** exploratory concept demonstration (2026-11-04). This is **not** a claim of an original mathematical discovery, a general compiler, or a peer-reviewed result.

## Question

For a deterministic update `s_{t+1}=F(s_t)`, is it sometimes possible to calculate one requested observable `g(s_T)` exactly without computing all `T` intermediate states?

If a small, certified family of observables is closed under one step, i.e. `G(F(s)) = A G(s)`, then `G(F^T(s))=A^T G(s)` (here `A^T` denotes the **T-th matrix power**, not transpose). Fast exponentiation can evaluate the requested observable with logarithmically many matrix multiplications, subject to arithmetic-cost assumptions and the size of the observable family.

## Demo

The Python program symbolically discovers a hidden observable for a deliberately constructed nonlinear polynomial update:

- `y' = y^2 + 1`
- `x' = 3x - 3y^2 + 1 + (y^2 + 1)^2`
- Discovered observable: `g(x,y)=x-y^2`
- Certified exact recurrence: `g(F(x,y))=3g(x,y)+1`

It compares direct iteration against jump-ahead at 500,000 steps over a finite field, and checks the composition of two jumps to one trillion steps. Runtime measurements are illustrative single-machine Python measurements, **not** a general performance claim.

## Reproduce

Requires Python 3 and SymPy:

```bash
python -m pip install sympy
python observable_jump_research.py
```

## Files

- [Detailed research note](observable_jump_research_note.md): derivation, algebraic certificates, limitations, related work, and research directions.
- [Python proof-of-concept](observable_jump_research.py): symbolic discovery, exact identity verification and finite-field tests.

## Limits and attribution

This toy demonstration searches a **narrow hand-specified polynomial ansatz**, not arbitrary programs or observables. More general automated discovery is the open research question. Koopman invariant subspaces, polynomial program invariants, and C-finite recurrences provide substantial prior art; see the note for starting references.

This folder is hosted in the public `agent-house` repository only as a separate research artifact and does not change that web application's source. Developed with AI assistance.
