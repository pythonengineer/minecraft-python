# cython: language_level=3

from libc.math cimport sin, cos, sqrt, pi

from mc.net.minecraft.level.liquid.Liquid cimport Liquid
from mc.net.minecraft.level.tile.Tiles import SoundType, tiles
from mc.net.minecraft.phys.AABB cimport AABB

cdef class Entity:

    def __cinit__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.xo = 0.0
        self.yo = 0.0
        self.zo = 0.0
        self.xd = 0.0
        self.yd = 0.0
        self.zd = 0.0
        self.yRot = 0.0
        self.xRot = 0.0
        self.yRotO = 0.0
        self.xRotO = 0.0
        self.bb = None
        self.onGround = False
        self.horizontalCollision = False
        self.collision = False
        self.slide = True
        self.removed = False
        self.heightOffset = 0.0
        self.bbWidth = 0.6
        self.bbHeight = 1.8
        self.walkDistO = 0.0
        self.walkDist = 0.0
        self.makeStepSound = True
        self.fallDistance = 0.0
        self.__nextStep = 1
        self.blockMap = None
        self.xOld = 0.0
        self.yOld = 0.0
        self.zOld = 0.0

    def __init__(self, level):
        self.level = level
        self.setPos(0.0, 0.0, 0.0)

    def resetPos(self):
        if not self.level:
            return

        x = self.level.xSpawn + 0.5
        y = self.level.ySpawn
        z = self.level.zSpawn + 0.5
        while y > 0.0:
            self.setPos(x, y, z)
            if len(self.level.getCubes(self.bb)) == 0:
                break

            y += 1.0

        self.xd = self.yd = self.zd = 0.0
        self.yRot = self.level.rotSpawn
        self.xRot = 0.0

    def remove(self):
        self.removed = True

    def setSize(self, w, h):
        self.bbWidth = w
        self.bbHeight = h

    def setMovePos(self, pos):
        if pos.moving:
            self.setPos(pos.x, pos.y, pos.z)
        else:
            self.setPos(self.x, self.y, self.z)

        if pos.rotating:
            self.setRot(pos.yRot, pos.xRot)
        else:
            self.setRot(self.yRot, self.xRot)

    def setRot(self, float yRot, float xRot):
        self.yRot = yRot
        self.xRot = xRot

    def setPos(self, float x, float y, float z):
        self.x = x
        self.y = y
        self.z = z
        w = self.bbWidth / 2.0
        h = self.bbHeight / 2.0
        self.bb = AABB(x - w, y - h, z - w, x + w, y + h, z + w)

    def turn(self, float xo, float yo):
        orgXRot = self.xRot
        orgYRot = self.yRot
        self.yRot = self.yRot + xo * 0.15
        self.xRot = self.xRot - yo * 0.15
        if self.xRot < -90.0:
            self.xRot = -90.0
        if self.xRot > 90.0:
            self.xRot = 90.0

        self.xRotO += self.xRot - orgXRot
        self.yRotO += self.yRot - orgYRot

    def interpolateTurn(self, float xo, float yo):
        self.yRot = self.yRot + xo * 0.15
        self.xRot = self.xRot - yo * 0.15
        if self.xRot < -90.0:
            self.xRot = -90.0
        if self.xRot > 90.0:
            self.xRot = 90.0

    cpdef tick(self):
        self.walkDistO = self.walkDist
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self.xRotO = self.xRot
        self.yRotO = self.yRot

    cpdef bint isFree(self, float xa, float ya, float za):
        cdef AABB axisAlignedBB = self.bb.cloneMove(xa, ya, za)
        aABBs = self.level.getCubes(axisAlignedBB)
        if len(aABBs) > 0:
            return False

        return not self.level.containsAnyLiquid(axisAlignedBB)

    cpdef move(self, float xa, float ya, float za):
        cdef int tile
        cdef float xOrg, zOrg, xaOrg, yaOrg, zaOrg, xd, zd
        cdef bint onGround
        cdef AABB aABB

        xOrg = self.x
        zOrg = self.z
        xaOrg = xa
        yaOrg = ya
        zaOrg = za

        aABBs = self.level.getCubes(self.bb.expand(xa, ya, za))
        for aABB in aABBs:
            ya = aABB.clipYCollide(self.bb, ya)

        self.bb.move(0.0, ya, 0.0)
        if not self.slide and yaOrg != ya:
            za = 0.0
            ya = 0.0
            xa = 0.0

        for aABB in aABBs:
            xa = aABB.clipXCollide(self.bb, xa)

        self.bb.move(xa, 0.0, 0.0)
        if not self.slide and xaOrg != xa:
            za = 0.0
            ya = 0.0
            xa = 0.0

        for aABB in aABBs:
            za = aABB.clipZCollide(self.bb, za)

        self.bb.move(0.0, 0.0, za)
        if not self.slide and zaOrg != za:
            za = 0.0
            ya = 0.0
            xa = 0.0

        self.horizontalCollision = xaOrg != xa or zaOrg != za
        self.onGround = yaOrg != ya and yaOrg < 0.0
        self.collision = self.horizontalCollision or yaOrg != ya

        if self.onGround:
            if self.fallDistance > 0.0:
                self._causeFallDamage(self.fallDistance)
                self.fallDistance = 0.0
        elif ya < 0.0:
            self.fallDistance -= ya

        if xaOrg != xa:
            self.xd = 0.0
        if yaOrg != ya:
            self.yd = 0.0
        if zaOrg != za:
            self.zd = 0.0

        self.x = (self.bb.x0 + self.bb.x1) / 2.0
        self.y = self.bb.y0 + self.heightOffset
        self.z = (self.bb.z0 + self.bb.z1) / 2.0

        xd = self.x - xOrg
        zd = self.z - zOrg
        self.walkDist = <float>(self.walkDist + sqrt(xd * xd + zd * zd) * 0.6)
        if self.makeStepSound:
            tile = self.level.getTile(<int>self.x, <int>(self.y - 0.2 - self.heightOffset), <int>self.z)
            if self.walkDist > self.__nextStep and tile > 0:
                self.__nextStep += 1
                soundType = tiles.tiles[tile].soundType
                if soundType != SoundType.none:
                    self.playSound('step.' + soundType.soundName,
                                   soundType.getVolume() * 0.75,
                                   soundType.getPitch())

    cdef _causeFallDamage(self, float distance):
        pass

    cdef bint isInWater(self):
        return self.level.containsLiquid(self.bb.grow(0.0, -0.4, 0.0), Liquid.water)

    def isUnderWater(self):
        tile = self.level.getTile(<int>self.x, <int>(self.y + 0.12), <int>self.z)
        if tile != 0:
            return tiles.tiles[tile].getLiquidType() == Liquid.water

        return False

    cdef bint isInLava(self):
        return self.level.containsLiquid(self.bb.grow(0.0, -0.4, 0.0), Liquid.lava)

    cdef moveRelative(self, float xa, float za, float speed):
        cdef float dist, si, co

        dist = sqrt(xa * xa + za * za)
        if dist < 0.01:
            return

        if dist < 1.0:
            dist = 1.0

        dist = speed / dist
        xa *= dist
        za *= dist

        si = sin(self.yRot * pi / 180.0)
        co = cos(self.yRot * pi / 180.0)

        self.xd += xa * co - za * si
        self.zd += za * co + xa * si

    def isLit(self):
        return self.level.isLit(<int>self.x, <int>self.y, <int>self.z)

    cpdef float getBrightness(self, float a):
        cdef int x, y, z
        x = <int>self.x
        y = <int>(self.y + self.heightOffset / 2.0)
        z = <int>self.z
        return self.level.getBrightness(x, y, z)

    cpdef render(self, textures, float translation):
        pass

    def setLevel(self, level):
        self.level = level

    def playSound(self, str name, float volume, float pitch):
        self.level.playSoundAtEntity(name, self, volume, pitch)

    def moveTo(self, float x, float y, float z, float yRot, float xRot):
        self.xo = self.x = x
        self.yo = self.y = y
        self.zo = self.z = z
        self.yRot = yRot
        self.xRot = xRot
        self.setPos(x, y, z)

    def distanceTo(self, entity):
        cdef float x, y, z
        x = self.x - entity.x
        y = self.y - entity.y
        z = self.z - entity.z
        return sqrt(x * x + y * y + z * z)

    def distanceToSqr(self, entity):
        cdef float x, y, z
        x = self.x - entity.x
        y = self.y - entity.y
        z = self.z - entity.z
        return x * x + y * y + z * z

    def getDistanceSq(self, float x, float y, float z):
        cdef float d
        x -= self.x
        y -= self.y
        z = z - self.z
        d = sqrt(x * x + y * y + z * z)
        d = 1.0 - d / 32.0
        if d < 0.0:
            d = 0.0

        return d

    def playerTouch(self, player):
        pass

    cdef push(self, entity):
        cdef float x, z, d
        x = entity.x - self.x
        z = entity.z - self.z
        d = x * x + z * z
        if d >= 0.01:
            d = sqrt(d)
            x /= d
            z /= d
            x /= d
            z /= d
            x *= 0.05
            z *= 0.05
            self._push(-x, 0.0, -z)
            entity._push(x, 0.0, z)

    def _push(self, float x, float y, float z):
        self.xd += x
        self.yd += y
        self.zd += z

    def hurt(self, entity, hp):
        pass

    def intersects(self, float x0, float y0, float z0,
                   float x1, float y1, float z1):
        return self.bb.intersects(x0, y0, z0, x1, y1, z1)

    def isPickable(self):
        return False

    def isPushable(self):
        return False

    def isShootable(self):
        return False

    def awardKillScore(self, entity, score):
        pass