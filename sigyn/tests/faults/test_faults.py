import unittest
from sigyn.faults import GaussianNoise, InterruptionFault


class TestBasicFaults(unittest.TestCase):
    def test_gaussian(self):
        p_fault = GaussianNoise(sigma=0.1)
        true_value = 100
        if p_fault.condition(None):
            observed = p_fault.impact_truth(true_value)
        error_amount = abs(true_value - observed) / true_value
        self.assertLess(error_amount, 0.15)
        pass

    def test_interruption(self):
        i_fault = InterruptionFault(likelihood=1)
        true_value = 100
        if i_fault.condition(None):
            observed = i_fault.impact_truth(true_value)
        self.assertEqual(observed, None)
        pass

