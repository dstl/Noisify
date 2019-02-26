from noisify.attributes import Attribute


def generate_object_attribute_identifiers(unknown_object):
    if hasattr(unknown_object, 'keys'):
        return (i for i in unknown_object.keys())
    return []


def generate_object_attributes(unknown_object, attribute_faults=None):
    for identifier in generate_object_attribute_identifiers(unknown_object):
        yield Attribute(identifier, faults=attribute_faults)
