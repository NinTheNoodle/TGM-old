"""Tests for tgm.system.base"""
from unittest import TestCase
from tgm.system import BaseObject
from weakref import ref
import gc


class TestBaseObject(TestCase):
    def test_no_parent(self):
        """Test that game objects with no parent return None for their parent.
        """
        obj = BaseObject(None)
        self.assertIs(obj.parent(), None)

    def test_parent(self):
        """Test if objects have the correct parent set upon instantiation."""
        parent = BaseObject(None)
        child = BaseObject(parent)
        self.assertIs(child.parent(), parent)

    def test_parent_changed(self):
        """Test if objects have the correct parent set after having it changed.
        """
        old_parent = BaseObject(None)
        new_parent = BaseObject(None)
        child = BaseObject(old_parent)
        child.set_parent(new_parent)
        self.assertIs(child.parent(), new_parent)

    def test_deletion(self):
        """Test if objects are deleted from memory when destroyed."""
        parent = BaseObject(None)
        child = ref(BaseObject(parent))
        child().destroy()
        gc.collect()
        self.assertIsNone(child())

    def test_child_deletion(self):
        """Test that the children of objects are deleted when they are destroyed.
        """
        parent = BaseObject(None)
        child = ref(BaseObject(parent))
        parent.destroy()
        gc.collect()
        self.assertIsNone(child())

    def test_no_reference_deletion(self):
        """Test that objects are deleted when there is no reference to them."""
        parent = BaseObject(None)
        weak_parent = ref(parent)
        child = ref(BaseObject(parent))
        del parent
        gc.collect()
        self.assertIsNone(weak_parent())
        self.assertIsNone(child())

    def test_strong_ref(self):
        """Test that objects are kept alive by their parents."""
        parent = BaseObject(None)
        child = ref(BaseObject(parent))
        gc.collect()
        self.assertIsNotNone(child())

    def test_parent_has_child(self):
        """Test that objects are in their parent's children set."""
        parent = BaseObject(None)
        child = BaseObject(parent)
        self.assertIn(child, parent.children(BaseObject))
