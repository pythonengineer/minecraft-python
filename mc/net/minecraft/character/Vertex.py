from mc.net.minecraft.character.Vec3 import Vec3

class Vertex:

    @staticmethod
    def fromPos(x, y, z, u, v):
        return Vertex(x=x, y=y, z=z, u=u, v=v)

    def __init__(self, vertex=None, pos=None, x=0.0, y=0.0, z=0.0, u=0.0, v=0.0):
        if vertex:
            self.pos = vertex.pos
        elif pos:
            self.pos = pos
        else:
            self.pos = Vec3(x, y, z)

        self.u = u
        self.v = v

    def remap(self, u, v):
        return Vertex(vertex=self, u=u, v=v)
