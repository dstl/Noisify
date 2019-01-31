from sigyn.attributes import Attribute


def generate_object_attribute_identifiers(unknown_object):
    if hasattr(unknown_object, 'keys'):
        return (i for i in unknown_object.keys())
    if hasattr(unknown_object, '__len__'):
        return range(len(unknown_object))
    return (att for att in dir(unknown_object) if not hasattr(att, '__call__') and att[0] != '_')


def generate_object_attributes(unknown_object, attribute_faults=None):
    for identifier in generate_object_attribute_identifiers(unknown_object):
        yield Attribute(identifier, faults=attribute_faults)
