"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.faults import ScrambleAttributes, ConfuseSpecificAttributes, GaussianNoise
from noisify.reporters import Reporter
from noisify.attribute_readers import DictValue


class TestReportFaults(unittest.TestCase):
    def test_attribute_scrambling(self):
        attributes_list = [DictValue('att%d' % index) for index in range(50)]
        new_reporter = Reporter(attributes=attributes_list)
        data = {'att%d' % index: index for index in range(50)}
        output_data = new_reporter(data).observed
        scramble_fault = ScrambleAttributes(likelihood=100)
        output_data = scramble_fault.impact_dictionary(output_data)
        self.assertNotEqual(data, output_data)
        self.assertEqual({i for i in data.keys()}, {i for i in output_data.keys()})
        pass

    def test_specific_attribute_confusion(self):
        new_reporter = Reporter(attributes=[DictValue('att1'), DictValue('att2')],
                                faults=ConfuseSpecificAttributes('att1', 'att2', likelihood=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        self.assertEqual(data['att1'], output_data['att2'])
        self.assertEqual(data['att2'], output_data['att1'])
        self.assertNotEqual(data, output_data)
        pass

    def test_attribute_fault_mapping(self):
        new_reporter = Reporter(attributes=[DictValue('att1'), DictValue('att2')], faults=GaussianNoise(sigma=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        self.assertNotEqual(data, output_data)
        pass

    def test_introspected_attribute_fault_mapping(self):
        new_reporter = Reporter(faults=GaussianNoise(sigma=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        self.assertNotEqual(data, output_data)
        self.assertEqual(data.keys(), output_data.keys())
        pass
