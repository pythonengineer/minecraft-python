from mc.net.minecraft.level.tile.Tile import Tile

class FallingTile(Tile):

    def onBlockAdded(self, level, x, y, z):
        FallingTile.__tryToFall(level, x, y, z)

    def neighborChanged(self, level, x, y, z, type_):
        FallingTile.__tryToFall(level, x, y, z)

    @staticmethod
    def __tryToFall(level, x, y, z):
        for i in range(y, -1, -1):
            if level.getTile(x, i - 1, z) != 0:
                break

        if i != y:
            level.swap(x, y, z, x, i, z)
