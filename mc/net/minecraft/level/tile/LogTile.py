from mc.net.minecraft.level.tile.Tile import Tile

import random
import math

class LogTile(Tile):

    def __init__(self, tiles, id_):
        super().__init__(tiles, 17)
        self.tex = 20

    def resourceCount(self):
        return math.floor(3 * random.random()) + 3

    def _getTexture(self, face):
        return 21 if face == 1 else (21 if face == 0 else 20)
