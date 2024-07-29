from mc.net.minecraft.game.physics.Vec3D import Vec3D

class PositionTextureVertex:

    @staticmethod
    def fromPos(x, y, z, u, v):
        return PositionTextureVertex(None, x, y, z, u, v)

    def __init__(self, obj, x=0.0, y=0.0, z=0.0, u=0.0, v=0.0):
        if isinstance(obj, Vec3D):
            self.vector3D = obj
        elif isinstance(obj, PositionTextureVertex):
            self.vector3D = obj.vector3D
        else:
            self.vector3D = Vec3D(x, y, z)

        self.texturePositionX = u
        self.texturePositionY = v

    def setTexturePosition(self, u, v):
        return PositionTextureVertex(self, u=u, v=v)
