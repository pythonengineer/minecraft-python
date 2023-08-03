# cython: language_level=3

from mc.net.minecraft.level.Tile cimport Tile

cdef class Tiles:

    cdef:
        public Tile rock
        public Tile grass
