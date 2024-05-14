from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.JavaUtils import random

class EntityLavaFX(EntityFX):

    def __init__(self, world, x, y, z):
        super().__init__(world, x, y, z, 0.0, 0.0, 0.0)
        self._motionX1 *= 0.8
        self._motionY1 *= 0.8
        self._motionZ1 *= 0.8
        self._motionY1 = self._rand.nextFloat() * 0.4 + 0.05
        self._particleRed = self._particleGreen = self._particleBlue = 1.0
        self._particleScale *= self._rand.nextFloat() * 2.0 + 0.2
        self.__lavaScale = self._particleScale
        self._particleMaxAge = int(16.0 / (random() * 0.8 + 0.2))
        self.noClip = False
        self._particleTextureIndex = 49

    def getBrightness(self, a):
        return 1.0

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        age = (self._particleAge + a) / self._particleMaxAge
        self._particleScale = self.__lavaScale * (1.0 - age * age)
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self._particleAge += 1
        if self._particleAge - 1 >= self._particleMaxAge:
            self.setEntityDead()

        age = self._particleAge / self._particleMaxAge
        if self._rand.nextFloat() > age:
            self._worldObj.spawnParticle(
                'smoke', self.posX, self.posY, self.posZ,
                self._motionX1, self._motionY1, self._motionZ1
            )

        self._motionY1 -= 0.03
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.999
        self._motionY1 *= 0.999
        self._motionZ1 *= 0.999
        if self.onGround:
            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7
