"""Independent property checks for deterministic-observer experiment. Run python tests.py."""
import unittest
from experiment import debruijn_binary,cyclic_counts,stats,bm,lfsr_from_taps,predict_bm
from diagonal import diagonal_world,predictor

class TestExactProperties(unittest.TestCase):
    def test_debruijn_coverage_and_conditional_entropy(self):
        for k in range(2,11):
            s=debruijn_binary(k)
            assert len(s)==2**k
            for m in range(k):
                c=cyclic_counts(s,m)
                self.assertEqual(len(c),2**m)
                self.assertTrue(all(x==[2**(k-m-1)]*2 for x in c.values()))
                self.assertAlmostEqual(stats(s,m)['entropy'],1)
            self.assertAlmostEqual(stats(s,k)['entropy'],0)

    def test_reversible_nonlinear_state_mapping(self):
        k=10;s=debruijn_binary(k);n=len(s)
        transition={tuple(s[(t+j)%n] for j in range(k)):
                    tuple(s[(t+j+1)%n] for j in range(k)) for t in range(n)}
        self.assertEqual(len(transition),n)
        self.assertEqual(len(set(transition.values())),n)
        self.assertEqual(set(transition.keys()),set(transition.values()))

    def test_lfsr_reconstruction_multiple_phases(self):
        k=12; N=2**k-1;tap=(0,1,4,6)
        s=lfsr_from_taps(k,tap,2*N+24)
        self.assertEqual(s[:N],s[N:2*N])
        for phase in [0,1,2,23,101,1000,4094]:
            observed=s[phase:phase+2*k]
            L,C=bm(observed)
            self.assertEqual(L,k)
            predicted=predict_bm(observed,C,100)
            self.assertEqual(predicted,s[phase:phase+2*k+100])

    def test_debruijn_no_short_linear_reconstruction(self):
        k=12;s=debruijn_binary(k); N=len(s)
        L,C=bm(s*2)
        self.assertEqual(L,4094)
        self.assertEqual(predict_bm(s*2,C,128)[-128:],(s*3)[2*N:2*N+128])

    def test_diagonal_world(self):
        stream=diagonal_world(64)
        self.assertTrue(all(predictor(stream[:i]) != stream[i] for i in range(len(stream))))

if __name__=='__main__': unittest.main(verbosity=2)
