# cython: language_level=3

from libc.math cimport sin, cos, sqrt, pi

from mc.net.minecraft.game.level.material.Material cimport Material
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB

from random import Random

cdef class Entity:

    def __cinit__(self):
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        self.prevPosX = 0.0
        self.prevPosY = 0.0
        self.prevPosZ = 0.0
        self.motionX = 0.0
        self.motionY = 0.0
        self.motionZ = 0.0
        self.rotationYaw = 0.0
        self.rotationPitch = 0.0
        self.prevRotationYaw = 0.0
        self.prevRotationPitch = 0.0
        self.boundingBox = None
        self.onGround = False
        self.isCollidedHorizontally = False
        self.__surfaceCollision = True
        self.isDead = False
        self.yOffset = 0.0
        self.width = 0.6
        self.height = 1.8
        self.prevDistanceWalkedModified = 0.0
        self.distanceWalkedModified = 0.0
        self._canTriggerWalking = True
        self._fallDistance = 0.0
        self.__nextStepDistance = 1
        self.lastTickPosX = 0.0
        self.lastTickPosY = 0.0
        self.lastTickPosZ = 0.0
        self.__ySize = 0.0
        self.stepHeight = 0.0
        self.__noClip = False
        self.__entityCollisionReduction = 0.0
        self._rand = Random()
        self.ticksExisted = 0
        self.fireResistance = 1
        self.fire = 0

    def __init__(self, world):
        self._worldObj = world
        self.setPosition(0.0, 0.0, 0.0)

    def preparePlayerToSpawn(self):
        if not self._worldObj:
            return

        x = self._worldObj.xSpawn + 0.5
        y = self._worldObj.ySpawn
        z = self._worldObj.zSpawn + 0.5
        while y > 0.0:
            self.setPosition(x, y, z)
            if len(self._worldObj.getCollidingBoundingBoxes(self.boundingBox)) == 0:
                break

            y += 1.0

        self.motionX = self.motionY = self.motionZ = 0.0
        self.rotationYaw = self._worldObj.rotSpawn
        self.rotationPitch = 0.0

    def setEntityDead(self):
        self.isDead = True

    def setSize(self, w, h):
        self.width = w
        self.height = h

    def setPosition(self, float x, float y, float z):
        self.posX = x
        self.posY = y
        self.posZ = z
        w = self.width / 2.0
        h = self.height / 2.0
        self.boundingBox = AxisAlignedBB(x - w, y - h, z - w, x + w, y + h, z + w)

    def turn(self, float xo, float yo):
        orgXRot = self.rotationPitch
        orgYRot = self.rotationYaw
        self.rotationYaw = self.rotationYaw + xo * 0.15
        self.rotationPitch = self.rotationPitch - yo * 0.15
        if self.rotationPitch < -90.0:
            self.rotationPitch = -90.0
        if self.rotationPitch > 90.0:
            self.rotationPitch = 90.0

        self.prevRotationPitch += self.rotationPitch - orgXRot
        self.prevRotationYaw += self.rotationYaw - orgYRot

    def interpolateTurn(self, float xo, float yo):
        self.rotationYaw = self.rotationYaw + xo * 0.15
        self.rotationPitch = self.rotationPitch - yo * 0.15
        if self.rotationPitch < -90.0:
            self.rotationPitch = -90.0
        if self.rotationPitch > 90.0:
            self.rotationPitch = 90.0

    cpdef onEntityUpdate(self):
        self.prevDistanceWalkedModified = self.distanceWalkedModified
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ
        self.prevRotationPitch = self.rotationPitch
        self.prevRotationYaw = self.rotationYaw

    cpdef bint isOffsetPositionInLiquid(self, float xa, float ya, float za):
        cdef AxisAlignedBB axisAlignedBB = self.boundingBox.cloneMove(xa, ya, za)
        aABBs = self._worldObj.getCollidingBoundingBoxes(axisAlignedBB)
        if len(aABBs) > 0:
            return False

        return not self._worldObj.getIsAnyLiquid(axisAlignedBB)

    cpdef moveEntity(self, float x, float y, float z):
        cdef int block
        cdef float xOrg, zOrg, xaOrg, yaOrg, zaOrg, xo, yo, zo, xd, zd
        cdef bint onGround
        cdef AxisAlignedBB aabbOrg, aABB, aabb

        xOrg = self.posX
        zOrg = self.posZ
        xaOrg = x
        yaOrg = y
        zaOrg = z

        aabbOrg = self.boundingBox.copy()
        aABBs = self._worldObj.getCollidingBoundingBoxes(self.boundingBox.addCoord(x, y, z))
        for aABB in aABBs:
            y = aABB.calculateYOffset(self.boundingBox, y)

        self.boundingBox.offset(0.0, y, 0.0)
        if not self.__surfaceCollision and yaOrg != y:
            z = 0.0
            y = 0.0
            x = 0.0

        onGround = self.onGround or yaOrg != y and yaOrg < 0.0
        for aABB in aABBs:
            x = aABB.calculateXOffset(self.boundingBox, x)

        self.boundingBox.offset(x, 0.0, 0.0)
        if not self.__surfaceCollision and xaOrg != x:
            z = 0.0
            y = 0.0
            x = 0.0

        for aABB in aABBs:
            z = aABB.calculateZOffset(self.boundingBox, z)

        self.boundingBox.offset(0.0, 0.0, z)
        if not self.__surfaceCollision and zaOrg != z:
            z = 0.0
            y = 0.0
            x = 0.0

        if self.stepHeight > 0.0 and onGround and self.__ySize < 0.05 and (xaOrg != x or zaOrg != z):
            xo = x
            yo = y
            zo = z
            x = xaOrg
            y = self.stepHeight
            z = zaOrg
            aabb = self.boundingBox.copy()
            self.boundingBox = aabbOrg.copy()
            aABBs = self._worldObj.getCollidingBoundingBoxes(self.boundingBox.addCoord(xaOrg, y, zaOrg))
            for aABB in aABBs:
                y = aABB.calculateYOffset(self.boundingBox, y)

            self.boundingBox.offset(0.0, y, 0.0)
            if not self.__surfaceCollision and yaOrg != y:
                z = 0.0
                y = 0.0
                x = 0.0

            for aABB in aABBs:
                x = aABB.calculateXOffset(self.boundingBox, x)

            self.boundingBox.offset(x, 0.0, 0.0)
            if not self.__surfaceCollision and xaOrg != x:
                z = 0.0
                y = 0.0
                x = 0.0

            for aABB in aABBs:
                z = aABB.calculateZOffset(self.boundingBox, z)

            self.boundingBox.offset(0.0, 0.0, z)
            if not self.__surfaceCollision and zaOrg != z:
                z = 0.0
                y = 0.0
                x = 0.0

            if xo * xo + zo * zo >= x * x + z * z:
                x = xo
                y = yo
                z = zo
                self.boundingBox = aabb.copy()
            else:
                self.__ySize += 0.5

        self.posX = (self.boundingBox.minX + self.boundingBox.maxX) * (1 / 2)
        self.posY = self.boundingBox.minY + self.yOffset - self.__ySize
        self.posZ = (self.boundingBox.minZ + self.boundingBox.maxZ) * (1 / 2)
        self.isCollidedHorizontally = xaOrg != x or zaOrg != z
        self.onGround = yaOrg != y and yaOrg < 0.0
        if self.onGround:
            if self._fallDistance > 0.0:
                self._fall(self._fallDistance)
                self._fallDistance = 0.0
        elif y < 0.0:
            self._fallDistance -= y

        if xaOrg != x:
            self.motionX = 0.0
        if yaOrg != y:
            self.motionY = 0.0
        if zaOrg != z:
            self.motionZ = 0.0

        xd = self.posX - xOrg
        zd = self.posZ - zOrg
        self.distanceWalkedModified = <float>(self.distanceWalkedModified + sqrt(xd * xd + zd * zd) * 0.6)
        if self._canTriggerWalking:
            block = self._worldObj.getBlockId(<int>self.posX,
                                              <int>(self.posY - 0.2 - self.yOffset),
                                              <int>self.posZ)
            if self.distanceWalkedModified > self.__nextStepDistance and block > 0:
                self.__nextStepDistance += 1
                sound = blocks.blocksList[block].stepSound
                self._worldObj.playSoundAtEntity(self, 'step.' + sound.soundDir,
                                                 sound.soundVolume * 0.15, sound.soundPitch)

        self.__ySize *= 0.4
        inWater = self.handleWaterMovement()
        if self._worldObj.isBoundingBoxBurning(self.boundingBox):
            self.attackEntityFrom(None, 1)
            if not inWater:
                self.fire += 1
                if self.fire == 0:
                    self.fire = 300
        elif self.fire <= 0:
            self.fire = -self.fireResistance

        if inWater and self.fire > 0:
            self._worldObj.playSoundAtEntity(
                self, 'random.fizz', 0.7,
                1.6 + (self._rand.random() - self._rand.random()) * 0.4
            )
            self.fire = -self.fireResistance

    cdef _fall(self, float distance):
        pass

    cdef bint handleWaterMovement(self):
        return self._worldObj.handleMaterialAcceleration(self.boundingBox.expand(0.0, -0.4, 0.0),
                                                         Material.water)

    def isInsideOfMaterial(self):
        block = self._worldObj.getBlockId(<int>self.posX,
                                          <int>(self.posY + 0.12),
                                          <int>self.posZ)
        if block != 0:
            return blocks.blocksList[block].getBlockMaterial() == Material.water

        return False

    cdef bint handleLavaMovement(self):
        return self._worldObj.handleMaterialAcceleration(self.boundingBox.expand(0.0, -0.4, 0.0),
                                                         Material.lava)

    cpdef moveFlying(self, float xa, float za, float speed):
        cdef float dist, si, co

        dist = sqrt(xa * xa + za * za)
        if dist < 0.01:
            return

        if dist < 1.0:
            dist = 1.0

        dist = speed / dist
        xa *= dist
        za *= dist

        si = sin(self.rotationYaw * pi / 180.0)
        co = cos(self.rotationYaw * pi / 180.0)

        self.motionX += xa * co - za * si
        self.motionZ += za * co + xa * si

    cpdef float getBrightness(self):
        cdef int x, y, z
        x = <int>self.posX
        y = <int>(self.posY + self.yOffset / 2.0)
        z = <int>self.posZ
        return self._worldObj.getBlockLightValue(x, y, z)

    def setWorld(self, world):
        self._worldObj = world

    def setPositionAndRotation(self, x, y, z, yaw, pitch):
        self.prevPosX = self.posX = x
        self.prevPosY = self.posY = y
        self.prevPosZ = self.posZ = z
        self.rotationYaw = yaw
        self.rotationPitch = 0.0
        self.setPosition(x, y, z)

    cdef applyEntityCollision(self, entity):
        cdef float x, z, d
        x = entity.posX - self.posX
        z = entity.posZ - self.posZ
        d = x * x + z * z
        if d >= 0.01:
            d = sqrt(d)
            x /= d
            z /= d
            x /= d
            z /= d
            x *= 0.05
            z *= 0.05
            self.__addVelocity(-x, -z)
            entity.__addVelocity(x, z)

    def __addVelocity(self, float x, float z):
        self.motionX += x
        self.motionY = self.motionY
        self.motionZ += z

    def attackEntityFrom(self, player, damage):
        pass

    def canBeCollidedWith(self):
        return False

    def canBePushed(self):
        return False

    cpdef bint shouldRender(self, vec):
        cdef float xd, yd, zd
        xd = self.posX - vec.xCoord
        yd = self.posY - vec.yCoord
        zd = self.posZ - vec.zCoord
        return self.shouldRenderAtSqrDistance(xd * xd + yd * yd + zd * zd)

    cdef bint shouldRenderAtSqrDistance(self, float d):
        cdef float size = self.boundingBox.getSize() * 64.0
        return d < size * size
