"""
.. Dstl (c) Crown Copyright 2019
"""
from noisify.helpers import Fallible
from .reporter import Reporter
from pprint import pformat
import itertools


def is_atom(unknown_object):
    """Determines whether an object is an atom or a collection"""
    if hasattr(unknown_object, 'shape'):
        return True
    if hasattr(unknown_object, '__len__') and not hasattr(unknown_object, 'keys'):
        return False
    return True


class Noisifier(Fallible):
    """The Noisifier class handles pipelining objects through an underlying reporter class,
    it can also be configured to apply faults at the pipeline level, such as confusing elements from one
    object to another."""
    def __init__(self, reporter=None, faults=None):
        self.reports = []
        Fallible.__init__(self, faults)
        self.reporter = reporter or Reporter()
        pass

    def get_series(self, source_truths, key=None, loop=False):
        """
        Calling the noisifier object directly on an object will call this method.

        :param source_truths: a series of objects (or a single object)
        :param key: function which will extract a name from each object to be used as an
        identifier for the resultant report.
        :param loop: whether to generate indefinitely by looping over the source truths
        :return: a report generator
        """
        if is_atom(source_truths):
            source_truths = [source_truths]
        if loop:
            source_truths = itertools.cycle(source_truths)
        if self.faults:
            return self.apply_all_faults(self._create_reports(source_truths, key=key))
        else:
            return self._generate_reports(source_truths, key=key)

    def _create_reports(self, source_truths, key=None):
        return [i for i in self._generate_reports(source_truths, key=key)]

    def _generate_reports(self, source_truths, key=None):
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
