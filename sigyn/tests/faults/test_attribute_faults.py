import unittest
from sigyn.faults import GaussianNoise, InterruptionFault, TypographicalFault


class TestBasicFaults(unittest.TestCase):
    def test_gaussian(self):
        p_fault = GaussianNoise(sigma=0.1)
        true_value = 100
        observed = p_fault.impact(true_value)
        error_amount = abs(true_value - observed) / true_value
        self.assertLess(error_amount, 0.15)
        self.assertNotEqual(true_value, observed)
        pass

    def test_interruption(self):
        i_fault = InterruptionFault(likelihood=1)
        true_value = 100
        observed = i_fault.impact(true_value)
        self.assertEqual(observed, None)
        pass

    def test_typo(self):
        t_fault = TypographicalFault(likelihood=1, severity=1)
        true_value = "Hello World"
        observed = t_fault.impact(true_value)
        self.assertNotEqual(true_value, observed)
        pass
