from tgm.system import Entity, World, Index, CompoundIndex, sys_event


class Player(Entity):
    x = Index(0)
    y = Index(0)

    pos = CompoundIndex(x, y)

    def __init__(self, parent, hat):
        print(hat, parent, self.ancestor(Entity), self.children(Entity))
        self.ancestor(World)

    @sys_event
    def sys_update(self):
        print(self.children(Entity))

root = Player(None, "root")
c = Player(root, "c")
root.sys_update()
c.pos = (1, 2)
c.x = 6
print(c.x, c.y, c.pos)
