import unittest
from PIL import Image
import hashlib
import numpy as np
from noisify.faults import GaussianNoise
import pkg_resources


class TestPillow(unittest.TestCase):
    def test_gaussian(self):
        noise = GaussianNoise(30)
        input_image = Image.open(str(pkg_resources.resource_filename(__name__, 'test_image.jpeg')))
        initial_hash = hashlib.sha512()
        initial_hash.update(np.array(input_image))
        messy_image = noise.impact(input_image)
        messy_hash = hashlib.sha512()
        messy_hash.update(np.array(messy_image))
        self.assertNotEqual(initial_hash.digest(), messy_hash.digest())
        pass