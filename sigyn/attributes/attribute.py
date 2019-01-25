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

    def __add__(self, other):
        if self.attribute_identifier == other.attribute_identifier:
            return Fallible.__add__(self, other)
        else:
            raise TypeError('Attribute addition requires attributes of the same type')


def generate_object_attribute_identifiers(unknown_object):
    if hasattr(unknown_object, 'keys'):
        return (i for i in unknown_object.keys())
    if hasattr(unknown_object, '__len__'):
        return range(len(unknown_object))
    return (att for att in dir(unknown_object) if not hasattr(att, '__call__') and att[0] != '_')


def generate_object_attributes(unknown_object, attribute_faults=None):
    for identifier in generate_object_attribute_identifiers(unknown_object):
        yield Attribute(identifier, faults=attribute_faults)
