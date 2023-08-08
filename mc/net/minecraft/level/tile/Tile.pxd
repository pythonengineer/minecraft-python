# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator

cdef class Tile:

    cdef:
        public object tiles
        public int tex
        public int id

        public float _xx0
        public float _yy0
        public float _zz0
        public float _xx1
        public float _yy1
        public float _zz1

    cpdef void render(self, Tesselator t, level, int layer, int x, int y, int z) except *
    cdef bint _shouldRenderFace(self, level, int x, int y, int z, int layer, int face)
    cpdef int _getTexture(self, int face)
    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef renderBackFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef renderFaceNoTexture(self, player, Tesselator t, int x, int y, int z, int face)
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef void tick(self, level, int x, int y, int z, random) except *
    cpdef int getLiquidType(self)
    cpdef void neighborChanged(self, level, int x, int y, int z, int type_) except *
