# cython: language_level=3

from libc.math cimport floor

from mc.cCompatibilityShims cimport Random

cdef class ImprovedNoise:

    def __init__(self, Random random):
        cdef int i, j, tmp

        for i in range(256):
            self.__p[i] = i

        for i in range(256):
            j = random.randInt(256 - i) + i
            tmp = self.__p[i]
            self.__p[i] = self.__p[j]
            self.__p[j] = tmp
            self.__p[i + 256] = self.__p[i]

    @staticmethod
    cdef double __fade(double t):
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

    @staticmethod
    cdef double __lerp(double d0, double d2, double d4):
        return d2 + d0 * (d4 - d2)

    @staticmethod
    cdef double __grad(int hash, double x, double y, double z):
        cdef double d8, d10

        hash &= 15
        d8 = x if hash < 8 else y
        d10 = y if hash < 4 else (z if hash != 12 and hash != 14 else x)
        return (d8 if (hash & 1) == 0 else -d8) + (d10 if (hash & 2) == 0 else -d10)

    cdef double getValue(self, double x, double y):
        cdef int X, Y, Z, A, AA, AB, B, BA, BB
        cdef double z, u, v, w

        X = <int>floor(x) & 0xFF
        Y = <int>floor(y) & 0xFF
        Z = <int>floor(0.0) & 0xFF

        x -= floor(x)
        y -= floor(y)
        z = floor(0.0)

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
