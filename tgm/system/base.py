from weakref import ref
from tgm.system import select_descendants, select_ancestor
from tgm.system.util import AttrDict, call_auto_callable

auto_call = {}


class MetaObject(type):
    """Required to make indexing classes possible for queries."""

    def __getitem__(self, item):
        """Parse the query string and return a Query object."""
        pass


class BaseObject(object, metaclass=MetaObject):
    """The base object for all game objects and components."""

    def __new__(cls, parent, *args, **kwargs):
        """Setup the TGM related structures of the object."""
        obj = super().__new__(cls)
        obj.__tgm__ = AttrDict(
            children=set(),
            parent=lambda: None
        )
        obj.parent = parent
        call_auto_callable(auto_call, obj, cls)
        return obj

    def ancestor(self, query):
        """Get the closest direct ancestor of this object to fulfil the query.
        """
        return select_ancestor(self, query)

    def ancestors(self, query):
        """Get all the direct ancestors of this object that fulfil the query."""
        return select_ancestor(self, query)

    def children(self, query):
        """Get all the immediate children of this object that fulfil the query.
        """
        if query == BaseObject:
            return self.__tgm__.children.copy()
        return self.__tgm__.children

    def descendants(self, query):
        """Get all the direct descendants of this object that fulfil the query.
        """
        return select_descendants(self, query)

    @property
    def parent(self):
        """Return the object's direct parent."""
        return self.__tgm__.parent()

    @parent.setter
    def parent(self, value):
        """Set the object's parent and update appropriate structures.

        The object's parent is stored as a weak reference since it doesn't
        make sense for a child object to keep its parent alive."""
        if self.parent is not None:
            self.parent.__tgm__.children.remove(self)

        if value is not None:
            self.__tgm__.parent = ref(value)
            value.__tgm__.children.add(self)
        else:
            self.__tgm__.parent = lambda: None
