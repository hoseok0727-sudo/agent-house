# Epistemic Viability: Safe Actions Can Destroy Future Identifiability

**Status:** reproducible finite-state research laboratory / synthesis of known ideas. Written 2026-11-04. **No priority or novelty claim.** This note defines a small counterexample, proves its exact properties, verifies an exhaustive planner, and spells out where the analogy with real systems breaks.

## Question

Can a physically safe experiment that maximizes immediate information irreversibly destroy the opportunity to fully identify an unknown deterministic model? Yes, in a simple model with irreversible instrumentation. Can the value of that experiment become positive again if the identification goal changes? Yes. We distinguish *physical viability*, *epistemic reachability*, and *goal-relative identifiability*.

## 1. Exact model and assumptions

Unknown, static parameter `theta in {0,...,63}`, prior uniform (64 worlds, 6 bits of entropy). Time is discrete. The observer knows the candidate set and full possible action/observation semantics (real-world model misspecification is excluded). The external world is deterministic, and every observation is noise-free. The observable laboratory phase is one of RAW, ACTIVE, SEALED. Inactive phase transitions are known to the observer; only theta is hidden.

- In **RAW**, `wait` leaves state unchanged and reveals nothing; `snapshot` safely reports the two low bits of theta and irreversibly enters SEALED; `prepare` safely enters ACTIVE and reports no information. A hypothetical `core` action reveals theta but is fatal whenever theta's top bit is 1; thus it is not robustly safe from the initial belief.
- In **ACTIVE**, each `test_i` reveals the selected bit of theta, without changing the phase. Every `test_i` is robustly safe, each test requires one time step.
- In **SEALED**, only `wait` is safe; it returns no additional information.

Safety is **worst-case across all currently possible worlds**. Experiments have no measurement noise. The world parameter does not change. `snapshot` and `prepare` cannot be combined because snapshot permanently closes diagnostics. This irreversibility is an explicit modeling premise, NOT something proven about any physical domain.

## 2. Closed-form horizon result

With an action budget `h` and the goal of maximizing expected Shannon information about the entire theta:

- `snapshot` yields `m=2` bits for any h>=1 and permanently prevents more learning.
- `prepare` consumes one step with zero immediate bits; each following `test_i` reveals at most one new, previously unknown bit, hence at most `min(n,h-1)` for n=6.
- `wait` cannot improve information and has no beneficial state effect.
- `core` is not robustly safe from the initial belief.

Consequently, the exact optimum is

```
I*(h) = max( m * 1[h>=1], min(n, max(0,h-1)) )
```

for the constructed n=6, m=2 world (and generalized to n>m). A myopic information-gain algorithm chooses snapshot for its 2-bit immediate gain over prepare's 0-bit gain. At h=7 it still has only 2 bits, whereas the optimal horizon-aware agent obtains all 6. The horizon at which prepare becomes strictly better is h>=m+2=4, provided n>=m+1; at h=m+1 there is a tie.

The greedy-to-optimal information ratio at a sufficiently long horizon is m/n and can approach zero at fixed m as n increases. This is a **constructed counterexample**, not a theorem that greedy learning usually fails or that information is negative. Existing records are not forgotten: the capacity to obtain more records is lost.

## 3. Safe belief-space reachability theorem

Let `W` be finite (possible pairs of model and dynamic physical state). For belief `B subset W`, an action `a` is robustly safe iff executing it is safe in every w in B. Define `B_{a,o}` to be the successor belief after action a and observation o. For a target function `g(theta)`, a belief is solved if g is constant on its model candidates. Define

```
K_0 = { B : | {g(theta(w)) : w in B} | = 1 }
K_{h+1} = K_h U { B : exists robustly safe a,
                         for all nonempty observation branches o,
                         B_{a,o} in K_h }
```

**Proposition.** For finite deterministic partially observed systems where actions are chosen adaptively after observations, B lies in K_h iff there exists a policy guaranteeing physical safety and determining g(theta) within h actions, in every world consistent with B.

*Proof.* Base h=0 holds by the definition of solved belief. Inductive step: any guaranteeing policy either already solved, or must choose a safe first action; every possible observation leaves a belief from which the remaining h actions guarantee success, so all successors are in K_h. Conversely, choose an action satisfying this criterion, observe the outcome and follow the winning child policy. QED.

`K_infinity` is the fixed point of the monotone iteration, reached after finitely many iterations on a finite belief graph. The number of possible beliefs may be exponential in the number of physical-model states, making general explicit enumeration impractical without compact representations or abstraction. This is a standard strong reachability / belief-state game construction, NOT a new general theorem.

## 4. Exhaustive numerical/model-checking evidence

The reference Python implementation actually enumerates every model-consistent reachable belief and every safely allowed action. For n=6:

- 1 raw initial belief.
- `3^6=729` active beliefs: each of six coefficients is unknown, known-0 or known-1.
- 4 sealed beliefs, one per two-bit snapshot output.
- Total: `1+729+4=734` reachable beliefs.
- All 729 active beliefs are eventually solvable. The raw belief is solved at h=7. All 4 sealed beliefs have 16 indistinguishable candidate worlds and are unsolvable for full identification, even over an arbitrarily large number of safe actions.
- Thus 730 states are eventually solvable and exactly 4 are terminal epistemic dead-ends.

**Winning set sizes K_0...K_7:** `64, 256, 496, 656, 716, 728, 729, 730`. For active beliefs this follows the combinatorial identity

```
|K_h inter ACTIVE| = sum_{j=0}^{min(h,6)} binomial(6,j) * 2^(6-j)
```

There are C(6,j) ways to choose j unknown bits and 2^(6-j) assignments of the remaining bits. For j=6 all active beliefs are included at h=6. The initial RAW belief enters K_7 (one prepare step + six tests). The sealed beliefs never enter K_h for full identification.

A separate explicit simulation executes the optimal 7-step adaptive strategy in **all 64 ground-truth worlds** and confirms no unsafe action, exact singleton inference, and a unique observation/action transcript in every world.

## 5. Goal-relativity

Redefine the target as `g(theta)=theta & 3` (only the two low bits). All four sealed beliefs are already solved and `snapshot` identifies g in one action. The initial belief belongs to K_1 for this target.

Redefine target as `g(theta)= (theta>>5)&1` (only the high bit). Snapshot never identifies g, while prepare + test_5 does so in exactly 2 actions. The initial belief belongs to K_2 but not K_1.

For full theta, the initial belief belongs to K_7 but not K_6. Therefore **epistemic safety and knowledge reachability are relative to the observer's target**. It is incorrect to call snapshot absolutely 'epistemically unsafe'; it is a dead end for full identification but optimal for some narrower tasks.

## 6. Information capacity versus accumulated knowledge

The ordinary mutual information for an observation is nonnegative. Nothing in this example violates data processing or says that recording new observations erases stored information. Define future attainable learning capacity under a specified target, policy class and model as the most additional information obtainable while remaining safe. At the initial RAW belief, capacity for full theta is 6 bits. After prepare, the capacity remains 6 bits. After snapshot, 2 bits were learned, but **additional** attainable information becomes 0 bits. The decrease concerns options, not what is already known.

## 7. Relevance to real-world debates (careful mapping)

1. **AI assurance.** Evaluation under fixed safeguards proves performance within that evaluation regime, not in an unobserved alternate regime. It does not follow that safeguards should be removed; rather, empirical claims must specify scope, and safe surrogate, sandbox, and mechanistic evidence may expand scope without exposing users to dangerous behavior. Do not confuse epistemic coverage with a duty to run risky tests.
2. **Clinical counterfactuals.** If certain patient strata never receive one treatment, nonparametric treatment-effect identification can fail for that stratum without further assumptions, an instance of overlap/positivity failure. The model does not prescribe harmful randomization or withholding indicated treatment. Well-justified structural assumptions or other designs may still yield useful inferences.
3. **Policy evaluation / regulation.** A stabilizing intervention changes the data-generation process; extrapolating from a controlled regime to another regime can be invalid without assumptions. Current stability is not proof of stability in a counterfactual no-policy regime.
4. **Simulation and philosophical underdetermination.** An internal observer's causal and experimental access can prevent discrimination of underlying implementations, even under determinism. This is a logical possibility, not empirical evidence that our universe is simulated.

## 8. Prior work and novelty limits

- A. A. Feldbaum (1964), *On a class of dual control learning systems*: https://www.mathnet.ru/eng/at11622
- W. Nam and R. Alur (2010), *Active learning of plans for safety and reachability goals with partial observability*: https://pubmed.ncbi.nlm.nih.gov/19661004/
- M. Fatemi et al. (2019), *Dead-ends and Secure Exploration in Reinforcement Learning*: https://www.microsoft.com/en-us/research/publication/dead-ends-and-secure-exploration-in-reinforcement-learning/
- H. S. Le, B. Juba, R. Stern (2024), *Learning Safe Action Models with Partial Observability*: https://doi.org/10.1609/aaai.v38i18.29995
- B. Plaut et al. (2026), *Safe Learning Under Irreversible Dynamics via Asking for Help*: https://www.jmlr.org/papers/v27/25-2248.html
- K.-C. Hsu et al. (2024), *The Safety Filter: A Unified View of Safety-Critical Control in Autonomous Systems*: https://doi.org/10.1146/annurev-control-071723-102940
- In causal inference: *Diagnosing and responding to violations in the positivity assumption*: https://pmc.ncbi.nlm.nih.gov/articles/PMC4107929/

The core ideas (nonmyopic learning, belief-space planning, strong reachability, irreversible exploratory dead ends, task-aware observation) have extensive prior art. The notebook is a tiny pedagogical construction, *not* a peer-reviewed novelty claim. A real research contribution would require a new structural condition, complexity bound, approximate-certified algorithm, or credible transfer to a substantial benchmark against prior methods.

## 9. Next genuinely hard technical direction

For a system class larger than explicitly enumerated finite hypotheses, compute a conservative *goal-relative epistemic viability certificate* without enumerating all posterior belief sets. Candidate work:

- Build compact symbolic descriptions of all parameter-world states reachable under safely admissible controls.
- Prove sufficient (not necessarily necessary) conditions that specific experiments preserve future target identifiability, possibly with barrier-function-like certificates in belief space.
- Contrast guaranteed exact identification with high-probability identification under noisy observations; finite-time certainty may be impossible with overlapping observation likelihoods.
- Explicitly measure computation cost and conservatism vs planning with no safety constraints or with only instantaneous physical safety.
- Test on published safe system-identification or fault-diagnosis benchmarks; check novelty against the extensive prior work above.

## Reproduction

Python 3.10+ standard library only:

```bash
python experiment.py
```

Writes `horizon_frontier.csv` and `winning_layers.csv`, prints all checks, and exits with an assertion failure if the exact claims break. Timings not claimed because performance is not the research result.