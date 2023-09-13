# cython: language_level=3

cimport cython

from libc.math cimport floor, atan2, sqrt, pi

from mc.net.minecraft.model.Vec3 import Vec3
from mc.net.minecraft.Entity cimport Entity
from mc.net.minecraft.mob.Mob cimport Mob
from mc.net.minecraft.level.Level cimport Level
from mc.cCompatibilityShims cimport Random

cdef class BasicAI:

    def __cinit__(self):
        self.defaultLookAngle = 0
        self.__rand = Random()
        self.xxa = 0.0
        self.yya = 0.0
        self._yRotA = 0.0
        self.level = None
        self.mob = None
        self.jumping = False
        self._attackDelay = 0
        self.runSpeed = 0.7
        self._noActionTime = 0
        self.attackTarget = None

    cpdef tick(self, Level level, Mob mob):
        cdef Entity entity
        cdef bint isInWater, isInLava
        cdef float xd, yd, zd

        self._noActionTime += 1
        entity = level.getPlayer()
        if self._noActionTime > 600 and <int>self.__rand.randFloatM(800) == 0 and entity:
            xd = entity.x - mob.x
            yd = entity.y - mob.y
            zd = entity.z - mob.z
            if xd * xd + yd * yd + zd * zd < 1024.0:
                self._noActionTime = 0
            else:
                mob.remove()

        self.level = level
        self.mob = mob
        if self._attackDelay > 0:
            self._attackDelay -= 1

        if mob.health <= 0:
            self.jumping = False
            self.xxa = 0.0
            self.yya = 0.0
            self._yRotA = 0.0
        else:
            self.update()

        isInWater = mob.isInWater()
        isInLava = mob.isInLava()
        if self.jumping:
            if isInWater:
                mob.yd += 0.04
            elif isInLava:
                mob.yd += 0.04
            elif mob.onGround:
                self._jumpFromGround()

        self.xxa *= 0.98
        self.yya *= 0.98
        self._yRotA *= 0.9
        mob.travel(self.xxa, self.yya)
        entities = level.findEntities(mob, mob.bb.grow(0.2, 0.0, 0.2))
        if entities and len(entities) > 0:
            for entity in entities:
                if not entity.isPushable():
                    continue

                entity.push(mob)

    def _jumpFromGround(self):
        self.mob.yd = 0.42

    cpdef update(self):
        if self.__rand.randFloat() < 0.07:
            self.xxa = (self.__rand.randFloat() - 0.5) * self.runSpeed
            self.yya = self.__rand.randFloat() * self.runSpeed

        self.jumping = self.__rand.randFloat() < 0.01
        if self.__rand.randFloat() < 0.04:
            self._yRotA = (self.__rand.randFloat() - 0.5) * 60.0

        self.mob.yRot += self._yRotA
        self.mob.xRot = self.defaultLookAngle
        if self.attackTarget:
            self.yya = self.runSpeed
            self.jumping = self.__rand.randFloat() < 0.04

        if self.mob.isInWater() or self.mob.isInLava():
            self.jumping = self.__rand.randFloat() < 0.8

    def beforeRemove(self):
        pass

    def hurt(self, Entity entity, int hp):
        self._noActionTime = 0
