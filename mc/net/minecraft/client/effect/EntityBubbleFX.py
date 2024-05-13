from mc.net.minecraft.client.effect.EntityFX import EntityFX
from mc.net.minecraft.game.level.material.Material import Material
from mc.JavaUtils import random

class EntityBubbleFX(EntityFX):

    def __init__(self, world, x, y, z, xr, yr, zr):
        super().__init__(world, x, y, z, xr, yr, zr)
        self._particleRed = 1.0
        self._particleGreen = 1.0
        self._particleBlue = 1.0
        self._particleTextureIndex = 32
        self.setSize(0.02, 0.02)
        self._motionX1 = xr * 0.2 + (random() * 2.0 - 1.0) * 0.02
        self._motionY1 = yr * 0.2 + (random() * 2.0 - 1.0) * 0.02
        self._motionZ1 = zr * 0.2 + (random() * 2.0 - 1.0) * 0.02
        self._particleMaxAge = int(8.0 / (random() * 0.8 + 0.2))

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self._motionY1 += 0.002
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.85
        self._motionY1 *= 0.85
        self._motionZ1 *= 0.85
        if self._worldObj.getBlockMaterial(int(self.posX), int(self.posY),
                                           int(self.posZ)) != Material.water:
            self.setEntityDead()

        self._particleMaxAge -= 1
        if self._particleMaxAge + 1 <= 0:
            self.setEntityDead()
