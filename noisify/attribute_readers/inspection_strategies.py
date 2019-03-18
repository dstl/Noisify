"""
.. Dstl (c) Crown Copyright 2019
Inspection strategies are used by reporters to create attribute_readers for given objects when none are specified.
"""
from noisify.attribute_readers import DictValue, ObjectAttribute


def dictionary_lookup(unknown_dictionary, attribute_faults=None):
    """
    Generates attribute_readers for each key/value pair of a given dictionary, enables
    reporters to map faults across dictionaries without further specification.
    """
    if hasattr(unknown_dictionary, 'keys'):
        for identifier in unknown_dictionary.keys():
            yield DictValue(identifier, faults=attribute_faults)


def object_attributes_lookup(unknown_object, attribute_faults=None):
    """
    Generates attribute_readers for each attribute of a given object, enables
    reporters to map faults across objects without further specification.
    Ignores methods and private attributes marked with '_'.
    """
    for attribute in dir(unknown_object):
        if not callable(attribute) and attribute[0] != '_':
            yield ObjectAttribute(attribute, faults=attribute_faults)
