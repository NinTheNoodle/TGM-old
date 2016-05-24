"""Test stuff for now."""
from tgm.system import (
    Entity, World, compound_index, DummyIndex, sys_event, BaseObject
)


class Player(Entity):
    x = DummyIndex(5)
    y = DummyIndex(7)

    compound_index(x, y)

    def __init__(self, parent, hat):
        print("INIT", hat, parent, self.parent(), self.children(BaseObject))
        self.parent(World)

    @sys_event
    def sys_update(self):
        print("UPDATE", self.children(BaseObject))

root = Player(None, "root")
c = Player(root, "c")
root.sys_update()
c.x = 6
c.y = 0
c.x = 2
print(c.x, c.y)
