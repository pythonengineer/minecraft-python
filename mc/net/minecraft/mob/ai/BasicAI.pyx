# cython: language_level=3

cimport cython

from libc.math cimport floor, atan2, sqrt, pi

from mc.net.minecraft.character.Vec3 import Vec3
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
        self.__yRotA = 0.0
        self.level = None
        self.mob = None
        self.jumping = False
        self.__attackDelay = 0

    cdef tick(self, Level level, Mob mob):
        cdef Entity entity
        cdef bint isInWater, isInLava

        self.level = level
        self.mob = mob
        if self.__attackDelay > 0:
            self.__attackDelay -= 1

        if mob.health <= 0:
            self.jumping = False
            self.xxa = 0.0
            self.yya = 0.0
            self.__yRotA = 0.0
        else:
            self._tick()

        isInWater = mob.isInWater()
        isInLava = mob.isInLava()
        if self.jumping:
            if isInWater:
                mob.yd += 0.04
            elif isInLava:
                mob.yd += 0.04
            elif mob.onGround:
                mob.yd = 0.42

        self.xxa *= 0.98
        self.yya *= 0.98
        self.__yRotA *= 0.9
        mob.travel(self.xxa, self.yya)
        entities = level.findEntities(mob, mob.bb.grow(0.2, 0.0, 0.2))
        if entities and len(entities) > 0:
            for entity in entities:
                if not entity.isPushable():
                    continue

                entity.push(mob)

    cpdef _tick(self):
        if self.__rand.randFloat() < 0.07:
            self.xxa = self.__rand.randFloat() - 0.5
            self.yya = self.__rand.randFloat()
        if self.__rand.randFloat() < 0.04:
            self.__yRotA = (self.__rand.randFloat() - 0.5) * 60.0
        self.mob.yRot += self.__yRotA
        self.mob.xRot = self.defaultLookAngle
        self.jumping = self.__rand.randFloat() < 0.01
        if self.mob.isInWater() or self.mob.isInLava():
            self.jumping = self.__rand.randFloat() < 0.8

    @cython.cdivision(True)
    cpdef _attack(self, Entity entity):
        cdef float xd, zd, d, yd

        if entity is None:
            return

        xd = entity.x - self.mob.x
        zd = entity.z - self.mob.z
        d = sqrt(xd * xd + zd * zd)
        if d < 8.0:
            yd = entity.y - self.mob.y
            self.mob.yRot = (atan2(zd, xd) * 180.0 / pi) - 90.0
            self.mob.xRot = -(atan2(yd, d) * 180.0 / pi)
            d = sqrt(xd * xd + yd * yd + zd * zd)
            if d < 2.0 and self.__attackDelay == 0:
                self.hurt(entity)

    def hurt(self, Entity entity):
        if self.level.clip(Vec3(self.mob.x, self.mob.y, self.mob.z),
                           Vec3(entity.x, entity.y, entity.z)):
            return

        self.mob.attackTime = 5
        self.__attackDelay = <int>floor(self.__rand.randFloatM(20)) + 10
        entity.hurt(self.mob, <int>floor(self.__rand.randFloatM(4)) + <int>floor(self.__rand.randFloatM(4)) + 1)

    def beforeRemove(self):
        pass
