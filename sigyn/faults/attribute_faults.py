from .fault import AttributeFault
import random


class GaussianNoise(AttributeFault):
    name = "Gaussian Noise"

    def __init__(self, sigma=0):
        AttributeFault.__init__(self, sigma=sigma)
        self.sigma = sigma
        pass

    def condition(self, triggering_object):
        return True

    def impact_truth(self, truth):
        return random.gauss(truth, self.sigma)


class InterruptionFault(AttributeFault):
    name = "Interrupted recording"

    def __init__(self, likelihood=0):
        AttributeFault.__init__(self, likelihood=likelihood)
        self.likelihood = 1 - likelihood
        pass

    def condition(self, triggering_object):
        return random.random() > self.likelihood

    def impact_truth(self, truth):
        return None
