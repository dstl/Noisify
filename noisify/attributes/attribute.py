from noisify.helpers import Fallible
from pprint import pformat


class Attribute(Fallible):
    """
    The Attribute interface describes a mechanism to read and write values from an object based upon
    """
    def __init__(self, attribute_identifier, faults=None):
        """
        Takes an identifier for the desired attribute, and a series of faults to be applied
        to it.

        :param attribute_identifier:
        :param faults:
        """
        Fallible.__init__(self, faults)
        self.attribute_identifier = attribute_identifier

    def get_value(self, truth_object):
        """Returns the ground truth for the given attribute of the original object"""
        raise NotImplementedError

    def measure(self, truth_object):
        """Takes a 'measurement' of the ground truth, applying all faults in the process"""
        truth = self.get_value(truth_object)
        return self.apply_all_faults(truth)

    def update_value(self, output_object, new_value):
        raise NotImplementedError

    def __add__(self, other):
        if self.attribute_identifier == other.attribute_identifier:
            return Fallible.__add__(self, other)
        else:
            raise TypeError('Attribute addition requires attributes of the same type')

    def __repr__(self):
        return pformat((self.attribute_identifier, {'faults': [i for i in self.faults]}))


class DictValue(Attribute):
    """
    Provides support for attributes in the form of dictionary value lookups.
    """
    def get_value(self, truth_object):
        """Queries the truth object using a dictionary lookup"""
        return truth_object[self.attribute_identifier]

    def update_value(self, output_object, new_value):
        output_object[self.attribute_identifier] = new_value
        return output_object


class ObjectAttribute(Attribute):
    """
    Provides support for attributes in the form of literal object attributes
    """
    def get_value(self, truth_object):
        """Returns the ground truth for the given attribute of the original object"""
        return getattr(truth_object, self.attribute_identifier)

    def update_value(self, output_object, new_value):
        setattr(output_object, self.attribute_identifier, new_value)
        return output_object
