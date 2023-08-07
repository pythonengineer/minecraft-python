# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.particle.Particle import Particle
from mc.net.minecraft.phys.AABB import AABB

cdef class Tile:

    def __init__(self, tiles, int id_, int tex=0):
        self.tiles = tiles
        self.id = id_
        if tex:
            self.tex = tex

    cpdef void render(self, Tesselator t, level, int layer, int x, int y, int z) except *:
        cdef float c1 = 1.0
        cdef float c2 = 0.8
        cdef float c3 = 0.6

        if self.shouldRenderFace(level, x, y - 1, z, layer):
            t.colorRGB(c1, c1, c1)
            self.renderFace(t, x, y, z, 0)
        if self.shouldRenderFace(level, x, y + 1, z, layer):
            t.colorRGB(c1, c1, c1)
            self.renderFace(t, x, y, z, 1)
        if self.shouldRenderFace(level, x, y, z - 1, layer):
            t.colorRGB(c2, c2, c2)
            self.renderFace(t, x, y, z, 2)
        if self.shouldRenderFace(level, x, y, z + 1, layer):
            t.colorRGB(c2, c2, c2)
            self.renderFace(t, x, y, z, 3)
        if self.shouldRenderFace(level, x - 1, y, z, layer):
            t.colorRGB(c3, c3, c3)
            self.renderFace(t, x, y, z, 4)
        if self.shouldRenderFace(level, x + 1, y, z, layer):
            t.colorRGB(c3, c3, c3)
            self.renderFace(t, x, y, z, 5)

    cdef bint shouldRenderFace(self, level, int x, int y, int z, int layer):
        if not level.isSolidTile(x, y, z) and (level.isLit(x, y, z) ^ layer) == 1:
            return True
        else:
            return False

    cpdef int getTexture(self, int face):
        return self.tex

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
        cdef int tex
        cdef float u0, u1, v0, v1, x0, x1, y0, y1, z0, z1

        tex = self.getTexture(face)
        u0 = tex % 16 / 16.0
        u1 = u0 + 0.0624375
        v0 = tex // 16 / 16.0
        v1 = v0 + 0.0624375

        x0 = x + 0.0
        x1 = x + 1.0
        y0 = y + 0.0
        y1 = y + 1.0
        z0 = z + 0.0
        z1 = z + 1.0

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

    cpdef renderFaceNoTexture(self, Tesselator t, int x, int y, int z, int face):
        cdef float x0, x1, y0, y1, z0, z1

        x0 = x + 0.0
        x1 = x + 1.0
        y0 = y + 0.0
        y1 = y + 1.0
        z0 = z + 0.0
        z1 = z + 1.0

        if face == 0:
            t.vertex(x0, y0, z1)
            t.vertex(x0, y0, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x1, y0, z1)
        elif face == 1:
            t.vertex(x1, y1, z1)
            t.vertex(x1, y1, z0)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y1, z1)
        elif face == 2:
            t.vertex(x0, y1, z0)
            t.vertex(x1, y1, z0)
            t.vertex(x1, y0, z0)
            t.vertex(x0, y0, z0)
        elif face == 3:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y0, z1)
            t.vertex(x1, y0, z1)
            t.vertex(x1, y1, z1)
        elif face == 4:
            t.vertex(x0, y1, z1)
            t.vertex(x0, y1, z0)
            t.vertex(x0, y0, z0)
            t.vertex(x0, y0, z1)
        elif face == 5:
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
