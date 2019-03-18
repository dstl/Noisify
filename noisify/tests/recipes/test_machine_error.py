"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.recipes.default_recipes import machine_error


class TestMachineError(unittest.TestCase):
    def test_multiple_series(self):
        test_noisifier = machine_error(0)
        test_input = [{'test1': 1}, {'test2': 2}]
        test_output = [i.observed for i in test_noisifier(test_input)]
        for input_term, output_term in zip(test_input, test_output):
            self.assertEqual(input_term, output_term)
        pass

    def test_single(self):
        test_noisifier = machine_error(0)
        test_input = {'test1': 1}
        test_output = [i.observed for i in test_noisifier(test_input)][0]
        self.assertEqual(test_input, test_output)
        pass

    def test_noise(self):
        test_noisifier = machine_error(100)  # Always interrupts
        test_input = {'test1': 'hello', 'test2': 'world'}
        test_output = [i.observed for i in test_noisifier(test_input)][0]
        self.assertNotEqual(test_input, test_output)
        pass
