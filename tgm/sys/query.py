"""Search the object tree for objects fulfilling arbitrary criteria."""


class Query(object):
    """An object representing a query to be performed.

    This object is not the result of a query. This is the object created
    to represent the structure of a query."""

    def __init__(self, operation, *arguments):
        self.operation = operation
        self.args = arguments

    def get_optimizable(self, world):
        """Get the operations that can be sped up using set operations."""
        pass

    def get_unoptimizable(self):
        """Get the operations that should tested on the objects one by one."""
        pass
