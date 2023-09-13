# cython: language_level=3

from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.liquid.Liquid cimport Liquid
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.phys.AABB import AABB

import random

cdef list Tile_shouldTick
cdef list Tile_opaqueTileLookup
cdef list Tile_lightOpacity
cdef list Tile_isLiquid
cdef list Tile_tickSpeed

cdef class Tile:

    def __cinit__(self):
        if not self.shouldTick:
            self.shouldTick = [False] * 256
        if not self.opaqueTileLookup:
            self.opaqueTileLookup = [False] * 256
        if not self.lightOpacity:
            self.lightOpacity = [False] * 256
        if not self.isLiquid:
            self.isLiquid = [False] * 256
        if not self.tickSpeed:
            self.tickSpeed = [0] * 256

    def __init__(self, tiles, int id_, int tex=0):
        self.tiles = tiles
        self.explodeable = True
        self.id = id_
        if tex:
            self.tex = tex
        self._setShape(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        self.opaqueTileLookup[id_] = self.isSolid()
        self.lightOpacity[id_] = self.isOpaque()
        self.isLiquid[id_] = False

    @property
    def shouldTick(self):
        return Tile_shouldTick

    @shouldTick.setter
    def shouldTick(self, x):
        global Tile_shouldTick
        Tile_shouldTick = x

    @property
    def opaqueTileLookup(self):
        return Tile_opaqueTileLookup

    @opaqueTileLookup.setter
    def opaqueTileLookup(self, x):
        global Tile_opaqueTileLookup
        Tile_opaqueTileLookup = x

    @property
    def lightOpacity(self):
        return Tile_lightOpacity

    @lightOpacity.setter
    def lightOpacity(self, x):
        global Tile_lightOpacity
        Tile_lightOpacity = x

    @property
    def isLiquid(self):
        return Tile_isLiquid

    @isLiquid.setter
    def isLiquid(self, x):
        global Tile_isLiquid
        Tile_isLiquid = x

    @property
    def tickSpeed(self):
        return Tile_tickSpeed

    @tickSpeed.setter
    def tickSpeed(self, x):
        global Tile_tickSpeed
        Tile_tickSpeed = x

    cpdef bint isOpaque(self):
        return True

    def setSoundAndGravity(self, soundType, float volume, float gravity, float pitch):
        self.particleGravity = gravity
        self.soundType = soundType
        self.__destroyProgress = <int>(pitch * 20.0)
        return self

    def _setTicking(self, bint tick):
        self.shouldTick[self.id] = tick

    def _setShape(self, float minX, float minY, float minZ,
                  float maxX, float maxY, float maxZ):
        self.xx0 = minX
        self.yy0 = minY
        self.zz0 = minZ
        self.xx1 = maxX
        self.yy1 = maxY
        self.zz1 = maxZ

    cdef setTickSpeed(self, int rate):
        self.tickSpeed[self.id] = 16

    cpdef void render(self, Tesselator t) except *:
        t.colorFloat(0.5, 0.5, 0.5)
        self.renderFace(t, -2, 0, 0, 0)
        t.colorFloat(1.0, 1.0, 1.0)
        self.renderFace(t, -2, 0, 0, 1)
        t.colorFloat(0.8, 0.8, 0.8)
        self.renderFace(t, -2, 0, 0, 2)
        t.colorFloat(0.8, 0.8, 0.8)
        self.renderFace(t, -2, 0, 0, 3)
        t.colorFloat(0.6, 0.6, 0.6)
        self.renderFace(t, -2, 0, 0, 4)
        t.colorFloat(0.6, 0.6, 0.6)
        self.renderFace(t, -2, 0, 0, 5)

    cdef float _getBrightness(self, Level level, int x, int y, int z):
        return level.getBrightness(x, y, z)

    cpdef bint shouldRenderFace(self, Level level, int x, int y, int z, int layer):
        return not level.isSolidTile(x, y, z)

    cpdef int _getTexture(self, int face):
        return self.tex

    cpdef void renderFace(self, Tesselator t, int x, int y, int z, int face):
        self.renderFaceNoTexture(t, x, y, z, face, self._getTexture(face))

    cpdef void renderFaceNoTexture(self, Tesselator t, int x, int y, int z, int face, int tex):
        cdef int xt, yt
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

        xt = tex % 16 << 4
        yt = tex // 16 << 4
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = yt / 256.0
        v1 = (yt + 15.99) / 256.0
        if face >= 2 and tex < 240:
            if self.yy0 >= 0.0 and self.yy1 <= 1.0:
                v0 = (yt + self.yy0 * 15.99) / 256.0
                v1 = (yt + self.yy1 * 15.99) / 256.0
            else:
                v0 = yt / 256.0
                v1 = (yt + 15.99) / 256.0

        x0 = x + self.xx0
        x1 = x + self.xx1
        y0 = y + self.yy0
        y1 = y + self.yy1
        z0 = z + self.zz0
        z1 = z + self.zz1

        if face == 0:
            t.vertexUV(x0, y0, z1, u0, v1)
            t.vertexUV(x0, y0, z0, u0, v0)
            t.vertexUV(x1, y0, z0, u1, v0)
            t.vertexUV(x1, y0, z1, u1, v1)
        elif face == 1:
            t.vertexUV(x1, y1, z1, u1, v1)
            t.vertexUV(x1, y1, z0, u1, v0)
            t.vertexUV(x0, y1, z0, u0, v0)
            t.vertexUV(x0, y1, z1, u0, v1)
        elif face == 2:
            t.vertexUV(x0, y1, z0, u1, v0)
            t.vertexUV(x1, y1, z0, u0, v0)
            t.vertexUV(x1, y0, z0, u0, v1)
            t.vertexUV(x0, y0, z0, u1, v1)
        elif face == 3:
            t.vertexUV(x0, y1, z1, u0, v0)
            t.vertexUV(x0, y0, z1, u0, v1)
            t.vertexUV(x1, y0, z1, u1, v1)
            t.vertexUV(x1, y1, z1, u1, v0)
        elif face == 4:
            t.vertexUV(x0, y1, z1, u1, v0)
            t.vertexUV(x0, y1, z0, u0, v0)
            t.vertexUV(x0, y0, z0, u0, v1)
            t.vertexUV(x0, y0, z1, u1, v1)
        elif face == 5:
            t.vertexUV(x1, y0, z1, u0, v1)
            t.vertexUV(x1, y0, z0, u1, v1)
            t.vertexUV(x1, y1, z0, u1, v0)
            t.vertexUV(x1, y1, z1, u0, v0)

    cdef renderBackFace(self, Tesselator t, int x, int y, int z, int face):
        cdef int tex
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

        tex = self._getTexture(face)
        u0 = (tex % 16) / 16.0
        u1 = u0 + 0.0624375
        v0 = (tex // 16) / 16.0
        v1 = v0 + 0.0624375

        x0 = x + self.xx0
        x1 = x + self.xx1
        y0 = y + self.yy0
        y1 = y + self.yy1
        z0 = z + self.zz0
        z1 = z + self.zz1

        if face == 0:
            t.vertexUV(x1, y0, z1, u1, v1)
            t.vertexUV(x1, y0, z0, u1, v0)
            t.vertexUV(x0, y0, z0, u0, v0)
            t.vertexUV(x0, y0, z1, u0, v1)
        elif face == 1:
            t.vertexUV(x0, y1, z1, u0, v1)
            t.vertexUV(x0, y1, z0, u0, v0)
            t.vertexUV(x1, y1, z0, u1, v0)
            t.vertexUV(x1, y1, z1, u1, v1)
        elif face == 2:
            t.vertexUV(x0, y0, z0, u1, v1)
            t.vertexUV(x1, y0, z0, u0, v1)
            t.vertexUV(x1, y1, z0, u0, v0)
            t.vertexUV(x0, y1, z0, u1, v0)
        elif face == 3:
            t.vertexUV(x1, y1, z1, u1, v0)
            t.vertexUV(x1, y0, z1, u1, v1)
            t.vertexUV(x0, y0, z1, u0, v1)
            t.vertexUV(x0, y1, z1, u0, v0)
        elif face == 4:
            t.vertexUV(x0, y0, z1, u1, v1)
            t.vertexUV(x0, y0, z0, u0, v1)
            t.vertexUV(x0, y1, z0, u0, v0)
            t.vertexUV(x0, y1, z1, u1, v0)
        elif face == 5:
            t.vertexUV(x1, y1, z1, u0, v0)
            t.vertexUV(x1, y1, z0, u1, v0)
            t.vertexUV(x1, y0, z0, u1, v1)
            t.vertexUV(x1, y0, z1, u0, v1)

    def getAABB(self, int x, int y, int z):
        return AABB(x + self.xx0, y + self.yy0, z + self.zz0,
                    x + self.xx1, y + self.yy1, z + self.zz1)

    def getTileAABB(self, int x, int y, int z):
        return AABB(x + self.xx0, y + self.yy0, z + self.zz0,
                    x + self.xx1, y + self.yy1, z + self.zz1)

    cpdef bint blocksLight(self):
        return True

    cpdef bint isSolid(self):
        return True

    cpdef void tick(self, Level level, int x, int y, int z, random) except *:
        pass

    def destroy(self, Level level, int x, int y, int z, particleEngine):
        from mc.net.minecraft.particle.TerrainParticle import TerrainParticle
        cdef int SD, xx, yy, zz
        cdef float xp, yp, zp

        SD = 4
        for xx in range(SD):
            for yy in range(SD):
                for zz in range(SD):
                    xp = x + (xx + 0.5) / SD
                    yp = y + (yy + 0.5) / SD
                    zp = z + (zz + 0.5) / SD
                    particleEngine.addParticle(TerrainParticle(level, xp, yp, zp,
                                                        xp - x - 0.5,
                                                        yp - y - 0.5,
                                                        zp - z - 0.5, self))

    def addParticleOnBlockBreaking(self, Level level, int x, int y, int z,
                                   int sideHit, particleEngine):
        from mc.net.minecraft.particle.TerrainParticle import TerrainParticle
        cdef float f, xp, yp, zp

        f = 0.1
        xp = x + random.random() * (self.xx1 - self.xx0 - f * 2.0) + f + self.xx0
        yp = y + random.random() * (self.yy1 - self.yy0 - f * 2.0) + f + self.yy0
        zp = z + random.random() * (self.zz1 - self.zz0 - f * 2.0) + f + self.zz0
        if sideHit == 0:
            yp = y + self.yy0 - f
        elif sideHit == 1:
            yp = y + self.yy1 + f
        elif sideHit == 2:
            zp = z + self.zz0 - f
        elif sideHit == 3:
            zp = z + self.zz1 + f
        elif sideHit == 4:
            xp = x + self.xx0 - f
        elif sideHit == 5:
            xp = x + self.xx1 + f

        particleEngine.addParticle(TerrainParticle(level, xp, yp, zp,
                                            0.0, 0.0, 0.0,
                                            self).setPower(0.2).scale(0.6))

    cpdef int getLiquidType(self):
        return Liquid.none

    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *:
        pass

    def onPlace(self, Level level, int x, int y, int z):
        pass

    cdef int getTickDelay(self):
        return 0

    def onTileAdded(self, Level level, int x, int y, int z):
        pass

    def onTileRemoved(self, Level level, int x, int y, int z):
        pass

    cpdef int resourceCount(self):
        return 1

    def getDestroyProgress(self):
        return self.__destroyProgress

    def spawnResources(self, Level level, int x, int y, int z):
        self.wasExplodedResources(1.0)

    cdef wasExplodedResources(self, float chance):
        from mc.net.minecraft.item.Item import Item
        cdef int i
        cdef float f2, xx, yy, zz

        for i in range(self.resourceCount()):
            if random.random() > chance:
                continue

            random.random()
            random.random()
            random.random()

    def renderGuiTile(self, Tesselator t):
        cdef int i

        t.begin()
        for i in range(6):
            if i == 0:
                t.normal(0.0, 1.0, 0.0)
            elif i == 1:
                t.normal(0.0, -1.0, 0.0)
            elif i == 2:
                t.normal(0.0, 0.0, 1.0)
            elif i == 3:
                t.normal(0.0, 0.0, -1.0)
            elif i == 4:
                t.normal(1.0, 0.0, 0.0)
            elif i == 5:
                t.normal(-1.0, 0.0, 0.0)

            self.renderFace(t, 0, 0, 0, i)

        t.end()

    cdef bint isExplodeable(self):
        return self.explodeable

    cdef clip(self, int x, int y, int z, v0, v1):
        v0 = v0.add(-x, -y, -z)
        v1 = v1.add(-x, -y, -z)
        vec36 = v0.clipX(v1, self.xx0)
        vec37 = v0.clipX(v1, self.xx1)
        vec38 = v0.clipY(v1, self.yy0)
        vec39 = v0.clipY(v1, self.yy1)
        vec310 = v0.clipZ(v1, self.zz0)
        v1 = v0.clipZ(v1, self.zz1)
        if not self.__containsX(vec36):
            vec36 = None
        if not self.__containsX(vec37):
            vec37 = None
        if not self.__containsY(vec38):
            vec38 = None
        if not self.__containsY(vec39):
            vec39 = None
        if not self.__containsZ(vec310):
            vec310 = None
        if not self.__containsZ(v1):
            v1 = None

        vec311 = None
        if vec36:
            vec311 = vec36

        if vec37 and (not vec311 or v0.distanceTo(vec37) < v0.distanceTo(vec311)):
            vec311 = vec37
        if vec38 and (not vec311 or v0.distanceTo(vec38) < v0.distanceTo(vec311)):
            vec311 = vec38
        if vec39 and (not vec311 or v0.distanceTo(vec39) < v0.distanceTo(vec311)):
            vec311 = vec39
        if vec310 and (not vec311 or v0.distanceTo(vec310) < v0.distanceTo(vec311)):
            vec311 = vec310

        if v1 and (not vec311 or v0.distanceTo(v1) < v0.distanceTo(vec311)):
            vec311 = v1

        if not vec311:
            return

        cdef char v01 = -1
        if vec311 == vec36:
            v01 = 4
        elif vec311 == vec37:
            v01 = 5
        elif vec311 == vec38:
            v01 = 0
        elif vec311 == vec39:
            v01 = 1
        elif vec311 == vec310:
            v01 = 2
        elif vec311 == v1:
            v01 = 3

        return HitResult(x, y, z, v01, vec311.add(x, y, z))

    cdef bint __containsX(self, vec):
        if not vec:
            return False
        else:
            return vec.y >= self.yy0 and vec.y <= self.yy1 and vec.z >= self.zz0 and vec.z <= self.zz1

    cdef bint __containsY(self, vec):
        if not vec:
            return False
        else:
            return vec.x >= self.xx0 and vec.x <= self.xx1 and vec.z >= self.zz0 and vec.z <= self.zz1

    cdef bint __containsZ(self, vec):
        if not vec:
            return False
        else:
            return vec.x >= self.xx0 and vec.x <= self.xx1 and vec.y >= self.yy0 and vec.y <= self.yy1

    cpdef bint renderFull(self, Level level, int x, int y, int z, Tesselator t) except *:
        cdef float f8, f9, f10, b
        cdef bint layerOk

        layerOk = False
        f8 = 0.5
        f9 = 0.8
        f10 = 0.6
        if self.shouldRenderFace(level, x, y - 1, z, 0):
            b = self._getBrightness(level, x, y - 1, z)
            t.colorFloat(f8 * b, f8 * b, f8 * b)
            self.renderFace(t, x, y, z, 0)
            layerOk = True
        if self.shouldRenderFace(level, x, y + 1, z, 1):
            b = self._getBrightness(level, x, y + 1, z)
            t.colorFloat(b * 1.0, b * 1.0, b * 1.0)
            self.renderFace(t, x, y, z, 1)
            layerOk = True
        if self.shouldRenderFace(level, x, y, z - 1, 2):
            b = self._getBrightness(level, x, y, z - 1)
            t.colorFloat(f9 * b, f9 * b, f9 * b)
            self.renderFace(t, x, y, z, 2)
            layerOk = True
        if self.shouldRenderFace(level, x, y, z + 1, 3):
            b = self._getBrightness(level, x, y, z + 1)
            t.colorFloat(f9 * b, f9 * b, f9 * b)
            self.renderFace(t, x, y, z, 3)
            layerOk = True
        if self.shouldRenderFace(level, x - 1, y, z, 4):
            b = self._getBrightness(level, x - 1, y, z)
            t.colorFloat(f10 * b, f10 * b, f10 * b)
            self.renderFace(t, x, y, z, 4)
            layerOk = True
        if self.shouldRenderFace(level, x + 1, y, z, 5):
            b = self._getBrightness(level, x + 1, y, z)
            t.colorFloat(f10 * b, f10 * b, f10 * b)
            self.renderFace(t, x, y, z, 5)
            layerOk = True

        return layerOk

    cdef int getRenderLayer(self):
        return 0
