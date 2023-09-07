from mc.net.minecraft.mob.ai.BasicAttackAI import BasicAttackAI
from mc.net.minecraft.particle.TerrainParticle import TerrainParticle
from mc.net.minecraft.level.tile.Tiles import tiles

import random
import math

class CreeperAI(BasicAttackAI):

    def _attack(self, entity):
        if super().attack(entity):
            self.mob.hurt(entity, 6)
            return True
        else:
            return False

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
            self.level.particleEngine.addParticle(TerrainParticle(self.level,
                                                                  self.mob.x + x,
                                                                  self.mob.y + y,
                                                                  self.mob.z + z,
                                                                  xp, yp, zp,
                                                                  tiles.leaf))
