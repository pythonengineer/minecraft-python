# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.Level cimport Level

cdef class Tile:

    cdef:
        public object tiles
        public int tex
        public int id
        public float particleGravity
        public object soundType
        int __destroyProgress

        float __xx0
        float __yy0
        float __zz0
        float __xx1
        float __yy1
        float __zz1

    cdef bint isOpaque(self)
    cdef setTickSpeed(self, int speed)
    cpdef bint render(self, Tesselator t, Level level, int layer, int x, int y, int z) except *
    cdef float _getBrightness(self, Level level, int x, int y, int z)
    cpdef bint shouldRenderFace(self, Level level, int x, int y, int z, int layer, int face)
    cpdef int _getTexture(self, int face)
    cpdef void renderFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef void renderFaceNoTexture(self, Tesselator t, int x, int y, int z, int face, int tex)
    cdef renderBlockFromSide(self, Tesselator t, int x, int y, int z, int face, int layer)
    cdef renderBackFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef void tick(self, Level level, int x, int y, int z, random) except *
    cpdef int getLiquidType(self)
    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *
    cdef int getTickDelay(self)
    cpdef int resourceCount(self)
    cpdef int getId(self)
    cdef wasExploded(self, Level level, int x, int y, int z, float f)
