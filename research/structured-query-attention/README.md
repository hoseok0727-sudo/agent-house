# Structured-Query Softmax Attention — Research Prototype

**Status:** Exploratory mathematical research note and reproducible synthetic-data tests (2026-11-04). **Not** a published novelty claim, peer-reviewed theorem, numerically stable GPU kernel, or demonstrated speedup for real language models.

This standalone research artifact is hosted in a subdirectory of the public **agent-house** repository for convenience. It is not part of the Agent House web application.

## Idea

If queries follow an affine trajectory `q_t = a + t b`, the exact softmax weights factor as `exp(q_t · k_j / sqrt(d)) = w_j z_j^t`. Their sums become coefficients of the rational generating function

`F(x) = Σ_j w_j / (1 - z_j x)`.

Fast polynomial operations can evaluate all these coefficients in quasi-linear *algebraic* time under that strong structural assumption. A divide-and-conquer reduction handles the causal mask, and a first-order covariance correction handles some low-rank departures from the affine path.

The proof outline uses an idealized unit-cost arithmetic model. The prototype validates the algebra in an NTT finite field and separately checks real exponential softmax at high precision; it **does not** supply a stable fast floating-point kernel.

## Files

- [Research note (Korean)](structured_attention_research_note.md) — derivation, conditional asymptotic bounds, correction and error bound, limitations, selected prior work.
- [Research prototype (Python)](structured_attention_research.py) — finite-field, high-precision and synthetic causal-attention checks.

## Reproduce

```bash
python -m pip install numpy mpmath
python structured_attention_research.py
```

No model weights or private datasets are needed. Random seeds are fixed. Timings are illustrative and will vary by machine.

## Important limitations

1. General transformer queries are **not** known to satisfy the required affine/low-rank structure.
2. Vandermonde/generating-function methods can be highly numerically unstable in standard floating-point arithmetic.
3. The speed comparison is not an end-to-end comparison against optimized FlashAttention on GPU.
4. The polynomial and Vandermonde techniques have established prior art. **Originality has not been established** by systematic literature review.
5. Some cited references are starting points for verification and not an exhaustive literature review.

This work was developed with AI assistance. Interpret it as an open research experiment, not an academically verified breakthrough.
