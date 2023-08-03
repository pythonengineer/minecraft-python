# cython: language_level=3

from mc.net.minecraft.level.Tesselator cimport Tesselator
from mc.net.minecraft.level.Level cimport Level

cdef class Tile:

    def __init__(self, int tex):
        self.tex = tex

    cpdef render(self, Tesselator t, Level level, int layer, int x, int y, int z):
        cdef float u0, u1, v0, v1, c1, c2, c3, x0, x1, y0, y1, z0, z1, br

        u0 = self.tex / 16.0
        u1 = u0 + 0.0624375
        v0 = 0.0
        v1 = v0 + 0.0624375
        c1 = 1.0
        c2 = 0.8
        c3 = 0.6

        x0 = x + 0.0
        x1 = x + 1.0
        y0 = y + 0.0
        y1 = y + 1.0
        z0 = z + 0.0
        z1 = z + 1.0

        if not level.isSolidTile(x, y - 1, z):
            br = level.getBrightness(x, y - 1, z) * c1
            if (1 if br == c1 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u0, v1)
                t.vertex(x0, y0, z1)
                t.tex(u0, v0)
                t.vertex(x0, y0, z0)
                t.tex(u1, v0)
                t.vertex(x1, y0, z0)
                t.tex(u1, v1)
                t.vertex(x1, y0, z1)
        if not level.isSolidTile(x, y + 1, z):
            br = level.getBrightness(x, y, z) * c1
            if (1 if br == c1 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u1, v1)
                t.vertex(x1, y1, z1)
                t.tex(u1, v0)
                t.vertex(x1, y1, z0)
                t.tex(u0, v0)
                t.vertex(x0, y1, z0)
                t.tex(u0, v1)
                t.vertex(x0, y1, z1)
        if not level.isSolidTile(x, y, z - 1):
            br = level.getBrightness(x, y, z - 1) * c2
            if (1 if br == c2 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u1, v0)
                t.vertex(x0, y1, z0)
                t.tex(u0, v0)
                t.vertex(x1, y1, z0)
                t.tex(u0, v1)
                t.vertex(x1, y0, z0)
                t.tex(u1, v1)
                t.vertex(x0, y0, z0)
        if not level.isSolidTile(x, y, z + 1):
            br = level.getBrightness(x, y, z + 1) * c2
            if (1 if br == c2 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u0, v0)
                t.vertex(x0, y1, z1)
                t.tex(u0, v1)
                t.vertex(x0, y0, z1)
                t.tex(u1, v1)
                t.vertex(x1, y0, z1)
                t.tex(u1, v0)
                t.vertex(x1, y1, z1)
        if not level.isSolidTile(x - 1, y, z):
            br = level.getBrightness(x - 1, y, z) * c3
            if (1 if br == c3 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u1, v0)
                t.vertex(x0, y1, z1)
                t.tex(u0, v0)
                t.vertex(x0, y1, z0)
                t.tex(u0, v1)
                t.vertex(x0, y0, z0)
                t.tex(u1, v1)
                t.vertex(x0, y0, z1)
        if not level.isSolidTile(x + 1, y, z):
            br = level.getBrightness(x + 1, y, z) * c3
            if (1 if br == c3 else 0) ^ (1 if layer == 1 else 0) != 0:
                t.color(br, br, br)
                t.tex(u0, v1)
                t.vertex(x1, y0, z1)
                t.tex(u1, v1)
                t.vertex(x1, y0, z0)
                t.tex(u1, v0)
                t.vertex(x1, y1, z0)
                t.tex(u0, v0)
                t.vertex(x1, y1, z1)

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
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
