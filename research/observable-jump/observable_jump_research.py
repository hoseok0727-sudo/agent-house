"""Proof-carrying observable jump-ahead: a minimal, reproducible concept demo.

This is NOT a claimed novel Koopman result or a general-purpose accelerator.
It automatically finds an affine-evolving quadratic observable in one example,
checks the identity symbolically, and compares ordinary iteration to jump-ahead.

Requires: sympy
Run: python observable_jump_research.py
"""
from __future__ import annotations
from time import perf_counter
import sympy as sp

x, y = sp.symbols('x y')
# Hidden linear coordinate u = x-y**2, mixed with a nonlinear (degree-doubling)
# second coordinate y -> y**2+1. The raw state has no small monomial closure.
Fy = y**2 + 1
Fx = 3*x - 3*y**2 + 1 + Fy**2


def discover_observable():
    c, d, a, b = sp.symbols('c d a b')
    candidate = x + c*y**2 + d*y
    residual = sp.expand(candidate.subs({x: Fx, y: Fy}, simultaneous=True)
                         - a*candidate - b)
    coeffs = list(sp.Poly(residual, x, y).coeffs())
    solutions = sp.solve(coeffs, (a,b,c,d), dict=True)
    good = []
    for s in solutions:
        if set(s) == {a, b, c, d}:
            good.append(s)
    if not good:
        raise AssertionError('no exact eigen/affine observable within the ansatz')
    s = good[0]
    g = sp.expand(candidate.subs(s))
    rate = sp.simplify(s[a])
    shift = sp.simplify(s[b])
    assert sp.expand(g.subs({x:Fx,y:Fy}, simultaneous=True) - rate*g - shift) == 0
    return g,rate,shift


def iterate(x0: int,y0:int,n:int,p:int) -> tuple[int,int]:
    a,b=x0%p,y0%p
    for _ in range(n):
        bn=(b*b+1)%p
        an=(3*a-3*b*b+1+bn*bn)%p
        a,b=an,bn
    return a,b


def jump_observable(g0:int,n:int,p:int) -> int:
    # For g' = 3*g+1, g_n = 3**n*g0 + (3**n-1)/(3-1).
    power=pow(3,n,p)
    return (power*g0+(power-1)*pow(2,-1,p))%p


def main():
    g,rate,shift=discover_observable()
    print('Discovered polynomial observable:',g)
    print('Certified symbolic relation: g(F(x,y)) =',rate,'* g(x,y) +',shift)
    print('Certificate residual:',sp.expand(g.subs({x:Fx,y:Fy},simultaneous=True)-rate*g-shift))
    p=1_000_000_007
    seeds=[(713,97),(0,0),(382773,45602),(123_456_789,987_654_321)]
    N=500_000
    start=perf_counter()
    direct=[]
    for u,v in seeds:
        X,Y=iterate(u,v,N,p)
        direct.append((X-Y*Y)%p)
    direct_seconds=perf_counter()-start
    start=perf_counter()
    accelerated=[jump_observable((u-v*v)%p,N,p) for u,v in seeds]
    jump_seconds=perf_counter()-start
    assert direct==accelerated
    print(f'PASS: {len(seeds)} exact comparisons at N={N:,} steps (mod {p})')
    print('Direct:',direct)
    print(f'Direct elapsed: {direct_seconds:.6f}s; jump elapsed: {jump_seconds:.6f}s')
    print(f'Observed Python speed ratio on this example: {direct_seconds/jump_seconds:.0f}x')
    BIG=10**12
    u,v=seeds[0]
    g0=(u-v*v)%p
    A=314_159_265_359
    B=BIG-A
    part=jump_observable(g0,A,p)
    checked=jump_observable(part,B,p)
    whole=jump_observable(g0,BIG,p)
    assert checked==whole
    print(f'For N={BIG:,}, g_N mod {p} = {whole} (split-composition check PASS)')
    print('Limitation: the result only applies to observables with a certified small closed update.')
    print('Control failure: y -> y^2+1 doubles degree under iteration: deg F^n_y = 2^n.')

if __name__=='__main__':
    main()