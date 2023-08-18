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
        self.stoneBrick = Tile(self, 4, 16)
        self.stoneBrick.particleGravity = 1.0
        self.wood = Tile(self, 5, 4)
        self.wood.particleGravity = 1.0
        self.bush = Bush(self, 6, 15)
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

        self.clothRed = Tile(self, 21, 64)
        self.clothRed.particleGravity = 1.0
        self.clothOrange = Tile(self, 22, 65)
        self.clothOrange.particleGravity = 1.0
        self.clothYellow = Tile(self, 23, 66)
        self.clothYellow.particleGravity = 1.0
        self.clothChartreuse = Tile(self, 24, 67)
        self.clothChartreuse.particleGravity = 1.0
        self.clothGreen = Tile(self, 25, 68)
        self.clothGreen.particleGravity = 1.0
        self.clothSpringGreen = Tile(self, 26, 69)
        self.clothSpringGreen.particleGravity = 1.0
        self.clothCyan = Tile(self, 27, 70)
        self.clothCyan.particleGravity = 1.0
        self.clothCapri = Tile(self, 28, 71)
        self.clothCapri.particleGravity = 1.0
        self.clothUltramarine = Tile(self, 29, 72)
        self.clothUltramarine.particleGravity = 1.0
        self.clothViolet = Tile(self, 30, 73)
        self.clothViolet.particleGravity = 1.0
        self.clothPurple = Tile(self, 31, 74)
        self.clothPurple.particleGravity = 1.0
        self.clothMagenta = Tile(self, 32, 75)
        self.clothMagenta.particleGravity = 1.0
        self.clothRose = Tile(self, 33, 76)
        self.clothRose.particleGravity = 1.0
        self.clothDarkGray = Tile(self, 34, 77)
        self.clothDarkGray.particleGravity = 1.0
        self.clothGray = Tile(self, 35, 78)
        self.clothGray.particleGravity = 1.0
        self.clothWhite = Tile(self, 36, 79)
        self.clothWhite.particleGravity = 1.0

        self.plantYellow = Bush(self, 37, 13)
        self.plantYellow.particleGravity = 1.0
        self.plantRed = Bush(self, 38, 12)
        self.plantRed.particleGravity = 1.0

        self.mushroomBrown = Bush(self, 39, 29)
        self.mushroomBrown.particleGravity = 1.0
        self.mushroomRed = Bush(self, 40, 28)
        self.mushroomRed.particleGravity = 1.0

        self.blockGold = Tile(self, 41, 40)
        self.blockGold.particleGravity = 1.0

        self.tiles[1:41] = [self.rock, self.grass, self.dirt, self.stoneBrick, self.wood,
                            self.bush, self.unbreakable, self.water, self.calmWater,
                            self.lava, self.calmLava, self.sand, self.gravel, self.oreGold,
                            self.oreIron, self.oreCoal, self.log, self.leaf, self.sponge,
                            self.glass, self.clothRed, self.clothOrange, self.clothYellow,
                            self.clothChartreuse, self.clothGreen, self.clothSpringGreen,
                            self.clothCyan, self.clothCapri, self.clothUltramarine,
                            self.clothViolet, self.clothPurple, self.clothMagenta,
                            self.clothRose, self.clothDarkGray, self.clothGray,
                            self.clothWhite, self.plantYellow, self.plantRed,
                            self.mushroomBrown, self.mushroomRed, self.blockGold]

tiles = Tiles()
