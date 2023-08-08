from mc.net.minecraft.level.levelgen.synth.Synth import Synth

class Emboss(Synth):

    def __init__(self, synth):
        self.__synth = synth

    def getValue(self, x, y):
        return self.__synth.getValue(x, y) - self.__synth.getValue(x + 1.0, y + 1.0)
