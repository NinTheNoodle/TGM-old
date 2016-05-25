"""Index attributes to speed up queries."""
from tgm.sys import auto_call, Tag
from collections import defaultdict

NoValue = object()


def _update_index(inst, mappings):
    print("Index update: ", inst, mappings)


class Index(object):
    """A wrapper for a class attribute indicating that it should be indexed.

    Unlike DummyIndex, this class will automatically index the attribute by
    itself. Indexed attributes can be searched for more efficiently but incur
    a slight performance hit when having their value changed."""
    def __init__(self, value=NoValue):
        if value is NoValue:
            self.values = {}
        else:
            self.values = defaultdict(lambda: value)
        self.attributes = {}
        self.index_sets = {frozenset((self,))}
        auto_call[self] = self._auto_call

    def __get__(self, inst, owner):
        try:
            return self.values[inst]
        except KeyError:
            raise AttributeError(
                "object '{}' has no value assigned for '{}'".format(
                    inst, self.attributes[inst]
                )) from None

    def __set__(self, inst, value):
        self.values[inst] = value
        self.update(inst)

    def _auto_call(self, inst, cls, attr):
        self.attributes[inst] = attr
        self.update(inst)

    def update(self, inst):
        """Update all the indexes this attribute maps to.

        Called automatically when the attribute changes value."""
        for index_set in self.index_sets:
            try:
                mappings = {
                    x.attributes[inst]: x.values[inst]
                    for x in index_set
                }
            except KeyError:
                pass
            else:
                _update_index(inst, mappings)


class DummyIndex(Index):
    """A wrapper for a class attribute allowing for its use in compound indexes.

    Unlike Index, this class will not automatically index the attribute by
    itself. This is useful if a combination of attributes should be indexed
    without the individual attributes being indexed. The attributes for example
    may not be very useful when considered separately."""
    def __init__(self, value=NoValue):
        super().__init__(value)
        self.index_sets.clear()


def compound_index(*indexes):
    """Create a compound index from all the provided indexes.

    This will make queries containing every provided attribute faster
    for a small performance hit when changing any of the attributes' values."""
    index_set = frozenset(indexes)
    for index in indexes:
        index.index_sets.add(index_set)


class EventTag(Tag):
    """A tag indicating the presence of an event on an object.

    Typically created and attached behind the scenes by the event system.
    Can be created for queries by attribute accessing an event namespace.
    Example: Typing sys_event.update will create an instance of this class."""
    namespace = DummyIndex()
    event = DummyIndex()

    compound_index(namespace, event)

    def __init__(self, parent, namespace, event):
        self.namespace = namespace
        self.event = event


class EventNamespace(object):
    """A namespace holding a fixed list of valid event names for that namespace.

    Groups have no special meaning other than to improve readability. All groups
    are combined when the class is created, and as such two groups cannot
    contain an event with the same name. The first argument sets the prefix
    that must be applied to the names of functions decorated with this
    namespace."""
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
        return EventTag["namespace": self, "event": item]

    def __call__(self, func):
        auto_call[func] = self._auto_call
        return func

    def _auto_call(self, inst, cls, attr):
        EventTag(inst, self, attr)
