from mc.net.minecraft.particle.Particle cimport Particle
from mc.net.minecraft.renderer.Tesselator cimport Tesselator

cdef class SmokeParticle(Particle):

    def __init__(self, level, x, y, z):
        Particle.__init__(self, level, x, y, z, 0.0, 0.0, 0.0)
        self._xd *= 0.1
        self._yd *= 0.1
        self._zd *= 0.1
        self._rCol = self._gCol = self._bCol = self._random.randFloat() * 0.3
        self._lifetime = <int>(8.0 / (self._random.randFloat() * 0.8 + 0.2))

    def renderParticle(self, Tesselator t, float a, float xa, float ya,
                       float za, float xa2, float ya2):
        Particle.renderParticle(self, t, a, xa, ya, za, xa2, ya2)

    cpdef tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self._age += 1
        if self._age - 1 >= self._lifetime:
            self.remove()

        self._tex = 7 - (self._age << 3) // self._lifetime
        self._yd += 0.004
        self.move(self._xd, self._yd, self._zd)
        self._xd *= 0.96
        self._yd *= 0.96
        self._zd *= 0.96
        if self.onGround:
            self._xd *= 0.7
            self._zd *= 0.7

