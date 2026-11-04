"""Deterministic Observer Lab: De Bruijn vs LFSR exact predictability.
Reproducible with Python 3.10+ stdlib only.
All statistics are cyclic (uniform random phase of a finite deterministic orbit).
"""
from __future__ import annotations
import collections, csv, math, pathlib

OUT = pathlib.Path(__file__).resolve().parent


def debruijn_binary(k: int) -> list[int]:
    a = [0] * (2*k+2)
    sequence: list[int] = []
    def db(t: int, p: int) -> None:
        if t > k:
            if k % p == 0:
                sequence.extend(a[1:p+1])
        else:
            a[t] = a[t-p]
            db(t+1, p)
            for j in range(a[t-p]+1, 2):
                a[t] = j
                db(t+1, t)
    db(1,1)
    assert len(sequence) == 2**k
    return sequence


def cyclic_counts(bits: list[int], m: int):
    N=len(bits)
    c=collections.defaultdict(lambda:[0,0])
    for t in range(N):
        # Context consists of m consecutive bits followed by next bit.
        context=tuple(bits[(t+i)%N] for i in range(m))
        next_bit=bits[(t+m)%N]
        c[context][next_bit] += 1
    return c


def H2(p):
    return 0.0 if p==0 or p==1 else -p*math.log2(p)-(1-p)*math.log2(1-p)


def stats(bits: list[int], m: int):
    c=cyclic_counts(bits, m)
    N=len(bits)
    entropy=sum((v[0]+v[1])/N * H2(v[1]/sum(v)) for v in c.values())
    accuracy=sum(max(v) for v in c.values())/N
    return {'context':m,'entropy':entropy,'best_markov_accuracy':accuracy,'distinct_contexts':len(c)}


def lfsr_from_taps(k: int, taps: tuple[int,...], length: int, seed: list[int]|None=None):
    # b[t+k] = XOR b[t+j] over taps j in 0..k-1
    if seed is None: seed=[1]+[0]*(k-1)
    seq=seed[:]
    for t in range(length-k):
        q=0
        for j in taps: q^=seq[t+j]
        seq.append(q)
    return seq


def bm(bits: list[int]):
    # Berlekamp-Massey in GF(2); return coefficients c where b[t]=xor(c_i b[t-i]).
    C=[1]; B=[1]; L=0; m=1
    for N in range(len(bits)):
        d=bits[N]
        for i in range(1,L+1):
            if i<len(C): d ^= C[i]&bits[N-i]
        if d:
            temp=C[:]
            req=len(B)+m
            if len(C)<req: C += [0]*(req-len(C))
            for i,b in enumerate(B): C[i+m]^=b
            if 2*L<=N:
                L=N+1-L
                B=temp
                m=1
            else:
                m+=1
        else:
            m+=1
    C+= [0]*(L+1-len(C))
    return L,C[:L+1]


def predict_bm(seed: list[int], coefficients: list[int], new_steps: int):
    L=len(coefficients)-1
    s=seed[:]
    for _ in range(new_steps):
        pred=0
        for i in range(1,L+1):
            if coefficients[i]:pred ^= s[-i]
        s.append(pred)
    return s


def run():
    k=12
    n=2**k
    db=debruijn_binary(k)
    # Test combinatorial balance for all blocks up to k.
    for m in range(k+1):
        c=cyclic_counts(db,m)
        assert len(c)==2**m
        assert set(sum(v) for v in c.values())=={2**(k-m)}
        if m<k:
            assert all(v==[2**(k-m-1),2**(k-m-1)] for v in c.values())
        else:
            assert all(sum(v)==1 for v in c.values())

    # Primitive degree-12 polynomial x^12+x^6+x^4+x+1.
    taps=(0,1,4,6)
    lfsr=lfsr_from_taps(k,taps,n+48)
    period=n-1
    # Validate maximum period using k-bit states.
    window=set()
    for i in range(period):
        w=tuple(lfsr[i:i+k]); assert len(w)==k
        if w in window: raise AssertionError(f'LFSR repeats early at t={i}; polynomial not primitive')
        window.add(w)
    assert len(window)==period
    assert tuple(lfsr[period:period+k]) == tuple(lfsr[:k])
    assert (0,)*k not in window

    # Recover recurrence from exactly 2k observed output bits.
    L,C = bm(lfsr[:2*k])
    assert L==k, (L,C)
    recovered=predict_bm(lfsr[:2*k],C,period+100-2*k)
    expected=lfsr_from_taps(k,taps,period+100)
    assert recovered==expected

    # How hard is the nonlinear De Bruijn sequence for a *linear* predictor?
    db_linear_order, db_C = bm(db*2)
    assert db_linear_order == 4094, db_linear_order
    db_future = predict_bm(db*2, db_C, 256)
    assert db_future[-256:] == (db*3)[2*n:2*n+256]
    short_order, short_C = bm(db[:2*k])
    wrong_short = predict_bm(db[:2*k],short_C,n-2*k)
    first_fail = next((i for i,(a,b) in enumerate(zip(wrong_short,db)) if a!=b),None)
    assert first_fail == 2*k

    rows=[]
    for name,seq in [('debruijn',db),('lfsr',lfsr[:period])]:
        for m in range(k+1):
            s=stats(seq,m)
            rows.append({'universe':name,'k':k,'period':len(seq),**s})

    with (OUT/'conditional_entropy.csv').open('w',newline='') as fp:
        wr=csv.DictWriter(fp,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)

    # Exact finite observation statistical distinguishability (DB vs iid):
    # T<=k: all length T strings equally frequent; T>=k: 2^k unique strings.
    distinguish=[]
    for T in range(1,k+7):
        counts=collections.Counter(tuple(db[(t+i)%n] for i in range(T)) for t in range(n))
        tv=0.5*sum(abs(c/n-2**(-T)) for c in counts.values())+0.5*(2**T-len(counts))*2**(-T)
        formula=0 if T<=k else 1-2**(k-T)
        assert math.isclose(tv,formula,abs_tol=1e-12)
        distinguish.append({'observed_bits':T,'tv_from_iid':tv,'exact_formula':formula,'allowed_strings':len(counts),'possible_strings':2**T})
    with (OUT/'distinguishability.csv').open('w',newline='') as fp:
        wr=csv.DictWriter(fp,fieldnames=list(distinguish[0]));wr.writeheader();wr.writerows(distinguish)

    # Show that order-k table has no out-of-sample coverage over half of a DB cycle.
    # Contexts in one turn are unique, so phase-disjoint partition yields 0 intersection.
    train=set(tuple(db[(t+i)%n] for i in range(k)) for t in range(n//2))
    test=set(tuple(db[(t+i)%n] for i in range(k)) for t in range(n//2,n))
    assert train.isdisjoint(test)

    # LFSR recurrences of less than k fail, and recovered recurrence extrapolates.
    for m in [0,4,8,10,11,12]:
        dbs=stats(db,m); ls=stats(lfsr[:period],m)
        print(f'm={m:2}  DB H={dbs["entropy"]:.9f} acc={dbs["best_markov_accuracy"]:.9f} | LFSR H={ls["entropy"]:.9f} acc={ls["best_markov_accuracy"]:.9f}')
    print(f'DB period {n}; LFSR period {period}; BM recovered linear complexity L={L} from {2*k} bits')
    print(f'DB infinite periodic stream linear complexity {db_linear_order} (BM on 2 periods); 24-bit BM first mismatch at bit {first_fail}')
    print(f'BM connection polynomial C(z) = '+ ' + '.join('z^'+str(i) if i else '1' for i,c in enumerate(C) if c))
    print('DB k-contexts seen in half cycle training',len(train),'in second half',len(test),'overlap',len(train&test))
    print('Distinguishability:',[(x['observed_bits'],x['tv_from_iid']) for x in distinguish if x['observed_bits'] in (k-1,k,k+1,k+2,k+4)])
    print('PASS all exact checks')

if __name__=='__main__':run()


def noise_trials(k=12, eps=0.05, trials=256, maxT=64, seed=20261104):
    """Bayesian/ML phase recovery with iid *measurement* bit flips, known phase prior.
    Uses NumPy only for this optional robustness experiment.
    """
    import numpy as np
    d=np.asarray(debruijn_binary(k),dtype=np.uint8)
    rng=np.random.default_rng(seed)
    N=len(d)
    checkpoints={8,12,13,16,20,24,32,48,64}
    result={t:{'unique_correct':0,'true_among_best':0,'unique_estimate':0,
               'posterior_true_sum':0.,'bayes_future_correct':0} for t in checkpoints}
    for trial in range(trials):
        phase=int(rng.integers(N))
        obs=d[(phase+np.arange(maxT))%N].copy()
        obs ^= (rng.random(maxT)<eps).astype(np.uint8)
        cost=np.zeros(N,dtype=np.int16)
        for t in range(1,maxT+1):
            cost+=(d[(np.arange(N)+t-1)%N]!=obs[t-1]).astype(np.int16)
            if t not in checkpoints: continue
            minimum=int(cost.min())
            best=np.flatnonzero(cost==minimum)
            o=result[t]
            o['true_among_best']+=int(phase in best)
            o['unique_estimate']+=int(len(best)==1)
            o['unique_correct']+=int(len(best)==1 and best[0]==phase)
            # Bayesian posterior over phase, known independent error rate.
            w=np.exp(-np.log((1-eps)/eps)*(cost-minimum)) if 0<eps<.5 else (cost==minimum).astype(float)
            w/=w.sum()
            o['posterior_true_sum']+=float(w[phase])
            next_bits=d[(np.arange(N)+t)%N]
            p_next=float(w @ next_bits)
            true_next=int(d[(phase+t)%N])
            o['bayes_future_correct']+=int((p_next>=.5)==true_next)
    return [{'T':t,'noise':eps,'trials':trials,
              'unique_correct_frac':v['unique_correct']/trials,
              'true_in_map_frac':v['true_among_best']/trials,
              'unique_map_frac':v['unique_estimate']/trials,
              'posterior_true_mean':v['posterior_true_sum']/trials,
              'bayes_next_accuracy':v['bayes_future_correct']/trials}
            for t,v in sorted(result.items())]


def run_robustness():
    all_rows=[]
    for eps in (0.02,0.05):
        rows=noise_trials(eps=eps,trials=256)
        all_rows.extend(rows)
        print('Noise',eps,[(r['T'],round(r['unique_correct_frac'],3),round(r['bayes_next_accuracy'],3)) for r in rows])
    with (OUT/'noise_robustness.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(all_rows[0]));w.writeheader();w.writerows(all_rows)

if __name__=='__main__':
    run_robustness()