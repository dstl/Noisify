from sigyn.helpers import SavedInitStatement


class Fault(SavedInitStatement):
    def __init__(self, *args, **kwargs):
        super(SavedInitStatement, self).__init__(*args, **kwargs)
        pass

    def apply(self, truth_object):
        if self.condition(truth_object):
            new_observation = self.impact_truth(truth_object)
            return self, new_observation
        return None, truth_object

    def condition(self, triggering_object):
        raise NotImplementedError
        pass

    def impact_truth(self, truth):
        raise NotImplementedError
        pass

