from mc.net.minecraft.level.levelgen.synth.Synth import Synth

import math

class Rotate(Synth):

    def __init__(self, synth, angle):
        self.__synth = synth

        self.__sin = math.sin(angle)
        self.__cos = math.cos(angle)

    def getValue(self, x, y):
        return self.__synth.getValue(x * self.__cos + y * self.__sin, y * self.__cos - x * self.__sin)
