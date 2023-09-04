# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.tile.Tile cimport Tile

cdef class LiquidTile(Tile):

    cdef:
        public int _liquid
        public int _calmTileId
        public int _tileId

    cdef bint isOpaque(self)
    cpdef void tick(self, level, int x, int y, int z, random) except *
    cdef bint __checkSponge(self, level, int x, int y, int z)
    cdef bint __checkWater(self, level, int x, int y, int z)
    cdef float _getBrightness(self, level, int x, int y, int z)
    cpdef bint shouldRenderFace(self, level, int x, int y, int z, int layer, int face)
    cpdef void renderFace(self, Tesselator t, int x, int y, int z, int face)
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef int getLiquidType(self)
    cpdef void neighborChanged(self, level, int x, int y, int z, int type_) except *
    cdef int getTickDelay(self)
    cdef wasExploded(self, level, int x, int y, int z, float f)
    cpdef int getResourceCount(self)
