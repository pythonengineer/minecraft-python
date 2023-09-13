# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.renderer.Tesselator cimport Tesselator

cdef class Flower(Tile):

    cpdef void tick(self, Level level, int x, int y, int z, random) except *
    cdef void __renderFlower(self, Tesselator t, float x, float y, float z) except *
    cpdef bint blocksLight(self)
    cpdef bint isSolid(self)
    cpdef bint isOpaque(self)
    cpdef bint renderFull(self, Level level, int x, int y, int z, Tesselator t) except *
    cpdef void render(self, Tesselator t) except *
