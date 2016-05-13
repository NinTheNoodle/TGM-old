from tgm.system import auto_call


class Indexed(object):
    """A wrapper for class attributes indicating that they should be indexed.

    Indexed attributes can be searched for more efficiently but incur a slight
    performance hit when having their value changed."""
    def __init__(self, value):
        self.value = value
        print("create> ", value)
        auto_call[self] = lambda inst, cls, attr: self.update(inst)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        self.value = value
        self.update(instance)

    def update(self, instance):
        print("update> ", instance)
