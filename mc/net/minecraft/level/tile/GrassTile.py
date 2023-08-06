from mc.net.minecraft.level.tile.Tile import Tile

import math

class GrassTile(Tile):

    def __init__(self, tiles, id_):
        super().__init__(tiles, id_)
        self.tex = 3

    def getTexture(self, face):
        if face == 1: return 0
        if face == 0: return 2
        return 3

    def tick(self, level, x, y, z, random):
        if not level.isLit(x, y, z):
            level.setTile(x, y, z, self.tiles.dirt.id)
        else:
            for i in range(4):
                xt = x + math.floor(3 * random.random()) - 1
                yt = y + math.floor(5 * random.random()) - 3
                zt = z + math.floor(3 * random.random()) - 1
                if level.getTile(xt, yt, zt) == self.tiles.dirt.id and level.isLit(xt, yt, zt):
                    level.setTile(xt, yt, zt, self.tiles.grass.id)

