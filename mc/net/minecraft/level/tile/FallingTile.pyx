# cython: language_level=3

from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.liquid.Liquid cimport Liquid

cdef class FallingTile(Tile):

    def onBlockAdded(self, Level level, int x, int y, int z):
        self.__tryToFall(level, x, y, z)

    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *:
        self.__tryToFall(level, x, y, z)

    cdef __tryToFall(self, Level level, int x, int y, int z):
        cdef int lastY, nextY, tile
        cdef bint isFallable

        lastY = y
        while True:
            isFallable = False
            nextY = lastY - 1
            tile = level.getTile(x, nextY, z)
            if tile == 0:
                isFallable = True
            else:
                liquid = (<Tile>self.tiles.tiles[tile]).getLiquidType()
                if liquid == Liquid.water:
                    isFallable = True
                elif liquid == Liquid.lava:
                    isFallable = True

            if not isFallable or lastY <= 0:
                if lastY != y:
                    level.swap(x, y, z, x, lastY, z)

                break

            lastY -= 1
