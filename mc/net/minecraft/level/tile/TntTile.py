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

    def wasExploded(self, level, x, y, z):
        from mc.net.minecraft.item.PrimedTnt import PrimedTnt
        primedTnt = PrimedTnt(level, x + 0.5, y + 0.5, z + 0.5)
        primedTnt.life = int(random.random() * (primedTnt.life // 4)) + primedTnt.life // 8
        level.addEntity(primedTnt)

    def destroy(self, level, x, y, z, particleEngine):
        from mc.net.minecraft.item.PrimedTnt import PrimedTnt
        level.addEntity(PrimedTnt(level, x + 0.5, y + 0.5, z + 0.5))
