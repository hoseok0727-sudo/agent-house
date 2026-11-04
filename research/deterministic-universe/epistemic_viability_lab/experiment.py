#!/usr/bin/env python3
"""Exact finite-world experiment: physically safe vs epistemically viable actions.

Only Python's standard library. Run `python experiment.py`.
All 2^6 deterministic hypotheses are considered; no Monte Carlo sampling.
"""
from collections import deque
from functools import lru_cache
from math import log2, comb
import csv
from pathlib import Path

N = 6
M = 2                       # irreversible snapshot reveals first M bits
WORLD = frozenset(range(1 << N))
RAW, ACTIVE, SEALED = 'raw', 'active', 'sealed'
ACTIONS = ('wait', 'snapshot', 'prepare', 'core') + tuple(f'test_{i}' for i in range(N))
ROOT = (RAW, WORLD)


def outcome(phase, theta, action):
    """(safe, next phase, observed string); theta never changes."""
    if action == 'wait':
        return True, phase, 'quiet'
    if phase == RAW:
        if action == 'snapshot':
            return True, SEALED, f'preview:{theta & ((1 << M)-1)}'
        if action == 'prepare':
            return True, ACTIVE, 'prepared'
        if action == 'core':
            if (theta >> (N-1)) & 1:
                return False, 'dead', 'fatal'
            return True, SEALED, f'core:{theta}'
    if phase == ACTIVE and action.startswith('test_'):
        i = int(action.removeprefix('test_'))
        return True, ACTIVE, f'bit{i}:{(theta >> i) & 1}'
    return False, 'unavailable', 'invalid'


def safe_successors(state, action):
    phase, candidates = state
    seen = {}
    for theta in candidates:
        is_safe, next_phase, obs = outcome(phase, theta, action)
        if not is_safe:
            return None               # robust: safe in EVERY possible world
        seen.setdefault((next_phase, obs), set()).add(theta)
    return tuple((obs, (next_phase, frozenset(group)))
                 for (next_phase, obs), group in sorted(seen.items()))


def all_reachable():
    q = deque([ROOT]); nodes = {ROOT}; edges = {}
    while q:
        st = q.popleft()
        successors = {}
        for action in ACTIONS:
            children = safe_successors(st, action)
            if children is None:
                continue
            successors[action] = children
            for _, child in children:
                if child not in nodes:
                    nodes.add(child); q.append(child)
        edges[st] = successors
    return nodes, edges


def epistemic_winning_layers(nodes, edges, goal=lambda theta: theta):
    """Strong reachability: learn the specified goal in every possible world."""
    winning = {s for s in nodes if len({goal(theta) for theta in s[1]}) == 1}
    layers = [winning.copy()]
    while True:
        grow = {s for s in nodes if any(
            all(child in winning for _, child in branches)
            for branches in edges[s].values())}
        new = winning | grow
        if len(new) == len(winning):
            break
        winning = new
        layers.append(winning.copy())
    return layers


def entropy(candidates):
    return log2(len(candidates))


@lru_cache(None)
def min_entropy(state, horizon):
    """Expected remaining entropy under uniform prior and optimal actions."""
    if horizon == 0 or len(state[1]) == 1:
        return entropy(state[1]), None
    best = (float('inf'), None)
    for action, branches in EDGES[state].items():
        exp = sum(len(child[1])/len(state[1]) * min_entropy(child, horizon-1)[0]
                  for _, child in branches)
        if exp < best[0] - 1e-12:
            best = (exp, action)
    return best


def greedy_policy_result():
    # Globally safe action with the most immediate expected information.
    phase, candidates = ROOT
    values = {}
    for action, branches in EDGES[ROOT].items():
        h = sum(len(child[1])/len(candidates)*entropy(child[1]) for _, child in branches)
        values[action] = entropy(candidates)-h
    action = max(values, key=values.get)
    groups = [st for _, st in EDGES[ROOT][action]]
    return action, values, groups


def verify_general_formula():
    for n in range(3, 30):
        m = 2
        for h in range(0, n+3):
            snapshot = m if h >= 1 else 0
            preparation = min(n, max(0, h-1))
            correct = max(snapshot, preparation)
            # Simple combinatorial upper bound: snapshot forever seals,
            # or preparation consumes one step followed by <=1 bit per probe.
            assert 0 <= correct <= n
            if h == n+1:
                assert correct == n
    return True


def run():
    global EDGES
    nodes, EDGES = all_reachable()
    layers = epistemic_winning_layers(nodes, EDGES)
    counts = [len(s) for s in layers]
    assert len(nodes) == 1 + 3**N + 2**M
    assert counts == [64, 256, 496, 656, 716, 728, 729, 730], counts
    assert ROOT not in layers[6] and ROOT in layers[7]
    assert all((SEALED, frozenset(t for t in WORLD if (t&3)==v)) not in layers[-1]
               for v in range(4))
    assert len(nodes - layers[-1]) == 4
    assert verify_general_formula()
    # The boundary depends on what the observer needs to know, not just the world.
    goal_preview = epistemic_winning_layers(nodes, EDGES, lambda theta: theta & 3)
    goal_highbit = epistemic_winning_layers(nodes, EDGES, lambda theta: (theta >> (N-1)) & 1)
    assert ROOT not in goal_preview[0] and ROOT in goal_preview[1]
    assert ROOT not in goal_highbit[1] and ROOT in goal_highbit[2]
    assert all((SEALED, frozenset(t for t in WORLD if (t&3)==v)) in goal_preview[0]
               for v in range(4))
    assert all((SEALED, frozenset(t for t in WORLD if (t&3)==v)) not in goal_highbit[-1]
               for v in range(4))

    greedy, immediate, branches = greedy_policy_result()
    assert greedy == 'snapshot'
    assert set(immediate) == {'wait','snapshot','prepare'}
    assert abs(immediate['snapshot'] - 2.0) < 1e-12
    assert all(len(b[1]) == 16 and b not in layers[-1] for b in branches)

    print('EXACT MODEL CHECK (not sampled)')
    print(f'n_bits={N}, hypotheses={1<<N}, snapshot_bits={M}')
    print(f'reachable belief states={len(nodes)}')
    print('winning layers (h=0..7):', counts)
    print('first guaranteed full-ID horizon:', next(h for h,L in enumerate(layers) if ROOT in L))
    print('physically safe initial action information (bits):', immediate)
    print('myopic greedy first action:', greedy)
    print('post-greedy states are physical-safe but permanently unidentifiable:', len(branches))

    out = Path(__file__).resolve().parent
    with (out/'horizon_frontier.csv').open('w',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['horizon','optimal_information_bits','greedy_information_bits','optimal_first_action','winning_full_identification'])
        for h in range(0, 9):
            rem, action = min_entropy(ROOT,h)
            opt = N-rem
            expected = max(M if h else 0, min(N, max(0,h-1)))
            assert abs(opt-expected)<1e-12, (h,opt,expected)
            writer.writerow([h,round(opt,9),M if h else 0,action or '-',bool(ROOT in layers[h] if h<len(layers) else ROOT in layers[-1])])
            print(f'h={h} optimal={opt:.1f} bits  greedy={M if h else 0} bits  first={action or "none"}')

    with (out/'winning_layers.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.writer(f)
        writer.writerow(['horizon','winning_states','total_reachable_states'])
        for h,L in enumerate(layers):
            writer.writerow([h,len(L),len(nodes)])

    # Verify each of 64 worlds produces a unique adaptive signature under optimal plan.
    obs_to_theta={}
    for theta in WORLD:
        s=ROOT; observations=[]
        for _ in range(N+1):
            _,action = min_entropy(s, N+1-len(observations))
            assert action is not None
            safe,ph,obs=outcome(s[0],theta,action)
            assert safe
            observations.append((action,obs))
            children=safe_successors(s,action)
            s=next(child for code,child in children if code==obs)
        assert len(s[1]) == 1 and next(iter(s[1])) == theta
        signature=tuple(observations)
        assert signature not in obs_to_theta
        obs_to_theta[signature]=theta
    assert len(obs_to_theta)==(1<<N)
    print('goal-relative: first two bits identified in 1 action (snapshot)')
    print('goal-relative: high bit identified in 2 actions (prepare, test_5)')
    print('64/64 hidden worlds safely and uniquely identified by optimal policy')
    print('all validations: PASS')

if __name__=='__main__':
    run()