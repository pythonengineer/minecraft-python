from mc.net.minecraft.level.tile.Tile import Tile

class BaseLeafTile(Tile):

    def __init__(self, tiles, id_, tex, z3):
        super().__init__(tiles, id_, tex)
        self.__renderAdjacentFaces = True

    def isSolid(self):
        return False

    def shouldRenderFace(self, level, x, y, z, layer):
        if not self.__renderAdjacentFaces and level.getTile(x, y, z) == self.id:
            return False
        else:
            return super().shouldRenderFace(level, x, y, z, layer)

    def blocksLight(self):
        return False
