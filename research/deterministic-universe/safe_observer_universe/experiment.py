"""Safe observer universe: exact finite-state safety-aware identification demo.

All worlds have deterministic laws and a preselected deterministic measurement
error tape. Probabilities below express the observer's uncertainty about tapes.
Requires Python 3.9+ standard library only.
Run: python experiment.py
"""
from __future__ import annotations
from functools import lru_cache
from itertools import product
from math import comb, log2
from pathlib import Path
import csv

THETAS = frozenset(range(4))  # hidden laws 0,1,2,3; bit0=parity, bit1=high bit
ACTIONS = ("wait", "scan", "probe_even", "probe_odd")


def outcome(theta: int, action: str, scan_error: int = 0):
    """Return (observation, is_alive). An unsafe probe ends this observer."""
    if action == "wait": return 0, True
    if action == "scan": return (theta % 2) ^ scan_error, True
    if action == "probe_even":
        return ((theta >> 1), True) if theta % 2 == 0 else (None, False)
    if action == "probe_odd":
        return ((theta >> 1), True) if theta % 2 == 1 else (None, False)
    raise ValueError(action)


def safe(action: str, belief: frozenset[int]) -> bool:
    return all(outcome(theta, action)[1] for theta in belief)


def groups(belief: frozenset[int], action: str):
    assert safe(action, belief)
    partition = {}
    for theta in belief:
        result, _ = outcome(theta, action)
        partition.setdefault(result, set()).add(theta)
    return {obs: frozenset(subset) for obs, subset in partition.items()}


@lru_cache(None)
def synthesise(belief: frozenset[int], depth: int):
    """Exhaustive search for a robust-safe adaptive identification decision tree."""
    if len(belief) == 1: return {"identified": next(iter(belief))}
    if depth <= 0: return None
    for action in ACTIONS:
        if not safe(action, belief): continue
        branches = groups(belief, action)
        if len(branches) == 1: continue  # no information; no hidden dynamics in demo
        children = {str(obs): synthesise(sub, depth-1) for obs, sub in branches.items()}
        if all(v is not None for v in children.values()):
            return {"action": action, "branches": children}
    return None


def has_safe_preset_strategy(belief: frozenset[int], max_depth: int) -> bool:
    """A fixed action sequence used identically for every theta, no adaptation."""
    for depth in range(max_depth+1):
        for seq in product(ACTIONS, repeat=depth):
            if not all(all(outcome(theta, a)[1] for a in seq) for theta in belief):
                continue
            histories = [tuple(outcome(theta,a)[0] for a in seq) for theta in belief]
            if len(set(histories)) == len(belief):
                return True
    return False


def majority_error(n: int, epsilon: float) -> float:
    assert n % 2 == 1
    return sum(comb(n,j)*epsilon**j*(1-epsilon)**(n-j) for j in range(n//2+1,n+1))


def enumerate_tapes(n: int, epsilon: float):
    """Enumerate deterministic bit tapes, weighted by an epistemic Bernoulli prior."""
    deaths = 0.0
    full_success = 0.0
    for theta in THETAS:
        for tape in product((0,1), repeat=n):
            weight=(epsilon**sum(tape))*((1-epsilon)**(n-sum(tape)))/len(THETAS)
            observations = [outcome(theta,"scan",e)[0] for e in tape]
            parity_guess=int(sum(observations)>n//2)
            action="probe_odd" if parity_guess else "probe_even"
            observed,alive=outcome(theta,action)
            if not alive:
                deaths+=weight
            else:
                full_success+=weight
                inferred=2*observed+parity_guess
                assert inferred==theta
    return deaths,full_success


def posterior_remaining_entropy(n: int, epsilon: float) -> float:
    """H(theta | n safe noisy scans); the high bit always remains unknown."""
    total=0.0
    for ones in range(n+1):
        p0=comb(n,ones)*epsilon**ones*(1-epsilon)**(n-ones)/2
        p1=comb(n,ones)*(1-epsilon)**ones*epsilon**(n-ones)/2
        mass=p0+p1
        if mass==0: continue
        q=p1/mass
        h=-(q*log2(q) if q>0 else 0)-((1-q)*log2(1-q) if q<1 else 0)
        total+=mass*h
    return 1+total


def main():
    for theta in THETAS:
        assert outcome(theta,"scan")[0]==theta%2
        assert outcome(theta,"probe_odd" if theta%2 else "probe_even")[0]==theta//2
    assert synthesise(THETAS,1) is None
    plan=synthesise(THETAS,2)
    assert plan is not None
    assert plan["action"]=="scan"
    assert not has_safe_preset_strategy(THETAS,4)
    assert not any(safe(a,THETAS) for a in ("probe_even", "probe_odd"))
    assert not any(safe(a,THETAS) for a in ("probe_even", "probe_odd"))
    print('4 deterministic worlds, no measurement noise:')
    print('minimum robust-safe adaptive identification steps = 2')
    print('optimal decision tree =',plan)
    print('fixed open-loop safe identifying sequence <=4 steps =',has_safe_preset_strategy(THETAS,4))
    print('\nNoisy parity screening (worlds deterministic conditional on error tape):')
    rows=[]
    epsilon=0.1
    for n in (1,3,5,7,9,11):
        analytic=majority_error(n,epsilon)
        enum_deaths, enum_survives = enumerate_tapes(n,epsilon)
        entropy=posterior_remaining_entropy(n,epsilon)
        assert abs(enum_deaths-analytic)<1e-12,(n,enum_deaths,analytic)
        assert abs(enum_deaths+enum_survives-1)<1e-12
        assert entropy>=1-1e-12
        print(f'n={n:2d}: death risk={analytic:.10f}, survival={enum_survives:.10f}, H(theta|scans)={entropy:.7f} bits')
        rows.append({'scans':n,'error_rate':epsilon,'death_probability':f'{analytic:.12f}', 'survival_probability':f'{enum_survives:.12f}', 'safe_scans_remaining_entropy_bits':f'{entropy:.12f}'})
    file=Path(__file__).with_name('risk_frontier.csv')
    with file.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print('\nPASS: all exhaustive tests; wrote', file.name)

if __name__=='__main__':
    main()