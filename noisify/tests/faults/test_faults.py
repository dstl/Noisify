import unittest
from noisify.faults import Fault
from noisify.helpers.multi_dispatch import register_implementation


class AddOneFault(Fault):
    def condition(self, triggering_object):
        return True

    @register_implementation(priority=1)
    def add_to_int_string(self, integer_string_object):
        return integer_string_object + "1"

    @register_implementation(priority=2)
    def make_uppercase(self, lowercase_string):
        return lowercase_string.upper()


class TestGeneralFaultBehaviour(unittest.TestCase):
    def test_missing_implementation(self):
        p_fault = AddOneFault()

        class UselessClass:
            pass

        useless_object = UselessClass()
        with self.assertRaises(NotImplementedError):
            p_fault.impact(useless_object)
        pass

    def test_fault_priority(self):
        p_fault = AddOneFault()
        test_string = 'this is a test'
        self.assertEqual(p_fault.impact(test_string), 'THIS IS A TEST')
        pass
