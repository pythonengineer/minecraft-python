from mc.net.minecraft.level.tile.Tile import Tile

import math

class Bush(Tile):

    def __init__(self, tiles, id_):
        super().__init__(tiles, id_)
        self.tex = 15

    def tick(self, level, x, y, z, random):
        below = level.getTile(x, y - 1, z)
        if not level.isLit(x, y, z) or (below != self.tiles.dirt.id and below != self.tiles.grass.id):
            level.setTile(x, y, z, 0)

    def render(self, t, level, layer, x, y, z):
        if level.isLit(x, y, z) ^ layer != 1:
            return

        tex = self.getTexture(15)
        u0 = tex % 16 / 16.0
        u1 = u0 + 0.0624375
        v0 = tex // 16 / 16.0
        v1 = v0 + 0.0624375

        rots = 2
        t.color(1.0, 1.0, 1.0)
        for r in range(rots):
            xa = math.sin(r * math.pi / rots + 0.7854) * 0.5
            za = math.cos(r * math.pi / rots + 0.7854) * 0.5
            x0 = x + 0.5 - xa
            x1 = x + 0.5 + xa
            y0 = y + 0.0
            y1 = y + 1.0
            z0 = z + 0.5 - za
            z1 = z + 0.5 + za

            t.vertexUV(x0, y1, z0, u1, v0)
            t.vertexUV(x1, y1, z1, u0, v0)
            t.vertexUV(x1, y0, z1, u0, v1)
            t.vertexUV(x0, y0, z0, u1, v1)

            t.vertexUV(x1, y1, z1, u0, v0)
            t.vertexUV(x0, y1, z0, u1, v0)
            t.vertexUV(x0, y0, z0, u1, v1)
            t.vertexUV(x1, y0, z1, u0, v1)

    def getAABB(self, x, y, z):
        return None

    def blocksLight(self):
        return False

    def isSolid(self):
        return False
