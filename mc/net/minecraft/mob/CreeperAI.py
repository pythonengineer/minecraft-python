from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI
from mc.net.minecraft.particle.Particle import Particle
from mc.net.minecraft.level.tile.Tiles import tiles

import random
import math

class CreeperAI(BasicAttackAI):

    def __init__(self, creeper):
        super().__init__()
        self.__creeper = creeper

    def _hurt(self, entity):
        super().hurt(entity)
        self.__creeper.hurt(entity, 4)

    def beforeRemove(self):
        f = 4.0
        self.level.explode(self.mob, self.mob.x, self.mob.y, self.mob.z, f)
        for i in range(500):
            x = random.gauss(0.0, 1.0) * f / 4.0
            y = random.gauss(0.0, 1.0) * f / 4.0
            z = random.gauss(0.0, 1.0) * f / 4.0
            f5 = math.sqrt(x * x + y * y + z * z)
            xp = x / f5 / f5
            yp = y / f5 / f5
            zp = z / f5 / f5
            self.level.particleEngine.addParticle(Particle(self.level,
                                                           self.mob.x + x,
                                                           self.mob.y + y,
                                                           self.mob.z + z,
                                                           xp, yp, zp,
                                                           tiles.leaf))
