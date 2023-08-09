# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.FallingTile import FallingTile
from mc.net.minecraft.level.tile.LiquidTile cimport LiquidTile
from mc.net.minecraft.level.tile.CalmLiquidTile import CalmLiquidTile
from mc.net.minecraft.level.tile.GrassTile import GrassTile
from mc.net.minecraft.level.tile.DirtTile import DirtTile
from mc.net.minecraft.level.tile.LeafTile import LeafTile
from mc.net.minecraft.level.tile.LogTile import LogTile
from mc.net.minecraft.level.tile.Bush import Bush

cdef class Tiles:

    def __init__(self):
        self.tiles = [None] * 256

        self.rock = Tile(self, 1, 1)
        self.grass = GrassTile(self, 2)
        self.dirt = DirtTile(self, 3, 2)
        self.stoneBrick = Tile(self, 4, 16)
        self.wood = Tile(self, 5, 4)
        self.bush = Bush(self, 6)
        self.unbreakable = Tile(self, 7, 17)

        self.water = LiquidTile(self, 8, 1)
        self.calmWater = CalmLiquidTile(self, 9, 1)

        self.lava = LiquidTile(self, 10, 2)
        self.calmLava = CalmLiquidTile(self, 11, 2)

        self.sand = FallingTile(self, 12, 18)
        self.gravel = FallingTile(self, 13, 19)

        self.oreGold = Tile(self, 14, 32)
        self.oreIron = Tile(self, 15, 33)
        self.oreCoal = Tile(self, 16, 34)

        self.log = LogTile(self, 17)
        self.leaf = LeafTile(self, 18, 22)

        self.tiles[1:18] = [self.rock, self.grass, self.dirt, self.stoneBrick, self.wood,
                           self.bush, self.unbreakable, self.water, self.calmWater,
                           self.lava, self.calmLava, self.sand, self.gravel, self.oreGold,
                           self.oreIron, self.oreCoal, self.log, self.leaf]

tiles = Tiles()
