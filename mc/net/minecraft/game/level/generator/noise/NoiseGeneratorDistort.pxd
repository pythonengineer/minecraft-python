# cython: language_level=3

from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorOctaves cimport NoiseGeneratorOctaves

cdef class NoiseGeneratorDistort:

    cdef:
        NoiseGeneratorOctaves __source
        NoiseGeneratorOctaves __distort

    cdef double generateNoise(self, double x, double y)
