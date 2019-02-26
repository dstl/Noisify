from noisify.helpers import Fallible
from pprint import pformat


class Attribute(Fallible):
    def __init__(self, attribute_identifier, faults=None):
        Fallible.__init__(self, faults)
        self.attribute_identifier = attribute_identifier

    def get_truth(self, truth_object):
        try:
            return truth_object[self.attribute_identifier]
        except:
            if hasattr(truth_object, self.attribute_identifier):
                return getattr(truth_object, self.attribute_identifier)
        raise ValueError("Attribute %s not found in %s" % (self.attribute_identifier, repr(truth_object)))

    def measure(self, truth_object):
        truth = self.get_truth(truth_object)
        return self.apply_all_faults(truth)

    def __add__(self, other):
        if self.attribute_identifier == other.attribute_identifier:
            return Fallible.__add__(self, other)
        else:
            raise TypeError('Attribute addition requires attributes of the same type')

    def __repr__(self):
        return pformat((self.attribute_identifier, {'faults': [i for i in self.faults]}))
