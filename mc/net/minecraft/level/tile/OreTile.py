from mc.net.minecraft.level.tile.Tile import Tile

import random

class OreTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, id_)
        self.tex = tex

    def resourceCount(self):
        return int(random.random() * 3) + 1
