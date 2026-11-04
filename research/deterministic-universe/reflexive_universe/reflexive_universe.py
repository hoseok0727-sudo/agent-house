#!/usr/bin/env python3
"""A deterministic ensemble with forecast-feedback bifurcation.

Research prototype (2026-11-04). Python standard library only.
Not a claim of scientific novelty or a realistic model of free will.

Each microstate z follows z_{t+1}=2z_t mod M, M odd prime, so all M
initial microstates form a permutation at every step. Individuals act
according to a deterministic threshold conditioned on public forecast q.
The ensemble's aggregate is thus exactly count/M, with no stochastic draw.
"""

from __future__ import annotations
import csv
import math
from pathlib import Path

M = 10007    # prime, 2 invertible mod M
T = 100


def sigma(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def response(q: float, beta: float, exposure: float = 1.0, baseline: float = 0.5) -> float:
    """Fraction choosing action 1 after seeing q.

    Non-exposed agents use baseline; exposed agents oppose a more probable action.
    """
    odds = math.log(baseline / (1-baseline))
    return (1-exposure) * baseline + exposure * sigma(odds - beta * (2*q-1))


def step(q: float, beta: float, exposure: float = 1.0, baseline: float = .5, alpha: float = 1.0):
    return (1-alpha)*q + alpha*response(q,beta,exposure,baseline)


def fixed_point(beta: float, exposure: float = 1, baseline: float = .5) -> float:
    lo,hi=0.0,1.0
    for _ in range(100):
        mid=(lo+hi)/2
        if response(mid,beta,exposure,baseline) > mid:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2


def amplitude(beta: float, exposure: float = 1.0) -> float:
    """Nonnegative period-2 magnetization m=2q_high-1."""
    if beta*exposure <= 2:
        return 0.0
    lo, hi = 1e-14, exposure
    for _ in range(120):
        mid = (lo+hi)/2
        if exposure * math.tanh(beta*mid/2) > mid:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2


def finite_universe(beta: float, exposure: float = 1, n_steps: int = T, q0: float = .51):
    """Enumerate every microstate and its deterministic action at each time.

    z=0,...,M-1 initial states; z_t=2^t z_0 mod M.
    Their values form a permutation of the M residues, so the action count
    can be checked both by enumeration and by the forecast threshold.
    """
    z = list(range(M))
    q=q0
    result=[]
    for t in range(n_steps):
        r = response(q,beta,exposure)
        # round to nearest integer threshold, forcing a deterministic action
        threshold = math.floor(M*r+0.5)
        count=sum(x < threshold for x in z)
        assert count == threshold
        realized=count/M
        result.append((t,q,realized,abs(q-realized),count))
        q=realized
        z=[(2*x)%M for x in z]
    return result


def trajectory(beta, exposure=1, alpha=1, baseline=.5, n_steps=T, q0=.51):
    q=q0
    result=[]
    for t in range(n_steps):
        realized=response(q,beta,exposure,baseline)
        result.append((t,q,realized,abs(q-realized)))
        q=(1-alpha)*q+alpha*realized
    return result


def regression_tests():
    # Unique stationary value and correct stability threshold.
    for beta in [0,0.1,1,1.99,2,2.01,3,4,8]:
        for c in [.1,.4,.8,1]:
            fp=fixed_point(beta,c)
            assert abs(fp-.5)<1e-12
            assert abs(response(fp,beta,c)-fp)<1e-12
            m=amplitude(beta,c)
            if beta*c > 2:
                assert m>0 and abs(m-c*math.tanh(beta*m/2))<1e-12
                assert abs(response((1+m)/2,beta,c)-(1-m)/2)<1e-12
            else:
                assert m==0
    # Factor-of-two chaos horizon from a finite-window binary shift:
    # Observing the first k bits of a stream cannot detect a flipped bit j
    # (1-indexed) until t=j-k (t starts at zero), if j>=k.
    bits=list((i*73 % 101)<50 for i in range(192))
    j,k=100,8
    shifted=bits[:]
    shifted[j-1]=not shifted[j-1]
    first=next(t for t in range(192-k+1) if bits[t:t+k]!=shifted[t:t+k])
    assert first == j-k
    # Two cyclic attractors for strong response, one point for weak response.
    strong=trajectory(4,n_steps=250)[-10:]
    weak=trajectory(1,n_steps=150)[-10:]
    m=amplitude(4)
    assert max(abs(v[1]-.5) for v in weak) < 1e-10
    assert max(abs(abs(2*v[1]-1)-m) for v in strong) < 1e-10
    # Damping stabilization criterion alpha < 4/(2+beta*exposure)
    damped=trajectory(4,alpha=.5,n_steps=120)[-10:]
    assert max(abs(v[1]-.5) for v in damped)<1e-10
    # Microstates explicitly evolve, and the exact fractions match the target
    # within one grid step at every time.
    micro=finite_universe(4,n_steps=64)
    assert max(abs(q1-response(q,4)) for _,q,q1,_,_ in micro) <= 1/M
    return True


def write_results(target: Path):
    target.mkdir(parents=True,exist_ok=True)
    with (target/'trajectories.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['model','beta','exposure','alpha','t','forecast_q','realized_rate','abs_gap'])
        for beta,c,alpha,name in [(1,1,1,'subcritical'),(2,1,1,'critical'),(2.5,1,1,'supercritical'),(4,1,1,'strong'),(4,.4,1,'partial_disclosure'),(4,1,.5,'damped')]:
            for t,q,r,gap in trajectory(beta,c,alpha,n_steps=100):
                w.writerow([name,beta,c,alpha,t,f'{q:.12f}',f'{r:.12f}',f'{gap:.12f}'])
        for t,q,r,gap,_ in finite_universe(4,n_steps=100):
            w.writerow(['finite_deterministic',4,1,1,t,f'{q:.12f}',f'{r:.12f}',f'{gap:.12f}'])
    with (target/'phase_diagram.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['beta','exposure','product','amplitude','q_low','q_high','naive_stable'])
        for c in [.25,.4,.5,.6,.8,1.0]:
            for beta in [0,.5,1,1.5,1.9,2,2.01,2.1,2.5,3,4,5,6,8,10]:
                m=amplitude(beta,c)
                w.writerow([beta,c,beta*c,f'{m:.12f}',f'{(1-m)/2:.12f}',f'{(1+m)/2:.12f}',beta*c<2])


def summarize():
    print('regression tests:',regression_tests())
    for beta,c,alpha,name in [(1,1,1,'beta1'),(2,1,1,'beta2'),(2.5,1,1,'beta2.5'),(4,1,1,'beta4'),(4,.4,1,'beta4 exposed40%'),(4,1,.5,'beta4 damped')]:
        data=trajectory(beta,c,alpha,n_steps=500)
        tail=[v[1] for v in data[-20:]]
        print(f'{name:>20}: last q min={min(tail):.9f}, max={max(tail):.9f}, theoretical amplitude={amplitude(beta,c):.9f}, criterion beta*c={beta*c}')
    for beta in [2.01,2.05,2.1,2.2,3,4,6,8]:
        print(f'beta={beta:4g}  m={amplitude(beta):.9f} qlow={(1-amplitude(beta))/2:.9f}, qhigh={(1+amplitude(beta))/2:.9f}')
    for beta in [0,1,2,4,8,16,32]:
        q=fixed_point(beta,baseline=.9)
        H=-(q*math.log2(q)+(1-q)*math.log2(1-q))
        print(f'biased r=0.9 beta={beta:2d} stationary q={q:.9f} H={H:.9f} bits')
    finite=finite_universe(4,n_steps=500)
    print('finite universe 10007 microstates:', ', '.join(f'{v[1]:.6f}' for v in finite[-8:]))
    print('finite vs continuous abs pair extreme:',min(v[1] for v in finite[-20:]), max(v[1] for v in finite[-20:]))
    print('max discrete fraction error:',max(abs(v[2]-response(v[1],4)) for v in finite))

if __name__ == '__main__':
    summarize()
    write_results(Path(__file__).parent)
    print('Wrote trajectories.csv and phase_diagram.csv')
