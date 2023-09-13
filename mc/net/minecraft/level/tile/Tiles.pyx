# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.FallingTile import FallingTile
from mc.net.minecraft.level.tile.LiquidTile cimport LiquidTile
from mc.net.minecraft.level.tile.CalmLiquidTile import CalmLiquidTile
from mc.net.minecraft.level.tile.BookshelfTile import BookshelfTile
from mc.net.minecraft.level.tile.SpongeTile import SpongeTile
from mc.net.minecraft.level.tile.Mushroom import Mushroom
from mc.net.minecraft.level.tile.Flower import Flower
from mc.net.minecraft.level.tile.GlassTile import GlassTile
from mc.net.minecraft.level.tile.GrassTile import GrassTile
from mc.net.minecraft.level.tile.DirtTile import DirtTile
from mc.net.minecraft.level.tile.LeafTile import LeafTile
from mc.net.minecraft.level.tile.LogTile import LogTile
from mc.net.minecraft.level.tile.OreTile import OreTile
from mc.net.minecraft.level.tile.MetalTile import MetalTile
from mc.net.minecraft.level.tile.SlabTile import SlabTile
from mc.net.minecraft.level.tile.StoneTile import StoneTile
from mc.net.minecraft.level.tile.TntTile import TntTile
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
        self.soundName = name
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
        self.rock.setSoundAndGravity(SoundType.stone, 1.0, 1.0, 1.0)
        self.rock.explodeable = False

        self.grass = GrassTile(self, 2).setSoundAndGravity(SoundType.grass, 0.9, 1.0, 0.6)
        self.dirt = DirtTile(self, 3, 2).setSoundAndGravity(SoundType.grass, 0.8, 1.0, 0.5)
        self.stoneBrick = Tile(self, 4, 16).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 2.0)
        self.stoneBrick.explodeable = False
        self.wood = Tile(self, 5, 4).setSoundAndGravity(SoundType.wood, 1.0, 1.0, 2.0)
        self.bush = Bush(self, 6, 15).setSoundAndGravity(SoundType.none, 0.7, 1.0, 0.0)
        self.unbreakable = Tile(self, 7, 17).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 100.0)
        self.unbreakable.explodeable = False

        self.water = LiquidTile(self, 8, Liquid.water).setSoundAndGravity(SoundType.none, 1.0, 1.0, 100.0)
        self.calmWater = CalmLiquidTile(self, 9, Liquid.water).setSoundAndGravity(SoundType.none, 1.0, 1.0, 100.0)

        self.lava = LiquidTile(self, 10, Liquid.lava).setSoundAndGravity(SoundType.none, 1.0, 1.0, 100.0)
        self.calmLava = CalmLiquidTile(self, 11, Liquid.lava).setSoundAndGravity(SoundType.none, 1.0, 1.0, 100.0)

        self.sand = FallingTile(self, 12, 18).setSoundAndGravity(SoundType.gravel, 0.8, 1.0, 0.5)
        self.gravel = FallingTile(self, 13, 19).setSoundAndGravity(SoundType.gravel, 0.8, 1.0, 0.6)

        self.goldOre = OreTile(self, 14, 32).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 3.0)
        self.goldOre.explodeable = False
        self.ironOre = OreTile(self, 15, 33).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 3.0)
        self.ironOre.explodeable = False
        self.coalOre = OreTile(self, 16, 34).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 3.0)
        self.coalOre.explodeable = False

        self.log = LogTile(self, 17).setSoundAndGravity(SoundType.wood, 1.0, 1.0, 2.5)
        self.leaf = LeafTile(self, 18, 22).setSoundAndGravity(SoundType.grass, 1.0, 0.4, 0.2)

        self.sponge = SpongeTile(self, 19).setSoundAndGravity(SoundType.cloth, 1.0, 0.9, 0.6)
        self.glass = GlassTile(self, 20, 49, False).setSoundAndGravity(SoundType.metal, 1.0, 1.0, 0.3)

        self.clothRed = Tile(self, 21, 64).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothOrange = Tile(self, 22, 65).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothYellow = Tile(self, 23, 66).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothChartreuse = Tile(self, 24, 67).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothGreen = Tile(self, 25, 68).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothSpringGreen = Tile(self, 26, 69).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothCyan = Tile(self, 27, 70).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothCapri = Tile(self, 28, 71).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothUltramarine = Tile(self, 29, 72).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothViolet = Tile(self, 30, 73).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothPurple = Tile(self, 31, 74).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothMagenta = Tile(self, 32, 75).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothRose = Tile(self, 33, 76).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothDarkGray = Tile(self, 34, 77).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothGray = Tile(self, 35, 78).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)
        self.clothWhite = Tile(self, 36, 79).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.8)

        self.flower = Flower(self, 37, 13).setSoundAndGravity(SoundType.none, 0.7, 1.0, 0.0)
        self.rose = Flower(self, 38, 12).setSoundAndGravity(SoundType.none, 0.7, 1.0, 0.0)

        self.mushroomBrown = Mushroom(self, 39, 29).setSoundAndGravity(SoundType.none, 0.7, 1.0, 0.0)
        self.mushroomRed = Mushroom(self, 40, 28).setSoundAndGravity(SoundType.none, 0.7, 1.0, 0.0)

        self.gold = MetalTile(self, 41, 40).setSoundAndGravity(SoundType.metal, 0.7, 1.0, 3.0)
        self.gold.explodeable = False
        self.iron = MetalTile(self, 42, 39).setSoundAndGravity(SoundType.metal, 0.7, 1.0, 5.0)
        self.iron.explodeable = False

        self.slabFull = SlabTile(self, 43, True).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 2.0)
        self.slabFull.explodeable = False
        self.slabHalf = SlabTile(self, 44, False).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 2.0)
        self.slabHalf.explodeable = False

        self.brick = Tile(self, 45, 7).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 2.0)
        self.brick.explodeable = False

        self.tnt = TntTile(self, 46, 8).setSoundAndGravity(SoundType.cloth, 1.0, 1.0, 0.0)

        self.bookshelf = BookshelfTile(self, 47, 35).setSoundAndGravity(SoundType.wood, 1.0, 1.0, 1.5)

        self.mossStone = Tile(self, 48, 36).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 1.0)
        self.mossStone.explodeable = False
        self.obsidian = StoneTile(self, 49, 37).setSoundAndGravity(SoundType.stone, 1.0, 1.0, 1.0)
        self.obsidian.explodeable = False

        self.tiles[1:49] = [self.rock, self.grass, self.dirt, self.stoneBrick, self.wood,
                            self.bush, self.unbreakable, self.water, self.calmWater,
                            self.lava, self.calmLava, self.sand, self.gravel, self.goldOre,
                            self.ironOre, self.coalOre, self.log, self.leaf, self.sponge,
                            self.glass, self.clothRed, self.clothOrange, self.clothYellow,
                            self.clothChartreuse, self.clothGreen, self.clothSpringGreen,
                            self.clothCyan, self.clothCapri, self.clothUltramarine,
                            self.clothViolet, self.clothPurple, self.clothMagenta,
                            self.clothRose, self.clothDarkGray, self.clothGray,
                            self.clothWhite, self.flower, self.rose,
                            self.mushroomBrown, self.mushroomRed, self.gold, self.iron,
                            self.slabFull, self.slabHalf, self.brick, self.tnt,
                            self.bookshelf, self.mossStone, self.obsidian]

tiles = Tiles()
