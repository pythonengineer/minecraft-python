from mc.net.minecraft.level.levelgen.synth.Synth import Synth

class Distort(Synth):

    def __init__(self, source, distort):
        self.__source = source
        self.__distort = distort

    def getValue(self, x, y):
        return self.__source.getValue(x + self.__distort.getValue(x, y), y)
