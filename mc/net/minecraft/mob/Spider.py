from mc.net.minecraft.mob.QuadrupedMob import QuadrupedMob
from mc.net.minecraft.mob.ai.JumpAttackAI import JumpAttackAI

class Spider(QuadrupedMob):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.heightOffset = 0.72
        self.modelName = 'spider'
        self._textureName = 'mob/spider.png'
        self.setSize(1.4, 0.9)
        self.setPos(x, y, z)
        self._deathScore = 105
        self._bobStrength = 0.0
        self.ai = JumpAttackAI()
