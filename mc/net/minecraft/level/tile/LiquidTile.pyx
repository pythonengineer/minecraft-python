# cython: language_level=3

from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.level.tile.Tile cimport Tile

cdef class LiquidTile(Tile):

    def __init__(self, tiles, int id_, int liquidType):
        Tile.__init__(self, tiles, id_)
        self._liquidType = liquidType

        self.tex = 14

        if liquidType == 2:
            self.tex = 30

        self._tileId = id_
        self._calmTileId = id_ + 1

        dd = 0.1
        self._setShape(0.0, 0.0 - dd, 0.0, 1.0, 1.0 - dd, 1.0)
        self._setTicking(True)

    def onBlockAdded(self, level, int x, int y, int z):
        level.addToTickNextTick(x, y, z, self._tileId)

    cpdef void tick(self, level, int x, int y, int z, random) except *:
        cdef bint hasChanged, change
        hasChanged = False
        while True:
            y -= 1
            if level.getTile(x, y, z):
                break

            change = level.setTile(x, y, z, self._tileId)
            if change:
                hasChanged = True

            if not change or self._liquidType == 2:
                break

        y += 1
        if self._liquidType == 1 or not hasChanged:
            hasChanged |= self.__checkWater(level, x - 1, y, z)
            hasChanged |= self.__checkWater(level, x + 1, y, z)
            hasChanged |= self.__checkWater(level, x, y, z - 1)
            hasChanged |= self.__checkWater(level, x, y, z + 1)

        if hasChanged:
            level.addToTickNextTick(x, y, z, self._tileId)
        else:
            level.setTileNoUpdate(x, y, z, self._calmTileId)

    cdef bint __checkWater(self, level, int x, int y, int z):
        if level.getTile(x, y, z) == 0 and level.setTile(x, y, z, self._tileId):
            level.addToTickNextTick(x, y, z, self._tileId)

        return False

    cdef bint _shouldRenderFace(self, level, int x, int y, int z, int layer, int face):
        cdef int id_

        if x < 0 or y < 0 or z < 0 or x >= level.width or z >= level.height:
            return False
        if layer != 1 and self._liquidType == 1:
            return False

        id_ = level.getTile(x, y, z)
        if id_ == self._tileId or id_ == self._calmTileId:
            return False

        return Tile._shouldRenderFace(self, level, x, y, z, -1, face)

    cpdef renderFace(self, Tesselator t, int x, int y, int z, int face):
        Tile.renderFace(self, t, x, y, z, face)
        self.renderBackFace(t, x, y, z, face)

    cdef bint mayPick(self):
        return False

    def getAABB(self, int x, int y, int z):
        return None

    cpdef bint blocksLight(self):
        return True

    cpdef bint isSolid(self):
        return False

    cpdef int getLiquidType(self):
        return self._liquidType

    cpdef void neighborChanged(self, level, int x, int y, int z, int type_) except *:
        if self._liquidType == 1 and (type_ == self.tiles.lava.id or type_ == self.tiles.calmLava.id):
            level.setTileNoUpdate(x, y, z, self.tiles.rock.id)
        if self._liquidType == 2 and (type_ == self.tiles.water.id or type_ == self.tiles.calmWater.id):
            level.setTileNoUpdate(x, y, z, self.tiles.rock.id)

        level.addToTickNextTick(x, y, z, type_)
