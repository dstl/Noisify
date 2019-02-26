from .fault import Fault
from .utilities import scramble
import random
import copy


class ScrambleAttributes(Fault):
    def __init__(self, scrambledness=0, attribute_identifiers=None):
        self.scrambledness = scrambledness
        self.attribute_identifiers = attribute_identifiers
        Fault.__init__(self, likelihood=scrambledness, attribute_identifiers=attribute_identifiers)

    def condition(self, triggering_object):
        return True

    @register_implementation(priority=1)
    def numpy_array(self, array_like):
        import numpy as np
        old_value_indices = [i for i in np.ndenumerate(array_like)]
        out_array = array_like.copy()
        scrambled_values = scramble([i[1] for i in old_value_indices], self.scrambledness, 3)
        for coordinate, value in zip((i[0] for i in old_value_indices), scrambled_values):
            out_array[coordinate] = value
        return out_array

    @register_implementation(priority=10)
    def impact_report(self, report_object):
        confusable_attribute_identifiers = list(report_object.keys())
        new_attribute_order = scramble(confusable_attribute_identifiers, self.scrambledness, 3)
        output = {}
        for expected_attribute, found_attribute in zip(confusable_attribute_identifiers, new_attribute_order):
            output[expected_attribute] = report_object[found_attribute]
        return output


class ConfuseSpecificAttributes(Fault):
    def __init__(self, attribute1, attribute2, likelihood=0):
        self.likelihood = likelihood
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        Fault.__init__(self, attribute1, attribute2, likelihood=likelihood)

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=10)
    def impact_report(self, report_object):
        output = copy.deepcopy(report_object)
        output[self.attribute1], output[self.attribute2] = \
            (report_object[self.attribute2], report_object[self.attribute1])
        return output


class LoseEntireReport(Fault):
    """
    Replaces entire report with None, activates according to set likelihood.
    """
    def __init__(self, likelihood=0):
        """
        Instantiate with likelihood of interruption as a 0-1 float.
        :param likelihood:
        """
        Fault.__init__(self, likelihood=likelihood)
        self.likelihood = likelihood
        pass

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=10)
    def impact_truth(self, truth):
        return None
