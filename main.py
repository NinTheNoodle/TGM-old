from tgm.system import Entity, World, Indexed


class Player(Entity):
    x = Indexed(5)

    def __init__(self, parent, hat):
        print(hat, parent, self.ancestor(Entity), self.children(Entity))
        self.ancestor(World)

    def lol(self):
        print(self.children(Entity))

root = Player(None, "root")
c = Player(root, "c")
root.lol()
