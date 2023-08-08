# cython: language_level=3

from mc.net.minecraft.level.levelgen.synth.PerlinNoise cimport PerlinNoise

cdef class Distort:

    cdef:
        PerlinNoise __source
        PerlinNoise __distort

    cdef double getValue(self, double x, double y)
