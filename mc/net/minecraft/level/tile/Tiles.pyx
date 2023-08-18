# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.FallingTile import FallingTile
from mc.net.minecraft.level.tile.LiquidTile cimport LiquidTile
from mc.net.minecraft.level.tile.CalmLiquidTile import CalmLiquidTile
from mc.net.minecraft.level.tile.SpongeTile import SpongeTile
from mc.net.minecraft.level.tile.GlassTile import GlassTile
from mc.net.minecraft.level.tile.GrassTile import GrassTile
from mc.net.minecraft.level.tile.DirtTile import DirtTile
from mc.net.minecraft.level.tile.LeafTile import LeafTile
from mc.net.minecraft.level.tile.LogTile import LogTile
from mc.net.minecraft.level.tile.Bush import Bush
from mc.net.minecraft.level.liquid.Liquid cimport Liquid

cdef class Tiles:

    def __init__(self):
        self.tiles = [None] * 256

        self.rock = Tile(self, 1, 1)
        self.rock.particleGravity = 1.0
        self.grass = GrassTile(self, 2)
        self.grass.particleGravity = 1.0
        self.dirt = DirtTile(self, 3, 2)
        self.dirt.particleGravity = 1.0
        stoneBrick = Tile(self, 4, 16)
        self.wood = Tile(self, 5, 4)
        self.wood.particleGravity = 1.0
        self.bush = Bush(self, 6)
        self.bush.particleGravity = 1.0
        self.unbreakable = Tile(self, 7, 17)
        self.unbreakable.particleGravity = 1.0

        self.water = LiquidTile(self, 8, Liquid.water)
        self.water.particleGravity = 1.0
        self.calmWater = CalmLiquidTile(self, 9, Liquid.water)
        self.calmWater.particleGravity = 1.0

        self.lava = LiquidTile(self, 10, Liquid.lava)
        self.lava.particleGravity = 1.0
        self.calmLava = CalmLiquidTile(self, 11, Liquid.lava)
        self.calmLava.particleGravity = 1.0

        self.sand = FallingTile(self, 12, 18)
        self.sand.particleGravity = 1.0
        self.gravel = FallingTile(self, 13, 19)
        self.gravel.particleGravity = 1.0

        self.oreGold = Tile(self, 14, 32)
        self.oreGold.particleGravity = 1.0
        self.oreIron = Tile(self, 15, 33)
        self.oreIron.particleGravity = 1.0
        self.oreCoal = Tile(self, 16, 34)
        self.oreCoal.particleGravity = 1.0

        self.log = LogTile(self, 17)
        self.log.particleGravity = 1.0
        self.leaf = LeafTile(self, 18, 22, True)
        self.leaf.particleGravity = 0.4

        self.sponge = SpongeTile(self, 19)
        self.sponge.particleGravity = 0.9
        self.glass = GlassTile(self, 20, 49, False)
        self.glass.particleGravity = 1.0

        self.tiles[1:20] = [self.rock, self.grass, self.dirt, stoneBrick, self.wood,
                            self.bush, self.unbreakable, self.water, self.calmWater,
                            self.lava, self.calmLava, self.sand, self.gravel, self.oreGold,
                            self.oreIron, self.oreCoal, self.log, self.leaf, self.sponge,
                            self.glass]

tiles = Tiles()
