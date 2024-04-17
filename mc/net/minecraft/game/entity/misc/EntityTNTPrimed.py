from mc.net.minecraft.game.entity.Entity import Entity

import random
import math

class EntityTNTPrimed(Entity):

    def __init__(self, world, x, y, z):
        super().__init__(world)
        self.setSize(0.98, 0.98)
        self.yOffset = self.height / 2.0
        self.setPosition(x, y, z)
        r = random.random() * math.pi * 2.0
        self.__tntMotionX1 = -math.sin(r * math.pi / 180.0) * 0.02
        self.__tntMotionY1 = 0.2
        self.__tntMotionZ1 = -math.cos(r * math.pi / 180.0) * 0.02
        self._canTriggerWalking = False
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
        self.__tntMotionY1 -= 0.04
        self.moveEntity(self.__tntMotionX1, self.__tntMotionY1, self.__tntMotionZ1)
        self.__tntMotionX1 *= 0.98
        self.__tntMotionY1 *= 0.98
        self.__tntMotionZ1 *= 0.98
        if self.onGround:
            self.__tntMotionX1 *= 0.7
            self.__tntMotionZ1 *= 0.7
            self.__tntMotionY1 *= -0.5

        if self.fuse <= 0:
            self._worldObj.playSoundAtEntity(
                self, 'random.explode', 4.0,
                (1.0 + (self._rand.random() - self._rand.random()) * 0.2) * 0.7
            )
            self.setEntityDead()
            self._worldObj.createExplosion(
                None, self.posX, self.posY, self.posZ, 4.0
            )

        self.fuse -= 1
