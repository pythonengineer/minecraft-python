# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.GrassTile import GrassTile
from mc.net.minecraft.level.tile.DirtTile import DirtTile
from mc.net.minecraft.level.tile.Bush import Bush

cdef class Tiles:

    def __init__(self):
        self.tiles = [None] * 256

        self.rock = Tile(self, 1, 1)
        self.tiles[1] = self.rock
        self.grass = GrassTile(self, 2)
        self.tiles[2] = self.grass
        self.dirt = DirtTile(self, 3, 2)
        self.tiles[3] = self.dirt
        self.stoneBrick = Tile(self, 4, 16)
        self.tiles[4] = self.stoneBrick
        self.wood = Tile(self, 5, 4)
        self.tiles[5] = self.wood
        self.bush = Bush(self, 6)
        self.tiles[6] = self.bush

tiles = Tiles()
