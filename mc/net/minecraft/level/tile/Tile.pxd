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
        public bint explodeable

        public float xx0
        public float yy0
        public float zz0
        public float xx1
        public float yy1
        public float zz1

    cpdef bint isOpaque(self)
    cdef setTickSpeed(self, int speed)
    cpdef void render(self, Tesselator t) except *
    cdef float _getBrightness(self, Level level, int x, int y, int z)
    cpdef bint shouldRenderFace(self, Level level, int x, int y, int z, int layer)
    cpdef int _getTexture(self, int face)
    cpdef void renderFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef void renderFaceNoTexture(self, Tesselator t, int x, int y, int z, int face, int tex)
    cdef renderBackFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef void tick(self, Level level, int x, int y, int z, random) except *
    cpdef int getLiquidType(self)
    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *
    cdef int getTickDelay(self)
    cpdef int resourceCount(self)
    cdef wasExplodedResources(self, float chance)
    cdef bint isExplodeable(self)
    cdef clip(self, int x, int y, int z, v0, v1)
    cdef bint __containsX(self, vec)
    cdef bint __containsY(self, vec)
    cdef bint __containsZ(self, vec)
    cpdef bint renderFull(self, Level level, int x, int y, int z, Tesselator t) except *
    cdef int getRenderLayer(self)
