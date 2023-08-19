# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.level.Level cimport Level

cdef class LiquidTile(Tile):

    def __init__(self, tiles, int id_, int liquid):
        Tile.__init__(self, tiles, id_)
        self._liquid = liquid

        self.tex = 14

        if liquid == Liquid.lava:
            self.tex = 30

        self._tileId = id_
        self._calmTileId = id_ + 1

        f4 = 0.01
        dd = 0.1
        self._setShape(f4 + 0.0, 0.0 - dd + f4, f4 + 0.0, f4 + 1.0, 1.0 - dd + f4, f4 + 1.0)
        self._setTicking(True)
        if liquid == Liquid.lava:
            self.setTickSpeed(16)

    def onBlockAdded(self, Level level, int x, int y, int z):
        level.addToTickNextTick(x, y, z, self._tileId)

    cpdef void tick(self, Level level, int x, int y, int z, random) except *:
        cdef bint hasChanged, change
        hasChanged = False
        while True:
            y -= 1
            if level.getTile(x, y, z) != 0 or not self.__checkSponge(level, x, y, z):
                break

            change = level.setTile(x, y, z, self._tileId)
            if change:
                hasChanged = True

            if not change or self._liquid == Liquid.lava:
                break

        y += 1
        if self._liquid == Liquid.water or not hasChanged:
            hasChanged |= self.__checkWater(level, x - 1, y, z)
            hasChanged |= self.__checkWater(level, x + 1, y, z)
            hasChanged |= self.__checkWater(level, x, y, z - 1)
            hasChanged |= self.__checkWater(level, x, y, z + 1)

        if hasChanged:
            level.addToTickNextTick(x, y, z, self._tileId)
        else:
            level.setTileNoUpdate(x, y, z, self._calmTileId)

    cdef bint __checkSponge(self, Level level, int x, int y, int z):
        cdef int xx, yy, zz

        if self._liquid == Liquid.water:
            for xx in range(x - 2, x + 3):
                for yy in range(y - 2, y + 3):
                    for zz in range(z - 2, z + 3):
                        if level.getTile(xx, yy, zz) == self.tiles.sponge.id:
                            return False

        return True

    cdef bint __checkWater(self, Level level, int x, int y, int z):
        if level.getTile(x, y, z) == 0:
            if not self.__checkSponge(level, x, y, z):
                return False

            if level.setTile(x, y, z, self._tileId):
                level.addToTickNextTick(x, y, z, self._tileId)

        return False

    cdef float _getBrightness(self, Level level, int x, int y, int z):
        return 100.0 if self._liquid == Liquid.lava else level.getBrightness(x, y, z)

    cpdef bint _shouldRenderFace(self, Level level, int x, int y, int z, int layer, int face):
        cdef int tile

        if x >= 0 and y >= 0 and z >= 0 and x < level.width and z < level.height:
            if layer != 1:
                 return False
            else:
                tile = level.getTile(x, y, z)
                if tile != self._tileId and tile != self._calmTileId:
                    if face != 1 or level.getTile(x - 1, y, z) != 0 and \
                       level.getTile(x + 1, y, z) != 0 and \
                       level.getTile(x, y, z - 1) != 0 and \
                       level.getTile(x, y, z + 1) != 0:
                        return Tile._shouldRenderFace(self, level, x, y, z, -1, face)
                    else:
                        return True
                else:
                    return False
        else:
            return False

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
        Tile.renderFace(self, t, x, y, z, face)
        self.renderBackFace(t, x, y, z, face)

    def getTileAABB(self, int x, int y, int z):
        return None

    cpdef bint blocksLight(self):
        return True

    cpdef bint isSolid(self):
        return False

    cpdef int getLiquidType(self):
        return self._liquid

    cpdef void neighborChanged(self, Level level, int x, int y, int z, int type_) except *:
        cdef int liquid

        if type_ != 0:
            liquid = (<Tile>self.tiles.tiles[type_]).getLiquidType()
            if self._liquid == Liquid.water and liquid == Liquid.lava or liquid == Liquid.water and self._liquid == Liquid.lava:
                level.setTile(x, y, z, self.tiles.rock.id)
                return

        level.addToTickNextTick(x, y, z, type_)

    cdef int getTickDelay(self):
        return 5 if self._liquid == Liquid.lava else 0
