from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.JavaUtils import random

class EntitySmokeFX(EntityFX):

    def __init__(self, world, x, y, z):
        super().__init__(world, x, y, z, 0.0, 0.0, 0.0)
        self._motionX1 *= 0.1
        self._motionY1 *= 0.1
        self._motionZ1 *= 0.1
        self._particleRed = random() * 0.3
        self._particleGreen = self._particleRed
        self._particleBlue = self._particleRed
        self._particleMaxAge = int(8.0 / (random() * 0.8 + 0.2))
        self.noClip = True

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self._particleAge += 1
        if self._particleAge - 1 >= self._particleMaxAge:
            self.setEntityDead()

        self._particleTextureIndex = 7 - (self._particleAge << 3) // self._particleMaxAge
        self._motionY1 = float(self._motionY1 + 0.004)
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.96
        self._motionY1 *= 0.96
        self._motionZ1 *= 0.96
        if self.onGround:
            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7
