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
from random import Random
from enum import Enum

_random = Random()

class SoundType(Enum):
    none = ('-', 0.0, 0.0)
    grass = ('grass', 0.6, 1.0)
    cloth = ('grass', 0.7, 1.2)
    gravel = ('gravel', 1.0, 1.0)
    stone = ('stone', 1.0, 1.0)
    metal = ('stone', 1.0, 2.0)
    wood = ('wood', 1.0, 1.0)

    def __init__(self, name, volume, pitch):
        Enum.__init__(self)
        self._name = name
        self.__volume = volume
        self.__pitch = pitch

    def getVolume(self):
        return self.__volume / (_random.random() * 0.4 + 1.0) * 0.5

    def getPitch(self):
        return self.__pitch / (_random.random() * 0.2 + 0.9)

cdef class Tiles:

    def __init__(self):
        self.tiles = [None] * 256

        self.rock = Tile(self, 1, 1)
        self.rock.setSoundAndGravity(SoundType.stone, 1.0, 1.0)

        self.grass = GrassTile(self, 2).setSoundAndGravity(SoundType.grass, 0.9, 1.0)
        self.dirt = DirtTile(self, 3, 2).setSoundAndGravity(SoundType.grass, 0.8, 1.0)
        self.wood = Tile(self, 4, 16).setSoundAndGravity(SoundType.stone, 1.0, 1.0)
        self.stoneBrick = Tile(self, 5, 4).setSoundAndGravity(SoundType.wood, 1.0, 1.0)
        self.bush = Bush(self, 6, 15).setSoundAndGravity(SoundType.none, 0.7, 1.0)
        self.unbreakable = Tile(self, 7, 17).setSoundAndGravity(SoundType.stone, 1.0, 1.0)

        self.water = LiquidTile(self, 8, Liquid.water).setSoundAndGravity(SoundType.none, 1.0, 1.0)
        self.calmWater = CalmLiquidTile(self, 9, Liquid.water).setSoundAndGravity(SoundType.none, 1.0, 1.0)

        self.lava = LiquidTile(self, 10, Liquid.lava).setSoundAndGravity(SoundType.none, 1.0, 1.0)
        self.calmLava = CalmLiquidTile(self, 11, Liquid.lava).setSoundAndGravity(SoundType.none, 1.0, 1.0)

        self.sand = FallingTile(self, 12, 18).setSoundAndGravity(SoundType.gravel, 0.8, 1.0)
        self.gravel = FallingTile(self, 13, 19).setSoundAndGravity(SoundType.gravel, 0.8, 1.0)

        self.oreGold = Tile(self, 14, 32).setSoundAndGravity(SoundType.stone, 1.0, 1.0)
        self.oreIron = Tile(self, 15, 33).setSoundAndGravity(SoundType.stone, 1.0, 1.0)
        self.oreCoal = Tile(self, 16, 34).setSoundAndGravity(SoundType.stone, 1.0, 1.0)

        self.log = LogTile(self, 17).setSoundAndGravity(SoundType.wood, 1.0, 1.0)
        self.leaf = LeafTile(self, 18, 22, True).setSoundAndGravity(SoundType.grass, 1.0, 0.4)

        self.sponge = SpongeTile(self, 19).setSoundAndGravity(SoundType.cloth, 1.0, 0.9)
        self.glass = GlassTile(self, 20, 49, False).setSoundAndGravity(SoundType.metal, 1.0, 1.0)

        self.clothRed = Tile(self, 21, 64).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothOrange = Tile(self, 22, 65).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothYellow = Tile(self, 23, 66).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothChartreuse = Tile(self, 24, 67).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothGreen = Tile(self, 25, 68).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothSpringGreen = Tile(self, 26, 69).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothCyan = Tile(self, 27, 70).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothCapri = Tile(self, 28, 71).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothUltramarine = Tile(self, 29, 72).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothViolet = Tile(self, 30, 73).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothPurple = Tile(self, 31, 74).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothMagenta = Tile(self, 32, 75).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothRose = Tile(self, 33, 76).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothDarkGray = Tile(self, 34, 77).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothGray = Tile(self, 35, 78).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)
        self.clothWhite = Tile(self, 36, 79).setSoundAndGravity(SoundType.cloth, 1.0, 1.0)

        self.plantYellow = Bush(self, 37, 13).setSoundAndGravity(SoundType.none, 0.7, 1.0)
        self.plantRed = Bush(self, 38, 12).setSoundAndGravity(SoundType.none, 0.7, 1.0)

        self.mushroomBrown = Bush(self, 39, 29).setSoundAndGravity(SoundType.none, 0.7, 1.0)
        self.mushroomRed = Bush(self, 40, 28).setSoundAndGravity(SoundType.none, 0.7, 1.0)

        self.blockGold = Tile(self, 41, 40).setSoundAndGravity(SoundType.metal, 0.7, 1.0)

        self.tiles[1:41] = [self.rock, self.grass, self.dirt, self.wood, self.stoneBrick,
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
