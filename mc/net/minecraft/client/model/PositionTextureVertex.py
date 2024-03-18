from mc.net.minecraft.game.physics.Vec3D import Vec3D

class PositionTextureVertex:

    @staticmethod
    def fromPos(x, y, z, u, v):
        return PositionTextureVertex(x=x, y=y, z=z, u=u, v=v)

    def __init__(self, vertex=None, pos=None, x=0.0, y=0.0, z=0.0, u=0.0, v=0.0):
        if vertex:
            self.vec3D = vertex.vec3D
        elif pos:
            self.vec3D = pos
        else:
            self.vec3D = Vec3D(x, y, z)

    def setTexturePosition(self, u, v):
        return PositionTextureVertex(vertex=self)
