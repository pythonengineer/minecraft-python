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
        self.xd = self.xd / dd * speed * 0.4
        self.yd = self.yd / dd * speed * 0.4 + 0.1
        self.zd = self.zd / dd * speed * 0.4

        self.uo = random.random() * 3.0
        self.vo = random.random() * 3.0

        self.size = random.random() * 0.5 + 0.5

        self.lifetime = 4.0 // (random.random() * 0.9 + 0.1)
        self.age = 0

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

        if self.age >= self.lifetime:
            self.remove()
        self.age += 1

        self.yd -= 0.04
        self.move(self.xd, self.yd, self.zd)
        self.xd *= 0.98
        self.yd *= 0.98
        self.zd *= 0.98

        if self.onGround:
            self.xd *= 0.7
            self.zd *= 0.7

    def render(self, t, a, xa, ya, za, xa2, za2):
        u0 = (self.tex % 16 + self.uo / 4.0) / 16.0
        u1 = u0 + 0.01560938
        v0 = (self.tex // 16 + self.vo / 4.0) / 16.0
        v1 = v0 + 0.01560938
        r = 0.1 * self.size

        x = self.xo + (self.x - self.xo) * a
        y = self.yo + (self.y - self.yo) * a
        z = self.zo + (self.z - self.zo) * a
        t.vertexUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - za2 * r, u0, v1)
        t.vertexUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + za2 * r, u0, v0)
        t.vertexUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + za2 * r, u1, v0)
        t.vertexUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - za2 * r, u1, v1)
