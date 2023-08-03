# cython: language_level=3

from mc.net.minecraft.level.Tesselator cimport Tesselator
from mc.net.minecraft.level.Level cimport Level

cdef class Tile:

    cdef:
        public int tex

    cpdef render(self, Tesselator t, Level level, int layer, int x, int y, int z)
    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face)
