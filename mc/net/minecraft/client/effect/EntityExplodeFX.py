from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.JavaUtils import Random, random

class EntityExplodeFX(EntityFX):

    def __init__(self, world, x, y, z, xr, yr, zr):
        super().__init__(world, x, y, z, xr, yr, zr)
        self._motionX1 = xr + (random() * 2.0 - 1.0) * 0.05
        self._motionY1 = yr + (random() * 2.0 - 1.0) * 0.05
        self._motionZ1 = zr + (random() * 2.0 - 1.0) * 0.05
        self._particleRed = self._rand.nextFloat() * 0.3 + 0.7
        self._particleGreen = self._particleRed
        self._particleBlue = self._particleRed
        self._particleScale = self._rand.nextFloat() * self._rand.nextFloat() * 6.0 + 1.0
        self._particleMaxAge = int(16.0 / (self._rand.nextFloat() * 0.8 + 0.2))

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
        self._motionY1 += 0.004
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.9
        self._motionY1 *= 0.9
        self._motionZ1 *= 0.9
        if self.onGround:
            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7
