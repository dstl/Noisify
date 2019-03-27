"""
.. Dstl (c) Crown Copyright 2019

The base classes for faults.
"""
from noisify.helpers import SavedInitStatement
from typing import get_type_hints
import random
from noisify.helpers.multi_dispatch import MultipleDispatch


class Fault(SavedInitStatement, metaclass=MultipleDispatch):
    """
    Fault base class.

    Requires implementations to be registered in its subclasses.
    Subclasses register implementations with the "register_implementation(priority=x)" decorator.

    All implementations will be attempted using a try except loop which will except Type, Attribute and Import errors.
    If no implementations succeed, the Fault will return the original object, unchanged.

    By default faults are constitutively active, this can be overridden at instantiation by providing a
    'likelihood' keyword argument with a probability of activation as a float.

    Example Usage:

        >>> class AddOneFault(Fault):
        ...     def condition(self, triggering_object):
        ...         return True
        ...
        ...     @register_implementation(priority=2)
        ...     def make_uppercase(self, lowercase_string):
        ...         return lowercase_string.upper()
        ...
        ...     @register_implementation(priority=1)
        ...     def add_to_int_string(self, integer_object):
        ...         return int(str(integer_object) + "1")
        ...
        >>> adder = AddOneFault()
        >>> adder.impact("testing priority")
        'TESTING PRIORITY'
        >>> adder.impact(1234)
        12341

    This decorator will also honour any type hints in the decorated function.

    Example:

        >>> class AddOneFault(Fault):
        ...     @register_implementation(priority=1)
        ...     def make_uppercase(self, lowercase_string: str):
        ...         print('Called uppercase function')
        ...         return lowercase_string.upper()
        ...
        ...     @register_implementation(priority=2)
        ...     def add_to_int_string(self, integer_object: int):
        ...         print('Called integer adding function')
        ...         return int(str(integer_object) + "1")
        ...
        >>> adder = AddOneFault()
        >>> adder.impact("testing annotation")
        Called uppercase function
        'TESTING ANNOTATION'
        >>> adder.impact(1234)
        Called integer adding function
        12341

    """
    def __init__(self, *args, **kwargs):
        SavedInitStatement.__init__(self, *args, **kwargs)
        if 'likelihood' in kwargs:
            self.likelihood = kwargs['likelihood']
        else:
            self.likelihood = 1.0
        pass

    def condition(self, triggering_object):
        """
        Base condition method, applies fault either constitutively or according to a likelihood argument at
        instantiation.

        :param triggering_object: Can be used to create object-type dependant activation in overridden methods
        :return: Boolean of whether or not the fault applies
        """

        return random.random() < self.likelihood

    def apply(self, not_faulted_object):
        """
        Applies the fault to an object, returns self and the new object if the activation condition is met.

        :param not_faulted_object:
        :return: self or None, impacted_object
        """
        if self.condition(not_faulted_object):
            new_observation = self.impact(not_faulted_object)
            return self, new_observation
        return None, not_faulted_object

    def impact(self, impacted_object):
        """
        Attempts to apply the fault to an object, cycles through all implementations until one succesfully executes.
        If none execute it will return the original object, unharmed.

        :param impacted_object:
        :return:
        """
        for implementation, priority in self._implementations:
            type_hints = get_type_hints(implementation)
            if type_hints:
                accepted_type = [i for i in type_hints.values()][0]
                if isinstance(impacted_object, accepted_type):
                    return implementation(self, impacted_object)
                else:
                    continue
            try:
                return implementation(self, impacted_object)
            except TypeError:
                continue
            except AttributeError:
                continue
            except ImportError:
                continue
        return impacted_object

    @property
    def name(self):
        return type(self).__name__

    def __repr__(self):
        return 'Fault: %s %s' % (self.name, self.init_statement)


class AttributeFault(Fault):
    """
    Derived base class for attribute_readers, adds mapping behaviour which enables attribute faults to be added at
    higher levels of data representation.

    For example:

        >>> from noisify.faults import GaussianNoise
        >>> noise = GaussianNoise(sigma=0.5)
        >>> noise.impact(100)
        100.66812113455995
        >>> noise.impact({'A group': 100, 'of numbers': 123})
        {'of numbers': 122.83439465953323, 'A group': 99.69284150349345}
    """

    def condition(self, triggering_object):
        """
        Overrides the condition method to be constitutively active at the initial mapping stage.

        :param triggering_object:
        :return:
        """
        if isinstance(triggering_object, dict):
            return True
        else:
            return Fault.condition(self, triggering_object)

    @register_implementation(priority=0)
    def map_fault(self, truth_object):
        """
        Attempts to apply the fault to all subitems of the given object, in practice this means
        calling the fault on all values of a dict.

        :param truth_object:
        :return:
        """
        try:
            for attribute, value in truth_object.items():
                if self.condition(value):
                    truth_object[attribute] = self.impact(value)
            return truth_object
        except AttributeError:
            raise TypeError

