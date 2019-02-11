from .fault import AttributeFault, register_implementation
import random
from .utilities import typo


class GaussianNoise(AttributeFault):
    name = "Gaussian Noise"

    def __init__(self, sigma=0):
        AttributeFault.__init__(self, sigma=sigma)
        self.sigma = sigma
        pass

    def condition(self, triggering_object):
        return True

    @register_implementation(priority=10)
    def numpy_array(self, array_like_object):
        import numpy as np
        return np.random.normal(array_like_object, self.sigma)

    @register_implementation(priority=1)
    def python_numeric(self, python_numeric_object):
        return random.gauss(python_numeric_object, self.sigma)


class InterruptionFault(AttributeFault):
    name = "Interrupted recording"

    def __init__(self, likelihood=0):
        AttributeFault.__init__(self, likelihood=likelihood)
        self.likelihood = likelihood
        pass

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=10)
    def impact_truth(self, truth):
        return None


class TypographicalFault(AttributeFault):
    name = "Typo"

    def __init__(self, likelihood=0, severity=0):
        AttributeFault.__init__(self, likelihood=likelihood, severity=severity)
        self.likelihood = likelihood
        self.severity = severity

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=10)
    def impact_truth(self, truth_object):
        return typo(str(truth_object), self.severity)
