import unittest
from sigyn.reporters import Reporter
from sigyn.attributes import Attribute
from sigyn.faults import GaussianNoise


class TestReports(unittest.TestCase):
    def test_attribute_faults(self):
        new_prototype = Reporter('test',
                                 attributes=[Attribute('noisy', faults=GaussianNoise(sigma=0.1)),
                                                    Attribute('noiseless')])
        report0 = new_prototype.create_report({'noisy': 100, 'noiseless': 100})
        self.assertEqual(report0['truth'], {'noisy': 100, 'noiseless': 100})
        self.assertEqual(report0['observed']['noiseless'], 100)
        self.assertNotEqual(report0['observed']['noisy'], 100)
        self.assertEqual(len(report0['triggered_faults']['reporter']), 0)
        self.assertEqual(len(report0['triggered_faults']['noiseless']), 0)
        self.assertEqual(len(report0['triggered_faults']['noisy']), 1)
        self.assertIsInstance(report0['triggered_faults']['noisy'][0], GaussianNoise)
        pass

    def test_auto_increment(self):
        new_prototype = Reporter('test')
        report0 = new_prototype.create_report({})
        report1 = new_prototype.create_report({})
        self.assertEqual(report0['report_type'], 'test')
        self.assertEqual(report0['identifier'], 0)
        self.assertEqual(report1['identifier'], 1)
        pass
