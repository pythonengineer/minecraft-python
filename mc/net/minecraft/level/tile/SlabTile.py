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
            tile = level.getTile(x, y + 1, z)
            if tile > 0:
                level.setTile(x, y, z, self.tiles.slabFull.id)
                if tile == self.tiles.slabHalf.id:
                    level.setTile(x, y + 1, z, 0)

            if level.getTile(x, y - 1, z) == self.tiles.slabHalf.id:
                level.setTile(x, y, z, 0)
                level.setTile(x, y - 1, z, self.tiles.slabFull.id)

    def getId(self):
        return self.tiles.slabHalf.id

    def isOpaque(self):
        return self.__half
