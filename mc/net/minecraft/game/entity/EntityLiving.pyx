# cython: language_level=3

cimport cython

from libc.math cimport sin, cos, ceil, sqrt, atan2, pi

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.AILiving cimport AILiving
from pyglet import gl

import random

cdef class EntityLiving(Entity):
    ATTACK_DURATION = 5
    TOTAL_AIR_SUPPLY = 300

    def __init__(self, world):
        super().__init__(world)
        self.heartsHalvesLife = 20
        self.renderYawOffset = 0.0
        self.prevRenderYawOffset = 0.0
        self.__prevRotationYawHead = 0.0
        self.__rotationYawHead = 0.0
        self.__maxAir = 10
        self.health = 20
        self.prevHealth = 0
        self.scoreValue = 0
        self.air = EntityLiving.TOTAL_AIR_SUPPLY
        self.hurtTime = 0
        self.maxHurtTime = 0
        self.attackedAtYaw = 0.0
        self.deathTime = 0
        self.__attackTime = 0
        self.prevCameraPitch = 0.0
        self.cameraPitch = 0.0
        self.entityAI = AILiving()
        self.stepHeight = 0.5
        self.setPosition(self.posX, self.posY, self.posZ)

    def canBeCollidedWith(self):
        return not self.isDead

    def canBePushed(self):
        return not self.isDead

    @cython.cdivision(True)
    cpdef onEntityUpdate(self):
        cdef float xd, zd, f3, rot, step, f6
        cdef bint b1

        Entity.onEntityUpdate(self)
        self.prevCameraPitch = self.cameraPitch
        if self.__attackTime > 0:
            self.__attackTime -= 1
        if self.hurtTime > 0:
            self.hurtTime -= 1
        if self.scoreValue > 0:
            self.scoreValue -= 1
        if self.health <= 0:
            self.deathTime += 1
            if self.deathTime > 20:
                self.remove()

        if self.isInsideOfMaterial():
            if self.air > 0:
                self.air -= 1
            else:
                self.attackEntityFrom(None, 2)
        else:
            self.air = self.__maxAir

        if self.handleWaterMovement():
            self._fallDistance = 0.0
        if self.handleLavaMovement():
            self.attackEntityFrom(None, 10)

        self.prevRenderYawOffset = self.renderYawOffset
        self.prevRotationYaw = self.rotationYaw
        self.prevRotationPitch = self.rotationPitch
        self.ticksExisted += 1
        self.onLivingUpdate()
        xd = self.posX - self.prevPosX
        zd = self.posZ - self.prevPosZ
        f3 = sqrt(xd * xd + zd * zd)
        rot = self.renderYawOffset
        step = 0.0
        f6 = 0.0
        if not f3 <= 0.05:
            f6 = 1.0
            step = f3 * 3.0
            rot = atan2(zd, xd) * 180.0 / pi - 90.0
        if not self.onGround:
            f6 = 0.0

        self.__rotationYawHead += (f6 - self.__rotationYawHead) * 0.3
        rot -= self.renderYawOffset
        while rot < -180.0:
            rot += 360.0
        while rot >= 180.0:
            rot -= 360.0

        self.renderYawOffset += rot * 0.1
        rot = self.rotationYaw - self.renderYawOffset
        while rot < -180.0:
            rot += 360.0
        while rot >= 180.0:
            rot -= 360.0

        bl = rot < -90.0 or rot >= 90.0
        if rot < -75.0:
            rot = -75.0
        if rot >= 75.0:
            rot = 75.0

        self.renderYawOffset = self.rotationYaw - rot
        self.renderYawOffset += rot * 0.1
        if bl:
            step = -step

        while self.rotationYaw - self.prevRotationYaw < -180.0:
            self.prevRotationYaw -= 360.0
        while self.rotationYaw - self.prevRotationYaw >= 180.0:
            self.prevRotationYaw += 360.0
        while self.renderYawOffset - self.prevRenderYawOffset < -180.0:
            self.prevRenderYawOffset -= 360.0
        while self.renderYawOffset - self.prevRenderYawOffset >= 180.0:
            self.prevRenderYawOffset += 360.0
        while self.rotationPitch - self.prevRotationPitch < -180.0:
            self.prevRotationPitch -= 360.0
        while self.rotationPitch - self.prevRotationPitch >= 180.0:
            self.prevRotationPitch += 360.0

        self.__prevRotationYawHead += step

    cpdef onLivingUpdate(self):
        if self.entityAI:
            self.entityAI.onLivingUpdate(self.worldObj, self)

    def heal(self, int hp):
        if self.health <= 0:
            return

        self.health += hp
        if self.health > 20:
            self.health = 20

        self.scoreValue = self.heartsHalvesLife // 2

    def attackEntityFrom(self, Entity entity, int damage):
        cdef float xd, zd, f3, f4

        if not self.worldObj.survivalWorld:
            return

        if self.health <= 0:
            return

        if self.scoreValue > self.heartsHalvesLife // 2.0:
            if self.prevHealth - damage >= self.health:
                return

            self.health = self.prevHealth - damage
        else:
            self.prevHealth = self.health
            self.scoreValue = self.heartsHalvesLife
            self.health -= damage
            self.hurtTime = self.maxHurtTime = 10

        self.attackedAtYaw = 0.0
        if entity:
            xd = entity.posX - self.posX
            zd = entity.posZ - self.posZ
            self.attackedAtYaw = (atan2(zd, xd) * 180.0 / pi) - self.rotationYaw
            f3 = sqrt(xd * xd + zd * zd)
            f4 = 0.4
            self.motionX /= 2.0
            self.motionY /= 2.0
            self.motionZ /= 2.0
            self.motionX -= xd / f3 * f4
            self.motionY += 0.4
            self.motionZ -= zd / f3 * f4
            if self.motionY > 0.4:
                self.motionY = 0.4
        else:
            self.attackedAtYaw = <int>(random.random() * 2.0) * 180

        if self.health <= 0:
            self.onDeath(entity)

    def onDeath(self, Entity entity):
        pass

    cdef _fall(self, float d):
        cdef int damage = <int>ceil(d - 3.0)
        if damage > 0:
            self.attackEntityFrom(None, damage)

    cdef travel(self, float x, float z):
        if self.handleWaterMovement():
            self.moveFlying(x, z, 0.02)
            self.moveEntity(self.motionX, self.motionY, self.motionZ)
            self.motionX *= 0.8
            self.motionY *= 0.8
            self.motionZ *= 0.8
            self.motionY -= 0.02
            if self.horizontalCollision and self.isOffsetPositionInLiquid(
                self.motionX, self.motionY + 0.6 - self.posY + self.posY, self.motionZ
            ):
                self.motionY = 0.3
        elif self.handleLavaMovement():
            self.moveFlying(x, z, 0.02)
            self.moveEntity(self.motionX, self.motionY, self.motionZ)
            self.motionX *= 0.5
            self.motionY *= 0.5
            self.motionZ *= 0.5
            self.motionY -= 0.02
            if self.horizontalCollision and self.isOffsetPositionInLiquid(
                self.motionX, self.motionY + 0.6 - self.posY + self.posY, self.motionZ
            ):
                self.motionY = 0.3
        else:
            self.moveFlying(x, z, 0.1 if self.onGround else 0.02)
            self.moveEntity(self.motionX, self.motionY, self.motionZ)
            self.motionX *= 0.91
            self.motionY *= 0.98
            self.motionZ *= 0.91
            self.motionY -= 0.08
            if self.onGround:
                self.motionX *= 0.6
                self.motionZ *= 0.6
