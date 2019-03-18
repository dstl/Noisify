"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.attribute_readers import dictionary_lookup, object_attributes_lookup


class TestObjectAttributeIntrospection(unittest.TestCase):
    def test_dict_to_attributes(self):
        test_object = {'test1': 1, 'test2': 2}
        attributes = [a for a in dictionary_lookup(test_object)]
        attribute_names = set(a.attribute_identifier for a in attributes)
        expected_names = {'test1', 'test2'}
        self.assertEqual(attribute_names, expected_names)
        pass

    def test_object_to_attributes(self):
        class Tester:
            test1 = 1
            test2 = 2
            pass
        test_object = Tester()
        attributes = [a for a in object_attributes_lookup(test_object)]
        attribute_names = set(a.attribute_identifier for a in attributes)
        expected_names = {'test1', 'test2'}
        self.assertEqual(attribute_names, expected_names)
        pass
