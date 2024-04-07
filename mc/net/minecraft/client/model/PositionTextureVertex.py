from mc.net.minecraft.game.physics.Vec3D import Vec3D

class PositionTextureVertex:

    @staticmethod
    def fromPos(x, y, z, u, v):
        return PositionTextureVertex(None, x, y, z=z, u=u, v=v)

    def __init__(self, obj, x, y, z=0.0, u=0.0, v=0.0):
        if isinstance(obj, Vec3D):
            self.vec3D = obj
        elif isinstance(obj, PositionTextureVertex):
            self.vec3D = obj.vec3D
        else:
            self.vec3D = Vec3D(x, y, z)

    def setTexturePosition(self, u, v):
        return PositionTextureVertex(self, u, v)
