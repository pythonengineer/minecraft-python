# cython: language_level=3

cimport cython

from libc.math cimport sin, cos, ceil, sqrt, atan2, pi

from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.mob.ai.BasicAI cimport BasicAI
from pyglet import gl

import random

cdef object Tile_modelCache

cdef class Mob(Entity):
    ATTACK_DURATION = 5
    TOTAL_AIR_SUPPLY = 300

    def __init__(self, level):
        super().__init__(level)
        self.invulnerableDuration = 20
        self.rot = random.random() * pi * 2.0
        self.timeOffs = random.random() * 12398.0
        self.speed = 1.0
        self.rotA = (random.random() + 1.0) * 0.01
        self._yBodyRot = 0.0
        self._yBodyRotO = 0.0
        self._oRun = 0.0
        self._run = 0.0
        self._animStep = 0.0
        self._animStepO = 0.0
        self._tickCount = 0
        self.hasHair = True
        self._textureName = 'char.png'
        self.allowAlpha = True
        self.modelName = ''
        self._bobStrength = 1.0
        self._deathScore = 0
        self.renderOffset = 0.0
        self.rotOffs = 0.0
        self.health = 20
        self.lastHealth = 0
        self.invulnerableTime = 0
        self.airSupply = Mob.TOTAL_AIR_SUPPLY
        self.hurtTime = 0
        self.hurtDuration = 0
        self.hurtDir = 0.0
        self.deathTime = 0
        self.attackTime = 0
        self.oTilt = 0.0
        self.tilt = 0.0
        self._dead = False
        self.ai = BasicAI()
        self.footSize = 0.5
        self.setPos(self.x, self.y, self.z)

    @property
    def modelCache(self):
        return Mob_modelCache

    @modelCache.setter
    def modelCache(self, x):
        global Mob_modelCache
        Mob_modelCache = x

    def isPickable(self):
        return not self.removed

    def isPushable(self):
        return not self.removed

    @cython.cdivision(True)
    cpdef tick(self):
        cdef float xd, zd, f3, rot, step, f6
        cdef bint b1

        Entity.tick(self)
        self.oTilt = self.tilt
        if self.attackTime > 0:
            self.attackTime -= 1
        if self.hurtTime > 0:
            self.hurtTime -= 1
        if self.invulnerableTime > 0:
            self.invulnerableTime -= 1
        if self.health <= 0:
            self.deathTime += 1
            if self.deathTime > 20:
                if self.ai:
                    self.ai.beforeRemove()

                self.remove()

        if self.isUnderWater():
            if self.airSupply > 0:
                self.airSupply -= 1
            else:
                self.hurt(None, 2)
        else:
            self.airSupply = Mob.TOTAL_AIR_SUPPLY

        if self.isInWater():
            self.fallDistance = 0.0
        if self.isInLava():
            self.hurt(None, 10)

        self._animStepO = self._animStep
        self._yBodyRotO = self._yBodyRot
        self.yRotO = self.yRot
        self.xRotO = self.xRot
        self._tickCount += 1
        self.aiStep()
        xd = self.x - self.xo
        zd = self.z - self.zo
        f3 = sqrt(xd * xd + zd * zd)
        rot = self._yBodyRot
        step = 0.0
        self._oRun = self._run
        f6 = 0.0
        if not f3 <= 0.05:
            f6 = 1.0
            step = f3 * 3.0
            rot = atan2(zd, xd) * 180.0 / pi - 90.0
        if not self.onGround:
            f6 = 0.0

        self._run += (f6 - self._run) * 0.3
        rot -= self._yBodyRot
        while rot < -180.0:
            rot += 360.0
        while rot >= 180.0:
            rot -= 360.0

        self._yBodyRot += rot * 0.1
        rot = self.yRot - self._yBodyRot
        rot = self.yRot - self._yBodyRot
        while rot < -180.0:
            rot += 360.0
        while rot >= 180.0:
            rot -= 360.0

        bl = rot < -90.0 or rot >= 90.0
        if rot < -75.0:
            rot = -75.0
        if rot >= 75.0:
            rot = 75.0

        self._yBodyRot = self.yRot - rot
        self._yBodyRot += rot * 0.1
        if bl:
            step = -step

        while self.yRot - self.yRotO < -180.0:
            self.yRotO -= 360.0
        while self.yRot - self.yRotO >= 180.0:
            self.yRotO += 360.0
        while self._yBodyRot - self._yBodyRotO < -180.0:
            self._yBodyRotO -= 360.0
        while self._yBodyRot - self._yBodyRotO >= 180.0:
            self._yBodyRotO += 360.0
        while self.xRot - self.xRotO < -180.0:
            self.xRotO -= 360.0
        while self.xRot - self.xRotO >= 180.0:
            self.xRotO += 360.0

        self._animStep += step

    cpdef aiStep(self):
        if self.ai:
            self.ai.tick(self.level, self)

    def bindTexture(self, textures):
        self.textureId = textures.loadTexture(self._textureName)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)

    @cython.cdivision(True)
    cpdef render(self, textures, float translation):
        cdef float at, yBodyRot, run, rotX, rotY, step, b, rotZ, f10, ht, dt

        if not self.modelCache:
            return

        at = self.attackTime - translation
        if at < 0.0:
            at = 0.0

        while self._yBodyRotO - self._yBodyRot < -180.0:
            self._yBodyRotO += 360.0
        while self._yBodyRotO - self._yBodyRot >= 180.0:
            self._yBodyRotO -= 360.0

        while self.xRotO - self.xRot < -180.0:
            self.xRotO += 360.0
        while self.xRotO - self.xRot >= 180.0:
            self.xRotO -= 360.0
        while self.yRotO - self.yRot < -180.0:
            self.yRotO += 360.0
        while self.yRotO - self.yRot >= 180.0:
            self.yRotO -= 360.0

        yBodyRot = self._yBodyRotO + (self._yBodyRot - self._yBodyRotO) * translation
        run = self._oRun + (self._run - self._oRun) * translation
        rotX = self.yRotO + (self.yRot - self.yRotO) * translation
        rotY = self.xRotO + (self.xRot - self.xRotO) * translation
        rotX -= yBodyRot
        gl.glPushMatrix()
        step = self._animStepO + (self._animStep - self._animStepO) * translation
        b = self.getBrightness(translation)
        gl.glColor3f(b, b, b)
        rotZ = 0.0625
        f10 = -abs(cos(step * 0.6662)) * 5.0 * run * self._bobStrength - 23.0
        gl.glTranslatef(self.xo + (self.x - self.xo) * translation,
                        self.yo + (self.y - self.yo) * translation - 1.62 + self.renderOffset,
                        self.zo + (self.z - self.zo) * translation)
        ht = self.hurtTime - translation
        if ht > 0.0 or self.health <= 0:
            if ht < 0.0:
                ht = 0.0
            else:
                ht /= self.hurtDuration
                ht = sin((ht * ht * ht * ht) * pi) * 14.0

            dt = 0.0
            if self.health <= 0:
                dt = (self.deathTime + translation) / 20.0
                ht += dt * dt * 800.0
                if ht > 90.0:
                    ht = 90.0

            dt = self.hurtDir
            gl.glRotatef(180.0 - yBodyRot + self.rotOffs, 0.0, 1.0, 0.0)
            gl.glScalef(1.0, 1.0, 1.0)
            gl.glRotatef(-dt, 0.0, 1.0, 0.0)
            gl.glRotatef(-ht, 0.0, 0.0, 1.0)
            gl.glRotatef(dt, 0.0, 1.0, 0.0)
            gl.glRotatef(-(180.0 - yBodyRot + self.rotOffs), 0.0, 1.0, 0.0)

        gl.glTranslatef(0.0, -f10 * rotZ, 0.0)
        gl.glScalef(1.0, -1.0, 1.0)
        gl.glRotatef(180.0 - yBodyRot + self.rotOffs, 0.0, 1.0, 0.0)
        if not self.allowAlpha:
            gl.glDisable(gl.GL_ALPHA_TEST)
        else:
            gl.glDisable(gl.GL_CULL_FACE)
        gl.glScalef(-1.0, 1.0, 1.0)
        self.modelCache.getModel(self.modelName).rot = at / 5.0

        self.bindTexture(textures)
        self.renderModel(textures, step, translation, run, rotX, rotY, rotZ)
        if self.invulnerableTime > self.invulnerableDuration - 10:
            gl.glColor4f(1.0, 1.0, 1.0, 0.75)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
            self.bindTexture(textures)
            self.renderModel(textures, step, translation, run, rotX, rotY, rotZ)
            gl.glDisable(gl.GL_BLEND)

        gl.glEnable(gl.GL_ALPHA_TEST)
        if self.allowAlpha:
            gl.glEnable(gl.GL_CULL_FACE)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glPopMatrix()

    def renderModel(self, textures, float x, float y, float z,
                    float rotX, float rotY, float rotZ):
        self.modelCache.getModel(self.modelName).render(x, z, self._tickCount + y, rotX, rotY, rotZ)

    def heal(self, int hp):
        if self.health <= 0:
            return

        self.health += hp
        if self.health > 20:
            self.health = 20

        self.invulnerableTime = self.invulnerableDuration // 2

    def hurt(self, Entity entity, int hp):
        cdef float xd, zd

        if self.level.creativeMode:
            return

        if self.health <= 0:
            return

        self.ai.hurt(entity, hp)
        if self.invulnerableTime > self.invulnerableDuration // 2.0:
            if self.lastHealth - hp >= self.health:
                return

            self.health = self.lastHealth - hp
        else:
            self.lastHealth = self.health
            self.invulnerableTime = self.invulnerableDuration
            self.health -= hp
            self.hurtDuration = 10
            self.hurtTime = 10

        self.hurtDir = 0.0
        if entity:
            xd = entity.x - self.x
            zd = entity.z - self.z
            self.hurtDir = (atan2(zd, xd) * 180.0 / pi) - self.yRot
            self.knockback(entity, hp, xd, zd)
        else:
            self.hurtDir = <int>(random.random() * 2.0) * 180

        if self.health <= 0:
            self.die(entity)

    @cython.cdivision(True)
    cdef knockback(self, Entity entity, int hp, float xd, float zd):
        cdef float f3, f4
        f3 = sqrt(xd * xd + zd * zd)
        f4 = 0.4
        self.xd /= 2.0
        self.yd /= 2.0
        self.zd /= 2.0
        self.xd -= xd / f3 * f4
        self.yd += 0.4
        self.zd -= zd / f3 * f4
        if self.yd > 0.4:
            self.yd = 0.4

    def die(self, Entity entity):
        if self.level.creativeMode:
            return

        if self._deathScore > 0 and entity:
            entity.awardKillScore(self, self._deathScore)

        self._dead = True

    cdef _causeFallDamage(self, float d):
        if self.level.creativeMode:
            return

        cdef int n = <int>ceil(d - 3.0)
        if n > 0:
            self.hurt(None, n)

    cdef travel(self, float x, float z):
        cdef float f3, f4

        if self.isInWater():
            f3 = self.y
            self.moveRelative(x, z, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.8
            self.yd *= 0.8
            self.zd *= 0.8
            self.yd -= 0.02
            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + f3, self.zd):
                self.yd = 0.3
            return
        if self.isInLava():
            f4 = self.y
            self.moveRelative(x, z, 0.02)
            self.move(self.xd, self.yd, self.zd)
            self.xd *= 0.5
            self.yd *= 0.5
            self.zd *= 0.5
            self.yd -= 0.02
            if self.horizontalCollision and self.isFree(self.xd, self.yd + 0.6 - self.y + f4, self.zd):
                self.yd = 0.3
            return

        self.moveRelative(x, z, 0.1 if self.onGround else 0.02)
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.91
        self.yd *= 0.98
        self.zd *= 0.91
        self.yd -= 0.08
        if self.onGround:
            f5 = 0.6
            self.xd *= f5
            self.zd *= f5

    def isShootable(self):
        return True
