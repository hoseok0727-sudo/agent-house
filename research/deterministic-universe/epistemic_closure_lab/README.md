# Epistemic Closure by Stabilization — Toy Research Lab

Research prototype, 2026-11-04. **Not a claimed novel theorem** or an empirical finding about the physical universe.

The lab investigates how a feedback policy can make two different deterministic systems observationally identical, and how a constrained safe probe can identify the hidden law only above a measurement-error threshold.

## Model

For an unknown coefficient `b` in `{1, 2}`:

`x_{t+1} = (1+b) x_t - b u_t`.

The nominal stabilizing controller `u_t=x_t` ensures `x_{t+1}=x_t` in both worlds. Under a probe `u_t=x_t+delta`, the state changes by `-b*delta`.

Under a one-step safety radius `R` for both models and an adversarial bounded sensor error `|eta|<=sigma`, a **single** universally safe, guaranteed-distinguishing probe exists **iff** `R>4*sigma`, assuming continuous control and exact knowledge of pre-probe state. See [the note](research_note.md) for the proof and scope.

In a repeated, independently reset experiment with Gaussian measurement noise of standard deviation `sigma`, the equal-prior Bayes error is `Phi(-|delta| sqrt(n)/(2 sigma))`.

## Reproduce

Python 3 standard library, no third-party dependencies:

```sh
python experiment.py
```

This writes:

- `robust_frontier.csv` — exhaustive integer probe and bounded-error classification.
- `stochastic_tradeoff.csv` — Gaussian analytic and simulated classification error.

Seeds are deterministic. Runtime and random simulation results may vary slightly between environments/Python versions.

## Limitations

- A narrow two-model, one-dimensional deterministic system, not a general theorem about universes, societies, or AI.
- Safety means **one-step displacement** from a known state, not a proof of long-run viability.
- Robust impossibility under repeated tests refers to independent one-step trials, each reset to the same initial state, with bounded **adversarial** sensor error. Without resets, richer inputs, additional measurements, or extra assumptions, conclusions may differ.
- Gaussian-noise gains require independent errors and repeatable experiments; finite repeated measurements do not confer absolute certainty.
- Policy intervention may change the target of prediction, as in performative prediction; that effect is not simulated here.

## Select prior art

- Perdomo et al. (ICML 2020), *Performative Prediction*: https://proceedings.mlr.press/v119/perdomo20a.html
- Shardt et al. (2015), *Minimal required excitation for closed-loop identification*: https://doi.org/10.1016/j.jprocont.2015.01.009
- Joshi et al. (AAAI 2024), *Towards Safe Policy Learning under Partial Identifiability*: https://doi.org/10.1609/aaai.v38i12.29198
- Capone et al. (ICML 2025), *Learning Safe Control via On-the-Fly Bandit Exploration*: https://proceedings.mlr.press/v267/capone25a.html
- Yang et al. (TPAMI 2026), *On the Equilibrium Between Feasible Zone and Uncertain Model in Safe Exploration*: https://doi.org/10.1109/TPAMI.2026.3669907

Developed with AI assistance. Not posted to GitHub.