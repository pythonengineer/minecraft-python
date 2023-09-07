from mc.net.minecraft.level.tile.Tile import Tile

class MetalTile(Tile):

    def __init__(self, tiles, id_, tex):
        super().__init__(tiles, id_)
        self.tex = tex

    def _getTexture(self, face):
        if face == 1:
            return self.tex - 16
        elif face == 0:
            return self.tex + 16
        else:
            return self.tex
