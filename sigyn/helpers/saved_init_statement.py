import inspect


class SavedInitStatement:
    def __init__(self, *args, **kwargs):
        frame = inspect.currentframe()
        _, _, _, values = inspect.getargvalues(frame)
        value_set = [str(values['args'])]
        if kwargs:
            if values['args']:
                value_set += [str(values['kwargs'])]
            else:
                value_set = [str(values['kwargs'])]
        self.init_statement = '-'.join(value_set)
        pass
