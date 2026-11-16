#!/usr/bin/env python3
"""Reversible 3D 6-velocity lattice gas; Python 3 + NumPy."""
import argparse
import csv
import math
from pathlib import Path
import numpy as np

VELOCITIES = ((0,1),(0,-1),(1,1),(1,-1),(2,1),(2,-1))

def parity_grid(L):
    if L % 2: raise ValueError("L must be even")
    return np.indices((L,L,L),dtype=np.int16).sum(axis=0)%2

def collide(state, parity):
    s=np.asarray(state,dtype=bool)
    pair=(s.sum(axis=-1)==2)
    x=s[...,0]&s[...,1]
    y=s[...,2]&s[...,3]
    z=s[...,4]&s[...,5]
    xy=(parity==0)&pair&(x|y)
    yz=(parity==1)&pair&(y|z)
    out=s.copy()
    for a,b in ((0,2),(1,3)):
        out[...,a]=np.where(xy,s[...,b],s[...,a])
        out[...,b]=np.where(xy,s[...,a],s[...,b])
    for a,b in ((2,4),(3,5)):
        out[...,a]=np.where(yz,s[...,b],out[...,a])
        out[...,b]=np.where(yz,s[...,a],out[...,b])
    return out

def stream(s,inverse=False):
    out=np.empty_like(s)
    for ch,(axis,sign) in enumerate(VELOCITIES):
        out[...,ch]=np.roll(s[...,ch], sign*(-1 if inverse else 1),axis=axis)
    return out

def forward(s,parity,collision=True):
    return stream(collide(s,parity) if collision else s)

def backward(s,parity,collision=True):
    x=stream(s,inverse=True)
    return collide(x,parity) if collision else x

def invariants(s):
    totals=s.sum(axis=(0,1,2),dtype=np.int64)
    return (int(totals.sum()),int(totals[0]-totals[1]),int(totals[2]-totals[3]),int(totals[4]-totals[5]))

def initial(L,p,seed):
    rng=np.random.default_rng(seed)
    s=np.zeros((L,L,L,6),dtype=bool)
    s[:L//2]=rng.random((L//2,L,L,6))<p
    return s

def coarse_score(s,block,lookup,maximum):
    L=s.shape[0]; n=L//block
    counts=s.reshape(n,block,n,block,n,block,6).sum(axis=(1,3,5,6),dtype=np.int32)
    return float(lookup[counts].sum()/maximum) if maximum>0 else 1.0

def multiplicities(L,block,particles):
    if L%block or block<1: raise ValueError("block must divide L")
    m=6*block**3; B=(L//block)**3
    arr=np.array([math.lgamma(m+1)-math.lgamma(k+1)-math.lgamma(m-k+1) for k in range(m+1)])
    q,r=divmod(particles,B)
    mx=(B-r)*arr[q]+r*arr[q+1] if r else B*arr[q]
    return arr,float(mx)

def run_one(L=16,block=4,steps=64,p=.35,seed=0,collision=True):
    s0=initial(L,p,seed); s=s0.copy(); parity=parity_grid(L)
    conserved=invariants(s0); lookup,mx=multiplicities(L,block,conserved[0])
    scores=[]
    for t in range(steps+1):
        assert invariants(s)==conserved, ("conservation",seed,t)
        scores.append(coarse_score(s,block,lookup,mx))
        if t<steps: s=forward(s,parity,collision)
    for _ in range(steps): s=backward(s,parity,collision)
    assert np.array_equal(s,s0), ("inverse",seed)
    return scores

def suite(L=16,block=4,steps=64,p=.35,seeds=24,output="data"):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    rows=[]; summary=[]
    for collision in (False,True):
        changes=[]
        for seed in range(seeds):
            scores=run_one(L,block,steps,p,seed,collision)
            for t,value in enumerate(scores):
                rows.append(dict(L=L,block=block,probability=p,seed=seed,
                                 dynamics="collision" if collision else "ballistic",
                                 t=t,macro_score=value))
            changes.append(scores[-1]-scores[0])
        d=np.array(changes)
        sd=float(d.std(ddof=1)) if seeds>1 else float("nan")
        summary.append(dict(L=L,block=block,probability=p,
                            dynamics="collision" if collision else "ballistic",
                            seeds=seeds,t_final=steps,mean_delta_macro=float(d.mean()),
                            std_delta_macro=sd,
                            approximate_ci95_halfwidth=1.96*sd/(seeds**.5)))
    for name,data in (("trajectories.csv",rows),("summary.csv",summary)):
        with (output/name).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]))
            w.writeheader();w.writerows(data)
    for r in summary: print(r)
    return summary

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--L",type=int,default=16)
    a.add_argument("--block",type=int,default=4)
    a.add_argument("--steps",type=int,default=64)
    a.add_argument("--seeds",type=int,default=24)
    a.add_argument("--probability",type=float,default=.35)
    a.add_argument("--out",default="data")
    v=a.parse_args()
    suite(v.L,v.block,v.steps,v.probability,v.seeds,v.out)
