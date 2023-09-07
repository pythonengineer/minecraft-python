from mc.net.minecraft.level.tile.Tile import Tile

class BookshelfTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, 47, 35)

    def _getTexture(self, face):
        return 4 if face <= 1 else self.tex

    def resourceCount(self):
        return 0
