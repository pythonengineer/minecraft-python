from mc.net.minecraft.level.tile.Flower import Flower

import math

class Bush(Flower):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, 6, 15)
        f = 0.4
        self._setShape(0.5 - f, 0.0, 0.5 - f, f + 0.5, f * 2.0, f + 0.5)

    def tick(self, level, x, y, z, random):
        below = level.getTile(x, y - 1, z)
        if not level.isLit(x, y, z) or below != self.tiles.dirt.id and below != self.tiles.grass.id:
            level.setTile(x, y, z, 0)
            return

        if math.floor(5 * random.random()) == 0:
            level.setTileNoUpdate(x, y, z, 0)
            if not level.maybeGrowTree(x, y, z):
                level.setTileNoUpdate(x, y, z, self.id)
