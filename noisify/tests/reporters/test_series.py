"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.reporters import Noisifier, Reporter
from noisify.attribute_readers import DictValue, ObjectAttribute
from noisify.faults import GaussianNoise


class TestSeries(unittest.TestCase):
    def test_dict_series_call(self):
        new_prototype = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                             DictValue('noiseless')])
        series_builder = Noisifier(reporter=new_prototype)
        data = [{'noisy': 100, 'noiseless': 100},
                {'noisy': 10, 'noiseless': 100},
                {'noisy': 100, 'noiseless': 10}]
        result = series_builder(data)
        self.assertEqual(len([i for i in result]), 3)
        for truth, new in zip(data, result):
            self.assertEqual(truth['noiseless'], new['noiseless'])
            self.assertNotEqual(truth['noisy'], new['noisy'])
        pass

    def test_object_series_call(self):
        class Foo:
            def __init__(self, noisy, noiseless):
                self.noisy = noisy
                self.noiseless = noiseless

        new_prototype = Reporter(attributes=[ObjectAttribute('noisy', faults=GaussianNoise(sigma=0.1)),
                                             ObjectAttribute('noiseless')])
        series_builder = Noisifier(reporter=new_prototype)

        data = [Foo(100, 100), Foo(10, 100), Foo(100, 10)]
        result = series_builder(data)

        self.assertEqual(len([i for i in result]), 3)
        for truth, new in zip(data, result):
            self.assertEqual(truth.noiseless, new.noiseless)
            self.assertNotEqual(truth.noisy, new.noisy)
        pass

    def test_looping(self):
        new_prototype = Reporter(attributes=[DictValue('noisy', faults=GaussianNoise(sigma=0.1)),
                                             DictValue('noiseless')])
        series_builder = Noisifier(reporter=new_prototype)
        data = [{'noisy': 100, 'noiseless': 100},
                {'noisy': 10, 'noiseless': 50},
                {'noisy': 100, 'noiseless': 10}]
        result = series_builder(data, loop=True)
        for index, value in enumerate(result):
            if index == 4:
                break
        self.assertEqual(value['noiseless'], 50)
        pass
