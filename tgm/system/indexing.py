from tgm.system import auto_call, Tag
from weakref import ref
from collections import defaultdict

NoValue = object()


def _update_index(inst, mappings):
    print("update> ", inst, mappings)

#######
# Index is stored on the class dangit!
#######


# class Index(object):
#     """A wrapper for class attributes indicating that they should be indexed.
#
#     Indexed attributes can be searched for more efficiently but incur a slight
#     performance hit when having their value changed."""
#     def __init__(self, value=NoValue):
#         if value is not NoValue:
#             self.values = defaultdict(lambda: value)
#         else:
#             self.values = {}
#         self.compound_indexes = set()
#         auto_call[self] = self._auto_call
#
#     def __get__(self, inst, owner):
#         return self.get_value(inst)
#
#     def __set__(self, inst, value):
#         self.set_value(inst, value)
#
#     def _auto_call(self, inst, cls, attr):
#         self.attr = attr
#         self.update(inst)
#
#     def get_value(self, inst):
#         return self.values[inst]
#
#     def set_value(self, inst, value):
#         self.values[inst] = value
#         self.update(inst)
#
#     def update(self, inst):
#         try:
#             value = self.values[inst]
#         except KeyError:
#             pass
#         else:
#             _update_index(inst, self.attr, value)
#             for compound in self.compound_indexes:
#                 compound.init_index(inst, self.attr)
#
#
#
# class CompoundIndex(object):
#     """A wrapper for groups of Index objects to create combined indexes.
#
#     Each index object included will retain its own index. This object
#     can be accessed as a tuple of the fields it's indexing. This object can
#     be used to create create a 'pos' field from an 'x' and 'y' field for
#     example, so that pos can be searched for efficiently."""
#     def __init__(self, *indexes):
#         self.indexes = []
#         self.attributes = set()
#         for index in indexes:
#             index.compound_indexes.add(self)
#             self.indexes.append(ref(index))
#
#     def __get__(self, inst, owner):
#         return self.get_value(inst)
#
#     def __set__(self, inst, value):
#         self.set_value(inst, value)
#
#     def init_index(self, inst, attr):
#         if attr not in self.attributes:
#             self.attributes.add(attr)
#             self.inst = inst
#             if len(self.indexes) == len(self.attributes):
#                 self.attributes = frozenset(self.attributes)
#                 self.update(inst)
#
#     def get_value(self, inst):
#         return tuple(index().get_value(inst) for index in self.indexes)
#
#     def set_value(self, inst, value):
#         for val, index in zip(value, self.indexes):
#             index().set_value(val)
#         self.update(inst)
#
#     def update(self, inst):
#         if len(self.indexes) == len(self.attributes):
#             _update_index(inst, self.attributes, self.get_value(inst))
#
#
# class DummyIndex(Index):
#     def update(self):
#         pass


class Index(object):
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
        try:
            value = self.values[inst]
        except KeyError:
            return

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
    def __init__(self, value=NoValue):
        super().__init__(value)
        self.index_sets.clear()


def compound_index(*indexes):
    index_set = frozenset(indexes)
    for index in indexes:
        index.index_sets.add(index_set)


class EventTag(Tag):
    namespace = DummyIndex()
    event = DummyIndex()

    compound_index(namespace, event)

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
