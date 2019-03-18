"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.reporters import Reporter
from noisify.attribute_readers import DictValue
from noisify.faults import GaussianNoise, InterruptionFault


class TestReporters(unittest.TestCase):
    def test_attribute_faults(self):
        new_prototype = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                             DictValue('noiseless')])
        report0 = new_prototype({'noisy': 100, 'noiseless': 100})
        self.assertEqual(report0.truth, {'noisy': 100, 'noiseless': 100})
        self.assertEqual(report0.observed['noiseless'], 100)
        self.assertNotEqual(report0.observed['noisy'], 100)
        self.assertEqual(len(report0.triggered_faults['reporter']), 0)
        self.assertEqual(len(report0.triggered_faults['noiseless']), 0)
        self.assertEqual(len(report0.triggered_faults['noisy']), 1)
        self.assertIsInstance(report0.triggered_faults['noisy'][0], GaussianNoise)
        pass

    def test_auto_increment(self):
        new_prototype = Reporter()
        report0 = new_prototype.create_report({})
        report1 = new_prototype.create_report({})
        self.assertEqual(report0.identifier, 0)
        self.assertEqual(report1.identifier, 1)
        pass

    def test_addition(self):
        prototype1 = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                          DictValue('noisier', faults=GaussianNoise(sigma=0.2))])
        prototype2 = Reporter(attributes=[DictValue('noised', faults=GaussianNoise(sigma=0.1)),
                                          DictValue('noisier', faults=InterruptionFault(likelihood=0.1))])
        new_prototype = prototype1 + prototype2
        self.assertIs(len(new_prototype.attributes), 3)
        self.assertIs(len(new_prototype.get_attribute_by_id('noisier').faults), 2)
        pass


class TestReports(unittest.TestCase):
    def test_method_delegation(self):
        new_prototype = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                             DictValue('noiseless')])
        report = new_prototype({'noisy': 100, 'noiseless': 100})
        self.assertEqual(set(report.keys()), {'noisy', 'noiseless'})
        pass

    def test_slicing(self):
        new_prototype = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                             DictValue('noiseless')])
        report = new_prototype({'noisy': 100, 'noiseless': 100})
        self.assertEqual(report['noiseless'], 100)
        pass
