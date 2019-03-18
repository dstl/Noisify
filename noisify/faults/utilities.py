"""
.. Dstl (c) Crown Copyright 2019

Fault utility functions, general purpose code that is used by multiple functions.
"""
import random


def scramble(collection, scrambledness, confusion_range):
    """
    Scrambles the order of objects in a collection using a gaussian distribution, can lead to
    duplicate objects

    :param collection:
    :param scrambledness: How likely two objects are to be switched
    :param confusion_range: How far apart objects can be confused with one another
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
    :param scrambledness: How likely two objects are to be switched
    :param confusion_range: How far apart objects can be confused with one another
    :return:
    """
    return [i for i in scramble(collection, scrambledness, confusion_range) if random.random() > scrambledness / 10]
