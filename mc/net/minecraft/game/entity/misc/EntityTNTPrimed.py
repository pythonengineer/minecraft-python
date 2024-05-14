from mc.net.minecraft.game.entity.Entity import Entity
from mc.JavaUtils import random

from nbtlib.tag import Byte

import math

class EntityTNTPrimed(Entity):

    def __init__(self, world, x, y, z):
        super().__init__(world)
        self.preventEntitySpawning = True
        self.setSize(0.98, 0.98)
        self.yOffset = self.height / 2.0
        self.setPosition(x, y, z)
        r = random() * math.pi * 2.0
        self.motionX = -math.sin(r * math.pi / 180.0) * 0.02
        self.motionY = 0.2
        self.motionZ = -math.cos(r * math.pi / 180.0) * 0.02
        self._canTriggerWalking = False
        self.fuse = 80
        self.prevPosX = x
        self.prevPosY = y
        self.prevPosZ = z

    def canBeCollidedWith(self):
        return not self.isDead

    def onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.motionY -= 0.04
        self.moveEntity(self.motionX, self.motionY, self.motionZ)
        self.motionX *= 0.98
        self.motionY *= 0.98
        self.motionZ *= 0.98
        if self.onGround:
            self.motionX *= 0.7
            self.motionZ *= 0.7
            self.motionY *= -0.5

        if self.fuse <= 0:
            self._worldObj.playSoundAtEntity(
                self, 'random.explode', 4.0,
                (1.0 + (self._rand.nextFloat() - self._rand.nextFloat()) * 0.2) * 0.7
            )
            self.setEntityDead()
            self._worldObj.createExplosion(
                None, self.posX, self.posY, self.posZ, 4.0
            )
        else:
            self._worldObj.spawnParticle(
                'smoke', self.posX, self.posY + 0.5, self.posZ, 0.0, 0.0, 0.0
            )

        self.fuse -= 1

    def _writeEntityToNBT(self, compound):
        compound['Fuse'] = Byte(self.fuse)

    def _readEntityFromNBT(self, compound):
        self.fuse = compound['Fuse'].real

    def _getEntityString(self):
        return 'PrimedTnt'

    def getShadowSize(self):
        return 0.0
