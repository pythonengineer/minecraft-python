from mc.net.minecraft.Entity import Entity

import random
import math

class Particle(Entity):

    def __init__(self, level, x, y, z, xa, ya, za, tex):
        super().__init__(level)
        self.tex = tex
        self.setSize(0.2, 0.2)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)

        self.xd = xa + (random.random() * 2.0 - 1.0) * 0.4
        self.yd = ya + (random.random() * 2.0 - 1.0) * 0.4
        self.zd = za + (random.random() * 2.0 - 1.0) * 0.4
        speed = (random.random() + random.random() + 1.0) * 0.15

        dd = math.sqrt(self.xd * self.xd + self.yd * self.yd + self.zd * self.zd)
        self.xd = self.xd / dd * speed * 0.7
        self.yd = self.yd / dd * speed
        self.zd = self.zd / dd * speed * 0.7

        self.uo = random.random() * 3.0
        self.vo = random.random() * 3.0

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

        if random.random() < 0.1:
            self.remove()

        self.yd -= 0.06
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.98
        self.yd *= 0.98
        self.zd *= 0.98

        if self.onGround:
            self.xd *= 0.7
            self.zd *= 0.7

    def render(self, t, a, xa, ya, za):
        u0 = (self.tex % 16 + self.uo / 4.0) / 16.0
        u1 = u0 + 0.01560938
        v0 = (self.tex // 16 + self.vo / 4.0) / 16.0
        v1 = v0 + 0.01560938
        r = 0.1

        x = self.xo + (self.x - self.xo) * a
        y = self.yo + (self.y - self.yo) * a
        z = self.zo + (self.z - self.zo) * a
        t.vertexUV(x - xa * r, y - ya * r, z - za * r, u0, v1)
        t.vertexUV(x - xa * r, y + ya * r, z - za * r, u0, v0)
        t.vertexUV(x + xa * r, y + ya * r, z + za * r, u1, v0)
        t.vertexUV(x + xa * r, y - ya * r, z + za * r, u1, v1)
