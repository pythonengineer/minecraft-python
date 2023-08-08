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

        self.__xd = xa + (random.random() * 2.0 - 1.0) * 0.4
        self.__yd = ya + (random.random() * 2.0 - 1.0) * 0.4
        self.__zd = za + (random.random() * 2.0 - 1.0) * 0.4
        speed = (random.random() + random.random() + 1.0) * 0.15

        dd = math.sqrt(self.__xd * self.__xd + self.__yd * self.__yd + self.__zd * self.__zd)
        self.__xd = self.__xd / dd * speed * 0.4
        self.__yd = self.__yd / dd * speed * 0.4 + 0.1
        self.__zd = self.__zd / dd * speed * 0.4

        self.uo = random.random() * 3.0
        self.vo = random.random() * 3.0

        self.size = random.random() * 0.5 + 0.5

        self.__lifetime = 4.0 // (random.random() * 0.9 + 0.1)
        self.__age = 0

    def tick(self):
        self.xo = self.x
        self.yo = self.y
        self.zo = self.z

        if self.__age >= self.__lifetime:
            self.removed = True
        self.__age += 1

        self.__yd -= 0.04
        self.move(self.__xd, self.__yd, self.__zd)
        self.__xd *= 0.98
        self.__yd *= 0.98
        self.__zd *= 0.98

        if self.onGround:
            self.__xd *= 0.7
            self.__zd *= 0.7
