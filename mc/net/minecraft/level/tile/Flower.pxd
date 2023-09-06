# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.renderer.Tesselator cimport Tesselator

cdef class Flower(Tile):

    cpdef void tick(self, Level level, int x, int y, int z, random) except *
    cpdef bint render(self, Tesselator t, Level level, int layer, int x, int y, int z) except *
    cdef void __renderFlower(self, Tesselator t, float x, float y, float z) except *
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cdef bint isOpaque(self)
