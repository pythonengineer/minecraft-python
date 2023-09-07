from mc.net.minecraft.particle.Particle import Particle

class TerrainParticle(Particle):

    def __init__(self, level, x, y, z, xr, yr, zr, tile):
        super().__init__(level, x, y, z, xr, yr, zr)
        self._tex = tile.tex
        self._gravity = tile.particleGravity
        self._rCol = self._gCol = self._bCol = 0.6

    def getParticleTexture(self):
        return 1

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        u0 = ((self._tex % 16) + self._uo / 4.0) / 16.0
        u1 = u0 + 0.015609375
        v0 = ((self._tex // 16) + self._vo / 4.0) / 16.0
        v1 = v0 + 0.015609375
        r = 0.1 * self._size
        x = self.xo + (self.x - self.xo) * a
        y = self.yo + (self.y - self.yo) * a
        z = self.zo + (self.z - self.zo) * a
        br = self.getBrightness(a)
        t.colorFloat(br * self._rCol, br * self._gCol, br * self._bCol)
        t.vertexUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - ya2 * r, u0, v1)
        t.vertexUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + ya2 * r, u0, v0)
        t.vertexUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + ya2 * r, u1, v0)
        t.vertexUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - ya2 * r, u1, v1)
