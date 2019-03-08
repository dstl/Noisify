from noisify.attributes import Attribute


def generate_noise_attributes_from_dict(unknown_dictionary, attribute_faults=None):
    """
    Generates attributes for each key/value pair of a given dictionary, enables
    reporters to map faults across dictionaries without further specification.
    
    :param unknown_dictionary: 
    :param attribute_faults: 
    :return: 
    """
    if hasattr(unknown_dictionary, 'keys'):
        for identifier in unknown_dictionary.keys():
            yield Attribute(identifier, faults=attribute_faults)
