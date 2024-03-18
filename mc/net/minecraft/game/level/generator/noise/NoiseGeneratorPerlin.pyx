# cython: language_level=3

from libc.math cimport floor

from mc.CompatibilityShims cimport Random

cdef class NoiseGeneratorPerlin:

    def __init__(self, Random random):
        cdef int i, j, tmp

        for i in range(256):
            self.__permutations[i] = i

        for i in range(256):
            j = random.nextInt(256 - i) + i
            tmp = self.__permutations[i]
            self.__permutations[i] = self.__permutations[j]
            self.__permutations[j] = tmp
            self.__permutations[i + 256] = self.__permutations[i]

    @staticmethod
    cdef double __generateNoise(double t):
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

    @staticmethod
    cdef double __lerp(double d0, double d2, double d4):
        return d2 + d0 * (d4 - d2)

    @staticmethod
    cdef double __grad(int hash, double x, double y, double z):
        cdef double d8, d10

        hash &= 0xF
        d8 = x if hash < 8 else y
        d10 = y if hash < 4 else (z if hash != 12 and hash != 14 else x)
        return (d8 if (hash & 1) == 0 else -d8) + (d10 if (hash & 2) == 0 else -d10)

    cdef double generateNoise(self, double x, double y):
        cdef int X, Y, Z, A, AA, AB, B, BA, BB
        cdef double z, u, v, w

        X = <int>floor(x) & 0xFF
        Y = <int>floor(y) & 0xFF
        Z = <int>floor(0.0) & 0xFF

        x -= floor(x)
        y -= floor(y)
        z = floor(0.0)

        u = NoiseGeneratorPerlin.__generateNoise(x)
        v = NoiseGeneratorPerlin.__generateNoise(y)
        w = NoiseGeneratorPerlin.__generateNoise(z)

        A = self.__permutations[X] + Y
        AA = self.__permutations[A] + Z
        AB = self.__permutations[A + 1] + Z
        B = self.__permutations[X + 1] + Y
        BA = self.__permutations[B] + Z
        BB = self.__permutations[B + 1] + Z

        return NoiseGeneratorPerlin.__lerp(w,
                   NoiseGeneratorPerlin.__lerp(v,
                       NoiseGeneratorPerlin.__lerp(u,
                           NoiseGeneratorPerlin.__grad(self.__permutations[AA], x, y, z),
                           NoiseGeneratorPerlin.__grad(self.__permutations[BA], x - 1.0, y, z)),
                       NoiseGeneratorPerlin.__lerp(u,
                           NoiseGeneratorPerlin.__grad(self.__permutations[AB], x, y - 1.0, z),
                           NoiseGeneratorPerlin.__grad(self.__permutations[BB], x - 1.0, y - 1.0, z))),
                   NoiseGeneratorPerlin.__lerp(v,
                       NoiseGeneratorPerlin.__lerp(u,
                           NoiseGeneratorPerlin.__grad(self.__permutations[AA + 1], x, y, z - 1.0),
                           NoiseGeneratorPerlin.__grad(self.__permutations[BA + 1], x - 1.0, y, z - 1.0)),
                       NoiseGeneratorPerlin.__lerp(u,
                           NoiseGeneratorPerlin.__grad(self.__permutations[AB + 1], x, y - 1.0, z - 1.0),
                           NoiseGeneratorPerlin.__grad(self.__permutations[BB + 1], x - 1.0, y - 1.0, z - 1.0))))
