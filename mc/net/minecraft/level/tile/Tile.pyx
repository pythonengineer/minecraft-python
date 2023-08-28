# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.liquid.Liquid cimport Liquid
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.particle.Particle import Particle
from mc.net.minecraft.phys.AABB import AABB

cdef list Tile_shouldTick
cdef list Tile_tickSpeed

cdef class Tile:

    property shouldTick:

        def __get__(self):
            return Tile_shouldTick

        def __set__(self, x):
            global Tile_shouldTick
            Tile_shouldTick = x

    property tickSpeed:

        def __get__(self):
            return Tile_tickSpeed

        def __set__(self, x):
            global Tile_tickSpeed
            Tile_tickSpeed = x

    def __cinit__(self):
        if not self.shouldTick:
            self.shouldTick = [False] * 256
        if not self.tickSpeed:
            self.tickSpeed = [0] * 256

    def __init__(self, tiles, int id_, int tex=0):
        self.tiles = tiles
        self.id = id_
        if tex:
            self.tex = tex
        self._setShape(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)

    def setSoundAndGravity(self, soundType, f2, particleGravity):
        self.particleGravity = particleGravity
        self.soundType = soundType
        return self

    def _setTicking(self, bint tick):
        self.shouldTick[self.id] = tick

    def _setShape(self, float x0, float y0, float z0, float x1, float y1, float z1):
        self.__xx0 = x0
        self.__yy0 = y0
        self.__zz0 = z0
        self.__xx1 = x1
        self.__yy1 = y1
        self.__zz1 = z1

    cdef setTickSpeed(self, int speed):
        self.tickSpeed[self.id] = 16

    cpdef bint render(self, Tesselator t, Level level, int layer, int x, int y, int z) except *:
        cdef float f8, f9, f10, f11
        cdef bint layerOk

        layerOk = False
        f8 = 0.5
        f9 = 0.8
        f10 = 0.6
        if self._shouldRenderFace(level, x, y - 1, z, layer, 0):
            f11 = self._getBrightness(level, x, y - 1, z)
            t.colorFloat(f8 * f11, f8 * f11, f8 * f11)
            self.renderFace(t, x, y, z, 0)
            layerOk = True
        if self._shouldRenderFace(level, x, y + 1, z, layer, 1):
            f11 = self._getBrightness(level, x, y + 1, z)
            t.colorFloat(f11 * 1.0, f11 * 1.0, f11 * 1.0)
            self.renderFace(t, x, y, z, 1)
            layerOk = True
        if self._shouldRenderFace(level, x, y, z - 1, layer, 2):
            f11 = self._getBrightness(level, x, y, z - 1)
            t.colorFloat(f9 * f11, f9 * f11, f9 * f11)
            self.renderFace(t, x, y, z, 2)
            layerOk = True
        if self._shouldRenderFace(level, x, y, z + 1, layer, 3):
            f11 = self._getBrightness(level, x, y, z + 1)
            t.colorFloat(f9 * f11, f9 * f11, f9 * f11)
            self.renderFace(t, x, y, z, 3)
            layerOk = True
        if self._shouldRenderFace(level, x - 1, y, z, layer, 4):
            f11 = self._getBrightness(level, x - 1, y, z)
            t.colorFloat(f10 * f11, f10 * f11, f10 * f11)
            self.renderFace(t, x, y, z, 4)
            layerOk = True
        if self._shouldRenderFace(level, x + 1, y, z, layer, 5):
            f11 = self._getBrightness(level, x + 1, y, z)
            t.colorFloat(f10 * f11, f10 * f11, f10 * f11)
            self.renderFace(t, x, y, z, 5)
            layerOk = True

        return layerOk

    cdef float _getBrightness(self, Level level, int x, int y, int z):
        return level.getBrightness(x, y, z)

    cpdef bint _shouldRenderFace(self, Level level, int x, int y, int z, int layer, int face):
        return False if layer == 1 else not level.isSolidTile(x, y, z)

    cpdef int _getTexture(self, int face):
        return self.tex

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
        cdef int tex
        cdef float xt, yt, u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

        tex = self._getTexture(face)
        xt = tex % 16 * 16
        yt = tex // 16 * 16
        u0 = xt / 256.0
        u1 = (xt + 15.99) / 256.0
        v0 = yt / 256.0
        v1 = (yt + 15.99) / 256.0

        x0 = x + self.__xx0
        x1 = x + self.__xx1
        y0 = y + self.__yy0
        y1 = y + self.__yy1
        z0 = z + self.__zz0
        z1 = z + self.__zz1

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

        x0 = x + self.__xx0
        x1 = x + self.__xx1
        y0 = y + self.__yy0
        y1 = y + self.__yy1
        z0 = z + self.__zz0
        z1 = z + self.__zz1

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

    @staticmethod
    def renderFaceNoTexture(entity, Tesselator t, int x, int y, int z, int face):
        cdef float x0, x1, y0, y1, z0, z1

        x0 = x + 0.0
        x1 = x + 1.0
        y0 = y + 0.0
        y1 = y + 1.0
        z0 = z + 0.0
        z1 = z + 1.0

        if face == 0 and y > entity.y:
            t.vertex(x0, y0, z1)
            t.vertex(x0, y0, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x1, y0, z1)
        elif face == 1 and y < entity.y:
            t.vertex(x1, y1, z1)
            t.vertex(x1, y1, z0)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y1, z1)
        elif face == 2 and z > entity.z:
            t.vertex(x0, y1, z0)
            t.vertex(x1, y1, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x0, y0, z0)
        elif face == 3 and z < entity.z:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y0, z1)
            t.vertex(x1, y0, z1)
            t.vertex(x1, y1, z1)
        elif face == 4 and x > entity.x:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y0, z0)
            t.vertex(x0, y0, z1)
        elif face == 5 and x < entity.x:
            t.vertex(x1, y0, z1)
            t.vertex(x1, y0, z0)
            t.vertex(x1, y1, z0)
            t.vertex(x1, y1, z1)

    def getTileAABB(self, int x, int y, int z):
        return AABB(x, y, z, x + 1, y + 1, z + 1)

    cpdef bint blocksLight(self):
        return True

    cpdef bint isSolid(self):
        return True

    cpdef void tick(self, Level level, int x, int y, int z, random) except *:
        pass

    def destroy(self, Level level, int x, int y, int z, particleEngine):
        cdef int SD, xx, yy, zz
        cdef float xp, yp, zp

        SD = 4
        for xx in range(SD):
            for yy in range(SD):
                for zz in range(SD):
                    xp = x + (xx + 0.5) / SD
                    yp = y + (yy + 0.5) / SD
                    zp = z + (zz + 0.5) / SD
                    particleEngine.add(Particle(level, xp, yp, zp,
                                                xp - x - 0.5,
                                                yp - y - 0.5,
                                                zp - z - 0.5, self))

    cpdef int getLiquidType(self):
        return Liquid.none

    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *:
        pass

    def onBlockAdded(self, Level level, int x, int y, int z):
        pass

    cdef int getTickDelay(self):
        return 0

    def onTileAdded(self, Level level, int x, int y, int z):
        pass

    def onTileRemoved(self, Level level, int x, int y, int z):
        pass
