from mc.net.minecraft.client.particle.EntityFX import EntityFX

class EntityDiggingFX(EntityFX):

    def __init__(self, world, x, y, z, xr, yr, zr, block):
        super().__init__(world, x, y, z, xr, yr, zr)
        self._particleTextureIndex = block.blockIndexInTexture
        self._particleGravity = block.blockParticleGravity
        self._particleRed = self._particleGreen = self._particleBlue = 0.6

    def getFXLayer(self):
        return 1

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        u0 = ((self._particleTextureIndex % 16) + self._particleTextureJitterX / 4.0) / 16.0
        u1 = u0 + 0.999 / 64.0
        v0 = ((self._particleTextureIndex // 16) + self._particleTextureJitterY / 4.0) / 16.0
        v1 = v0 + 0.999 / 64.0
        r = 0.1 * self._particleScale
        x = self.prevPosX + (self.posX - self.prevPosX) * a
        y = self.prevPosY + (self.posY - self.prevPosY) * a
        z = self.prevPosZ + (self.posZ - self.prevPosZ) * a
        br = self.getBrightness()
        t.setColorOpaque_F(br * self._particleRed, br * self._particleGreen, br * self._particleBlue)
        t.addVertexWithUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - ya2 * r, u0, v1)
        t.addVertexWithUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + ya2 * r, u0, v0)
        t.addVertexWithUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + ya2 * r, u1, v0)
        t.addVertexWithUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - ya2 * r, u1, v1)
