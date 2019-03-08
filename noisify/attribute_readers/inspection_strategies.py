"""
.. Dstl (c) Crown Copyright 2017
Inspection strategies are used by reporters to create attribute_readers for given objects when none are specified.
"""
from noisify.attribute_readers import DictValue


def dictionary_lookup(unknown_dictionary, attribute_faults=None):
    """
    Generates attribute_readers for each key/value pair of a given dictionary, enables
    reporters to map faults across dictionaries without further specification.
    
    :param unknown_dictionary: 
    :param attribute_faults: 
    :return: 
    """
    if hasattr(unknown_dictionary, 'keys'):
        for identifier in unknown_dictionary.keys():
            yield DictValue(identifier, faults=attribute_faults)
