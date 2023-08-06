# cython: language_level=3

from mc.net.minecraft.level.Tesselator cimport Tesselator

cdef class Tile:

    cdef:
        public object tiles
        public int tex
        public int id

    cpdef void render(self, Tesselator t, level, int layer, int x, int y, int z) except *
    cdef bint shouldRenderFace(self, level, int x, int y, int z, int layer)
    cpdef int getTexture(self, int face)
    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef renderFaceNoTexture(self, Tesselator t, int x, int y, int z, int face)
    cdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef void tick(self, level, int x, int y, int z, random) except *
