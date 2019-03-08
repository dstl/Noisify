"""
.. Dstl (c) Crown Copyright 2017
"""


class Report:
    """Report class, stores the noisified data with the faults and ground truth
    for future use. Delegates all methods and attribute_readers to the observed item."""
    def __init__(self, identifier, truth, triggered_faults, observed):
        self.identifier = identifier
        self.truth = truth
        self.triggered_faults = triggered_faults
        self.observed = observed

    def __getattr__(self, item):
        return getattr(self.observed, item)

    def __getitem__(self, item):
        return self.observed[item]
