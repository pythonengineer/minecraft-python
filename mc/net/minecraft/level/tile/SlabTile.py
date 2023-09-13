from mc.net.minecraft.level.tile.Tile import Tile

class SlabTile(Tile):

    def __init__(self, tiles, id_, half):
        self.__half = half
        super().__init__(tiles, id_, 6)
        if not self.__half:
            self._setShape(0.0, 0.0, 0.0, 1.0, 0.5, 1.0)

    def _getTexture(self, face):
        return 6 if face <= 1 else 5

    def isSolid(self):
        return self.__half

    def neighborChanged(self, level, x, y, z, type_):
        if self == self.tiles.slabHalf:
            pass

    def onTileAdded(self, level, x, y, z):
        if self != self.tiles.slabHalf:
            super().onTileAdded(level, x, y, z)

        if level.getTile(x, y - 1, z) == self.tiles.slabHalf.id:
            level.setTile(x, y, z, 0)
            level.setTile(x, y - 1, z, self.tiles.slabFull.id)

    def isOpaque(self):
        return self.__half

    def shouldRenderFace(self, level, x, y, z, layer):
        if self != self.tiles.slabHalf:
            super().shouldRenderFace(level, x, y, z, layer)

        if layer == 1:
            return True
        elif not super().shouldRenderFace(level, x, y, z, layer):
            return False
        elif layer == 0:
            return True
        else:
            return level.getTile(x, y, z) != self.id
