from mc.net.minecraft.mob.QuadrupedMob import QuadrupedMob
from mc.net.minecraft.model.QuadrupedModel import QuadrupedModel

class Pig(QuadrupedMob):
    __model = QuadrupedModel()

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.heightOffset = 1.72
        self.model = Pig.__model
        self._textureName = 'mob/pig.png'

    def die(self, entity):
        if entity:
            entity.awardKillScore(self, 10)

        super().die(entity)
