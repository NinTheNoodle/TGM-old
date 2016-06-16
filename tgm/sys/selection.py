"""The different ways to select objects when querying the object tree."""


def select_descendants(start, query):
    """Select every descendant of start fulfilling the query."""
    pass


def select_ancestor(start, query):
    """Select the first ancestor of start fulfilling the query."""
    pass


def select_ancestors(start, query):
    """Select every ancestor of start fulfilling the query."""
    pass


def select_children(start, query):
    """Select every direct child of start fulfilling the query."""
    pass


def test_query(obj, query):
    """Test to see if obj fulfills the query."""
    pass
