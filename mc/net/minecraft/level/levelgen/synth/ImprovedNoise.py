from mc.net.minecraft.level.levelgen.synth.Synth import Synth

import random
import math

_GRAD3 = ((1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1),
)

class ImprovedNoise(Synth):
    __p = [0] * 512

    def __init__(self, rand=None):
        if not rand:
            rand = random

        for i in range(256):
            self.__p[i] = i

        for i in range(256):
            j = math.floor(rand.random() * (256 - i))
            tmp = self.__p[i]
            self.__p[i] = self.__p[j]
            self.__p[j] = tmp
            self.__p[i + 256] = self.__p[i]

    @staticmethod
    def __fade(t):
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

    @staticmethod
    def __lerp(d0, d2, d4):
        return d2 + d0 * (d4 - d2)

    @staticmethod
    def __grad(hash, x, y, z):
        g = _GRAD3[hash % 16]
        return x * g[0] + y * g[1] + z * g[2]

    def getValue(self, x, y):
        X = int(math.floor(x) & 0xFF)
        Y = int(math.floor(y) & 0xFF)
        Z = int(math.floor(0.0) & 0xFF)

        x -= math.floor(x)
        y -= math.floor(y)
        z = math.floor(0.0)

        u = ImprovedNoise.__fade(x)
        v = ImprovedNoise.__fade(y)
        w = ImprovedNoise.__fade(z)

        A = self.__p[X] + Y
        AA = self.__p[A] + Z
        AB = self.__p[A + 1] + Z
        B = self.__p[X + 1] + Y
        BA = self.__p[B] + Z
        BB = self.__p[B + 1] + Z

        return ImprovedNoise.__lerp(w,
                         ImprovedNoise.__lerp(v,
                                   ImprovedNoise.__lerp(u,
                                             ImprovedNoise.__grad(self.__p[AA], x, y, z),
                                             ImprovedNoise.__grad(self.__p[BA], x - 1.0, y, z)),
                                   ImprovedNoise.__lerp(u,
                                             ImprovedNoise.__grad(self.__p[AB], x, y - 1.0, z),
                                             ImprovedNoise.__grad(self.__p[BB], x - 1.0, y - 1.0, z))),
                         ImprovedNoise.__lerp(v,
                                   ImprovedNoise.__lerp(u,
                                             ImprovedNoise.__grad(self.__p[AA + 1], x, y, z - 1.0),
                                             ImprovedNoise.__grad(self.__p[BA + 1], x - 1.0, y, z - 1.0)),
                                   ImprovedNoise.__lerp(u,
                                             ImprovedNoise.__grad(self.__p[AB + 1], x, y - 1.0, z - 1.0),
                                             ImprovedNoise.__grad(self.__p[BB + 1], x - 1.0, y - 1.0, z - 1.0))))
