from mc.net.minecraft.mob.Mob import Mob
from mc.net.minecraft.model.QuadrupedModel import QuadrupedModel

class QuadrupedMob(Mob):
    __model = QuadrupedModel()

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.setSize(1.4, 1.2)
        self.setPos(x, y, z)
        self.model = QuadrupedMob.__model
