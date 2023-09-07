from mc.net.minecraft.mob.Zombie import Zombie
from mc.net.minecraft.mob.SkeletonAI import SkeletonAI
from mc.net.minecraft.item.Arrow import Arrow

import random

class Skeleton(Zombie):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.modelName = 'skeleton'
        self._textureName = 'mob/skeleton.png'
        self.ai = SkeletonAI()
        self._deathScore = 120
        self.ai.runSpeed = 0.3
        self.ai.damage = 8

    def shootArrow(self, level):
        level.addEntity(Arrow(level, self, self.x, self.y, self.z,
                              self.yRot + 180.0 + (random.random() * 45.0 - 22.5),
                              self.xRot - (random.random() * 45.0 - 10.0), 1.0))

    def access(self):
        amount = int((random.random() + random.random()) * 3.0 + 4.0)
        for i in range(amount):
            self.level.addEntity(Arrow(self.level, self.level.getPlayer(),
                                       self.x, self.y - 0.2, self.z,
                                       random.random() * 360.0,
                                       -random.random() * 60.0, 0.4))
