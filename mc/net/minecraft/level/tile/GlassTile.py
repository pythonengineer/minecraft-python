from mc.net.minecraft.level.tile.Tile import Tile

class GlassTile(Tile):

    def __init__(self, tiles, id_, tex, z3):
        super().__init__(tiles, 20, 49)
        self.__renderAdjacentFaces = True

    def isSolid(self):
        return False

    def _shouldRenderFace(self, level, x, y, z, layer, face):
        tile = level.getTile(x, y, z)
        if not self.__renderAdjacentFaces and tile == self.id:
            return False
        else:
            return super()._shouldRenderFace(level, x, y, z, layer, face)

    def blocksLight(self):
        return False
