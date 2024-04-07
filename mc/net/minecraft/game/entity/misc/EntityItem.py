from mc.net.minecraft.game.entity.Entity import Entity

import random

class EntityItem(Entity):

    def __init__(self, world, x, y, z, item):
        super().__init__(world)
        self.setSize(0.25, 0.25)
        self.yOffset = self.bbHeight / 2.0
        self.setPosition(x, y, z)
        self.item = item
        random.random()
        self.motionX1 = random.random() * 0.2 - 0.1
        self.motionY1 = 0.2
        self.motionZ1 = random.random() * 0.2 - 0.1
        self._makeStepSound = False
        self.__unknownEntityItemInt = 0
        self.__age = 0
        self.delayBeforeCanPickup = 0

    def onEntityUpdate(self):
        if self.delayBeforeCanPickup > 0:
            self.delayBeforeCanPickup -= 1

        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.motionY1 -= 0.04
        self.moveEntity(self.motionX1, self.motionY1, self.motionZ1)
        self.motionX1 *= 0.98
        self.motionY1 *= 0.98
        self.motionZ1 *= 0.98
        if self.onGround:
            self.motionX1 *= 0.7
            self.motionZ1 *= 0.7
            self.motionY1 *= -0.5

        self.__unknownEntityItemInt += 1
        self.__age += 1
        if self.__age >= 6000:
            self.setEntityDead()
