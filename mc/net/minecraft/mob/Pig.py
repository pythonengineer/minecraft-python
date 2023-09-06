from mc.net.minecraft.mob.QuadrupedMob import QuadrupedMob
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.item.Item import Item

import random

class Pig(QuadrupedMob):

    def __init__(self, level, x, y, z):
        super().__init__(level, x, y, z)
        self.heightOffset = 1.72
        self.modelName = 'pig'
        self._textureName = 'mob/pig.png'

    def die(self, entity):
        if entity:
            entity.awardKillScore(self, 10)

        amount = int(random.random() + random.random() + 1.0)
        for i in range(amount):
            self.level.addEntity(Item(self.level, self.x, self.y, self.z, tiles.mushroomBrown.id))

        super().die(entity)
