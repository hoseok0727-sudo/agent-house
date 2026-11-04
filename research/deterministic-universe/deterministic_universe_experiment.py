#!/usr/bin/env python3
"""A causal-observability and public-prophecy experiment in a deterministic toy world.

Dependencies: numpy
Run: python deterministic_universe_experiment.py
The prophecy part is a coupled finite-state protocol *on top of* Rule 30,
not an implemented conscious agent or an infallible predictor.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

SEED = 20261104
SIZE = 513
CENTER = SIZE // 2
WINDOW = 4
STEPS = 150


def rule30(state: np.ndarray) -> np.ndarray:
    # Rule 30: new = left XOR (center OR right), all arithmetic Boolean.
    return np.bitwise_xor(np.roll(state, 1), np.bitwise_or(state, np.roll(state, -1)))


def history_with_flip(offset: int) -> dict:
    rng = np.random.default_rng(SEED)
    a = rng.integers(0, 2, SIZE, dtype=np.uint8)
    b = a.copy()
    b[CENTER + offset] ^= 1
    first_observed = None
    global_differences = {}
    observation_equal = {}
    for t in range(STEPS):
        different = not np.array_equal(
            a[CENTER-WINDOW:CENTER+WINDOW+1],
            b[CENTER-WINDOW:CENTER+WINDOW+1],
        )
        observation_equal[t] = not different
        if different and first_observed is None:
            first_observed = t
        if t in (0, 20, 40, 55, 56, 60, 70, 100, 149):
            global_differences[t] = int(np.count_nonzero(a != b))
        a, b = rule30(a), rule30(b)
    lower_bound = abs(offset) - WINDOW
    assert all(observation_equal[t] for t in range(min(STEPS, lower_bound)))
    assert first_observed is None or first_observed >= lower_bound
    return {
        'offset': offset,
        'earliest_allowed': lower_bound,
        'first_observed': first_observed,
        'global_difference_at_149': global_differences[149],
        'global_differences': global_differences,
    }


def forecast_delivery(source_position: int, target_position: int, steps: int, bit: int):
    """Explicit local channel: a presence flag and bit move right by one per step."""
    assert 0 <= source_position <= target_position < SIZE
    assert bit in (0, 1)
    present = np.zeros(SIZE, dtype=np.uint8)
    values = np.zeros(SIZE, dtype=np.uint8)
    present[source_position] = 1
    values[source_position] = bit
    latched = False
    latched_bit = 0
    for _ in range(steps):
        # No wraparound: message only travels right, one cell per tick.
        present = np.concatenate((np.zeros(1, dtype=np.uint8), present[:-1]))
        values = np.concatenate((np.zeros(1, dtype=np.uint8), values[:-1]))
        if present[target_position]:
            latched = True
            latched_bit = int(values[target_position])
    return latched, latched_bit


def background_bit(horizon: int) -> int:
    rng = np.random.default_rng(SEED)
    state = rng.integers(0, 2, SIZE, dtype=np.uint8)
    for _ in range(horizon):
        state = rule30(state)
    return int(state[CENTER])


def action(policy: str, forecast_bit: int, received: bool, base_bit: int) -> int:
    if not received:
        return base_bit
    if policy == 'invert':
        return 1 - forecast_bit
    if policy == 'copy':
        return forecast_bit
    if policy == 'ignore':
        return base_bit
    if policy == 'xor':
        return base_bit ^ forecast_bit
    raise ValueError(policy)


@dataclass(frozen=True)
class ForecastCase:
    horizon: int
    policy: str
    message_received: bool
    base_bit: int
    outcomes_for_announcements: tuple[int, int]
    self_consistent_announcements: tuple[int, ...]


def fixed_points(distance: int, horizon: int, policy: str) -> ForecastCase:
    base = background_bit(horizon)
    outputs = []
    receptions = []
    for prediction in (0, 1):
        delivered, arrived_bit = forecast_delivery(CENTER-distance, CENTER, horizon, prediction)
        receptions.append(delivered)
        outputs.append(action(policy, arrived_bit if delivered else prediction, delivered, base))
    assert receptions[0] == receptions[1]
    fps = tuple(p for p in (0, 1) if outputs[p] == p)
    return ForecastCase(horizon, policy, receptions[0], base, tuple(outputs), fps)


def main():
    print('EXPERIMENT A — deterministic local observability (Rule 30)')
    for offset in (-60, +60, -20, +20):
        r = history_with_flip(offset)
        print('offset={offset:+d}   causal_lower_bound={earliest_allowed}   first_observed={first_observed}   differing_cells_at_t149={global_difference_at_149}/513'.format(**r))
    print()
    print('EXPERIMENT B — forecast signal travels at 1 cell/step, 40 cells to agent')
    distance = 40
    for horizon in (39, 40, 41):
        for policy in ('invert','copy','ignore','xor'):
            r = fixed_points(distance, horizon, policy)
            print('H={:2d} policy={:6s} received={}  baseline={}   actions_given_(p=0,p=1)={}   correct_public_forecasts={}'.format(r.horizon,r.policy,r.message_received,r.base_bit,r.outcomes_for_announcements,list(r.self_consistent_announcements)))
            if policy == 'invert':
                assert (r.self_consistent_announcements == (r.base_bit,)) if horizon < distance else (r.self_consistent_announcements == ())
    print()
    print('EXPERIMENT C — probabilistic forecast consistency in an entirely deterministic ensemble')
    # Unknown microstate is one of 256 equally weighted deterministic states.
    # For announced probability q=k/256, the response is 1 exactly when u<256-k.
    candidates=[]
    for k in range(257):
        ones=sum(1 for u in range(256) if u < 256-k)
        if k == ones:
            candidates.append(k)
    assert candidates == [128]
    print('Epistemically calibrated probability forecasts (grid k/256):', [k/256 for k in candidates])
    print('At q=1/2: 128 of 256 deterministic microstates choose 1, 128 choose 0.')
    print()
    print('RESULT: a deterministic trajectory exists for every announcement;')
    print('the impossibility is of a public infallible binary forecast against a contrarian listener.')


if __name__ == '__main__':
    main()