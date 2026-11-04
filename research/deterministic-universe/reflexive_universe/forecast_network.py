#!/usr/bin/env python3
"""Forecast-consistency constraint networks: graph bipartiteness & MaxCut.

Simple educational reduction; not novel graph theory.
Edges (i,j) assert a pairwise preference that the published bits differ.
This is not the same model as an agent who simultaneously responds to
several incoming forecasts; edges are separate consistency requirements.
"""
from __future__ import annotations
import itertools
import random
from collections import deque
from pathlib import Path
import csv


def cycle(n):
    return [(i,(i+1)%n) for i in range(n)]

def clique(n):
    return list(itertools.combinations(range(n),2))

def bipartite_assignment(n,edges):
    """O(V+E) coloring or None. If None, some odd cycle is an obstruction."""
    adj=[[] for _ in range(n)]
    for i,j in edges:
        assert i!=j and 0<=i<n and 0<=j<n
        adj[i].append(j)
        adj[j].append(i)
    color=[-1]*n
    for s in range(n):
        if color[s]!=-1: continue
        color[s]=0
        queue=deque([s])
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                if color[v]<0:
                    color[v]=1-color[u]
                    queue.append(v)
                elif color[v]==color[u]:
                    return None
    return color


def brute_max_agreement(n,edges):
    if n>21: raise ValueError('exponential search; only small n supported')
    optimum=-1
    best=None
    count=0
    # fix first vertex=0; complements equivalent
    for bits in itertools.product([0,1], repeat=n-1):
        p=(0,)+bits
        value=sum(p[i]!=p[j] for i,j in edges)
        if value>optimum:
            optimum=value
            best=p
            count=1
        elif value==optimum:
            count+=1
    return optimum,best,2*count


def verify():
    for n in range(3,13):
        E=cycle(n)
        coloring=bipartite_assignment(n,E)
        best,p,num=brute_max_agreement(n,E)
        assert best==n if n%2==0 else best==n-1
        assert (coloring is not None)==(n%2==0)
        if n%2==0: assert num==2
    for n in range(3,10):
        E=clique(n)
        best,p,num=brute_max_agreement(n,E)
        assert best==(n*n)//4
        assert (bipartite_assignment(n,E) is None)
    rng=random.Random(20261104)
    for n in [5,7,10,12]:
        for _ in range(30):
            E=[(i,j) for i in range(n) for j in range(i+1,n) if rng.random()<.3]
            bp=bipartite_assignment(n,E)
            best,p,num=brute_max_agreement(n,E)
            assert (bp is not None) == (best==len(E))
            if bp is not None:
                assert sum(bp[i]!=bp[j] for i,j in E)==len(E)
    return True


def save_table(path):
    with path.open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['type','nodes','requirements','max_consistent','unavoidable_violations','perfectly_consistent','count_optimal_assignments'])
        for n in range(3,11):
            for ty,fun in [('cycle',cycle),('complete',clique)]:
                E=fun(n)
                best,p,num=brute_max_agreement(n,E)
                w.writerow([ty,n,len(E),best,len(E)-best, best==len(E),num])

if __name__=='__main__':
    print('graph-theory regression tests:',verify())
    for n in (3,4,5,6,7,8):
        for name,fun in [('ring',cycle),('complete',clique)]:
            E=fun(n)
            k,assignment,count=brute_max_agreement(n,E)
            print(f'{name:>8} n={n}: max agreements {k}/{len(E)}; forced violations={len(E)-k}; one best assignment={assignment}; #optima={count}')
    save_table(Path(__file__).parent/'network_constraints.csv')
    print('Wrote network_constraints.csv')
