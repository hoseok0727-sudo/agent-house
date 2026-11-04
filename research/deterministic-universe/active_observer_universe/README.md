# Active Observer Universe Lab

**Research prototype / reproducible mathematics, 2026-11-04**

This experiment compares *passive observation* with *a single active intervention* in an intentionally restricted deterministic, controlled binary shift-register universe. Its central result is an elementary instance of known **system identification / impulse-response / observability theory**, **not a claim of a new theorem in the literature**.

## Reproduce

No dependencies beyond Python 3.10+:

```bash
python experiment.py
```

It runs exhaustive coefficient recovery (up to k=11), exhaustive early input indistinguishability checks (up to k=5), exact information calculations (k=8), noisy measurement simulations (1000 repetitions per configuration), and a hidden-state counterexample. It writes `information_curve.csv` and `noise_recovery.csv`.

## Dynamics

The hidden state is `s in {0,1}^k`, initially zero. A bit `u_t` can be deliberately injected:

```
s_{t+1} = (s_{1,t}, ..., s_{k-1,t}, XOR_i(c_i & s_{i,t}) XOR u_t)
y_t = s_{0,t}
```

`c in {0,1}^k` is the unknown law. When `u=0` forever, the output `y` is all zero for **every** possible `c`, so no passive observations distinguish any of the `2^k` models.

When `u_0=1` and every later `u=0`, observe `y_0,...,y_{2k}`. Then `y_0,...,y_{k-1}=0` and `y_k=1`; the subsequent `k` bits determine `c_{k-1},...,c_0` sequentially via a triangular recurrence. For a uniformly drawn unknown `c`, the mutual information in outputs collected through time `t` is `min(k,max(0,t-k))` bits. One bit of deliberately injected action unlocks `k` bits of information about the hidden law; the observation horizon is `2k` time steps (including the initial observation).

**Time optimality, only within this controlled model:** For any (possibly adaptive) binary input strategy started from the zero state, two models that differ only in `c_0` produce the same observations until time `2k-1`. Thus no protocol can guarantee identifying all coefficients earlier than observing `y_{2k}`. The single-impulse strategy attains this time bound.

## Noise

For bit-flip noise probability `e`, repeat exactly the same controlled experiment `r` odd times **after fully resetting** the state. Take a majority vote independently for each of the `k` informative bits. The probability of one majority error is

```
q(e,r) = sum_{j=(r+1)/2}^r binom(r,j) e^j (1-e)^(r-j)
```

and the exact probability of recovering the **whole** unknown coefficient vector is `(1-q)^k`, assuming independent flips across times and resets. See `noise_recovery.csv` for simulations. Noisy data breaks the guarantee of exact recovery from one experiment.

## What observation and intervention still cannot prove

Adding an invisible state bit `h` with arbitrary dynamics that **never affects the observable variable or controllable portion** produces a new deterministic universe that generates the same output for *every possible input sequence*. No possible experimental history through this interface distinguishes these two ontological descriptions. This is a concrete model of *underdetermination by accessible interventions*, not evidence that our physical universe is simulated.

## Prior literature and caution

- Kalman (1963), [Mathematical Description of Linear Dynamical Systems](https://epubs.siam.org/doi/10.1137/0301010): controllability, observability, and realization from input-output behavior.
- [MIT Underactuated Robotics, System Identification](https://underactuated.mit.edu/sysid.html): insufficiently exciting passive trajectories, active excitation, impulse responses.
- [2025, The shortest experiment for linear system identification](https://www.sciencedirect.com/science/article/pii/S0167691125000271): sophisticated minimal experiment design in more general LTI settings.
- [2026, High Effort, Low Gain](https://proceedings.mlr.press/v300/chatzikiriakos26a.html): when active excitation improves system identification sample complexity.
- [Stanford Encyclopedia of Philosophy, Causal Models](https://plato.stanford.edu/entries/causal-models/): observational versus intervention-based reasoning.

**No claim of physical universality, new theoretical novelty, or hardware-level application is made.** Different initial states, unknown model families, restricted controls, measurement noise, nonlinearity, or absence of resets change what is identifiable.