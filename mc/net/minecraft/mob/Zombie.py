from mc.net.minecraft.mob.HumanoidMob import HumanoidMob
from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI

class Zombie(HumanoidMob):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.modelName = 'zombie'
        self._textureName = 'mob/zombie.png'
        self.heightOffset = 1.62
        self.ai = BasicAttackAI()
        self._deathScore = 80
        self.ai.defaultLookAngle = 30
        self.ai.runSpeed = 1.0
