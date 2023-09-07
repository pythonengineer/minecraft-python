from mc.net.minecraft.particle.Particle import Particle

import random

class WaterDropParticle(Particle):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z, 0.0, 0.0, 0.0)
        self._xd *= 0.3
        self._yd = random.random() * 0.2 + 0.1
        self._zd *= 0.3
        self._rCol = 1.0
        self._gCol = 1.0
        self._bCol = 1.0
        self._tex = 16
        self.setSize(0.01, 0.01)
        self._lifetime = int(8.0 / (random.random() * 0.8 + 0.2))

    def renderParticle(self, t, a, xa, ya, za, xa2, ya2):
        super().renderParticle(t, a, xa, ya, za, xa2, ya2)

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z
        self._yd = float(self._yd - 0.06)
        self.move(self._xd, self._yd, self._zd)
        self._xd *= 0.98
        self._yd *= 0.98
        self._zd *= 0.98
        self._lifetime -= 1
        if self._lifetime - 1 <= 0:
            self.remove()

        if self.onGround:
            if random.random() < 0.5:
                self.remove()

            self.xd *= 0.7
            self.zd *= 0.7

