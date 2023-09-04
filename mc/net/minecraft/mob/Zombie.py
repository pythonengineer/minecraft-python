from mc.net.minecraft.mob.HumanoidMob import HumanoidMob
from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI
from mc.net.minecraft.model.ZombieModel import ZombieModel

class Zombie(HumanoidMob):
    __model = ZombieModel()

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.model = self._humanoidModel = Zombie.__model
        self._textureName = 'mob/zombie.png'
        self.heightOffset = 1.62
        self.ai = BasicAttackAI()
        self.ai.defaultLookAngle = 30

    def die(self, entity):
        if entity:
            entity.awardKillScore(self, 100)

        super().die(entity)
