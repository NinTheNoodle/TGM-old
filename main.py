"""Test stuff for now."""
from tgm.sys import (
    Entity, World, compound_index, DummyIndex, sys_event, Node
)


class Player(Entity):
    x = DummyIndex(5)
    y = DummyIndex(7)

    compound_index(x, y)

    def __init__(self, hat):
        print("INIT", hat, self.parent(), self.children(Node))
        self.parent(World)

    @sys_event
    def sys_update(self):
        print("UPDATE", self.children(Node))

root = Player("root")
c = root.attach(Player("c"))
root.sys_update()
c.x = 6
c.y = 0
c.x = 2
print(c.x, c.y)
