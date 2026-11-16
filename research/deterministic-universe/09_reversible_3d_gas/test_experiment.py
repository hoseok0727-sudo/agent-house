"""No third-party test framework needed: python -m unittest -v."""
import unittest
import numpy as np
from experiment import (backward,collide,forward,initial,invariants,
                        multiplicities,parity_grid,coarse_score,run_one)
from stationary_predictability import verify

class TestReversibleGas(unittest.TestCase):
    def test_all_local_collision_configs(self):
        for flag in (0,1):
            parity=np.full((2,2,2),flag)
            for bits in range(64):
                s=np.broadcast_to(np.array([(bits>>j)&1 for j in range(6)],dtype=bool),
                                  (2,2,2,6)).copy()
                q=collide(s,parity)
                self.assertTrue(np.array_equal(s,collide(q,parity)))
                self.assertEqual(invariants(s),invariants(q))
    def test_exact_inverse_and_conservation(self):
        for L in (4,6,8):
            parity=parity_grid(L)
            for seed in (0,1,7):
                s=initial(L,.3,seed)
                for mode in (False,True):
                    x=s.copy()
                    for _ in range(25):
                        x=forward(x,parity,mode)
                        self.assertEqual(invariants(s),invariants(x))
                    for _ in range(25): x=backward(x,parity,mode)
                    self.assertTrue(np.array_equal(s,x))
    def test_macro_bounds(self):
        s=initial(8,.32,0)
        lookup,mx=multiplicities(8,2,invariants(s)[0])
        q=coarse_score(s,2,lookup,mx)
        self.assertTrue(0<=q<=1.00000000001)
    def test_short_dataset(self):
        self.assertEqual(len(run_one(4,2,6,.28,7,True)),7)
    def test_stationarity(self):
        verify()

if __name__=="__main__": unittest.main()
