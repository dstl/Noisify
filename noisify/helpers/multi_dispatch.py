"""
.. Dstl (c) Crown Copyright 2019
"""


def register_implementation(priority=-1):
    """
    Decorator for use with MultipleDispatch derived classes, accepts a priority numeric. It does not need to be
    imported.
    """
    def wrap(func):
        func._priority = priority
        return func
    return wrap


class MultipleDispatch(type):
    """
    Metaclass for providing a priority queue of methods under cls._implementations which can be used for multiple
    dispatch in a duck typing fashion. Larger priorities take precedence.
    """
    @classmethod
    def __prepare__(mcs, name, bases):
        return {'register_implementation': register_implementation}

    def __new__(cls, name, base, attrs):
        implementations = [(method, method._priority) for method in attrs.values() if hasattr(method, '_priority')]
        if implementations:
            attrs['_implementations'] = [i for i in implementations]
            for parent_implementations in (getattr(b, '_implementations', None) for b in base):
                if parent_implementations:
                    attrs['_implementations'] += parent_implementations
            attrs['_implementations'].sort(key=lambda x: x[1], reverse=True)
            del attrs['register_implementation']
        return super(MultipleDispatch, cls).__new__(cls, name, base, attrs)
