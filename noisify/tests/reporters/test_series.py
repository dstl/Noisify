import unittest
from noisify.reporters import Noisifier, Reporter
from noisify.attributes import Attribute
from noisify.faults import GaussianNoise


class TestSeries(unittest.TestCase):
    def test_series_call(self):
        new_prototype = Reporter(attributes=[Attribute('noisy', faults=GaussianNoise(sigma=0.1)),
                                             Attribute('noiseless')])
        series_builder = Noisifier(reporter=new_prototype)
        data = [{'noisy': 100, 'noiseless': 100},
                {'noisy': 10, 'noiseless': 100},
                {'noisy': 100, 'noiseless': 10}]
        result = series_builder(data)
        self.assertEqual(len([i for i in result]), 3)
        pass

