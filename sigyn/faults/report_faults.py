from .fault import ReportFault
from .utilities import scramble
import random
import copy


class ScrambleAttributes(ReportFault):
    def __init__(self, scrambledness=0, attribute_identifiers=None):
        self.scrambledness = scrambledness
        self.attribute_identifiers = attribute_identifiers
        ReportFault.__init__(self, likelihood=scrambledness, attribute_identifiers=attribute_identifiers)

    def condition(self, triggering_object):
        return True

    @register_implementation(priority=10)
    def impact_report(self, report_object):
        confusable_attribute_identifiers = self.attribute_identifiers or [att for att in report_object]
        new_attribute_order = scramble(confusable_attribute_identifiers, self.scrambledness, 3)
        output = {}
        for expected_attribute, found_attribute in zip(confusable_attribute_identifiers, new_attribute_order):
            output[expected_attribute] = report_object[found_attribute]
        return output


class ConfuseSpecificAttributes(ReportFault):
    def __init__(self, attribute1, attribute2, likelihood=0):
        self.likelihood = likelihood
        self.attribute1 = attribute1
        self.attribute2 = attribute2
        ReportFault.__init__(self, attribute1, attribute2, likelihood=likelihood)

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    def impact_report(self, report_object):
        output = copy.deepcopy(report_object)
        output[self.attribute1], output[self.attribute2] = \
            (report_object[self.attribute2], report_object[self.attribute1])
        return output
