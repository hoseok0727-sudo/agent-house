#!/usr/bin/env python3
"""Coupled predictor agents on a directed ring: spatial frustration vs temporal cycles.
Each node i's next forecast equals an anti-response to its successor's
current forecast. Fully deterministic. Illustrative known dynamical systems.
"""
import math
from pathlib import Path
import csv

def f(q,beta):
    return 1/(1+math.exp(beta*(2*q-1)))

def evolve(n,beta=4.0,steps=1000,init=None):
    q=list(init if init is not None else [0.31+.07*((i*17)%7) for i in range(n)])
    assert all(0<z<1 for z in q)
    rows=[]
    for t in range(steps):
        rows.append((t,*q))
        q=[f(q[(i+1)%n],beta) for i in range(n)]
    return rows

def max_phase_difference(rows,period,tail=100):
    vals=rows[-tail:]
    return max(abs(rows[t][i]-rows[t-period][i]) for t in range(len(rows)-tail,len(rows)) for i in range(1,len(rows[0])))

def proper_stationary_coloring(n):
    return None if n%2 else [i%2 for i in range(n)]

if __name__=='__main__':
    records=[]
    for n in (2,3,4,5,6,7):
        # Asymmetric, deterministic initial forecasts to break symmetry.
        init=[0.20+.11*((i*3+1)%6) for i in range(n)]
        rows=evolve(n,4,1100,init)
        # After transient, since f has an attracting two-cycle for beta=4,
        # each node is near either endpoint and sequence repeats within 2*n.
        p2n=max_phase_difference(rows,2*n)
        # For odd cycles, t+n yields the opposite binary pattern; for even
        # cycles, t+n recovers the original pattern.
        pn=max_phase_difference(rows,n)
        stationary=max_phase_difference(rows,1)
        print(f'n={n}, stationarity gap={stationary:.8f}, period-n gap={pn:.8e}, period-2n gap={p2n:.8e}, fixed alternating coloring={proper_stationary_coloring(n) is not None}')
        assert p2n<1e-10
        assert pn<1e-10 if n%2==0 else pn>0.9
        # Only selected generic initial states; no universal convergence claim.
        records.extend((n,t,*r[1:]) for t,r in enumerate(rows[-2*n:]))
    path=Path(__file__).parent/'cyclic_network_trajectories.csv'
    with path.open('w',newline='') as h:
        out=csv.writer(h)
        out.writerow(['n','relative_step']+[f'q{i}' for i in range(7)])
        for row in records:
            out.writerow(list(row)+['']*(9-len(row)))
    print('Wrote',path.name)
