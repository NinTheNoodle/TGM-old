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

    def __new__(cls, parent, *args, **kwargs):
        """Setup the TGM related structures of the object."""
        obj = super().__new__(cls)
        obj._tgm = AttrDict(
            children=set(),
            parent=lambda: None
        )
        obj.set_parent(parent)
        call_auto_callable(auto_call, obj, cls)
        return obj

    def destroy(self):
        """Delete the object and all its children."""
        pass

    def children(self, query):
        """Get all the immediate children of this object that fulfil the query.
        """
        if query is Node:
            return self._tgm.children.copy()
        return None

    def select(self, query):
        """Get all the descendants of this object that fulfil the query."""
        return select_descendants(self, query)

    def parent(self, query=None):
        """Return the closest of the object's parents that satisfies the query.

        If no query is given then the object's direct parent will be returned."""
        if query is None or query is Node:
            return self._tgm.parent()
        return None

    def set_parent(self, parent):
        """Set the object's parent and update appropriate structures.

        The object's parent is stored as a weak reference since it doesn't
        make sense for a child object to keep its parent alive."""
        if self.parent() is not None:
            self.parent()._tgm.children.remove(self)

        if parent is not None:
            self._tgm.parent = ref(parent)
            parent._tgm.children.add(self)
        else:
            self._tgm.parent = lambda: None
