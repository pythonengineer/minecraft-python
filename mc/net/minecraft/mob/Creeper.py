from mc.net.minecraft.mob.Mob import Mob
from mc.net.minecraft.mob.CreeperAI import CreeperAI

import math

class Creeper(Mob):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.heightOffset = 1.62
        self.modelName = 'creeper'
        self._textureName = 'mob/creeper.png'
        self.ai = CreeperAI()
        self.ai.defaultLookAngle = 45
        self._deathScore = 200
        self.setPos(x, y, z)

    def getBrightness(self, a):
        f = (20 - self.health) / 20.0
        f = (math.sin(self._tickCount + a) * 0.5 + 0.5) * f * 0.5 + 0.25 + f * 0.25
        return f * super().getBrightness(a)
