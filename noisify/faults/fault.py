from noisify.helpers import SavedInitStatement
from pprint import pformat
from typing import get_type_hints

from noisify.helpers.multi_dispatch import register_implementation, MultipleDispatch


class Fault(SavedInitStatement, metaclass=MultipleDispatch):
    """
    Fault base class.

    Requires implementations to be registered in its subclasses as well as activation conditions.
    Subclasses can decorate implementations with the "register_implementation(priority=x)" decorator.

    All implementations will be attempted using a try except loop which will except Type, Attribute and Import errors.
    If no implementations succeed, the Fault will raise a NotImplementedError.

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
        ...     def condition(self, triggering_object):
        ...         return True
        ...
        ...     @register_implementation(priority=2)
        ...     def make_uppercase(self, lowercase_string: str):
        ...         print('Called uppercase function')
        ...         return lowercase_string.upper()
        ...
        ...     @register_implementation(priority=1)
        ...     def add_to_int_string(self, integer_object: int):
        ...         print('Called integer adding function')
        ...         return int(str(integer_object) + "1")
        ...
        >>> adder = AddOneFault()
        >>> adder.impact("testing priority")
        Called uppercase function
        'TESTING PRIORITY'
        >>> adder.impact(1234)
        Called integer adding function
        12341

    """
    def __init__(self, *args, **kwargs):
        SavedInitStatement.__init__(self, *args, **kwargs)
        pass

    def apply(self, not_faulted_object):
        if self.condition(not_faulted_object):
            new_observation = self.impact(not_faulted_object)
            return self, new_observation
        return None, not_faulted_object

    def condition(self, triggering_object):
        raise NotImplementedError

    def impact(self, impacted_object):
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
        raise NotImplementedError

    @property
    def name(self):
        return type(self).__name__

    def __repr__(self):
        return 'Fault: %s %s' % (self.name, self.init_statement)

    def formatted_string(self, indent=0):
        return pformat(self, indent=indent)


class AttributeFault(Fault):
    """
    Derived base class for attributes, adds mapping behaviour which enables attribute faults to be added at
    higher levels of data representation.

    For example:

        >>> from noisify.faults import GaussianNoise
        >>> noise = GaussianNoise(sigma=0.5)
        >>> noise.impact(100)
        100.66812113455995
        >>> noise.impact({'A group': 100, 'of numbers': 123})
        {'of numbers': 122.83439465953323, 'A group': 99.69284150349345}
    """
    @register_implementation(priority=0)
    def map_fault(self, truth_object):
        try:
            for attribute, value in truth_object.items():
                if self.condition(value):
                    truth_object[attribute] = self.impact(value)
            return truth_object
        except AttributeError:
            raise TypeError

