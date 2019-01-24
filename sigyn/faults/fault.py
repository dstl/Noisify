from sigyn.helpers import SavedInitStatement


class Fault(SavedInitStatement):
    def __init__(self, *args, **kwargs):
        SavedInitStatement.__init__(self, *args, **kwargs)
        pass

    def apply(self, unfaulted_object):
        if self.condition(unfaulted_object):
            new_observation = self.impact(unfaulted_object)
            return self, new_observation
        return None, unfaulted_object

    def condition(self, triggering_object):
        raise NotImplementedError

    def impact(self, impacted_object):
        raise NotImplementedError


class AttributeFault(Fault):
    def impact(self, impacted_object):
        return self.impact_truth(impacted_object)

    def impact_truth(self, truth_object):
        raise NotImplementedError


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
