# cython: language_level=3

from libc.math cimport sqrt

from mc.cCompatibilityShims cimport Random
from mc.net.minecraft.renderer.Tesselator cimport Tesselator
from mc.net.minecraft.Entity cimport Entity

cdef class Particle(Entity):

    def __cinit__(self):
        self._random = Random()
        self._tex = 0
        self._gravity = 0.0

    def __init__(self, level, x, y, z, xr, yr, zr):
        Entity.__init__(self, level)
        self.setSize(0.2, 0.2)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)

        self._rCol = self._gCol = self._bCol = 1.0
        self._xd = xr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        self._yd = yr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        self._zd = zr + (self._random.randFloat() * 2.0 - 1.0) * 0.4
        speed = (self._random.randFloat() + self._random.randFloat() + 1.0) * 0.15

        dd = sqrt(self._xd * self._xd + self._yd * self._yd + self._zd * self._zd)
        self._xd = self._xd / dd * speed * 0.4
        self._yd = self._yd / dd * speed * 0.4 + 0.1
        self._zd = self._zd / dd * speed * 0.4

        self._uo = self._random.randFloat() * 3.0
        self._vo = self._random.randFloat() * 3.0

        self._size = self._random.randFloat() * 0.5 + 0.5

        self._lifetime = <int>(4 // (self._random.randFloat() * 0.9 + 0.1))
        self._age = 0
        self.makeStepSound = False

    def setPower(self, power):
        self._xd *= power
        self._yd = (self._yd - 0.1) * power + 0.1
        self._zd *= power
        return self

    def scale(self, scale):
        self.setSize(0.2 * scale, 0.2 * scale)
        self._size *= scale
        return self

    cpdef tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

        if self._age >= self._lifetime:
            self.removed = True

        self._age += 1

        self._yd = self._yd - 0.04 * self._gravity
        self.move(self._xd, self._yd, self._zd)
        self._xd *= 0.98
        self._yd *= 0.98
        self._zd *= 0.98

        if self.onGround:
            self._xd *= 0.7
            self._zd *= 0.7

    def renderParticle(self, Tesselator t, float a, float xa, float ya,
                       float za, float xa2, float ya2):
        cdef float u0, u1, v0, v1, r, x, y, z, br

        u0 = (self._tex % 16) / 16.0
        u1 = u0 + 0.0624375
        v0 = (self._tex // 16) / 16.0
        v1 = v0 + 0.0624375
        r = 0.1 * self._size

        x = self.xo + (self.x - self.xo) * a
        y = self.yo + (self.y - self.yo) * a
        z = self.zo + (self.z - self.zo) * a

        br = self.getBrightness(a)
        t.colorFloat(self._rCol * a, self._gCol * a, self._bCol * a)

        t.vertexUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - ya2 * r, u0, v1)
        t.vertexUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + ya2 * r, u0, v0)
        t.vertexUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + ya2 * r, u1, v0)
        t.vertexUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - ya2 * r, u1, v1)

    def getParticleTexture(self):
        return 0
