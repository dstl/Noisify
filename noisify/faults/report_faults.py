"""
.. Dstl (c) Crown Copyright 2019

Report level faults typically comprise faults that depend on multiple attributes. For example switching attribute
values.
"""
from .fault import Fault
from .utilities import scramble
import random
import copy


class ScrambleAttributes(Fault):
    """Switches the values of different attribute_readers within the object. By default it will
    apply to all attribute_readers."""
    def __init__(self, likelihood=0.1, attribute_identifiers=None):
        """
        Swaps the values of different attribute_readers in an object, can be restricted to a subset
        of all the attribute_readers using the optional attribute_identifiers keyword argument

        :param likelihood:
        :param attribute_identifiers:
        """
        self.scrambledness = likelihood
        self.attribute_identifiers = attribute_identifiers
        Fault.__init__(self, likelihood=likelihood, attribute_identifiers=attribute_identifiers)

    @register_implementation(priority=1)
    def numpy_array(self, array_like):
        """Swaps random cells in a numpy array-like object"""
        import numpy as np
        old_value_indices = [i for i in np.ndenumerate(array_like)]
        out_array = array_like.copy()
        scrambled_values = scramble([i[1] for i in old_value_indices], self.scrambledness, 3)
        for coordinate, value in zip((i[0] for i in old_value_indices), scrambled_values):
            out_array[coordinate] = value
        return out_array

    @register_implementation(priority=5)
    def pillow_image(self, pillow_image):
        """Swaps random pixels in a PIL Image"""
        x_size, y_size = pillow_image.size
        out_image = pillow_image.copy()
        pixels = out_image.load()
        for i in range(int(x_size * y_size * min(float(self.scrambledness)/10, 1.0) / 4)):
            x1 = random.randint(0, x_size-1)
            x2 = random.randint(0, x_size-1)
            y1 = random.randint(0, y_size-1)
            y2 = random.randint(0, y_size-1)
            pixels[x2, y2] = pixels[x1, y1]
        return out_image

    @register_implementation(priority=10)
    def impact_dictionary(self, dictionary_object):
        """Swaps random values in a dictionary"""
        confusable_attribute_identifiers = list(dictionary_object.keys())
        new_attribute_order = scramble(confusable_attribute_identifiers, self.scrambledness, 3)
        output = {}
        for expected_attribute, found_attribute in zip(confusable_attribute_identifiers, new_attribute_order):
            output[expected_attribute] = dictionary_object[found_attribute]
        return output


class ConfuseSpecificAttributes(Fault):
    """Swaps a specific pair of attribute values in a given object"""
    def __init__(self, attribute1, attribute2, likelihood=0):
        """Takes the two attribute_readers (as keys or strings) to be swapped and the likelihood
        of the swap taking place"""
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        Fault.__init__(self, attribute1, attribute2, likelihood=likelihood)

    @register_implementation(priority=10)
    def impact_dictionary(self, dictionary_object):
        """Support for dictionary like objects"""
        output = copy.deepcopy(dictionary_object)
        output[self.attribute1], output[self.attribute2] = \
            (dictionary_object[self.attribute2], dictionary_object[self.attribute1])
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
        pass

    @register_implementation(priority=10)
    def impact_truth(self, truth):
        """Just returns None!"""
        return None
