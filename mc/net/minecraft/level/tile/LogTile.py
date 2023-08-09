from mc.net.minecraft.level.tile.Tile import Tile

class LogTile(Tile):

    def __init__(self, tiles, id_):
        super().__init__(tiles, 17)
        self.tex = 20

    def _getTexture(self, face):
        return 21 if face == 1 else (21 if face == 0 else 20)
