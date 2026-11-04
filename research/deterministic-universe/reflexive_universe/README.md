# Reflexive Deterministic Universe

**Status:** exploratory mathematical/algorithmic research (2026-11-04), not an original-discovery or peer-review claim.

## Research question

Can a deterministic world containing agents that react to public predictions exhibit an instability in the predictor's learning process, even while an exactly self-consistent forecast exists?

The answer is yes *for the deliberately simplified response model below*. This is a constructive example, not evidence that the physical universe is a simulation or that agents possess libertarian free will.

## Mathematical model

A forecast `q_t` estimates the fraction selecting action 1. A fraction `c` of a large population is exposed to that report, and the response parameter `beta` measures how strongly recipients tend to oppose the publicly favored action. With unbiased baseline (`r = 0.5`), the aggregate response function is

```
F(q) = (1-c)/2 + c/(1+exp(beta*(2*q-1)))
```

Simple one-step retraining sets `q_{t+1} = F(q_t)`.

- There is exactly one performatively calibrated fixed forecast, `q*=1/2`.
- The derivative at the fixed point is `F'(1/2)=-c*beta/2`.
- **Global convergence** holds for `c*beta < 2` (contraction).
- For `c*beta > 2`, the fixed point is unstable and nonzero 2-cycles exist with amplitudes `m=2*q_high-1` obeying `m=c*tanh(beta*m/2)`.
- The 2-cycle is attracting in the ideal model. Its onset is a flip bifurcation; a transformed recurrence uses the same self-consistency equation as mean-field Ising magnetization.
- With damped retraining `q_{t+1}=(1-alpha)*q_t+alpha*F(q_t)`, any `0<alpha<=1` satisfying `alpha<4/(2+c*beta)` yields a global contraction (strict for positive beta, c).

## Deterministic microstate implementation

`reflexive_universe.py` enumerates all `M=10007` possible hidden states `z_0` of a finite universe. Each evolves as `z_{t+1}=2*z_t mod M`. Because 2 has an inverse modulo `M`, the states are a permutation at every step. A given state responds to a public forecast via a deterministic threshold; aggregate fractions reproduce the ideal response within at most one grid step. **No random number generator is used** in this experiment.

A separate `c` parameter analytically mixes exposed/non-exposed response populations. The explicit finite-microstate test uses `c=1`; the full `c`-dependent model is evaluated through its exact mean-field recurrence, not a separate simulation of access permissions.

## Reproduce

Python 3.9+ using the standard library only:

```sh
python reflexive_universe.py
```

The script runs assertions and saves `trajectories.csv` and `phase_diagram.csv`.

## Key caveats

- For `c*beta>2` this model **does not become chaotic**: its one-dimensional strictly decreasing response rule has an attracting 2-cycle, not unbounded complexity.
- Perfectly informed analysts who understand the feedback can forecast the oscillation. The failure is **naive repeated retraining** (using the last observed aggregate as the next published forecast), not an impossibility of knowing the future in general.
- Probabilities refer to observer uncertainty over hidden deterministic microstates, not intrinsic physical randomness.
- No general claims about the real world's determinism, the simulation hypothesis, the free-will debate, or actual societies follow from the toy model.

See [research_note.md](research_note.md) for derivations, numbers and source links.

## Network extension

- [Graph consistency & MAX-CUT note](network_note.md) — exact bipartiteness and parity results; selected directed-ring forecast dynamics.
- [Finite graph verifier](forecast_network.py) — exhaustive edge-agreement checks.
- [Coupled ring experiment](cyclic_forecast_world.py) — stationary alternating patterns and periodic traveling patterns.
- `network_constraints.csv` and `cyclic_network_trajectories.csv` — reproducible results of the two graph experiments.

Reproduce the graph extension with:

```sh
python forecast_network.py
python cyclic_forecast_world.py
```