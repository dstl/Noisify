import unittest
from sigyn.faults import GaussianNoise
from sigyn.helpers.fallible import Fallible, evaluate_faults
from ast import literal_eval


class TestFaultEvaluation(unittest.TestCase):
    def test_strategy(self):
        def fault_strategy():
            return [GaussianNoise(sigma=0.1)]
        faults = evaluate_faults(fault_strategy)
        self.assertEqual(len(faults), 1)
        self.assertIsInstance(faults[0], GaussianNoise)
        self.assertEqual(literal_eval(faults[0].init_statement), {'sigma': 0.1})
        pass

    def test_single_fault(self):
        faults = evaluate_faults(GaussianNoise(sigma=0.1))
        self.assertEqual(len(faults), 1)
        self.assertIsInstance(faults[0], GaussianNoise)
        self.assertEqual(literal_eval(faults[0].init_statement), {'sigma': 0.1})
        pass

    def test_fault_collection(self):
        faults = evaluate_faults([GaussianNoise(sigma=0.1), GaussianNoise(sigma=0.2)])
        self.assertEqual(len(faults), 2)
        for f in faults:
            self.assertIsInstance(f, GaussianNoise)
        self.assertEqual(literal_eval(faults[0].init_statement), {'sigma': 0.1})
        self.assertEqual(literal_eval(faults[1].init_statement), {'sigma': 0.2})
        pass