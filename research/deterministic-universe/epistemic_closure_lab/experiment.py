"""Epistemic closure under stabilization: finite exact verification + Gaussian checks.

Research toy, not a new general theorem or evidence about actual physics.
Model: x[t+1]=(1+b)x[t]-b*u[t], b in {1,2}; nominal u=x.
A probe u=x+delta produces residual -b*delta.
Robust test: absolute sensor error <= sigma, independently allowed each reset trial.
Gaussian test: independent zero-mean noise with standard deviation sigma.
"""
from __future__ import annotations
from math import erfc, sqrt
from pathlib import Path
import csv
import random

HERE=Path(__file__).resolve().parent


def step(x: int, u: int, b: int) -> int:
    return (1+b)*x-b*u


def residual_set(b: int, delta: int, sigma: int) -> set[int]:
    return {-b*delta+e for e in range(-sigma,sigma+1)}


def robust_possible(R: int, sigma: int) -> tuple[bool,int|None]:
    # Each world must stay within R of x at the end of a probe.
    for delta in range(-R,R+1):
        if all(abs(step(10,10+delta,b)-10)<=R for b in (1,2)):
            if residual_set(1,delta,sigma).isdisjoint(residual_set(2,delta,sigma)):
                return True,delta
    return False,None


def normal_error(delta:float, sigma:float, n:int) -> float:
    # Bayes minimum error for balanced two-Gaussian hypotheses / repeated reset probes.
    if delta==0: return .5
    return .5*erfc(abs(delta)*sqrt(n)/(2*sigma*sqrt(2)))


def simulate_error(delta:float, sigma:float, n:int, trials:int=50000, seed:int=20261104) -> float:
    rng=random.Random(seed)
    wrong=0
    midpoint=-1.5*delta
    for _ in range(trials):
        b=rng.choice((1,2))
        # Gaussian mean has sd sigma/sqrt(n), so can sample directly.
        observed=-b*delta+rng.gauss(0,sigma/sqrt(n))
        guessed=2 if observed<midpoint else 1
        wrong+=guessed!=b
    return wrong/trials


def run() -> None:
    for x0 in (-9,-1,0,1,7,18):
        for b in (1,2):
            x=x0
            for _ in range(200):
                x=step(x,x,b)
                assert x==x0
    print('PASS: 6 initial conditions x 2 worlds x 200 nominal steps produce identical states')

    sigma=2
    rows=[]
    for R in range(0,17):
        found,delta=robust_possible(R,sigma)
        expected=R>4*sigma and R//2>=2*sigma+1 # exact grid for sigma=2
        assert found==expected, (R,found,expected)
        rows.append((R,found,delta if delta is not None else ''))
    print('PASS: exhaustive bounded-error safe-probe classification at R=0..16, sigma=2')
    with (HERE/'robust_frontier.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['safety_radius_R','guaranteed_one_probe_identification','example_delta']);writer.writerows(rows)

    # Explicit worst-case indistinguishable observation for R=8 / delta=4.
    common=residual_set(1,4,2) & residual_set(2,4,2)
    assert common=={-6}
    print('R=8, delta=4 -> common measurement',common)
    ok,d=robust_possible(10,2)
    assert ok and abs(d)==5
    print('R=10 -> safe separating probe delta=',d)

    sample_rows=[]
    for R in (4,8,10):
        delta=R/2
        for n in (1,4,16,64):
            pred=normal_error(delta,2,n)
            emp=simulate_error(delta,2,n)
            # Monte Carlo tolerance wide enough for very small errors.
            assert abs(pred-emp)<0.008, (R,n,pred,emp)
            sample_rows.append((R,delta,n,pred,emp))
    with (HERE/'stochastic_tradeoff.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['safety_radius_R','probe_delta','number_of_reset_trials','theoretical_Bayes_error','simulated_error']);w.writerows(sample_rows)
    print('PASS: Gaussian experiment matches Bayes error formula at all 12 settings')
    for R,delta,n,exact,emp in sample_rows:
        if R==4:print('R=%d N=%d P(error) predicted %.6f / simulated %.6f'%(R,n,exact,emp))

if __name__=='__main__':run()