# cython: language_level=3

cimport cython

from libc.math cimport sin, cos, ceil, sqrt, atan2, pi

from mc.net.minecraft.game.entity.Entity cimport Entity
from mc.net.minecraft.game.entity.AILiving cimport AILiving
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.Items import items
from mc.JavaUtils cimport random
from pyglet import gl

from nbtlib.tag import Short

cdef class EntityLiving(Entity):
    ATTACK_DURATION = 5
    HEALTH = 10

    def __init__(self, world):
        super().__init__(world)
        self.preventEntitySpawning = True
        self.heartsHalvesLife = EntityLiving.HEALTH
        self.renderYawOffset = 0.0
        self.prevRenderYawOffset = 0.0
        self.__prevRotationYawHead = 0.0
        self.__rotationYawHead = 0.0
        self.texture = 'char.png'
        self.health = EntityLiving.HEALTH
        self.prevHealth = 0
        self.hurtTime = 0
        self.maxHurtTime = 0
        self.attackedAtYaw = 0.0
        self.deathTime = 0
        self.__attackTime = 0
        self.prevCameraPitch = 0.0
        self.cameraPitch = 0.0
        self._entityAI = AILiving()
        self.setPosition(self.posX, self.posY, self.posZ)
        self.rotationYaw = random() * (pi * 2.0)
        self.stepHeight = 0.5
        self.moveStrafing = 0.0
        self.moveForward = 0.0
        self.randomYawVelocity = 0.0

    def canBeCollidedWith(self):
        return not self.isDead

    def canBePushed(self):
        return not self.isDead

    cpdef float _getEyeHeight(self):
        return self.height * 0.85

    @cython.cdivision(True)
    def onEntityUpdate(self):
        cdef int i
        cdef float x, y, z, xd, zd, d, rot, step, head
        cdef bint angle

        Entity.onEntityUpdate(self)

        if self.isInsideOfMaterial():
            self.air -= 1
            if self.air == -20:
                self.air = 0
                for i in range(8):
                    x = self._rand.nextFloat() - self._rand.nextFloat()
                    y = self._rand.nextFloat() - self._rand.nextFloat()
                    z = self._rand.nextFloat() - self._rand.nextFloat()
                    self._worldObj.spawnParticle(
                        'bubble', self.posX + x, self.posY + y, self.posZ + z,
                        self.motionX, self.motionY, self.motionZ
                    )

                self.attackEntityFrom(None, 2)

            self.fire = 0
        else:
            self.air = self._maxAir

        self.prevCameraPitch = self.cameraPitch
        if self.__attackTime > 0:
            self.__attackTime -= 1
        if self.hurtTime > 0:
            self.hurtTime -= 1
        if self.heartsLife > 0:
            self.heartsLife -= 1
        if self.health <= 0:
            self.deathTime += 1
            if self.deathTime > 20:
                self.setEntityDead()

        self.prevRenderYawOffset = self.renderYawOffset
        self.prevRotationYaw = self.rotationYaw
        self.prevRotationPitch = self.rotationPitch
        self.ticksExisted += 1
        self.onLivingUpdate()
        xd = self.posX - self.prevPosX
        zd = self.posZ - self.prevPosZ
        d = sqrt(xd * xd + zd * zd)
        rot = self.renderYawOffset
        step = 0.0
        head = 0.0
        if not d <= 0.05:
            head = 1.0
            step = d * 3.0
            rot = atan2(zd, xd) * 180.0 / pi - 90.0
        if not self.onGround:
            head = 0.0

        self.__rotationYawHead += (head - self.__rotationYawHead) * 0.3
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

        angle = rot < -90.0 or rot >= 90.0
        rot = min(max(rot, -75.0), 75.0)

        self.renderYawOffset = self.rotationYaw - rot
        self.renderYawOffset += rot * 0.1
        if angle:
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

    def onLivingUpdate(self):
        if self._entityAI:
            self._entityAI.onLivingUpdate(self._worldObj, self)

    def heal(self, int hp):
        if self.health <= 0:
            return

        self.health += hp
        if self.health > EntityLiving.HEALTH:
            self.health = EntityLiving.HEALTH

        self.heartsLife = self.heartsHalvesLife // 2

    def setSize(self, w, h):
        super().setSize(w, h)

    def attackEntityFrom(self, Entity entity, int damage):
        cdef float xd, zd, d

        if not self._worldObj.survivalWorld:
            return

        if self.health <= 0:
            return

        self.moveForward = 1.5
        if self.heartsLife > self.heartsHalvesLife // 2.0:
            if self.prevHealth - damage >= self.health:
                return

            self.health = self.prevHealth - damage
        else:
            self.prevHealth = self.health
            self.heartsLife = self.heartsHalvesLife
            self.health -= damage
            self.hurtTime = self.maxHurtTime = 10

        self._worldObj.playSoundAtEntity(
            self, 'random.hurt', 1.0,
            (self._rand.nextFloat() - self._rand.nextFloat()) * 0.2 + 1.0
        )
        self.attackedAtYaw = 0.0
        if entity:
            xd = entity.posX - self.posX
            zd = entity.posZ - self.posZ
            self.attackedAtYaw = (atan2(zd, xd) * 180.0 / pi) - self.rotationYaw
            d = sqrt(xd * xd + zd * zd)
            self.motionX /= 2.0
            self.motionY /= 2.0
            self.motionZ /= 2.0
            self.motionX -= xd / d * 0.4
            self.motionY += 0.4
            self.motionZ -= zd / d * 0.4
            if self.motionY > 0.4:
                self.motionY = 0.4
        else:
            self.attackedAtYaw = <int>(random() * 2.0) * 180

        if self.health <= 0:
            self.onDeath(entity)

    def onDeath(self, Entity entity):
        cdef int i
        cdef int drops = self._rand.nextInt(3)
        cdef int drop = self._rand.nextInt(4)
        if drop == 0:
            for i in range(drops):
                self.entityDropItem(items.silk.shiftedIndex, 1)
        elif drop == 1:
            for i in range(drops):
                self.entityDropItem(items.gunpowder.shiftedIndex, 1)
        elif drop == 2:
            for i in range(drops):
                self.entityDropItem(items.feather.shiftedIndex, 1)
        elif drop == 3:
            self.entityDropItem(items.flintSteel.shiftedIndex, 1)

    cdef _fall(self, float d):
        cdef int damage = <int>ceil(d - 3.0)
        if damage > 0:
            self.attackEntityFrom(None, damage)
            block = self._worldObj.getBlockId(<int>self.posX,
                                              <int>(self.posY - 0.2 - self.yOffset),
                                              <int>self.posZ)
            if block > 0:
                sound = blocks.blocksList[block].stepSound
                self._worldObj.playSoundAtEntity(self, 'step.' + sound.soundDir,
                                               sound.soundVolume * 0.5,
                                               sound.soundPitch * (12.0 / 16.0))

    def setEntityAI(self, ai):
        self._entityAI = ai

    cdef travel(self, float x, float z):
        if self.handleWaterMovement():
            self.moveFlying(x, z, 0.02)
            self.moveEntity(self.motionX, self.motionY, self.motionZ)
            self.motionX *= 0.8
            self.motionY *= 0.8
            self.motionZ *= 0.8
            self.motionY -= 0.02
            if self.isCollidedHorizontally and self.isOffsetPositionInLiquid(
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
            if self.isCollidedHorizontally and self.isOffsetPositionInLiquid(
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

        self.moveStrafing = self.moveForward
        xd = self.posX - self.prevPosX
        zd = self.posZ - self.prevPosZ
        d = sqrt(xd * xd + zd * zd) * 4.0
        d = min(d, 1.0)

        self.moveForward += (d - self.moveForward) * 0.4
        self.randomYawVelocity += self.moveForward

    def _writeEntityToNBT(self, compound):
        compound['Health'] = Short(self.health)
        compound['HurtTime'] = Short(self.hurtTime)
        compound['DeathTime'] = Short(self.deathTime)
        compound['AttackTime'] = Short(self.__attackTime)

    def _readEntityFromNBT(self, compound):
        self.health = compound['Health'].real
        self.hurtTime = compound['HurtTime'].real
        self.deathTime = compound['DeathTime'].real
        self.__attackTime = compound['AttackTime'].real

    def _getEntityString(self):
        return 'Mob'
