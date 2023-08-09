# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.tile.Tile cimport Tile

cdef class LiquidTile(Tile):

    cdef:
        public int _liquidType
        public int _calmTileId
        public int _tileId

    cpdef void tick(self, level, int x, int y, int z, random) except *
    cdef bint __checkWater(self, level, int x, int y, int z)
    cdef bint _shouldRenderFace(self, level, int x, int y, int z, int layer, int face)
    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face)
    cdef bint mayPick(self)
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef int getLiquidType(self)
    cpdef void neighborChanged(self, level, int x, int y, int z, int type_) except *