from mc.net.minecraft.game.entity.Entity import Entity

import random

class EntityItem(Entity):

    def __init__(self, world, x, y, z, item):
        super().__init__(world)
        self.setSize(0.25, 0.25)
        self.yOffset = self.height / 2.0
        self.setPosition(x, y, z)
        self.item = item
        random.random()
        self.itemMotionX1 = random.random() * 0.2 - 0.1
        self.itemMotionY1 = 0.2
        self.itemMotionZ1 = random.random() * 0.2 - 0.1
        self._canTriggerWalking = False
        self.__unknownEntityItemInt = 0
        self.__age = 0
        self.delayBeforeCanPickup = 0

    def onEntityUpdate(self):
        if self.delayBeforeCanPickup > 0:
            self.delayBeforeCanPickup -= 1

        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.itemMotionY1 -= 0.04
        self.moveEntity(self.itemMotionX1, self.itemMotionY1, self.itemMotionZ1)
        self.itemMotionX1 *= 0.98
        self.itemMotionY1 *= 0.98
        self.itemMotionZ1 *= 0.98
        if self.onGround:
            self.itemMotionX1 *= 0.7
            self.itemMotionZ1 *= 0.7
            self.itemMotionY1 *= -0.5

        self.__unknownEntityItemInt += 1
        self.__age += 1
        if self.__age >= 6000:
            self.setEntityDead()
