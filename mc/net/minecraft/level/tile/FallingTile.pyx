# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.liquid.Liquid cimport Liquid
from mc.net.minecraft.level.Level cimport Level

cdef class FallingTile(Tile):

    def onPlace(self, Level level, int x, int y, int z):
        self.__tryToFall(level, x, y, z)

    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *:
        self.__tryToFall(level, x, y, z)

    cdef __tryToFall(self, Level level, int x, int y, int z):
        cdef int lastY, tile, liquid

        lastY = y
        while True:
            tile = level.getTile(x, lastY - 1, z)
            liquid = self.tiles.tiles[tile].getLiquidType() if tile > 0 else Liquid.none

            if not (tile == 0 or liquid == Liquid.water or liquid == Liquid.lava) or lastY <= 0:
                if lastY != y:
                    tile = level.getTile(x, lastY, z)
                    if tile > 0 and self.tiles.tiles[tile].getLiquidType() != Liquid.none:
                        level.setTileNoUpdate(x, lastY, z, 0)

                    level.swap(x, y, z, x, lastY, z)

                return

            lastY -= 1
