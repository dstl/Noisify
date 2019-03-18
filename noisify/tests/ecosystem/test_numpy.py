"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
import numpy as np
from noisify.faults import *
from noisify.recipes.default_recipes import human_error

class TestNumpy(unittest.TestCase):
    def test_gaussian(self):
        noise = GaussianNoise(sigma=1)
        test_array = np.array(range(10))
        out_array = noise.impact(test_array)
        self.assertNotEqual(test_array.all(), out_array.all())
        self.assertNotEqual(test_array[0]-out_array[0], test_array[1]-out_array[1])
        pass

    def test_interruption(self):
        interrupt = InterruptionFault(0.5)
        test_array = np.array(range(10))
        out_array = interrupt.impact(test_array)
        self.assertNotEqual(test_array.tolist(), out_array.tolist())
        pass

    def test_calibration(self):
        calibrate = CalibrationFault(0.5)
        test_array = np.array(range(10))
        out_array = calibrate.impact(test_array)
        self.assertNotEqual(test_array.tolist(), out_array.tolist())
        pass

    def test_human_error(self):
        error = human_error(10)
        test_array = np.array(range(10))
        out_array = list(error(test_array))[0].observed
        self.assertNotEqual(test_array.tolist(), out_array.tolist())
        pass