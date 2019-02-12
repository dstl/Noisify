import random


def scramble(collection, scrambledness, confusion_range):
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
    return [i for i in scramble(collection, scrambledness, confusion_range) if random.random() > scrambledness / 10]


def typo(string, severity):
    return ''.join(dropped_scramble(string, float(severity), 3))
