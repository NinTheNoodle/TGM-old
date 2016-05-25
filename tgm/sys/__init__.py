"""The object tree, querying and any other core systems of TGM."""
from .query import Query
from .selection import (
    select_ancestor, select_descendants, select_children, test_query
)
from .base import Node, auto_call
from .parents import Component, Entity, World, Tag
from .indexing import Index, DummyIndex, compound_index, EventNamespace
from .events import sys_event
