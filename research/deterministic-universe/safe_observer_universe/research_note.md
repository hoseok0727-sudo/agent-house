# A safety-constrained observer inside a deterministic universe

Date: 2026-11-04. **Exploratory model; not a new scientific discovery or a model of actual cosmology.**

## 1. Mathematical setup

The unknown physical law is a static parameter `theta in {0,1,2,3}`, with prior 1/4 per value. The observer is embedded in the world and has only one continuing life. Its actions and the (noiseless) outputs are:

| Action | Outcome | Survivor? |
|---|---|---|
| `wait` | 0 | yes, all theta |
| `scan` | `theta mod 2` | yes, all theta |
| `probe_even` | `floor(theta/2)` if theta even | yes iff theta even |
| `probe_odd` | `floor(theta/2)` if theta odd | yes iff theta odd |

A correct terminal report must identify theta, and a robust-safe policy must preserve survival for **every** candidate theta and (if included) every admissible error tape.

## 2. Noiseless adaptive result

An exhaustive belief-state search proves that `scan` followed by `probe_even` on scan=0 or `probe_odd` on scan=1 identifies theta in two steps for all four deterministic laws.

One step cannot robustly identify: `scan` gives only one bit; both probes are fatal for half the candidate laws. Hence the policy is depth-optimal.

No fixed nonadaptive sequence can both identify all laws and guarantee survival for every law: any identifying sequence must contain a probe; either specialized probe is fatal in two possible worlds. Without `scan` there is no safe, informative first action.

These are simple consequences of a deliberately constructed action table, not novel results about arbitrary dynamical systems.

## 3. Noisy sensing without physical randomness

Let the observation at safe scan `t` be `r_t = (theta mod 2) XOR e_t`. Each `e_t` is a fixed bit of the universe's initial hidden microstate. From the observer's perspective, the tape bits have an independent Bernoulli-epsilon prior for `0<epsilon<1/2`. Conditional on the full microstate and theta, the entire universe is deterministic.

For **every finite scan history**, both theta parities have positive likelihood, since all finite error patterns have positive prior probability. Therefore at any finite history both specialized probes are unsafe for at least one still-possible world. Robustly guaranteeing survival excludes both probes. Repeated safe scans never reveal `floor(theta/2)`, so no guaranteed-survival finite-time policy identifies all two law bits.

With a fixed odd number n of safe scans, choose the majority parity and perform the corresponding specialized probe. If the majority is wrong, the observer is destroyed; otherwise it learns the high bit and hence all of theta. For a uniform prior on theta:

`P(destruction) = sum_{j=(n+1)/2}^{n} C(n,j) epsilon^j (1-epsilon)^(n-j)`.

Under `epsilon=0.1`, the script evaluates the weighted probability by exhaustive enumeration of all 2^n deterministic error tapes (and all four theta) and checks that it equals the binomial-tail formula. Even as probability tends to zero with large n, every finite n retains strictly positive risk.

## 4. Knowledge ceiling under safe scans

Let `H(theta | R_1,...,R_n)` be Shannon entropy in bits. Under the prior, the high law bit is independent of **all** scan observations. Therefore

`H(theta | R_1,...,R_n) = 1 + H(theta mod 2 | R_1,...,R_n) >= 1`.

The observer can nearly eliminate uncertainty about parity through many repeated scans, but one independent law bit stays entirely beyond *safe sensing*. When it takes the high-bit probe, the remaining uncertainty vanishes **conditional on survival**, at the cost of a nonzero probability of destruction.

This is a model-specific example of **safe observational equivalence**: the law pairs {0,2} and {1,3} cannot be distinguished by safe scans alone.

## 5. Verified numerical outputs

| Number of scans | Probability of destruction, epsilon=0.1 | Remaining law entropy after safe scans (bits) |
| ---: | ---: | ---: |
| 1 | 0.1000000000 | 1.4689956 |
| 3 | 0.0280000000 | 1.1375823 |
| 5 | 0.0085600000 | 1.0430906 |
| 7 | 0.0027280000 | 1.0139409 |
| 9 | 0.0008909200 | 1.0046002 |
| 11 | 0.0002957061 | 1.0015385 |

The script verifies each analytic failure probability by weighted exhaustive enumeration, and verifies survival plus destruction sums to one. These are not real-world failure rates. The curve is for this particular fixed-length majority-vote strategy; it is **not** a universal optimal risk–information frontier.

## 6. Philosophical interpretation and boundaries

- Ontological determinism is compatible with epistemic uncertainty over initial microstates.
- Safe experimentation may impose a stricter information limit than computing power, even given infinite computation.
- The operator of a simulator may be able to duplicate a world and test a candidate action on disposable replicas. A single observer inside the simulated world has no such guarantee. This is a conditional observation about different experimental permissions, not evidence of simulation.
- A death outcome can be observed by an outside investigator, but the internal observer cannot continue learning after it dies; the identity of the observer therefore matters to the meaning of "successful knowledge acquisition."
- The safe scanning action and hidden law family are *assumed*, not derived from physical principles. Different instrumentation can change the conclusion completely.

## 7. Prior work (selected, not exhaustive)

- Ahmadi, Chaudhry, Sindhwani and Tu (2021), **Safely Learning Dynamical Systems from Short Trajectories**, PMLR 144. https://proceedings.mlr.press/v144/ahmadi21a.html — safe-identification feasibility and impossibility certificates.
- Bıyık, Margoliash, Alimo and Sadigh (2019), **Efficient and Safe Exploration in Deterministic Markov Decision Processes with Unknown Transition Models**. https://iliad.stanford.edu/pdfs/publications/biyik2019efficient.pdf
- Lee and Yannakakis (1994), **Testing finite-state machines: state identification and verification**. https://doi.org/10.1109/12.272431 — adaptive vs preset distinguishing tests.
- Hierons and Türker (2015), **Incomplete Distinguishing Sequences for Finite State Machines**. https://doi.org/10.1093/comjnl/bxv041
- Le, Juba and Stern (2024), **Learning Safe Action Models with Partial Observability**, AAAI. https://doi.org/10.1609/aaai.v38i18.29995

## 8. A genuinely hard follow-up

Can we compute the maximal **survival-constrained identifiable quotient** of a finite dynamical system with unknown laws, costs and partial observability, and synthesize a minimum-risk adaptive test? That becomes a nontrivial belief-space planning problem whose complexity and algorithms should be compared directly against the safe-control and automata-testing literature. If the world also contains a predictor that changes the observer's policy, add reflexive information dynamics, but do **not** assume this toy model establishes a new theorem about the actual universe.