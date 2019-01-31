import copy


class Fallible:
    def __init__(self, faults):
        if faults:
            self.faults = evaluate_faults(faults)
        else:
            self.faults = []

    def add_fault(self, fault):
        self.faults.append(fault)
        return self

    def apply_all_faults(self, incompletely_flawed_object, fault_type=None):
        applied_faults = []
        for fault in self.faults:
            if fault_type and not issubclass(type(fault), fault_type):
                continue
            applied_fault, result = fault.apply(incompletely_flawed_object)
            if applied_fault:
                incompletely_flawed_object = result
                applied_faults.append(applied_fault)
        return applied_faults, incompletely_flawed_object

    def __add__(self, other):
        clone = copy.deepcopy(self)
        clone.faults += other.faults
        return clone


def evaluate_faults(faults):
    from sigyn.faults import Fault
    if isinstance(faults, Fault):
        return [faults]
    try:
        return evaluate_faults(faults())
    except TypeError:
        return [i for i in faults if isinstance(i, Fault)]
