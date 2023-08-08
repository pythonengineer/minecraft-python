from mc.net.minecraft.level.levelgen.synth.Synth import Synth

class Scale(Synth):

    def __init__(self, synth, xScale, yScale):
        self.__synth = synth
        self.__xScale = 1.0 / xScale
        self.__yScale = 1.0 / yScale

    def getValue(self, x, y):
        return self.__synth.getValue(x * self.__xScale, y * self.__yScale)
