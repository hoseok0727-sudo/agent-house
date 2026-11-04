"""A third 'universe': computable sequence adversarial to a fixed total computable predictor.
This is standard diagonalization, NOT an original theorem; no runtime feedback channel is needed.
"""
from __future__ import annotations
from experiment import bm


def predictor(history: list[int]) -> int:
    """A fully specified total deterministic predictor on all finite binary prefixes.
    Tries Berlekamp-Massey, then low-order empirical context frequencies.
    """
    n=len(history)
    if n>=4:
        L,C=bm(history)
        if 0<L and 2*L<=n:
            next_bit=0
            for j in range(1,L+1):
                next_bit ^= C[j]&history[-j]
            return next_bit
    # fallback to learned order-3/2/1 context model with backoff and fixed ties
    for order in (3,2,1,0):
        if n<order+1: continue
        context=history[-order:] if order else []
        followers=[history[t] for t in range(order,n)
                   if (history[t-order:t] if order else [])==context]
        if followers:
            count=sum(followers)
            return int(2*count>len(followers))
    return 0


def diagonal_world(length: int) -> list[int]:
    history=[]
    for _ in range(length):
        history.append(1-predictor(history))
    return history


def check(length=256):
    stream=diagonal_world(length)
    errors=[predictor(stream[:t])!=stream[t] for t in range(length)]
    assert all(errors)
    # A different total computable predictor can predict the exact same world.
    successful=[1-predictor(stream[:t])==stream[t] for t in range(length)]
    assert all(successful)
    print(f'PASS: fixed predictor has {sum(errors)}/{length} wrong; alternative predictor {sum(successful)}/{length} correct')
    print('First 128 bits:', ''.join(map(str,stream[:128])))
    print('Empirical count of ones:', sum(stream),'/',length)
    return stream

if __name__=='__main__':check()
