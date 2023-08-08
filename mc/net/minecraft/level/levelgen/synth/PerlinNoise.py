from mc.net.minecraft.level.levelgen.synth.Synth import Synth
from mc.net.minecraft.level.levelgen.synth.ImprovedNoise import ImprovedNoise

import random
import math

class PerlinNoise(Synth):

    def __init__(self, levels, rand=None):
        if not rand:
            rand = random

        self.__levels = levels
        self.__noiseLevels = [None] * levels
        for i in range(levels):
            self.__noiseLevels[i] = ImprovedNoise(rand)

    def getValue(self, x, y):
        value = 0.0
        power = 1.0

        for i in range(self.levels):
            value += self.__noiseLevels[i].getValue(x / power, y / power) * power
            power *= 2.0

        return value
