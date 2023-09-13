from mc.net.minecraft.level.tile.BaseLeafTile import BaseLeafTile

import random
import math

class LeafTile(BaseLeafTile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, 18, 22, True)

    def resourceCount(self):
        if math.floor(10 * random.random()) == 0:
            return 1
        else:
            return 0
