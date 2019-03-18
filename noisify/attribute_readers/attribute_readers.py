"""
.. Dstl (c) Crown Copyright 2019

Attribute Readers allow faults to be directed to specific attributes of an input object. These do
not need to be literal attributes, they can be values in a dictionary or columns in a database for
example, as long as they can be accessed via a key.
"""
from noisify.helpers import Fallible
from pprint import pformat


class AttributeReader(Fallible):
    """
    The AttributeReader interface describes a mechanism to read and write values from an object
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
        """(Part of the interface) Must return the ground truth for the given attribute of the original object"""
        raise NotImplementedError

    def measure(self, truth_object):
        """Takes a 'measurement' of the ground truth, applying all faults in the process"""
        truth = self.get_value(truth_object)
        return self.apply_all_faults(truth)

    def update_value(self, output_object, new_value):
        """(Part of the interface) Must update the new output object at the given attribute key with a new value"""
        raise NotImplementedError

    def __add__(self, other):
        if self.attribute_identifier == other.attribute_identifier:
            return Fallible.__add__(self, other)
        else:
            raise TypeError('Attribute addition requires attribute_readers of the same type')

    def __repr__(self):
        return pformat((self.attribute_identifier, {'faults': [i for i in self.faults]}))


class DictValue(AttributeReader):
    """
    Provides support for dictionary value lookups as attributes.
    """
    def get_value(self, truth_object):
        """Queries the truth object using a dictionary lookup"""
        return truth_object[self.attribute_identifier]

    def update_value(self, output_object, new_value):
        """Sets using dictionary value assignment"""
        output_object[self.attribute_identifier] = new_value
        return output_object


class ObjectAttribute(AttributeReader):
    """
    Provides support for literal object attributes as attributes.
    """
    def get_value(self, truth_object):
        """Queries using getattr"""
        return getattr(truth_object, self.attribute_identifier)

    def update_value(self, output_object, new_value):
        """Sets using setattr"""
        setattr(output_object, self.attribute_identifier, new_value)
        return output_object
