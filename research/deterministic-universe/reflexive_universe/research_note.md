# The Forecast That Destabilizes Its Own Universe

**Exploratory research memorandum — 2026-11-04**

## Abstract

We construct a fully deterministic finite ensemble of agents whose aggregate behavioral response depends on a public forecast. A one-dimensional continuous mean-field model exhibits a flip bifurcation at the exact threshold of behavioral sensitivity times forecast exposure, `beta*c=2`. Strong response induces an attracting period-two orbit even though a unique, exactly calibrated fixed forecast continues to exist. The period-two amplitude obeys a self-consistency equation identical in form to the zero-field mean-field Ising magnetization equation. Simple damping eliminates oscillations and gives a global contraction criterion. We explicitly enumerate 10,007 deterministic microstates to demonstrate that ontic randomness is unnecessary for this aggregate behavior. These are known mathematical tools assembled into a philosophical/educational experiment; **no priority or novelty is claimed**.

## 1. Two kinds of prediction impossibility

**Published categorical prophecy.** If a deterministic agent observes a publicly announced bit `b` and chooses `a=1-b`, there is no self-consistent perfectly correct published bit: `a=b` requires `b=1-b`. Yet for each fixed announcement `b`, the resulting actual action is deterministic and knowable. A third party may truthfully describe the conditional outcome while the predictor may not announce it as the agent-facing forecast. This is a logical fixed-point obstruction rather than chaos, randomness or a proof of free will.

**Aggregate probabilistic prediction.** A group may have hidden deterministic states unknown to an observer. We define a deterministic rule for each member and study the actual fraction choosing action 1. A probability `q` is calibrated against the world *after it is announced* if `q=F(q)`. This is a performative fixed point, and its existence does not guarantee stability of an update algorithm `q_{t+1}=F(q_t)`.

## 2. The model

Assume a binary action, a population of private microstates, `0<=q<=1`, reaction strength `beta>=0`, and exposed share `c in [0,1]`. Under symmetric baseline choice, we posit

```
F(q)=(1-c)/2 + c/(1+exp(beta*(2*q-1)))
```

The unexposed population always chooses action 1 with aggregate rate one half; exposed agents choose it at a logistic rate decreasing in the public probability `q` of action 1. The exact choice of logistic function is a **model assumption**, not a discovered universal behavioral law. For any given private microstate, agent action can be made deterministic via a threshold rule.

The function satisfies `F(1-q)=1-F(q)`, `F(1/2)=1/2`, and `F'(q)=-2*c*beta*sigma(v)*(1-sigma(v))`, with `v=-beta*(2q-1)`. Therefore `|F'|<=c*beta/2`, attaining its maximum at `q=.5`.

### Proposition 1: uniqueness and stable phase

Since `F` is nonincreasing and `q` is strictly increasing, the equation `q=F(q)` has the unique solution `q*=1/2`. When `c*beta<2`, `F` is a strict contraction of `[0,1]`, giving global convergence from any initial forecast. At `c*beta=2`, the derivative is `-1` and simple contraction no longer proves convergence; its higher-order terms still draw nonexceptional trajectories slowly towards `1/2` in the ideal smooth model.

### Proposition 2: period-two phase

Set `m_t=2*q_t-1`. Then

```
m_{t+1}=-c*tanh((beta/2)*m_t).
```

The alternating-frame variable `u_t=(-1)^t*m_t` satisfies the *positive* map

```
u_{t+1}=c*tanh((beta/2)*u_t).
```

For `c*beta>2`, this concave increasing map has exactly one positive nonzero fixed point `m*` (and a negative partner), because the derivative at zero exceeds 1 while `c*tanh(beta*m/2) < m` for `m>=c` (with a strict inequality for `m=c>0`). Hence the original `q` recursion has an attracting 2-cycle

```
q_low=(1-m*)/2, q_high=(1+m*)/2,
m*=c*tanh((beta/2)*m*).
```

Its local stability follows from strict concavity of `g(m)=c*tanh(beta*m/2)`: at the positive crossing `0<g'(m*)<g(m*)/m*=1`. For initial `q0!=1/2`, the alternating-frame recurrence approaches one of the signs of `m*` under the stated conditions. A 1D continuous decreasing map can have an attracting period-two behavior here but no periodic orbits of prime period >2; **do not call this chaos**.

The equation for `m*` has the familiar zero-field *mean-field Ising* form `m=tanh(k*m)` for `c=1`, with an effective coupling `k=beta/2`. The similarity is mathematical, not a physical identity of systems.

For `c=1`, expanding `tanh` at small `m` gives

```
m* ~ sqrt((3/2)*(beta-2)) as beta decreases to 2 from above.
```

This is the standard square-root critical scaling in this model.

### Proposition 3: a simple stabilization policy

Replace immediate re-forecasting by an exponentially smoothed update

```
q_{t+1}=(1-alpha)*q_t+alpha*F(q_t), 0<alpha<=1.
```

The derivative lies in the interval `[1-alpha*(1+c*beta/2),1-alpha]`. A sufficient global contraction condition is

```
alpha < 4/(2+c*beta).
```

For `beta=4, c=1`, `alpha=0.5` satisfies the condition, while `alpha=1` leads to the 2-cycle. This says nothing about whether smoothing is optimal under changing realities; it proves stability *within this stationary toy model*.

## 3. Numerical checks and finite-state universe

Python standard-library script `reflexive_universe.py` implements the recurrences, bisection for fixed points and amplitudes, automated assertions, and exhaustive finite-microstate enumeration.

At `beta=4,c=1`, the ideal period-two orbit is approximately

```
q_low = 0.021247988
q_high= 0.978752012
m*    = 0.957504024
```

At `beta=2.5,c=1`, the period-two values are `0.144794108` and `0.855205892`; at `beta=1` the forecast tends to `0.5`.

The explicit universe uses `M=10007` initial microstates `z0=0,...,M-1`, and a deterministic update `z_{t+1}=2*z_t mod M`. Since `M` is odd, the evolution permutes the entire microstate population. At each time `t`, agent with hidden state `z_t` chooses 1 exactly when `z_t<round(M*F(q_t))`. The proportion agreeing is `round(M*F(q_t))/M`, a deterministic quantity within `1/(2M)` of the analytic rate (up to floating rounding). No random sampling or random seeds are used. The numerical test verified a maximum observed grid discrepancy below `4.8e-5`.

The final forecast values for `beta=4` alternate near `0.9787149` and `0.0212851`. These values differ slightly from the ideal mean-field values because the ensemble has only 10,007 members. This finite model alone does not constitute a physical chaotic universe or a literal thermodynamic phase transition.

The continuous approximation with partial exposure `c=0.4,beta=4` converges to `.5` because the effective product is `c*beta=1.6<2`.

## 4. Forecasts can alter aggregate entropy without ontic randomness

For an asymmetric baseline rate `r in (0,1)`, full exposure and a baseline log-odds offset give

```
F_r(q)=sigmoid(logit(r)-beta*(2q-1)).
```

The fixed point is uniquely determined by

```
logit(q*)+beta*(2*q*-1)=logit(r).
```

If `r>1/2`, then `1/2<q*<=r`, and implicit differentiation yields

```
dq*/d beta = -(2q*-1)/(1/[q*(1-q*)]+2beta) < 0.
```

Thus the self-consistent *population* rate moves towards 50-50 as reaction strength increases. At `r=.9`, our computations found stationary rates `0.900000` at `beta=0`, `0.680274` at `beta=4`, `0.561000` at `beta=16`, `0.532309` at `beta=32`. Bernoulli entropy increases correspondingly, but this is an epistemic/ensemble quantity, not a claim of fundamental physical randomness.

## 5. Relation to chaos, determinism, and simulation philosophy

- A deterministic initial condition `z0` plus a published forecast sequence determines every individual's action exactly. Ensemble uncertainty comes from which hidden microstate is present.
- A simple repeatedly updated predictor may fail despite a calibrated fixed point. This is an algorithmic feedback instability, *not* fundamental incomputability. An outside simulator knowing the correct response law can predict the period-two trajectory.
- Publishing a categorical forecast to an adversarial agent can produce a fixed-point obstruction even if its internal rules are trivially computable.
- Neither phenomenon decides whether our actual universe is deterministic or simulated, and neither demonstrates or refutes libertarian free will.
- A genuine unsolved next step is to characterize **which information channels and predictor models let agents enforce nonexistence of truthful public forecasts** while allowing low-complexity hidden or conditional forecasts. This should be studied against prior work before any novelty claim.

## 6. Reproducibility and references

```sh
python reflexive_universe.py
```

Outputs:

- `trajectories.csv` — model, forecasts, outcomes, forecast-outcome discrepancy.
- `phase_diagram.csv` — theoretical 2-cycle amplitudes across sensitivity and exposure.

Prior art and background:

1. David H. Wolpert (2008), *Physical limits of inference*, Physica D 237(9): https://doi.org/10.1016/j.physd.2008.03.040
2. Juan Perdomo et al. (2020), *Performative Prediction*, ICML / PMLR 119: https://proceedings.mlr.press/v119/perdomo20a.html
3. Moritz Hardt and Celestine Mendler-Dünner (2023), *Performative Prediction: Past and Future*: https://arxiv.org/abs/2310.16608
4. Gabriele Farina and Juan Carlos Perdomo (2026), *The Stability of Online Algorithms in Performative Prediction*: https://arxiv.org/abs/2602.24207
5. Standard mean-field Ising self-consistency / phase transition (textbook treatment): https://academic.oup.com/book/8876/chapter/155108213
6. The binary shift as a chaotic map: https://demonstrations.wolfram.com/ChaosInTheShiftMap/

## Limitations

Synthetic model chosen to exhibit a bifurcation; no evidence that real agents follow the logistic response function; no neural-network experiments; no statistical causal inference; no claim of academic originality. The goal is a transparent cross-domain formal experiment with independently checkable algebra and code.

## 7. Extension: topology determines which self-consistency failures can become oscillations

A separate exact graph reduction is given in [network_note.md](network_note.md). Pairwise requirements `p_i!=p_j` can all be met if and only if a graph is bipartite; maximizing the number satisfied is MAX-CUT, whose general case is NP-hard. We also studied a *dynamical* directed n-cycle `q_i(t+1)=F(q_{i+1}(t))` for full exposure. At strong opposition, it has an invariant two-level set with update `b_i(t+1)=1-b_{i+1}(t)`. This gives `b_i(t+2n)=b_i(t)` exactly, and odd rings cannot support a static polarized pattern. Simulations of chosen asymmetric starts at `beta=4` converged to stationary alternating spatial patterns for even n and periodic traveling patterns for odd n. These are elementary known parity/dynamics phenomena, not a claim of new physics.