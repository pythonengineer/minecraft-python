# cython: language_level=3

cdef class NoiseGeneratorCombined:

    def __init__(self, NoiseGeneratorOctaves source, NoiseGeneratorOctaves distort):
        self.__source = source
        self.__distort = distort

    cdef double generateNoise(self, double x, double y):
        return self.__source.generateNoise(x + self.__distort.generateNoise(x, y), y)
