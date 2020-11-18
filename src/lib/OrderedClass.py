from collections import OrderedDict

class OrderedClass(object):
    def __init__(self, *args, **kwargs):  
        self._attrs = OrderedDict(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(OrderedClass, self).__setattr__(name, value)
        self._attrs[name] = value
