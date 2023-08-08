# cython: language_level=3

cdef class PerlinNoise:

    cdef:
        list __noiseLevels
        int __levels

    cdef double getValue(self, double x, double y)
