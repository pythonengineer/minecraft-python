# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.LiquidTile cimport LiquidTile

cdef class Tiles:

    cdef:
        public list tiles

        public Tile rock
        public Tile grass
        public Tile dirt
        public Tile stoneBrick
        public Tile wood
        public Tile bush
        public Tile unbreakable
        public LiquidTile water
        public LiquidTile calmWater
        public LiquidTile lava
        public LiquidTile calmLava
        public Tile sand
        public Tile gravel
        public Tile oreGold
        public Tile oreIron
        public Tile oreCoal
        public Tile log
        public Tile leaf
