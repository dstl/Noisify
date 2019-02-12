import unittest
from noisify.attributes import generate_object_attributes


class TestObjectAttributeIntrospection(unittest.TestCase):
    def test_dict_to_attributes(self):
        test_object = {'test1': 1, 'test2': 2}
        attributes = [a for a in generate_object_attributes(test_object)]
        attribute_names = set(a.attribute_identifier for a in attributes)
        expected_names = {'test1', 'test2'}
        self.assertEqual(attribute_names, expected_names)
        pass

    def test_object_to_attributes(self):
        test_object = {'test1': 1, 'test2': 2}
        attributes = [a for a in generate_object_attributes(test_object)]
        attribute_names = set(a.attribute_identifier for a in attributes)
        expected_names = {'test1', 'test2'}
        self.assertEqual(attribute_names, expected_names)
        pass