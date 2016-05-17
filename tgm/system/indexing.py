from tgm.system import auto_call, Tag
from weakref import ref

NoValue = object()


def _update_index(inst, attr, value):
    print("update> ", inst, attr, value)

#######
# Index is stored on the class dangit!
#######

class Index(object):
    """A wrapper for class attributes indicating that they should be indexed.

    Indexed attributes can be searched for more efficiently but incur a slight
    performance hit when having their value changed."""
    def __init__(self, value=NoValue):
        if value is not NoValue:
            self.value = value
        self.compound_indexes = set()
        auto_call[self] = self._auto_call

    def __get__(self, inst, owner):
        return self.get_value()

    def __set__(self, inst, value):
        self.set_value(value)

    def _auto_call(self, inst, cls, attr):
        self.attr = attr
        self.inst = inst
        if hasattr(self, "value"):
            self.update()
            for compound in self.compound_indexes:
                compound.init_index(inst, attr)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.update()

    def update(self):
        _update_index(self.inst, self.attr, self.value)



class CompoundIndex(object):
    """A wrapper for groups of Index objects to create combined indexes.

    Each index object included will retain its own index. This object
    can be accessed as a tuple of the fields it's indexing. This object can
    be used to create create a 'pos' field from an 'x' and 'y' field for
    example, so that pos can be searched for efficiently."""
    def __init__(self, *indexes):
        self.indexes = []
        self.attributes = set()
        for index in indexes:
            index.compound_indexes.add(self)
            self.indexes.append(ref(index))

    def __get__(self, instance, owner):
        return self.get_value()

    def __set__(self, instance, value):
        self.set_value(value)

    def init_index(self, inst, attr):
        if attr not in self.attributes:
            self.attributes.add(attr)
            self.inst = inst
            if len(self.indexes) == len(self.attributes):
                self.attributes = frozenset(self.attributes)
                self.update()
        else:
            print("???", inst, attr)

    def get_value(self):
        return tuple(index().get_value() for index in self.indexes)

    def set_value(self, value):
        for val, index in zip(value, self.indexes):
            index().set_value(val)
        self.update()

    def update(self):
        _update_index(self.inst, self.attributes, self.get_value())


class DummyIndex(Index):
    def update(self):
        pass


class EventTag(Tag):
    namespace = DummyIndex()
    event = DummyIndex()

    CompoundIndex(namespace, event)

    def __init__(self, parent, namespace, event):
        self.data = (namespace, event)


class EventNamespace(object):
    """A namespace holding a fixed list of valid event names for that namespace.
    """
    def __init__(self, namespace, **groups):
        """Initialise the event group."""
        events = set()
        for group in groups.values():
            for event in group:
                if event in events:
                    raise ValueError("event '{}' listed more than once".format(
                        event
                    ))
                events.add(event)
        self._events = frozenset(events)
        self._namespace = namespace + "_"

    def __getattr__(self, item):
        return EventTag["data": (self, item)]

    def __call__(self, func):
        auto_call[func] = self._auto_call
        return func

    def _auto_call(self, inst, cls, attr):
        EventTag(inst, self, attr)
