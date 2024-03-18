# cython: language_level=3

from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorPerlin cimport NoiseGeneratorPerlin
from mc.CompatibilityShims cimport Random

cdef class NoiseGeneratorOctaves:

    def __init__(self, Random random, int octaves):
        cdef int i
        self.__octaves = octaves
        self.__generatorCollection = [None] * octaves
        for i in range(octaves):
            self.__generatorCollection[i] = NoiseGeneratorPerlin(random)

    cdef double generateNoise(self, double x, double y):
        cdef double value, power
        cdef int i
        cdef NoiseGeneratorPerlin noiseLevel

        value = 0.0
        power = 1.0

        for i in range(self.__octaves):
            noiseLevel = self.__generatorCollection[i]
            value += noiseLevel.generateNoise(x / power, y / power) * power
            power *= 2.0

        return value
