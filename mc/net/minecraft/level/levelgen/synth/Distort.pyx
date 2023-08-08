# cython: language_level=3

cdef class Distort:

    def __init__(self, PerlinNoise source, PerlinNoise distort):
        self.__source = source
        self.__distort = distort

    cdef double getValue(self, double x, double y):
        return self.__source.getValue(x + self.__distort.getValue(x, y), y)
