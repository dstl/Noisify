from noisify.helpers import Fallible
from .reporter import Reporter
from pprint import pformat


def is_atom(unknown_object):
    if hasattr(unknown_object, 'shape'):
        return True
    if hasattr(unknown_object, '__len__') and not hasattr(unknown_object, 'keys'):
        return False
    return True


class Noisifier(Fallible):
    def __init__(self, reporter=None, faults=None):
        self.reports = []
        Fallible.__init__(self, faults)
        self.reporter = reporter or Reporter()
        pass

    def get_series(self, source_truths, key=None):
        if is_atom(source_truths):
            source_truths = [source_truths]
        if self.faults:
            return self.apply_all_faults(self.create_reports(source_truths, key=key))
        else:
            return self.generate_reports(source_truths, key=key)

    def create_reports(self, source_truths, key=None):
        return [i for i in self.generate_reports(source_truths, key=key)]

    def generate_reports(self, source_truths, key=None):
        for truth in source_truths:
            if key:
                yield self.reporter(truth, identifier=key(truth))
            else:
                yield self.reporter(truth)

    def __add__(self, other):
        output = Fallible.__add__(self, other)
        output.reporter += other.reporter
        return output

    def __call__(self, *args, **kwargs):
        return self.get_series(*args, **kwargs)

    def __repr__(self):
        return pformat({'Noisifier': self.reporter})
