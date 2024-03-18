# cython: language_level=3

cdef class NoiseGeneratorOctaves:

    cdef:
        list __generatorCollection
        int __octaves

    cdef double generateNoise(self, double x, double y)
