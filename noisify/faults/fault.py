from noisify.helpers import SavedInitStatement
from pprint import pformat
from typing import get_type_hints

from noisify.helpers.multi_dispatch import register_implementation, MultipleDispatch


class Fault(SavedInitStatement, metaclass=MultipleDispatch):
    _implementations = []

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
    @register_implementation(priority=0)
    def map_fault(self, truth_object):
        try:
            for attribute, value in truth_object.items():
                if self.condition(value):
                    truth_object[attribute] = self.impact(value)
            return truth_object
        except AttributeError:
            raise TypeError


class ReportFault(Fault):
    pass


class SeriesFault(Fault):
    pass
