from mc.net.minecraft.Entity import Entity

import random
import math

class Particle(Entity):

    def __init__(self, level, x, y, z, xa, ya, za, tile):
        super().__init__(level)
        self.tex = tile.tex
        self.__gravity = tile.particleGravity
        self.setSize(0.2, 0.2)
        self.heightOffset = self.bbHeight / 2.0
        self.setPos(x, y, z)

        self.__xd = xa + (random.random() * 2.0 - 1.0) * 0.4
        self.__yd = ya + (random.random() * 2.0 - 1.0) * 0.4
        self.__zd = za + (random.random() * 2.0 - 1.0) * 0.4
        speed = (random.random() + random.random() + 1.0) * 0.15

        dd = math.sqrt(self.__xd * self.__xd + self.__yd * self.__yd + self.__zd * self.__zd)
        self.__xd = self.__xd / dd * speed * 0.4
        self.__yd = self.__yd / dd * speed * 0.4 + 0.1
        self.__zd = self.__zd / dd * speed * 0.4

        self.__uo = random.random() * 3.0
        self.__vo = random.random() * 3.0

        self.__size = random.random() * 0.5 + 0.5

        self.__lifetime = 4.0 // (random.random() * 0.9 + 0.1)
        self.__age = 0
        self.makeStepSound = False

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

        if self.__age >= self.__lifetime:
            self.removed = True
        self.__age += 1

        self.__yd -= 0.04 * self.__gravity
        self.move(self.__xd, self.__yd, self.__zd)
        self.__xd *= 0.98
        self.__yd *= 0.98
        self.__zd *= 0.98

        if self.onGround:
            self.__xd *= 0.7
            self.__zd *= 0.7

    def render(self, t, a, xa, ya, za, xa2, za2):
        u0 = (self.tex % 16 + self.__uo / 4.0) / 16.0
        u1 = u0 + 0.01560938
        v0 = (self.tex // 16 + self.__vo / 4.0) / 16.0
        v1 = v0 + 0.01560938
        r = 0.1 * self.__size

        x = self.xo + (self.x - self.xo) * a
        y = self.yo + (self.y - self.yo) * a
        z = self.zo + (self.z - self.zo) * a
        t.vertexUV(x - xa * r - xa2 * r, y - ya * r, z - za * r - za2 * r, u0, v1)
        t.vertexUV(x - xa * r + xa2 * r, y + ya * r, z - za * r + za2 * r, u0, v0)
        t.vertexUV(x + xa * r + xa2 * r, y + ya * r, z + za * r + za2 * r, u1, v0)
        t.vertexUV(x + xa * r - xa2 * r, y - ya * r, z + za * r - za2 * r, u1, v1)
