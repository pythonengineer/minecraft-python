from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.JavaUtils import random

class EntityRainFX(EntityFX):

    def __init__(self, world, x, y, z):
        super().__init__(world, x, y, z, 0.0, 0.0, 0.0)
        self._motionX1 *= 0.3
        self._motionY1 = random() * 0.2 + 0.1
        self._motionZ1 *= 0.3
        self._particleRed = 1.0
        self._particleGreen = 1.0
        self._particleBlue = 1.0
        self._particleTextureIndex = 16
        self.setSize(0.01, 0.01)
        self._particleGravity = 0.06
        self._particleMaxAge = int(8.0 / (random() * 0.8 + 0.2))

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self._motionY1 -= self._particleGravity
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.98
        self._motionY1 *= 0.98
        self._motionZ1 *= 0.98
        self._particleMaxAge -= 1
        if self._particleMaxAge + 1 <= 0:
            self.setEntityDead()

        if self.onGround:
            if random() < 0.5:
                self.setEntityDead()

            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7

        material = self._worldObj.getBlockMaterial(int(self.posX), int(self.posY),
                                                   int(self.posZ))
        if material.getIsLiquid() or material.isSolid():
            self.setEntityDead()
