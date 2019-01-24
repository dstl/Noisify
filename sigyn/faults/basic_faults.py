from .fault import Fault
import random


class GaussianNoise(Fault):
    name = "Gaussian Noise"

    def __init__(self, sigma=0):
        super(Fault, self).__init__(sigma=sigma)
        self.sigma = sigma
        pass

    def condition(self, triggering_object):
        return True

    def impact_truth(self, truth):
        return random.gauss(truth, self.sigma)


class InterruptionFault(Fault):
    name = "Interrupted recording"

    def __init__(self, likelihood=0):
        super(Fault, self).__init__(likelihood=likelihood)
        self.likelihood = 1 - likelihood
        pass

    def condition(self, triggering_object):
        return random.random() > self.likelihood

    def impact_truth(self, truth):
        return None
