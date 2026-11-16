"""Exact 8-bit reversible shift example: stationary vs prepared ensembles."""
from itertools import product
from collections import defaultdict

def optimal_accuracy(states,t,horizon=2,n=8):
    counts=defaultdict(lambda:[0,0])
    for x in states:
        obs=tuple(x[(j-t)%n] for j in (-1,0,1))
        target=x[(-t-horizon)%n]
        counts[obs][target]+=1
    return sum(max(k) for k in counts.values())/len(states)

def verify():
    uniform=list(product((0,1),repeat=8))
    prepared=[x+(0,0,0,0) for x in product((0,1),repeat=4)]
    a=[optimal_accuracy(uniform,t) for t in range(8)]
    b=[optimal_accuracy(prepared,t) for t in range(8)]
    assert a==[.5]*8
    assert b==[1.,1.,1.,.5,.5,.5,.5,1.]
    return a,b

if __name__=="__main__":
    print("uniform and nonstationary:",verify())
