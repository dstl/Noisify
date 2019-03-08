import random


def scramble(collection, scrambledness, confusion_range):
    """
    Scrambles the order of objects in a collection using a gaussian distribution, can lead to
    duplicate objects

    :param collection:
    :param scrambledness:
    :param confusion_range:
    :return:
    """
    new_collection = []
    visited_indices = set()
    for index, item in enumerate(collection):
        if random.random() <= scrambledness:
            index = int(abs(index + (confusion_range * (random.random() - 0.5))))
        if index not in visited_indices and index < len(collection):
            new_collection.append(collection[index])
            visited_indices.add(index)
        else:
            closest_remaining = float('inf')
            closest_index = None
            for unvisited_index in range(len(collection)):
                if unvisited_index in visited_indices:
                    continue
                difference = abs(unvisited_index - index)
                if difference < closest_remaining:
                    closest_remaining = difference
                    closest_index = unvisited_index
            new_collection.append(collection[closest_index])
    return new_collection


def dropped_scramble(collection, scrambledness, confusion_range):
    """
    Scrambles objects in a collection, with a chance to lose some objects

    :param collection:
    :param scrambledness:
    :param confusion_range:
    :return:
    """
    return [i for i in scramble(collection, scrambledness, confusion_range) if random.random() > scrambledness / 10]


def typo(string, severity):
    """
    Roughly rearranges string with the occasional missed character, based on applying a gaussian noise filter
    to the string character indexes and then rounding to the closest index.

    :param string:
    :param severity:
    :return: mistyped string
    """
    return ''.join(dropped_scramble(string, float(severity), 3))


def get_mode_size(mode):
    """Converts a PIL image mode string into a dimension cardinality"""
    return len([i for i in mode if i.isupper()])


def image_size(image_object):
    channels = get_mode_size(image_object.mode)
    if channels > 1:
        return image_object.height, image_object.width, channels
    else:
        return image_object.height, image_object.width
