from mc.net.minecraft.level.tile.Flower import Flower

class Mushroom(Flower):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, id_, tex)
        f = 0.2
        self._setShape(0.5 - f, 0.0, 0.5 - f, f + 0.5, f * 2.0, f + 0.5)

    def tick(self, level, x, y, z, random):
        below = level.getTile(x, y - 1, z)
        if level.isLit(x, y, z) or below != self.tiles.rock.id and \
           below != self.tiles.gravel.id and below != self.tiles.stoneBrick.id:
            level.setTile(x, y, z, 0)
