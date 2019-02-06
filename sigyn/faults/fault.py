from sigyn.helpers import SavedInitStatement


def register_implementation(priority=100):
    print('Called to register with priority %d' % priority)
    def wrap(func):
        func._priority = priority
        return func
    return wrap


class MultipleDispatch(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        print(name)
        return {'register_implementation': register_implementation}

    def __new__(cls, name, base, attrs):
        implementations = [(method, method._priority) for method in attrs.values() if hasattr(method, '_priority')]
        implementations.sort(key=lambda x: x[1])
        if implementations:
            attrs['_implementations'] = [i[0] for i in implementations]
            for parent_implementations in (getattr(b, '_implementations', None) for b in base):
                if parent_implementations:
                    attrs['_implementations'] += parent_implementations
            print(attrs['_implementations'])
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
        for implementation in self._implementations:
            try:
                return implementation(self, impacted_object)
            except(TypeError):
                continue
        return impacted_object


class AttributeFault(Fault):
    _implementations = []
    @register_implementation(priority=1)
    def map_fault(self, truth_object):
        try:
            for attribute, value in truth_object['attributes'].items():
                truth_object['attributes'][attribute] = self.impact(value)
        except TypeError:
            raise TypeError



class ReportFault(Fault):
    def impact(self, impacted_object):
        return self.impact_report(impacted_object)

    def impact_report(self, report_object):
        raise NotImplementedError


class SeriesFault(Fault):
    def impact(self, impacted_object):
        return self.impact_series(impacted_object)

    def impact_series(self, report_object):
        raise NotImplementedError
