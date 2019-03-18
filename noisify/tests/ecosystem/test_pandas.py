"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
import pandas as pd
import pandas.testing as pd_testing
from noisify.faults import GaussianNoise, InterruptionFault, CalibrationFault


class TestPandas(unittest.TestCase):
    def test_gaussian(self):
        test_frame = pd.DataFrame({'col1': range(5), 'col2': range(5)})
        noise = GaussianNoise(1)
        noisy_frame = noise.impact(test_frame)
        with self.assertRaises(AssertionError):
            pd_testing.assert_frame_equal(test_frame, noisy_frame)
        pass

    def test_interruption(self):
        test_frame = pd.DataFrame({'col1': range(5), 'col2': range(5)})
        interrupt = InterruptionFault(0.5)
        noisy_frame = interrupt.impact(test_frame)
        with self.assertRaises(AssertionError):
            pd_testing.assert_frame_equal(test_frame, noisy_frame)
        pass

    def test_calibration(self):
        test_frame = pd.DataFrame({'col1': range(5), 'col2': range(5)})
        calibrate = CalibrationFault(1.5)
        noisy_frame = calibrate.impact(test_frame)
        with self.assertRaises(AssertionError):
            pd_testing.assert_frame_equal(test_frame, noisy_frame)
        pass
