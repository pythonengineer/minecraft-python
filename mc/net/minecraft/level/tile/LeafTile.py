from mc.net.minecraft.level.tile.Tile import Tile

class LeafTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, 18, 22)

    def isSolid(self):
        return False

    def blocksLight(self):
        return False
