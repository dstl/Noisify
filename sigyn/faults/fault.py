from sigyn.helpers import SavedInitStatement


class Fault(SavedInitStatement):
    def __init__(self, *args, **kwargs):
        super(SavedInitStatement, self).__init__(*args, **kwargs)
        pass

    def apply(self, triggering_object, affected_recorder):
        if self.condition(triggering_object):
            new_observation = self.impact_truth(affected_recorder.working_observation)
            return new_observation
        return affected_recorder.working_observation

    def condition(self, triggering_object):
        raise NotImplementedError
        pass

    def impact_truth(self, truth):
        raise NotImplementedError
        pass

