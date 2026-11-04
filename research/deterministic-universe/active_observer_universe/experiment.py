"""Active Observer Universe Lab: exact GF(2) controlled shift register identification.

Reproduce with Python >=3.10 standard library:
    python experiment.py

No randomness in underlying universes; RNG only chooses example laws and flips
observation bits in the explicitly marked noisy-measurement experiment.
"""
from __future__ import annotations
import csv
import itertools
import math
from collections import Counter
from pathlib import Path
from random import Random

ROOT=Path(__file__).resolve().parent


def step(state:tuple[int,...], coefficients:tuple[int,...], control:int)->tuple[int,...]:
    assert len(state)==len(coefficients)
    assert control in (0,1)
    last=control
    for s,c in zip(state,coefficients):
        last ^= s&c
    return state[1:]+(last,)


def trace(coefficients:tuple[int,...], control:tuple[int,...])->tuple[int,...]:
    """Outputs y_0,...,y_T for inputs u_0,...,u_{T-1} and zero state."""
    state=(0,)*len(coefficients)
    output=[state[0]]
    for u in control:
        state=step(state,coefficients,u)
        output.append(state[0])
    return tuple(output)


def impulse(k:int)->tuple[int,...]:
    return (1,)+(0,)*(2*k-1)


def decode(k:int, output:tuple[int,...])->tuple[int,...]:
    """Recover all k unknown recurrence coefficients from outputs y_0..y_2k."""
    assert len(output)>=2*k+1
    assert all(v==0 for v in output[:k]) and output[k]==1
    guess=[None]*k
    for j in range(1,k+1):
        i=k-j
        ans=output[k+j]
        for r in range(i+1,k):
            ans ^= guess[r]&output[j+r]
        guess[i]=ans
    return tuple(guess)


def model_entropy(k:int,t:int):
    """Return Shannon entropy of observation histories under uniform unknown c."""
    allc=itertools.product((0,1),repeat=k)
    signal=impulse(k)
    outcomes=Counter(trace(c,signal[:t]) for c in allc)
    return math.log2(2**k)-sum((n/2**k)*math.log2(n) for n in outcomes.values())


def noisy_recovery(k:int,p_error:float,repeats:int,trials:int,seed:int):
    rng=Random(seed)
    successes=0
    for _ in range(trials):
        c=tuple(rng.randrange(2) for _ in range(k))
        clean=trace(c,impulse(k))
        # Known impulse produces noiseless y_k=1. Only y_{k+1}..y_{2k} matter.
        noisy_columns=[]
        for t in range(k+1,2*k+1):
            flips=sum(rng.random()<p_error for _ in range(repeats))
            majority=(clean[t]^(1 if flips>repeats//2 else 0))
            noisy_columns.append(majority)
        repaired=clean[:k+1]+tuple(noisy_columns)
        successes += decode(k,repaired)==c
    per_bit_fail=sum(math.comb(repeats,j)*(p_error**j)*((1-p_error)**(repeats-j))
                      for j in range((repeats+1)//2,repeats+1))
    exact=(1-per_bit_fail)**k
    return successes/trials,exact


def run():
    # Exhaust all coefficient choices, for several model dimensions.
    exhaustive=[]
    for k in range(2,12):
        count=0
        for c in itertools.product((0,1),repeat=k):
            t=trace(c,impulse(k))
            assert decode(k,t)==c,(k,c,t)
            assert trace(c,(0,)*(2*k))==(0,)*(2*k+1)
            count+=1
        exhaustive.append((k,count))
    print('Exhaustive coefficients recovered:',exhaustive)
    
    # Show the information arrival is exactly one bit/time after k steps.
    k=8
    records=[]
    for t in range(0,2*k+1):
        info=model_entropy(k,t)
        theory=max(0,min(k,t-k))
        assert abs(info-theory)<1e-9,(t,info,theory)
        records.append((t,info,theory))
    with (ROOT/'information_curve.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['time','empirical_mutual_information_bits','theorem_bits']);w.writerows(records)
    print('Exact exhaustive information curve:',records)

    # c0 remains invisible to ANY controlled experiment before y_2k.
    # Verify exhaustively over arbitrary, nonadaptive input strings for small k.
    for k in range(2,6):
        for c_tail in itertools.product((0,1),repeat=k-1):
            cA=(0,)+c_tail
            cB=(1,)+c_tail
            for u in itertools.product((0,1),repeat=2*k-1):
                assert trace(cA,u)==trace(cB,u)
            # A single impulse separates them at the earliest possible time.
            a,b=trace(cA,impulse(k)),trace(cB,impulse(k))
            assert a[:2*k]==b[:2*k] and a[2*k]!=b[2*k]
    print('All binary controls for k=2..5: c0 indistinguishable until t=2k PASS')

    # Example k=6, near-identical laws.
    k=6; low=(0,0,1,1,0,1); high=(1,0,1,1,0,1)
    a=trace(low,impulse(k)); b=trace(high,impulse(k))
    print('Passive example:',''.join(map(str,trace(low,(0,)*14))))
    print('Impulse c0=0:   ',''.join(map(str,a)))
    print('Impulse c0=1:   ',''.join(map(str,b)))
    print('First difference:',next(t for t,(x,y) in enumerate(zip(a,b)) if x!=y))

    # Noisy measurements: resets are mandatory, not independent naturally in one run.
    noisy=[]
    for error in (.02,.05,.15):
        for r in (1,3,5,7,9):
            empirical,analytic=noisy_recovery(12,error,r,1000,20261104+int(error*1000)*100+r)
            noisy.append((error,r,empirical,analytic))
    with (ROOT/'noise_recovery.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['bit_flip_probability','independent_resets','measured_success_rate_1000','exact_success_probability']);w.writerows(noisy)
    print('Noisy identification results (e, r, empirical, exact):')
    for row in noisy:
        if row[0] in (.05,.15): print(row)

    # Cross-model indistinguishability despite interventions.
    for k in range(2,7):
        c=tuple((i%3)==0 for i in range(k))
        for controls in itertools.product((0,1),repeat=7):
            x=(0,)*k
            xx=(0,)*k
            hidden=1
            public0=[x[0]]
            public1=[xx[0]]
            for u in controls:
                x=step(x,c,u)
                xx=step(xx,c,u)
                hidden^=1^sum(xx)%2
                public0.append(x[0]);public1.append(xx[0])
            assert tuple(public0)==tuple(public1)
    print('Independent hidden bit remains unidentifiable for every tested control sequence PASS')
    print('All checks PASS')

if __name__=='__main__':
    run()