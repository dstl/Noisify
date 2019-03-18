"""
.. Dstl (c) Crown Copyright 2019
"""
import copy


class Fallible:
    """
    Fallible mixin, adds faults to an object as well as getters and setters.
    Also provides methods for applying faults to an object.
    """
    def __init__(self, faults):
        if faults:
            self.faults = evaluate_faults(faults)
        else:
            self.faults = []

    def add_fault(self, fault):
        """
        Add a fault to the fallible object

        :param fault:
        :return:
        """
        self.faults.append(fault)
        return self

    def apply_all_faults(self, incompletely_flawed_object):
        """
        Runs through the fallible objects faults and applies them to an object, returns
        activated faults as well as the finished object

        :param incompletely_flawed_object:
        :return:
        """
        applied_faults = []
        for fault in self.faults:
            applied_fault, result = fault.apply(incompletely_flawed_object)
            if applied_fault:
                incompletely_flawed_object = result
                applied_faults.append(applied_fault)
        return applied_faults, incompletely_flawed_object

    def __add__(self, other):
        clone = copy.deepcopy(self)
        clone.faults += other.faults
        return clone


def evaluate_faults(faults):
    """
    Enables faults to be given as a single fault, or a list of faults,
    or a function to generate a fault or list of faults,
    to the instantiation of the fallible object.

    :param faults:
    :return:
    """
    from noisify.faults import Fault
    if isinstance(faults, Fault):
        return [faults]
    try:
        return evaluate_faults(faults())
    except TypeError:
        return [i for i in faults if isinstance(i, Fault)]
