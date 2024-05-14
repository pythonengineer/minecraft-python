from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.JavaUtils import random

class EntityFlameFX(EntityFX):

    def __init__(self, world, x, y, z):
        super().__init__(world, x, y, z, 0.0, 0.0, 0.0)
        self._motionX1 *= 0.01
        self._motionY1 *= 0.01
        self._motionZ1 *= 0.01
        self._rand.nextFloat()
        self._rand.nextFloat()
        self._rand.nextFloat()
        self._rand.nextFloat()
        self._rand.nextFloat()
        self._rand.nextFloat()
        self.__flameScale = self._particleScale
        self._particleRed = self._particleGreen = self._particleBlue = 1.0
        self._particleMaxAge = int(8.0 / (random() * 0.8 + 0.2)) + 4
        self.noClip = True
        self._particleTextureIndex = 48

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        age = (self._particleAge + a) / self._particleMaxAge
        self._particleScale = self.__flameScale * (1.0 - age * age * 0.5)
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def getBrightness(self, a):
        age = min(max((self._particleAge + a) / self._particleMaxAge, 0.0), 1.0)
        return super().getBrightness(a) * age + (1.0 - age)

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self._particleAge += 1
        if self._particleAge - 1 >= self._particleMaxAge:
            self.setEntityDead()

        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.96
        self._motionY1 *= 0.96
        self._motionZ1 *= 0.96
        if self.onGround:
            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7
