import unittest
from noisify.attributes import Attribute
from noisify.faults import GaussianNoise, InterruptionFault


class TestAttributeLookup(unittest.TestCase):
    def test_object_attribute_lookup(self):
        test_attribute = Attribute('test')

        class Foo:
            test = 'test_attribute'
        bar = Foo()
        self.assertIs(test_attribute.get_truth(bar), 'test_attribute')
        pass

    def test_dict_lookup(self):
        test_attribute = Attribute('test')
        bar = {'test': 'test_attribute'}
        self.assertIs(test_attribute.get_truth(bar), 'test_attribute')
        pass

    def test_fail(self):
        test_attribute = Attribute('test')
        with self.assertRaises(TypeError):
            test_attribute.get_truth(None)
        pass

    def test_addition(self):
        test_attribute1 = Attribute('test', faults=GaussianNoise(sigma=1))
        test_attribute2 = Attribute('test', faults=InterruptionFault(likelihood=1))
        new_attribute = test_attribute1 + test_attribute2
        self.assertIs(len(new_attribute.faults), 2)
        self.assertIsInstance(new_attribute.faults[0], GaussianNoise)
        self.assertIsInstance(new_attribute.faults[1], InterruptionFault)
        pass

    def test_invalid_addition(self):
        test_attribute1 = Attribute('test')
        test_attribute2 = Attribute('test2')
        with self.assertRaises(TypeError):
            test_attribute1 + test_attribute2
        pass
