# cython: language_level=3

cdef class ImprovedNoise:

    cdef:
        int __p[512]

    @staticmethod
    cdef double __fade(double t)
    @staticmethod
    cdef double __lerp(double d0, double d2, double d4)
    @staticmethod
    cdef double __grad(int hash, double x, double y, double z)
    cdef double getValue(self, double x, double y)
