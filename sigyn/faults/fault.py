from sigyn.helpers import SavedInitStatement


def register_implementation(priority=100):
    def wrap(func):
        func._priority = priority
        return func
    return wrap


class MultipleDispatch(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return {'register_implementation': register_implementation}

    def __new__(cls, name, base, attrs):
        implementations = [(method, method._priority) for method in attrs.values() if hasattr(method, '_priority')]
        implementations.sort(key=lambda x: x[1])
        if implementations:
            attrs['_implementations'] = [i for i in implementations]
            for parent_implementations in (getattr(b, '_implementations', None) for b in base):
                if parent_implementations:
                    attrs['_implementations'] += parent_implementations
            attrs['_implementations'].sort(key=lambda x: x[1], reverse=True)
        return super(MultipleDispatch, cls).__new__(cls, name, base, attrs)


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
            try:
                return implementation(self, impacted_object)
            except(TypeError):
                continue
            except(AttributeError):
                continue
            except(ImportError):
                continue
        raise NotImplementedError


class AttributeFault(Fault):
    @register_implementation(priority=0)
    def map_fault(self, truth_object):
        try:
            for attribute, value in truth_object.items():
                truth_object[attribute] = self.impact(value)
            return truth_object
        except AttributeError:
            raise TypeError


class ReportFault(Fault):
    pass


class SeriesFault(Fault):
    pass
