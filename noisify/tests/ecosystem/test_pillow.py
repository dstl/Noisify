"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from PIL import Image
import hashlib
import numpy as np
from noisify.faults import GaussianNoise, InterruptionFault, CalibrationFault, ScrambleAttributes
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
        self.assertEqual(input_image.size, messy_image.size)
        self.assertEqual(input_image.mode, messy_image.mode)
        pass

    def test_interruption(self):
        interrupt = InterruptionFault(0.5)
        input_image = Image.open(str(pkg_resources.resource_filename(__name__, 'test_image.jpeg')))
        initial_hash = hashlib.sha512()
        initial_hash.update(np.array(input_image))
        messy_image = interrupt.impact(input_image)
        messy_hash = hashlib.sha512()
        messy_hash.update(np.array(messy_image))
        self.assertNotEqual(initial_hash.digest(), messy_hash.digest())
        self.assertEqual(input_image.size, messy_image.size)
        self.assertEqual(input_image.mode, messy_image.mode)
        pass

    def test_calibration(self):
        calibrate = CalibrationFault(25)
        input_image = Image.open(str(pkg_resources.resource_filename(__name__, 'test_image.jpeg')))
        initial_hash = hashlib.sha512()
        initial_hash.update(np.array(input_image))
        messy_image = calibrate.impact(input_image)
        messy_hash = hashlib.sha512()
        messy_hash.update(np.array(messy_image))
        self.assertNotEqual(initial_hash.digest(), messy_hash.digest())
        self.assertEqual(input_image.size, messy_image.size)
        self.assertEqual(input_image.mode, messy_image.mode)
        pass

    def test_scramble(self):
        scramble = ScrambleAttributes(1)
        input_image = Image.open(str(pkg_resources.resource_filename(__name__, 'test_image.jpeg')))
        initial_hash = hashlib.sha512()
        initial_hash.update(np.array(input_image))
        messy_image = scramble.pillow_image(input_image)
        messy_hash = hashlib.sha512()
        messy_hash.update(np.array(messy_image))
        self.assertNotEqual(initial_hash.digest(), messy_hash.digest())
        self.assertEqual(input_image.size, messy_image.size)
        self.assertEqual(input_image.mode, messy_image.mode)
        pass
