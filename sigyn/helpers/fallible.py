class Fallible:
    def __init__(self, faults):
        if faults:
            self.faults = evaluate_faults(faults)
        else:
            self.faults = []

    def add_fault(self, fault):
        self.faults.append(fault)
        return self


def evaluate_faults(faults):
    from sigyn.faults import Fault
    if isinstance(faults, Fault):
        return [faults]
    try:
        return evaluate_faults(faults())
    except TypeError:
        return [i for i in faults if isinstance(i, Fault)]
