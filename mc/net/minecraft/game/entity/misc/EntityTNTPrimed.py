from mc.net.minecraft.game.entity.Entity import Entity

import random
import math

class EntityTNTPrimed(Entity):

    def __init__(self, world, x, y, z):
        super().__init__(world)
        self.setSize(0.98, 0.98)
        self.yOffset = self.bbHeight / 2.0
        self.setPosition(x, y, z)
        r = random.random() * math.pi * 2.0
        self.__motionX1 = -math.sin(r * math.pi / 180.0) * 0.02
        self.__motionY1 = 0.2
        self.__motionZ1 = -math.cos(r * math.pi / 180.0) * 0.02
        self._makeStepSound = False
        self.fuse = 40
        self.prevPosX = x
        self.prevPosY = y
        self.prevPosZ = z

    def canBeCollidedWith(self):
        return not self.isDead

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.__motionY1 -= 0.04
        self.moveEntity(self.__motionX1, self.__motionY1, self.__motionZ1)
        self.__motionX1 *= 0.98
        self.__motionY1 *= 0.98
        self.__motionZ1 *= 0.98
        if self.onGround:
            self.__motionX1 *= 0.7
            self.__motionZ1 *= 0.7
            self.__motionY1 *= -0.5

        if self.fuse <= 0:
            self._worldObj.playSoundEffect(
                self, 'random.explode', 2.0,
                1.0 + (self._rand.random() - self._rand.random()) * 0.2
            )
            self.setEntityDead()
            self._worldObj.createExplosion(
                None, self.posX, self.posY, self.posZ, 4.0
            )

        self.fuse -= 1
