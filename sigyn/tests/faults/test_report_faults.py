import unittest
from sigyn.faults import ScrambleAttributes, ConfuseSpecificAttributes, GaussianNoise
from sigyn.reporters import Reporter
from sigyn.attributes import Attribute


class TestReportFaults(unittest.TestCase):
    def test_attribute_scrambling(self):
        attributes_list = [Attribute('att%d' % index) for index in range(100)]
        new_reporter = Reporter(attributes=attributes_list, faults=ScrambleAttributes(scrambledness=100))
        data = {'att%d' % index: index for index in range(100)}
        output_data = new_reporter(data).observed
        self.assertNotEqual(data, output_data)
        pass

    def test_specific_attribute_confusion(self):
        new_reporter = Reporter(attributes=[Attribute('att1'), Attribute('att2')],
                                faults=ConfuseSpecificAttributes('att1', 'att2', likelihood=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        self.assertEqual(data['att1'], output_data['att2'])
        self.assertEqual(data['att2'], output_data['att1'])
        self.assertNotEqual(data, output_data)
        pass

    def test_attribute_fault_mapping(self):
        new_reporter = Reporter(attributes=[Attribute('att1'), Attribute('att2')], faults=GaussianNoise(sigma=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        self.assertNotEqual(data, output_data)
        pass

    def test_introspected_attribute_fault_mapping(self):
        new_reporter = Reporter(faults=GaussianNoise(sigma=1))
        data = {'att1': 1, 'att2': 2}
        output_data = new_reporter(data).observed
        print(new_reporter(data))
        self.assertNotEqual(data, output_data)
        self.assertEqual(data.keys(), output_data.keys())
        pass
