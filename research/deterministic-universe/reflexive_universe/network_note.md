# Prediction Constraint Graphs and Spatiotemporal Frustration

**Additional exploratory note (2026-11-04).** Demonstration of classical graph/Ising/parity ideas in a deterministic forecast-feedback model. Not claimed to be original.

## A. Static pairwise consistency

Consider public binary predictions `p_i in {0,1}` at the vertices of an undirected graph G. An edge `(i,j)` represents a *separate pairwise consistency requirement* `p_i=1-p_j`. One may imagine each constraint as a demand that two announced actions be opposite, not as a complete model of a single agent's choices when it receives multiple messages.

**Theorem (classical two-coloring):** All requirements can be simultaneously satisfied iff G is bipartite, equivalently iff it has no odd cycle. If G is connected and bipartite there are two solutions (colorings are complements). If G has an odd cycle, at least one edge must violate its requirement. This is a parity argument: following an odd cycle alternates the bit an odd number of times and arrives at its complement.

When not all constraints can be met, maximizing the number of satisfied requirements is exactly **MAX-CUT**:

```
maximize sum_{(i,j) in E} 1[p_i != p_j]
```

The general MAX-CUT optimization problem is NP-hard. This is an interpretation of known graph optimization, **not a new lower bound for forecasting**.

An exhaustive Python verifier, `forecast_network.py`, checks connected rings and complete graphs with 3-10 vertices and 120 reproducibly seeded random graphs with 5-12 vertices. Results include:

| Graph | Simultaneously satisfied | Total |
|---|---:|---:|
| 3-cycle | 2 | 3 |
| 4-cycle | 4 | 4 |
| 5-cycle | 4 | 5 |
| 6-cycle | 6 | 6 |
| Complete K5 | 6 | 10 |
| Complete K6 | 9 | 15 |

The script creates `network_constraints.csv`.

## B. Coupled deterministic anti-response on a directed ring

For each vertex i of a directed n-cycle, define a continuous public forecast `q_i(t)` and a deterministic next-step map (constant beta > 0)

```
q_i(t+1)=f(q_{i+1}(t)),
f(q)=1/(1+exp(beta*(2*q-1))),
```

with index mod n. For `beta>2`, the one-variable map f has an unstable fixed point `1/2` and an attracting pair `L,H` with `L=f(H)` and `H=f(L)`.

On the *exact invariant two-level set* `{L,H}^n`, encode `H=1`, `L=0` as b_i(t). Then

```
b_i(t+1) = 1 - b_{i+1}(t).
```

After n steps, every bit shifts n times (returning to its original vertex) and has been inverted n times. Therefore

```
b_i(t+n) = b_i(t)       if n is even
b_i(t+n) = 1-b_i(t)     if n is odd
b_i(t+2n) = b_i(t)      for every n.
```

This is an **exact combinatorial statement** about the two-level invariant set, and it explains the observed long-time periods of the continuous logistic simulations. Not every initial pattern has prime period 2n; e.g. even rings admit stationary alternating spatial patterns, while odd rings cannot admit such polarized stationary patterns. All-.5 remains a stationary solution but is locally unstable when beta > 2.

`cyclic_forecast_world.py` checks n=2,...,7 after transient with beta=4 and asymmetric initial forecasts. For selected even-ring seeds, stationary alternation emerged; selected odd-ring seeds asymptotically showed 2n cycles. The code validates recurrence to a tolerance of 1e-10; the continuous trajectories only converge asymptotically to the exact two-level patterns. Outputs in `cyclic_network_trajectories.csv`.

## C. What this does and doesn't mean

- The odd/even effect is mathematically related to frustration of antiferromagnetic Ising constraints on odd cycles.
- It demonstrates a structural choice between spatial alternation and temporal cycling in a chosen model; it does **not** demonstrate social or cosmological inevitability.
- Existence of a physical simulator with arbitrary foresight is not ruled out. For a given announced message, deterministic future behavior is computable in the model; self-consistency is a different restriction.
- It is not correct to call the observed 2n orbits chaos. They are periodic attractors.

## Further open technical questions

1. In a heterogeneous directed network `q_i(t+1)=sigma(h_i-beta*sum_j W_ij(2q_j(t)-1))`, which graph spectra determine the first loss of forecast stability? (Linearization at an unbiased fixed point suggests `J=-(beta/2)*W`, but nonlinear outcomes require proof.)
2. Which local information channels make truthful public prediction possible, and which induced constraint loops force violations?
3. When is a globally consistent solution easy to find, while maximizing the number of approximately consistent local forecasts is NP-hard?
4. How can a predictor provide *conditional* or *counterfactual* predictions without inducing the same reflexive impossibility?

Background: https://pmc.ncbi.nlm.nih.gov/articles/PMC6534389/ (MAX-CUT and Ising); https://onlinelibrary.wiley.com/doi/10.1002/net.21907 (frustration index); https://proceedings.mlr.press/v119/perdomo20a.html (performative prediction).