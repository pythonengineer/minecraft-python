# cython: language_level=3

from mc.net.minecraft.level.levelgen.synth.ImprovedNoise cimport ImprovedNoise
from mc.cCompatibilityShims cimport Random

cdef class PerlinNoise:

    def __cinit__(self):
        self.__levels = 8

    def __init__(self, Random random, levels):
        cdef int i
        self.__noiseLevels = [None] * 8
        for i in range(self.__levels):
            self.__noiseLevels[i] = ImprovedNoise(random)

    cdef double getValue(self, double x, double y):
        cdef double value, power
        cdef int i
        cdef ImprovedNoise noiseLevel

        value = 0.0
        power = 1.0

        for i in range(self.__levels):
            noiseLevel = self.__noiseLevels[i]
            value += noiseLevel.getValue(x / power, y / power) * power
            power *= 2.0

        return value
