import unittest
from sigyn.attributes import Attribute


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