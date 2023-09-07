from mc.net.minecraft.Entity import Entity
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.particle.SmokeParticle import SmokeParticle

import random

class Smolder(Entity):

    def __init__(self, level, x, y, z):
        super().__init__(level)
        self.life = 0
        self.setSize(0.0, 0.0)
        self.setPos(x + 0.5, y + 0.1, z + 0.5)
        self.heightOffset = 1.5
        self.makeStepSound = False
        self.lifeTime = int(40.0 / (random.random() * 0.8 + 0.2))

    def isPickable(self):
        return not self.removed

    def tick(self):
        f1 = random.random() - 0.5
        f2 = random.random() - 0.5
        for i in range(4):
            if random.random() > self.life / self.lifeTime:
                self.level.particleEngine.addParticle(SmokeParticle(self.level,
                                                                    self.x + f1,
                                                                    self.y,
                                                                    self.z + f2))

        self.life += 1
        if self.life - 1 < self.lifeTime:
            x = self.x
            y = int(self.y - 0.3)
            z = self.z
            tile = self.level.getTile(x, y, z)
            if tile and tiles.tiles[tile].isSolid():
                return

        self.remove()
