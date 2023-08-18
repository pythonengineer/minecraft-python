from mc.net.minecraft.level.tile.Tile import Tile

class SpongeTile(Tile):

    def __init__(self, tiles, id_):
        super().__init__(tiles, 19)
        self.tex = 48

    def onTileAdded(self, level, x, y, z):
        for xx in range(x - 2, x + 3):
            for yy in range(y - 2, y + 3):
                for zz in range(z - 2, z + 3):
                    if level.isWater(xx, yy, zz):
                        level.setTileNoNeighborChange(xx, yy, zz, 0)

    def onTileRemoved(self, level, x, y, z):
        for xx in range(x - 2, x + 3):
            for yy in range(y - 2, y + 3):
                for zz in range(z - 2, z + 3):
                    level.updateNeighborsAt(xx, yy, zz, level.getTile(xx, yy, zz))
