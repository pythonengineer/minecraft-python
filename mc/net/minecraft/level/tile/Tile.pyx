# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.particle.Particle import Particle
from mc.net.minecraft.phys.AABB import AABB

cdef list Tile_shouldTick

cdef class Tile:
    NOT_LIQUID = 0
    LIQUID_WATER = 1
    LIQUID_LAVA = 2

    property shouldTick:

        def __get__(self):
            return Tile_shouldTick

        def __set__(self, x):
            global Tile_shouldTick
            Tile_shouldTick = x

    def __cinit__(self):
        if not self.shouldTick:
            self.shouldTick = [False] * 256

    def __init__(self, tiles, int id_, int tex=0):
        self.tiles = tiles
        self.id = id_
        if tex:
            self.tex = tex
        self._setShape(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)

    def _setTicking(self, bint tick):
        self.shouldTick[self.id] = tick

    def _setShape(self, float x0, float y0, float z0, float x1, float y1, float z1):
        self.__xx0 = 0.0
        self.__yy0 = y0
        self.__zz0 = 0.0
        self.__xx1 = 1.0
        self.__yy1 = y1
        self.__zz1 = 1.0

    cpdef bint render(self, Tesselator t, level, int layer, int x, int y, int z) except *:
        cdef char c1 = -1
        cdef char c2 = -52
        cdef char c3 = -103
        cdef bint layerOk = False

        if self._shouldRenderFace(level, x, y - 1, z, layer, 0):
            t.colorByte(c1, c1, c1)
            self.renderFace(t, x, y, z, 0)
            layerOk = True
        if self._shouldRenderFace(level, x, y + 1, z, layer, 1):
            t.colorByte(c1, c1, c1)
            self.renderFace(t, x, y, z, 1)
            layerOk = True
        if self._shouldRenderFace(level, x, y, z - 1, layer, 2):
            t.colorByte(c2, c2, c2)
            self.renderFace(t, x, y, z, 2)
            layerOk = True
        if self._shouldRenderFace(level, x, y, z + 1, layer, 3):
            t.colorByte(c2, c2, c2)
            self.renderFace(t, x, y, z, 3)
            layerOk = True
        if self._shouldRenderFace(level, x - 1, y, z, layer, 4):
            t.colorByte(c3, c3, c3)
            self.renderFace(t, x, y, z, 4)
            layerOk = True
        if self._shouldRenderFace(level, x + 1, y, z, layer, 5):
            t.colorByte(c3, c3, c3)
            self.renderFace(t, x, y, z, 5)
            layerOk = True

        return layerOk

    cdef bint _shouldRenderFace(self, level, int x, int y, int z, int layer, int face):
        cdef bint layerOk = True
        if layer == 2:
            return False
        if layer >= 0:
            layerOk = level.isLit(x, y, z) ^ layer == 1

        tile = self.tiles.tiles[level.getTile(x, y, z)]
        return not (False if tile is None else tile.isSolid()) and layerOk

    cpdef int _getTexture(self, int face):
        return self.tex

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
        cdef int tex
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

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

    cpdef renderBackFace(self, Tesselator t, int x, int y, int z, int face):
        cdef int tex
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

        tex = self._getTexture(face)
        u0 = tex % 16 / 16.0
        u1 = u0 + 0.0624375
        v0 = tex // 16 / 16.0
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

    cpdef renderFaceNoTexture(self, player, Tesselator t, int x, int y, int z, int face):
        cdef float x0, x1, y0, y1, z0, z1

        x0 = x + 0.0
        x1 = x + 1.0
        y0 = y + 0.0
        y1 = y + 1.0
        z0 = z + 0.0
        z1 = z + 1.0

        if face == 0 and y > player.y:
            t.vertex(x0, y0, z1)
            t.vertex(x0, y0, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x1, y0, z1)
        elif face == 1 and y < player.y:
            t.vertex(x1, y1, z1)
            t.vertex(x1, y1, z0)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y1, z1)
        elif face == 2 and z > player.z:
            t.vertex(x0, y1, z0)
            t.vertex(x1, y1, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x0, y0, z0)
        elif face == 3 and z < player.z:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y0, z1)
            t.vertex(x1, y0, z1)
            t.vertex(x1, y1, z1)
        elif face == 4 and x > player.x:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y0, z0)
            t.vertex(x0, y0, z1)
        elif face == 5 and x < player.x:
            t.vertex(x1, y0, z1)
            t.vertex(x1, y0, z0)
            t.vertex(x1, y1, z0)
            t.vertex(x1, y1, z1)

    def getTileAABB(self, int x, int y, int z):
        return AABB(x, y, z, x + 1, y + 1, z + 1)

    def getAABB(self, int x, int y, int z):
        return AABB(x, y, z, x + 1, y + 1, z + 1)

    cpdef bint blocksLight(self):
        return True

    cpdef bint isSolid(self):
        return True

    def mayPick(self):
        return True

    cpdef void tick(self, level, int x, int y, int z, random) except *:
        pass

    def destroy(self, level, int x, int y, int z, particleEngine):
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
                                                zp - z - 0.5, self.tex))

    cpdef int getLiquidType(self):
        return 0

    cpdef void neighborChanged(self, level, int x, int y, int z, int type_) except *:
        pass
