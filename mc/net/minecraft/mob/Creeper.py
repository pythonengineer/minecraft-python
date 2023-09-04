from mc.net.minecraft.mob.Mob import Mob
from mc.net.minecraft.mob.CreeperAI import CreeperAI
from mc.net.minecraft.model.CreeperModel import CreeperModel

import math

class Creeper(Mob):
    __model = CreeperModel()

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.heightOffset = 1.62
        self.model = Creeper.__model
        self._textureName = 'mob/creeper.png'
        self.ai = CreeperAI(self)
        self.ai.defaultLookAngle = 45
        self.setPos(x, y, z)

    def getBrightness(self, a):
        f = (20 - self.health) / 20.0
        f = (math.sin(self._tickCount + a) * 0.5 + 0.5) * f * 0.5 + 0.25 + f * 0.25
        return f * super().getBrightness(a)

    def die(self, entity):
        if entity:
            entity.awardKillScore(self, 250)

        super().die(entity)
