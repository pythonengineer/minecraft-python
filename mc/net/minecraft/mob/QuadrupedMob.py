from mc.net.minecraft.mob.Mob import Mob

class QuadrupedMob(Mob):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.setSize(1.4, 1.2)
        self.setPos(x, y, z)
        self.modelName = 'pig'
