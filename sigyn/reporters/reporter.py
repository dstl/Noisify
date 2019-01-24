from sigyn.helpers import Fallible


class Reporter(Fallible):
    def __init__(self, report_type, attributes=None, faults=None, groups=None):
        self.report_type = report_type
        self.attributes = attributes or []
        Fallible.__init__(self, faults)
        self.inherit_group_faults(groups or [])
        self.identifier = None
        self.report_index = 0

    def inherit_group_faults(self, groups):
        for group in groups:
            for fault in group.faults:
                self.faults.append(fault)
        pass

    def create_report(self, truth_object, identifier=None):
        ident = identifier or self.report_index
        self.report_index += 1
        triggered_faults, measures = self.measure(truth_object)
        return Report(ident, self.report_type, self.get_truth(truth_object), triggered_faults, measures)

    def measure(self, truth_object):
        measurement, triggered_faults = self.get_attribute_measurements(truth_object)
        applied_faults, flawed_measurement = self.apply_all_faults(measurement)
        triggered_faults['reporter'] = applied_faults
        return triggered_faults, flawed_measurement

    def get_attribute_measurements(self, truth_object):
        measurement = {}
        triggered_faults = {}
        for attribute in self.attributes:
            faults, measure = attribute.measure(truth_object)
            measurement[attribute.attribute_identifier] = measure
            triggered_faults[attribute.attribute_identifier] = faults
        return measurement, triggered_faults

    def get_truth(self, truth_object):
        truth = {}
        for attribute in self.attributes:
            truth[attribute.attribute_identifier] = attribute.get_truth(truth_object)
        return truth

    def __call__(self, *args, **kwargs):
        return self.create_report(*args, **kwargs)


class Report:
    def __init__(self, identifier, report_type, truth, triggered_faults, observed):
        self.identifier = identifier
        self.report_type = report_type
        self.truth = truth
        self.triggered_faults = triggered_faults
        self.observed = observed

    def __repr__(self):
        return str(self.observed)