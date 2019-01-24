from sigyn.helpers import Fallible


class Attribute(Fallible):
    def __init__(self, attribute_identifier, faults=None):
        Fallible.__init__(self, faults)
        self.attribute_identifier = attribute_identifier

    def get_truth(self, truth_object):
        if hasattr(truth_object, self.attribute_identifier):
            return getattr(truth_object, self.attribute_identifier)
        elif self.attribute_identifier in truth_object:
            return truth_object[self.attribute_identifier]
        else:
            raise ValueError("Attribute %s not found in %s" % (self.attribute_identifier, repr(truth_object)))

    def measure(self, truth_object):
        truth = self.get_truth(truth_object)
        return self.apply_all_faults(truth)

