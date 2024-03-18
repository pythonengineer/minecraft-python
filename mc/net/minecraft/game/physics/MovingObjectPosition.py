from mc.net.minecraft.game.physics.Vec3D import Vec3D

class MovingObjectPosition:

    def __init__(self, x, y=None, z=None, sideHit=None, hitVec=None):
        if y is None:
            entity = x
            self.typeOfHit = 1
            self.entityHit = entity
            self.blockX = 0
            self.blockY = 0
            self.blockZ = 0
            self.sideHit = 0
            self.hitVec = None
        else:
            self.typeOfHit = 0
            self.blockX = x
            self.blockY = y
            self.blockZ = z
            self.sideHit = sideHit
            self.hitVec = Vec3D(hitVec.xCoord, hitVec.yCoord, hitVec.zCoord)
            self.entityHit = None
