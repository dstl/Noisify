from sigyn.helpers import Fallible
from sigyn.attributes import generate_object_attributes
from sigyn.faults import AttributeFault, ReportFault


class Reporter(Fallible):
    def __init__(self, attributes=None, faults=None):
        self.attributes = attributes
        Fallible.__init__(self, faults=faults)
        self.attribute_faults = [fault for fault in self.faults if issubclass(type(fault), AttributeFault)]
        if self.attributes:
            self.apply_attribute_faults()
        self.report_index = 0

    def apply_attribute_faults(self):
        for att in self.attributes:
            for fault in self.attribute_faults:
                att.add_fault(fault)
        pass

    def create_report(self, truth_object, identifier=None):
        identifier = identifier or self.report_index
        self.report_index += 1
        triggered_faults, measures = self.measure(truth_object)
        return Report(identifier, self.get_truth(truth_object), triggered_faults, measures)

    def measure(self, truth_object):
        measurement, triggered_faults = self.get_attribute_measurements(truth_object)
        applied_faults, flawed_measurement = self.apply_all_faults(measurement, fault_type=ReportFault)
        triggered_faults['reporter'] = applied_faults
        return triggered_faults, flawed_measurement

    def get_attribute_measurements(self, truth_object):
        measurement = {}
        triggered_faults = {}
        for attribute in self.get_or_introspect_attributes(truth_object):
            faults, measure = attribute.measure(truth_object)
            measurement[attribute.attribute_identifier] = measure
            triggered_faults[attribute.attribute_identifier] = faults
        return measurement, triggered_faults

    def get_or_introspect_attributes(self, truth_object):
        return self.attributes or generate_object_attributes(truth_object, attribute_faults=self.attribute_faults)

    def get_truth(self, truth_object):
        truth = {}
        for attribute in self.get_or_introspect_attributes(truth_object):
            truth[attribute.attribute_identifier] = attribute.get_truth(truth_object)
        return truth

    def get_attribute_by_id(self, attribute_identifier):
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


class Report:
    def __init__(self, identifier, truth, triggered_faults, observed):
        self.identifier = identifier
        self.truth = truth
        self.triggered_faults = triggered_faults
        self.observed = observed

    def __repr__(self):
        return str(self.observed)

