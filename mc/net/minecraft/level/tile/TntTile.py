from mc.net.minecraft.level.tile.Tile import Tile

import random

class TntTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, 46, 8)

    def _getTexture(self, face):
        if face == 0:
            return self.tex + 2
        elif face == 1:
            return self.tex + 1
        else:
            return self.tex

    def resourceCount(self):
        return 0

    def destroy(self, level, x, y, z, particleEngine):
        if level.creativeMode:
            super().destroy(level, x, y, z, particleEngine)
