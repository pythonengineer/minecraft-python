from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI

import random

class SkeletonAI(BasicAttackAI):

    def tick(self, level, mob):
        super().tick(level, mob)
        if mob.health > 0 and int(random.random() * 30) == 0 and self.attackTarget:
            self.mob.shootArrow(level)

    def beforeRemove(self):
        self.mob.access()
