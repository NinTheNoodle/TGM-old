"""The core objects of the system."""
from weakref import ref
from tgm.sys import select_descendants
from tgm.sys.util import AttrDict, call_auto_callable

auto_call = {}


class NodeMetaClass(type):
    """Required to make indexing classes possible for queries."""

    def __getitem__(self, item):
        """Parse the query string and return a Query object."""
        pass


class Node(object, metaclass=NodeMetaClass):
    """The base object for all game objects and components."""

    def __new__(cls, *args, **kwargs):
        """Setup the TGM related structures of the object."""
        obj = super().__new__(cls)
        obj._tgm = AttrDict(
            children=set(),
            parent=lambda: None,
            indexes={}
        )
        call_auto_callable(auto_call, obj, cls)
        return obj

    def children(self, query):
        """Get all the immediate children of this object that fulfil the query.
        """
        if query is Node:
            return self._tgm.children.copy()
        return None

    def find(self, query):
        """Get all the descendants of this object that fulfil the query."""
        return select_descendants(self, query)

    def parent(self, query=None):
        """Return the closest of the object's parents that satisfies the query.

        If no query is given then the object's direct parent will be returned."""
        if query is None or query is Node:
            return self._tgm.parent()
        return None

    def attach(self, node):
        """Add the given node as a child and update relevant indexes.

        This will detach the node from any parent it's currently attached to."""
        if node.parent() is not None:
            node.parent().detach(node)

        node._tgm.parent = ref(self)
        self._tgm.children.add(node)
        for key, node_set in node._tgm.indexes.items():
            if node_set:
                self._tgm.indexes[key].add(node)

        return node

    def detach(self, node):
        """Remove the given node as a child and update relevant indexes."""
        node._tgm.parent = lambda: None
        for node_set in self._tgm.indexes:
            try:
                node_set.remove(node)
            except KeyError:
                pass
        self._tgm.children.remove(node)

    def add_index(self, value):
        self._tgm.indexes[value].add(self)
        try:
            self.parent()._add_child_index(value, self)
        except AttributeError:
            pass

    def _add_child_index(self, value, child):
        self._tgm.indexes[value].add(child)
        try:
            self.parent()._add_child_index(value, self)
        except AttributeError:
            pass