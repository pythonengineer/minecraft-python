from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.physics.Vec3D import Vec3D

from nbtlib.tag import Short, Byte

import math

class EntityArrow(Entity):

    def __init__(self, world, entity):
        super().__init__(world)
        self.__owner = entity
        self.__xTile = -1
        self.__yTile = -1
        self.__zTile = -1
        self.__inTile = 0
        self.__inGround = False
        self.arrowShake = 0
        self.setSize(0.5, 0.5)
        self.setPositionAndRotation(entity.posX, entity.posY, entity.posZ,
                                    entity.rotationYaw, entity.rotationPitch)
        self.posX += math.cos(self.rotationYaw / 180.0 * math.pi) * 0.16
        self.posY -= 0.1
        self.posZ += math.sin(self.rotationYaw / 180.0 * math.pi) * 0.16
        self.setPosition(self.posX, self.posY, self.posZ)
        self.yOffset = 0.0
        self.motionX = math.sin(self.rotationYaw / 180.0 * math.pi) * math.cos(self.rotationPitch / 180.0 * math.pi) * 1.5
        self.motionZ = -math.cos(self.rotationYaw / 180.0 * math.pi) * math.cos(self.rotationPitch / 180.0 * math.pi) * 1.5
        self.motionY = -math.sin(self.rotationPitch / 180.0 * math.pi) * 1.5
        self.motionX += self._rand.nextGaussian() * 0.01
        self.motionY += self._rand.nextGaussian() * 0.01
        self.motionZ += self._rand.nextGaussian() * 0.01
        d = math.sqrt(self.motionX * self.motionX + self.motionZ * self.motionZ)
        self.prevRotationYaw = self.rotationYaw = math.atan2(self.motionX, self.motionZ) * 180.0 / math.pi
        self.prevRotationPitch = self.rotationPitch = math.atan2(self.motionY, d) * 180.0 / math.pi

    def onEntityUpdate(self):
        super().onEntityUpdate()
        if self.arrowShake > 0:
            self.arrowShake -= 1

        if self.__inGround:
            blockId = self._worldObj.getBlockId(self.__xTile, self.__yTile, self.__zTile)
            if blockId == self.__inTile:
                return

            self.__inGround = False
            self.motionX *= self._rand.nextFloat() * 0.2
            self.motionY *= self._rand.nextFloat() * 0.2
            self.motionZ *= self._rand.nextFloat() * 0.2

        posVec = Vec3D(self.posX, self.posY, self.posZ)
        motionVec = Vec3D(self.posX + self.motionX, self.posY + self.motionY, self.posZ + self.motionZ)
        hit = self._worldObj.rayTraceBlocks(posVec, motionVec)
        if hit:
            self.__xTile = hit.blockX
            self.__yTile = hit.blockY
            self.__zTile = hit.blockZ
            self.__inTile = self._worldObj.getBlockId(self.__xTile, self.__yTile, self.__zTile)
            self.motionX = hit.hitVec.xCoord - self.posX
            self.motionY = hit.hitVec.yCoord - self.posY
            self.motionZ = hit.hitVec.zCoord - self.posZ
            d = math.sqrt(self.motionX * self.motionX + \
                          self.motionY * self.motionY + \
                          self.motionZ * self.motionZ)
            self.posX -= self.motionX / d * 0.05
            self.posY -= self.motionY / d * 0.05
            self.posZ -= self.motionZ / d * 0.05
            self._worldObj.playSoundAtEntity(
                self, 'random.drr', 1.0, 1.2 / (self._rand.nextFloat() * 0.2 + 0.9)
            )
            self.__inGround = True
            self.arrowShake = 7

        self.posX += self.motionX
        self.posY += self.motionY
        self.posZ += self.motionZ
        d = math.sqrt(self.motionX * self.motionX + self.motionZ * self.motionZ)
        self.rotationYaw = math.atan2(self.motionX, self.motionZ) * 180.0 / math.pi
        self.rotationPitch = math.atan2(self.motionY, d) * 180.0 / (math.pi)
        while self.rotationPitch < -180.0:
            self.rotationPitch -= -360.0

        while self.rotationPitch - self.prevRotationPitch >= 180.0:
            self.prevRotationPitch += 360.0

        while self.rotationYaw - self.prevRotationYaw < -180.0:
            self.prevRotationYaw -= 360.0

        while self.rotationYaw - self.prevRotationYaw >= 180.0:
            self.prevRotationYaw += 360.0

        self.rotationPitch = self.prevRotationPitch + (self.rotationPitch - self.prevRotationPitch) * 0.2
        self.rotationYaw = self.prevRotationYaw + (self.rotationYaw - self.prevRotationYaw) * 0.2
        motion = 0.99
        if self.handleWaterMovement():
            for i in range(4):
                self._worldObj.spawnParticle(
                    'bubble', self.posX - self.motionX * 0.25,
                    self.posY - self.motionY * 0.25,
                    self.posZ - self.motionZ * 0.25,
                    self.motionX, self.motionY, self.motionZ
                )

            motion = 0.85

        self.motionX *= motion
        self.motionY *= motion
        self.motionZ *= motion
        self.motionY -= 0.03
        self.setPosition(self.posX, self.posY, self.posZ)

    def _writeEntityToNBT(self, compound):
        compound['xTile'] = Short(self.__xTile)
        compound['yTile'] = Short(self.__yTile)
        compound['zTile'] = Short(self.__zTile)
        compound['inTile'] = Byte(self.__inTile)
        compound['shake'] = Byte(self.arrowShake)
        compound['inGround'] = Byte(1 if self.__inGround else 0)

    def _readEntityFromNBT(self, compound):
        self.__xTile = compound['xTile'].real
        self.__yTile = compound['yTile'].real
        self.__zTile = compound['zTile'].real
        self.__inTile = compound['inTile'].real & 255
        self.arrowShake = compound['shake'].real & 255
        self.__inGround = compound['inGround'].real == 1

    def _getEntityString(self):
        return 'Arrow'

    def onCollideWithPlayer(self, player):
        from mc.net.minecraft.game.item.Items import items
        if self.__inGround and self.__owner == player and self.arrowShake <= 0 and \
           player.inventory.storePartialItemStack(ItemStack(items.arrow.shiftedIndex, 1)):
            self.setEntityDead()

    def getShadowSize(self):
        return 0.0
