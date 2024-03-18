# cython: language_level=3

cdef class NoiseGeneratorPerlin:

    cdef:
        int __permutations[512]

    @staticmethod
    cdef double __generateNoise(double t)
    @staticmethod
    cdef double __lerp(double d0, double d2, double d4)
    @staticmethod
    cdef double __grad(int hash, double x, double y, double z)
    cdef double generateNoise(self, double x, double y)
