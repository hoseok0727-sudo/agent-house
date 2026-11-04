"""Research prototype: structured-query softmax attention via fast power sums.

The finite-field tests verify an algebraic identity EXACTLY (no floating-point error).
This is a proof-of-concept, not a numerically stable production softmax kernel.
Run: python structured_attention_research.py
"""
from __future__ import annotations
import random, time, math
import numpy as np

P = 998244353
ROOT = 3


def ntt(a: list[int], invert: bool = False) -> None:
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        root = pow(ROOT, (P - 1)//length, P)
        if invert:
            root = pow(root, P-2, P)
        for i in range(0,n,length):
            w = 1
            half = length >> 1
            for j in range(i,i+half):
                u = a[j]
                v = a[j+half]*w % P
                a[j] = (u+v)%P
                a[j+half] = (u-v)%P
                w = w*root%P
        length <<= 1
    if invert:
        inv_n = pow(n, P-2, P)
        for i in range(n):
            a[i] = a[i]*inv_n%P


def mul(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return []
    out_len = len(a)+len(b)-1
    if min(len(a),len(b)) <= 16:
        c=[0]*out_len
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                c[i+j]=(c[i+j]+ai*bj)%P
        return c
    n=1
    while n<out_len:
        n<<=1
    x=a+[0]*(n-len(a))
    y=b+[0]*(n-len(b))
    ntt(x)
    ntt(y)
    for i in range(n):
        x[i]=x[i]*y[i]%P
    ntt(x, True)
    return x[:out_len]


def polyadd(a: list[int], b: list[int]) -> list[int]:
    return [((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%P
            for i in range(max(len(a),len(b)))]


def inverse_series(f: list[int], m: int) -> list[int]:
    assert f[0]%P != 0
    g=[pow(f[0],P-2,P)]
    while len(g)<m:
        length=min(2*len(g),m)
        fg=mul(f[:length],g)[:length]
        c=[0]*length
        c[0]=2
        for i in range(len(fg)):
            c[i]=(c[i]-fg[i])%P
        g=mul(g,c)[:length]
    return g[:m]


def make_tree(z: list[int]) -> tuple:
    """Subproduct tree D(x)=prod_j(1-z_j*x)."""
    if len(z)==1:
        return ([1,(-z[0])%P],None,None)
    mid=len(z)//2
    L=make_tree(z[:mid]); R=make_tree(z[mid:])
    return (mul(L[0],R[0]),L,R)


def numerator(tree: tuple, weights: list[int]) -> list[int]:
    D,L,R=tree
    if L is None:
        assert len(weights)==1
        return [weights[0]%P]
    split=len(L[0])-1
    PL=numerator(L, weights[:split]); PR=numerator(R,weights[split:])
    return polyadd(mul(PL,R[0]),mul(PR,L[0]))


def moments_fast(z: list[int], weights: list[int], m: int, tree=None, inv=None) -> list[int]:
    if tree is None:
        tree=make_tree(z)
    if inv is None:
        inv=inverse_series(tree[0],m)
    pn=numerator(tree,weights)
    return mul(pn,inv)[:m]


def moments_direct(z: list[int], weights: list[int], m: int) -> list[int]:
    powers=[1]*len(z)
    out=[]
    for t in range(m):
        out.append(sum(w*x for w,x in zip(weights,powers))%P)
        powers=[x*y%P for x,y in zip(powers,z)]
    return out


def verify_finite_field(ns=(8,32,128,256)):
    rng=random.Random(1142)
    print('Exact finite-field algebra verification (p=998244353)')
    print('N  fast_seconds  direct_seconds  ALL_MATCH')
    for n in ns:
        z=[rng.randrange(1,P) for _ in range(n)]
        w=[rng.randrange(1,P) for _ in range(n)]
        v=[rng.randrange(P) for _ in range(n)]
        t0=time.perf_counter()
        tree=make_tree(z)
        inv=inverse_series(tree[0],n)
        den=moments_fast(z,w,n,tree,inv)
        num=moments_fast(z,[a*b%P for a,b in zip(w,v)],n,tree,inv)
        fast=time.perf_counter()-t0
        t0=time.perf_counter()
        directden=moments_direct(z,w,n)
        directnum=moments_direct(z,[a*b%P for a,b in zip(w,v)],n)
        slow=time.perf_counter()-t0
        valid=(den==directden and num==directnum)
        print(f'{n:3d} {fast:12.4f} {slow:15.4f}  {valid}')
        assert valid


def test_real_smooth_trajectory():
    rng=np.random.default_rng(1142)
    n=120; d=12; dv=4
    k=rng.normal(size=(n,d))*.4
    v=rng.normal(size=(n,dv))*.4
    q0=rng.normal(size=d)*.3
    slope=rng.normal(size=d)*.002
    ts=np.arange(n)
    ref=q0[None,:]+ts[:,None]*slope[None,:]
    nonlinear=.08*np.sin(2*np.pi*ts/(n-1))[:,None]*rng.normal(size=d)[None,:]
    q=ref+nonlinear
    def attention(q):
        logits=q@k.T / math.sqrt(d)
        logits-=logits.max(axis=1,keepdims=True)
        s=np.exp(logits)
        return (s@v)/s.sum(axis=1,keepdims=True)
    actual=attention(q)
    approx=attention(ref)
    error=np.linalg.norm(actual-approx,axis=1).max()
    delta2=q[:-2]-2*q[1:-1]+q[2:]
    curvature=np.max(np.linalg.norm(delta2,axis=1))
    Rk=np.max(np.linalg.norm(k-k.mean(axis=0),axis=1))
    Rv=np.max(np.linalg.norm(v-v.mean(axis=0),axis=1))
    cert=Rk*Rv/math.sqrt(d)*curvature*(n-1)**2/8
    print('\nReal-valued smooth-path test (the approximate path is evaluated densely to isolate approximation error)')
    print(f'n={n}, d={d}, value_dim={dv}, max_output_error={error:.8g}, provable_upper_bound={cert:.8g}, pass={error <= cert + 1e-12}')

if __name__=='__main__':
    verify_finite_field()
    test_real_smooth_trajectory()


def causal_moments_fast(z: list[int], w: list[int], v: list[int]) -> tuple[list[int],list[int]]:
    """Compute sums over j<=t of w_j * z_j**t and v-weighted sums.
    Divide and conquer over the strict lower triangle (causal mask).
    """
    n=len(z)
    den=[w[t]*pow(z[t],t,P)%P for t in range(n)]
    num=[w[t]*v[t]*pow(z[t],t,P)%P for t in range(n)]
    def recurse(lo,hi):
        if hi-lo<=1:
            return
        mid=(lo+hi)//2
        recurse(lo,mid)
        recurse(mid,hi)
        nodes=z[lo:mid]
        weights=[w[j]*pow(z[j],mid,P)%P for j in range(lo,mid)]
        tree=make_tree(nodes)
        inv=inverse_series(tree[0],hi-mid)
        ds=moments_fast(nodes,weights,hi-mid,tree,inv)
        vs=moments_fast(nodes,[weights[j-lo]*v[j]%P for j in range(lo,mid)],hi-mid,tree,inv)
        for i in range(hi-mid):
            den[mid+i]=(den[mid+i]+ds[i])%P
            num[mid+i]=(num[mid+i]+vs[i])%P
    recurse(0,n)
    return den,num


def causal_moments_direct(z: list[int], w: list[int], v: list[int]) -> tuple[list[int],list[int]]:
    n=len(z)
    den=[0]*n
    num=[0]*n
    zp=[1]*n
    for t in range(n):
        for j in range(t+1):
            x=w[j]*zp[j]%P
            den[t]=(den[t]+x)%P
            num[t]=(num[t]+v[j]*x)%P
        zp=[zp[j]*z[j]%P for j in range(n)]
    return den,num


def verify_causal(ns=(16,64,256,512)):
    rng=random.Random(91742)
    print('\nCAUSAL ATTENTION (strict j<=t mask), exact finite field verification')
    print('N  fast_seconds  direct_seconds  ALL_MATCH')
    for n in ns:
        z=[rng.randrange(1,P) for _ in range(n)]
        w=[rng.randrange(1,P) for _ in range(n)]
        v=[rng.randrange(P) for _ in range(n)]
        t0=time.perf_counter()
        fast=causal_moments_fast(z,w,v)
        fast_s=time.perf_counter()-t0
        t0=time.perf_counter()
        direct=causal_moments_direct(z,w,v)
        slow_s=time.perf_counter()-t0
        ok=fast==direct
        print(f'{n:3d} {fast_s:12.4f} {slow_s:15.4f}  {ok}')
        assert ok

if __name__=='__main__':
    verify_causal()


def verify_real_softmax_high_precision(n=24, d=4, dv=3, dps=90):
    """Verify the generating-function identity against true exponential softmax.
    Uses high precision and O(n^2) polynomial arithmetic only as an oracle.
    """
    import mpmath as mp
    mp.mp.dps=dps
    rng=random.Random(944)
    def rvec(sz, scale):
        return [mp.mpf(rng.randrange(-25,26))/scale for _ in range(sz)]
    a=rvec(d,40)
    b=rvec(d,1200)
    ks=[rvec(d,30) for _ in range(n)]
    vs=[rvec(dv,30) for _ in range(n)]
    def dot(x,y):
        return sum(i*j for i,j in zip(x,y))
    sqrtd=mp.sqrt(d)
    z=[mp.exp(dot(b,k)/sqrtd) for k in ks]
    w=[mp.exp(dot(a,k)/sqrtd) for k in ks]

    def pmul(a,b):
        out=[mp.mpf(0)]*(len(a)+len(b)-1)
        for i,ai in enumerate(a):
            for j,bj in enumerate(b):
                out[i+j]+=ai*bj
        return out
    def padd(a,b):
        return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                for i in range(max(len(a),len(b)))]
    def build(lo,hi,weight):
        if hi-lo==1:
            return [mp.mpf(1),-z[lo]],[weight[lo]]
        mid=(lo+hi)//2
        dl,pl=build(lo,mid,weight)
        dr,pr=build(mid,hi,weight)
        return pmul(dl,dr),padd(pmul(pl,dr),pmul(pr,dl))
    def power_series(D,P,n):
        coefficients=[]
        for t in range(n):
            m=(P[t] if t<len(P) else 0)-sum(D[j]*coefficients[t-j]
                    for j in range(1,min(t,len(D)-1)+1))
            coefficients.append(m/D[0])
        return coefficients
    D,Pden=build(0,n,w)
    dens=power_series(D,Pden,n)
    nums=[]
    for feat in range(dv):
        _,Pnum=build(0,n,[w[j]*vs[j][feat] for j in range(n)])
        nums.append(power_series(D,Pnum,n))
    actual=[]
    for t in range(n):
        qi=[a[i]+t*b[i] for i in range(d)]
        p=[mp.exp(dot(qi,k)/sqrtd) for k in ks]
        denominator=sum(p)
        actual.append([sum(p[j]*vs[j][i] for j in range(n))/denominator
                       for i in range(dv)])
    err=max(abs(actual[t][c]-nums[c][t]/dens[t]) for t in range(n) for c in range(dv))
    print(f'\nReal EXPONENTIAL softmax identity, {dps}-digit arithmetic: n={n}, d={d}, value_dim={dv}')
    print('maximum_absolute_error =',mp.nstr(err,12))
    assert err<mp.mpf('1e-50')

if __name__=='__main__':
    verify_real_softmax_high_precision()


def test_causal_first_order_correction():
    """An output-level, *synthetic* causal softmax test of tangent correction.
    Numerics are dense for oracle convenience; all required linear moments admit
    the same rational-function fast algorithm for rank-one perturbations.
    """
    rng=np.random.default_rng(1142)
    n=120; d=12; dv=4
    k=rng.normal(size=(n,d))*.4
    v=rng.normal(size=(n,dv))*.4
    a=rng.normal(size=d)*.3
    b=rng.normal(size=d)*.002
    ts=np.arange(n)
    qline=a[None,:]+ts[:,None]*b
    c=rng.normal(size=d)
    amplitude=.08*np.sin(2*np.pi*ts/(n-1))
    q=qline+amplitude[:,None]*c

    def causal_att(qs):
        scores=qs@k.T/math.sqrt(d)
        scores[np.triu_indices(n,1)]=-np.inf
        tmp=np.exp(scores-np.max(scores,axis=1,keepdims=True))
        p=tmp/tmp.sum(axis=1,keepdims=True)
        return p@v,p

    y,_=causal_att(q)
    yline,p=causal_att(qline)
    s=k@c/math.sqrt(d)
    cov=p@(s[:,None]*v)-yline*(p@s)[:,None]
    corrected=yline+amplitude[:,None]*cov
    old_err=np.max(np.linalg.norm(y-yline,axis=1))
    new_err=np.max(np.linalg.norm(y-corrected,axis=1))
    Rk=np.max(np.linalg.norm(k-k.mean(0),axis=1))
    Rv=np.max(np.linalg.norm(v-v.mean(0),axis=1))
    delta=np.linalg.norm(q-qline,axis=1)
    rigorous_bound=Rv*Rk**2/d*delta**2
    per_row_error=np.linalg.norm(y-corrected,axis=1)
    ok=bool(np.all(per_row_error<=rigorous_bound+1e-12))
    print('\nSmooth rank-one deviation, actual CAUSAL exponential softmax')
    print(f'baseline_max_error={old_err:.9f}, corrected_max_error={new_err:.9f}, ratio={old_err/new_err:.2f}x')
    print(f'rigorous_max_bound={np.max(rigorous_bound):.9f}, all_rows_certified={ok}')
    assert ok

if __name__=='__main__':
    test_causal_first_order_correction()