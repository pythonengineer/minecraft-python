from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.material.Material import Material
from mc.JavaUtils import random

from nbtlib.tag import Compound, Short, Byte

import math

class EntityItem(Entity):

    def __init__(self, world, x, y, z, item):
        super().__init__(world)
        self.setSize(0.25, 0.25)
        self.yOffset = self.height / 2.0
        self.setPosition(x, y, z)
        self.item = item
        self.rotationYaw = random() * 360.0
        self.motionX = random() * 0.2 - 0.1
        self.motionY = 0.2
        self.motionZ = random() * 0.2 - 0.1
        self._canTriggerWalking = False
        self.__unknownEntityItemInt = 0
        self.age = 0
        self.delayBeforeCanPickup = 0
        self.__health = 5
        self.hoverStart = random() * math.pi * 2.0

    def onEntityUpdate(self):
        super().onEntityUpdate()
        if self.delayBeforeCanPickup > 0:
            self.delayBeforeCanPickup -= 1

        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.motionY -= 0.04
        if self._worldObj.getBlockMaterial(int(self.posX), int(self.posY),
                                           int(self.posZ)) == Material.lava:
            self.motionY = 0.2
            self.motionX = (self._rand.nextFloat() - self._rand.nextFloat()) * 0.2
            self.motionZ = (self._rand.nextFloat() - self._rand.nextFloat()) * 0.2
            self._worldObj.playSoundAtEntity(self, 'random.fizz', 0.4,
                                             2.0 + self._rand.nextFloat() * 0.4)

        zShift = self.posZ
        yShift = self.posY
        xShift = self.posX
        x = int(xShift)
        y = int(yShift)
        z = int(zShift)
        xShift -= x
        yShift -= y
        zShift -= z
        if blocks.opaqueCubeLookup[self._worldObj.getBlockId(x, y, z)]:
            minXOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x - 1, y, z)]
            maxXOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x + 1, y, z)]
            minYOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x, y - 1, z)]
            maxYOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x, y + 1, z)]
            minZOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x, y, z - 1)]
            maxZOpacity = not blocks.opaqueCubeLookup[self._worldObj.getBlockId(x, y, z + 1)]
            side = -1
            axis = 9999.0
            if minXOpacity and xShift < 9999.0:
                axis = xShift
                side = 0
            if maxXOpacity and 1.0 - xShift < axis:
                axis = 1.0 - xShift
                side = 1
            if minYOpacity and yShift < axis:
                axis = yShift
                side = 2
            if maxYOpacity and 1.0 - yShift < axis:
                axis = 1.0 - yShift
                side = 3
            if minZOpacity and zShift < axis:
                axis = zShift
                side = 4
            if maxZOpacity and 1.0 - zShift < axis:
                side = 5

            motion = self._rand.nextFloat() * 0.2 + 0.1
            if side == 0:
                self.motionX = -motion
            if side == 1:
                self.motionX = motion
            if side == 2:
                self.motionY = -motion
            if side == 3:
                self.motionY = motion
            if side == 4:
                self.motionZ = -motion
            if side == 5:
                self.motionZ = motion

        self.moveEntity(self.motionX, self.motionY, self.motionZ)
        self.motionX *= 0.98
        self.motionY *= 0.98
        self.motionZ *= 0.98
        if self.onGround:
            self.motionX *= 0.7
            self.motionZ *= 0.7
            self.motionY *= -0.5

        self.__unknownEntityItemInt += 1
        self.age += 1
        if self.age >= 6000:
            self.setEntityDead()

    def _dealFireDamage(self, hp):
        if self.item.getItem().onPlaced(self._worldObj, self.posX,
                                        self.posY, self.posZ):
            self.item.stackSize -= 1

        if self.item.stackSize == 0:
            self.setEntityDead()

    def attackEntityFrom(self, entity, damage):
        pass

    def _writeEntityToNBT(self, compound):
        compound['Health'] = Byte(self.__health)
        compound['Age'] = Short(self.age)
        compound['Item'] = self.item.writeToNBT(Compound({}))

    def _readEntityFromNBT(self, compound):
        self.__health = compound['Health'].real & 255
        self.age = compound['Age'].real
        self.item = ItemStack(dict(compound['Item']))

    def _getEntityString(self):
        return 'Item'

    def onCollideWithPlayer(self, player):
        if self.delayBeforeCanPickup == 0 and player.inventory.addItemStackToInventory(self.item):
            self._worldObj.playSoundAtEntity(
                self, 'random.pop', 0.2,
                ((self._rand.nextFloat() - self._rand.nextFloat()) * 0.7 + 1.0) * 2.0
            )
            player.onItemPickup(self)
            self.setEntityDead()
