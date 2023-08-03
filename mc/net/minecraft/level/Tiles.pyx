# cython: language_level=3

from mc.net.minecraft.level.Tile cimport Tile

cdef class Tiles:

    def __init__(self):
        self.rock = Tile(0)
        self.grass = Tile(1)

tiles = Tiles()
