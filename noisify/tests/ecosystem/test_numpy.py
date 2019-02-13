import unittest
import numpy as np
from noisify.faults import GaussianNoise


class TestNumpy(unittest.TestCase):
    def test_gaussian(self):
        noise = GaussianNoise(sigma=1)
        test_array = np.array(range(10))
        out_array = noise.impact(test_array)
        self.assertNotEqual(test_array.all(), out_array.all())
        self.assertNotEqual(test_array[0]-out_array[0], test_array[1]-out_array[1])
        pass
