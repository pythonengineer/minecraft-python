# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile

cdef class Tiles:

    cdef:
        public list tiles

        public Tile rock
        public Tile grass
        public Tile dirt
        public Tile stoneBrick
        public Tile wood
        public Tile bush
