from mc.net.minecraft.level.tile.Tile import Tile

import random

class OreTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, id_)
        self.tex = tex

    def getId(self):
        if self == self.tiles.coalOre:
            return self.tiles.slabHalf.id
        elif self == self.tiles.goldOre:
            return self.tiles.gold.id
        elif self == self.tiles.ironOre:
            return self.tiles.iron.id
        else:
            return self.id

    def resourceCount(self):
        return int(random.random() * 3) + 1
