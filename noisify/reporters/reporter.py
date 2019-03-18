"""
.. Dstl (c) Crown Copyright 2019
"""
from noisify.helpers import Fallible
from noisify.attribute_readers import dictionary_lookup
from pprint import pformat
from copy import deepcopy

from noisify.reporters.report import Report


class Reporter(Fallible):
    """The most important class in Noisify!

    Reporters define how objects should be changed. They can be as specific or a general
    as needed.
    """
    def __init__(self, attributes=None, attribute_type=dictionary_lookup, faults=None):
        self.attributes = attributes or []
        self.attribute_introspection_strategy = attribute_type
        Fallible.__init__(self, faults=faults)
        self.report_index = 0

    def create_report(self, truth_object, identifier=None):
        """
        Calling the reporter object directly on an object will call this method.

        :param truth_object: Anything
        :param identifier: Optional identifier for the output report, defaults to a serial integer
        :return: A report for the given input object
        """
        identifier = identifier or self.report_index
        self.report_index += 1
        triggered_faults, measures = self._measure(truth_object)
        return Report(identifier, self._get_truth(truth_object), triggered_faults, measures)

    def _measure(self, truth_object):
        """
        :param truth_object: object to apply flaws to
        :return: a dictionary of faults triggered for different attribute_readers, and the final noised object
        """
        measurement, triggered_faults = self._get_attribute_measurements(truth_object)
        applied_faults, flawed_measurement = self.apply_all_faults(measurement)
        triggered_faults['reporter'] = applied_faults
        return triggered_faults, flawed_measurement

    def _get_attribute_measurements(self, truth_object):
        output_object = deepcopy(truth_object)
        triggered_faults = {}
        attributes = self._get_or_introspect_attributes(truth_object)
        if not attributes:
            return truth_object, {}
        for attribute in attributes:
            faults, new_value = attribute.measure(truth_object)
            attribute.update_value(output_object, new_value)
            triggered_faults[attribute.attribute_identifier] = faults
        return output_object, triggered_faults

    def _get_or_introspect_attributes(self, truth_object):
        return self.attributes or list(self.attribute_introspection_strategy(truth_object))

    def _get_truth(self, truth_object):
        attributes = self._get_or_introspect_attributes(truth_object)
        if not attributes:
            return truth_object
        truth = {}
        for attribute in attributes:
            truth[attribute.attribute_identifier] = attribute.get_value(truth_object)
        return truth

    def get_attribute_by_id(self, attribute_identifier):
        """Getter method for report attribute_readers"""
        for attribute in self.attributes:
            if attribute.attribute_identifier == attribute_identifier:
                return attribute

    def __call__(self, *args, **kwargs):
        return self.create_report(*args, **kwargs)

    def __add__(self, other):
        output = Fallible.__add__(self, other)
        new_attributes = self.merge_attributes(other, output)
        output.attributes = new_attributes
        return output

    @staticmethod
    def merge_attributes(report1, report2):
        """Merges attribute_readers between two reporters, used for reporter addition"""
        report1_attributes = set(a.attribute_identifier for a in report1.attributes)
        report2_attributes = set(a.attribute_identifier for a in report2.attributes)
        new_attributes = []
        for attribute_id in report1_attributes & report2_attributes:
            local = report1.get_attribute_by_id(attribute_id) + report2.get_attribute_by_id(attribute_id)
            new_attributes.append(local)
        for attribute_id in report1_attributes - report2_attributes:
            new_attributes.append(report1.get_attribute_by_id(attribute_id))
        for attribute_id in report2_attributes - report1_attributes:
            new_attributes.append(report2.get_attribute_by_id(attribute_id))
        return new_attributes

    def __repr__(self):
        return pformat({'Reporter':
                    {'Attributes': [a for a in self.attributes],
                     'Faults': [f for f in self.faults]}
                })
