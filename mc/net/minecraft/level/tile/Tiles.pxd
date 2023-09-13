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
        public Tile goldOre
        public Tile ironOre
        public Tile coalOre
        public Tile log
        public Tile leaf
        public Tile sponge
        public Tile glass
        public Tile clothRed
        public Tile clothOrange
        public Tile clothYellow
        public Tile clothChartreuse
        public Tile clothGreen
        public Tile clothSpringGreen
        public Tile clothCyan
        public Tile clothCapri
        public Tile clothUltramarine
        public Tile clothViolet
        public Tile clothPurple
        public Tile clothMagenta
        public Tile clothRose
        public Tile clothDarkGray
        public Tile clothGray
        public Tile clothWhite
        public Tile flower
        public Tile rose
        public Tile mushroomBrown
        public Tile mushroomRed
        public Tile gold
        public Tile iron
        public Tile slabFull
        public Tile slabHalf
        public Tile brick
        public Tile tnt
        public Tile bookshelf
        public Tile mossStone
        public Tile obsidian
