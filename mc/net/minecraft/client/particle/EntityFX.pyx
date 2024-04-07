# cython: language_level=3

from libc.math cimport sqrt

from mc.CompatibilityShims cimport Random
from mc.net.minecraft.client.render.Tessellator cimport Tessellator
from mc.net.minecraft.game.entity.Entity cimport Entity

cdef class EntityFX(Entity):

    def __cinit__(self):
        self._random = Random()
        self._particleTextureIndex = 0
        self._particleGravity = 0.0

    def __init__(self, world, x, y, z, xr, yr, zr):
        Entity.__init__(self, world)
        self.setSize(0.2, 0.2)
        self.yOffset = self.bbHeight / 2.0
        self.setPosition(x, y, z)

        self._particleRed = self._particleGreen = self._particleBlue = 1.0
        self._motionX1 = xr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        self._motionY1 = yr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        self._motionZ1 = zr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        speed = (self._random.randFloat() + self._random.randFloat() + 1.0) * 0.15

        dd = sqrt(self._motionX1 * self._motionX1 + self._motionY1 * self._motionY1 + self._motionZ1 * self._motionZ1)
        self._motionX1 = self._motionX1 / dd * speed * 0.4
        self._motionY1 = self._motionY1 / dd * speed * 0.4 + 0.1
        self._motionZ1 = self._motionZ1 / dd * speed * 0.4

        self._particleTextureJitterX = self._random.randFloat() * 3.0
        self._particleTextureJitterY = self._random.randFloat() * 3.0

        self._particleScale = self._random.randFloat() * 0.5 + 0.5

        self._particleMaxAge = <int>(4 // (self._random.randFloat() * 0.9 + 0.1))
        self.__particleAge = 0
        self._makeStepSound = False

    def multiplyVelocity(self, power):
        self._motionX1 *= 0.2
        self._motionY1 = (self._motionY1 - 0.1) * 0.2 + 0.1
        self._motionZ1 *= 0.2
        return self

    def multipleParticleScaleBy(self, scale):
        self.setSize(0.120000005, 0.120000005)
        self._particleScale *= 0.6
        return self

    cpdef onEntityUpdate(self):
        self.prevPosX = self.posX
        self.prevPosY = self.posY
        self.prevPosZ = self.posZ

        if self.__particleAge >= self._particleMaxAge:
            self.setEntityDead()

        self.__particleAge += 1

        self._motionY1 = self._motionY1 - 0.04 * self._particleGravity
        self.moveEntity(self._motionX1, self._motionY1, self._motionZ1)
        self._motionX1 *= 0.98
        self._motionY1 *= 0.98
        self._motionZ1 *= 0.98

        if self.onGround:
            self._motionX1 *= 0.7
            self._motionZ1 *= 0.7

    def renderParticle(self, Tessellator t, float a, float xa, float ya,
                       float za, float xa2, float ya2):
        cdef float u0, u1, v0, v1, r, x, y, z, br

        u0 = (self._particleTextureIndex % 16) / 16.0
        u1 = u0 + 0.999 / 16.0
        v0 = (self._particleTextureIndex // 16) / 16.0
        v1 = v0 + 0.999 / 16.0
        r = 0.1 * self._particleScale

        x = self.prevPosX + (self.posX - self.prevPosX) * a
        y = self.prevPosY + (self.posY - self.prevPosY) * a
        z = self.prevPosZ + (self.posZ - self.prevPosZ) * a

        br = self.getBrightness()
        t.setColorOpaque_F(self._particleRed * a, self._particleGreen * a, self._particleBlue * a)

        t.addVertexWithUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - ya2 * r, u0, v1)
        t.addVertexWithUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + ya2 * r, u0, v0)
        t.addVertexWithUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + ya2 * r, u1, v0)
        t.addVertexWithUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - ya2 * r, u1, v1)

    def getFXLayer(self):
        return 0
