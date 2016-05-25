"""Tests for tgm.system.base"""
from unittest import TestCase
from tgm.sys import Node
from weakref import ref
import gc


class TestBaseObject(TestCase):
    def test_no_parent(self):
        """Test that game objects with no parent return None for their parent.
        """
        obj = Node(None)
        self.assertIs(obj.parent(), None)

    def test_parent(self):
        """Test if objects have the correct parent set upon instantiation."""
        parent = Node(None)
        child = Node(parent)
        self.assertIs(child.parent(), parent)

    def test_parent_changed(self):
        """Test if objects have the correct parent set after having it changed.
        """
        old_parent = Node(None)
        new_parent = Node(None)
        child = Node(old_parent)
        child.set_parent(new_parent)
        self.assertIs(child.parent(), new_parent)

    def test_deletion(self):
        """Test if objects are deleted from memory when destroyed."""
        parent = Node(None)
        child = ref(Node(parent))
        child().destroy()
        gc.collect()
        self.assertIsNone(child())

    def test_child_deletion(self):
        """Test that the children of objects are deleted when they are destroyed.
        """
        parent = Node(None)
        child = ref(Node(parent))
        parent.destroy()
        gc.collect()
        self.assertIsNone(child())

    def test_no_reference_deletion(self):
        """Test that objects are deleted when there is no reference to them."""
        parent = Node(None)
        weak_parent = ref(parent)
        child = ref(Node(parent))
        del parent
        gc.collect()
        self.assertIsNone(weak_parent())
        self.assertIsNone(child())

    def test_strong_ref(self):
        """Test that objects are kept alive by their parents."""
        parent = Node(None)
        child = ref(Node(parent))
        gc.collect()
        self.assertIsNotNone(child())

    def test_parent_has_child(self):
        """Test that objects are in their parent's children set."""
        parent = Node(None)
        child = Node(parent)
        self.assertIn(child, parent.children(Node))
