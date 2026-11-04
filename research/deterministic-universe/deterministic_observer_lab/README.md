# Deterministic Observer Lab

**A 12-bit reversible universe can appear exactly like independent coin tosses for the first 12 observed bits.** Another reversible 12-bit universe has an almost identical local statistical appearance, yet its entire linear law is recovered from 24 bits. This research demonstration separates deterministic dynamics, finite-window uncertainty, theory identification, and prediction.

- **Status:** reproducible mathematical thought experiment; not new peer-reviewed mathematics or evidence for a simulated universe.
- **Date:** 2026-11-04.
- **Main result:** the cyclic binary de Bruijn process of order k, observed from a uniformly random phase, has conditional next-bit entropy 1 bit for histories shorter than k and 0 thereafter. Its length-T observation distribution has total variation distance 0 from a fair IID coin for T <= k, and 1 - 2^(k-T) for T > k.
- **Comparison:** a primitive 12-bit LFSR reconstructed by Berlekamp–Massey from 24 bits; the particular 12-bit de Bruijn sequence has periodic linear complexity 4094, despite a 12-bit nonlinear state.
- **Robustness:** Bayesian phase reconstruction with 2% and 5% observational bit-flip noise.

## Reproduce

```bash
python -m pip install numpy
python experiment.py
python tests.py
python diagonal.py
```

## Contents

| File | Purpose |
|---|---|
| `research_note.md` | Derivations, assumptions, proof sketches, philosophical interpretation, novelty limitations, references |
| `experiment.py` | Exact cyclic enumeration, Berlekamp–Massey recovery, optional noisy measurements |
| `tests.py` | Four independent property tests |
| `diagonal.py` | Construct a computable world that defeats a fixed total computable predictor at every step |
| `conditional_entropy.csv` | Per-order conditional entropies and best Markov accuracy |
| `distinguishability.csv` | Total variation distances from IID |
| `noise_robustness.csv` | Finite-sample Bayesian phase inference |
| `test_output.txt` | Saved experimental stdout |

All public descriptions are conditional on a known model family and a uniform unknown phase. The simulation makes no claim that our physical universe has these properties. AI-assisted research prototype; treat novelty as unverified.