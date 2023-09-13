from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.mob.Zombie import Zombie
from mc.net.minecraft.mob.Skeleton import Skeleton
from mc.net.minecraft.mob.Pig import Pig
from mc.net.minecraft.mob.Creeper import Creeper
from mc.net.minecraft.mob.Spider import Spider
from mc.net.minecraft.mob.Sheep import Sheep

import math

class MobSpawner:

    def __init__(self, level):
        self.level = level

    def spawnMobs(self, count, entity, loader):
        mobs = 0
        for i in range(count):
            mobType = math.floor(self.level.rand.random() * 5)
            i7 = math.floor(self.level.rand.random() * self.level.width)
            i8 = int(min(self.level.rand.random(), self.level.rand.random()) * self.level.depth)
            i9 = math.floor(self.level.rand.random() * self.level.height)
            if not self.level.isSolidTile(i7, i8, i9) and self.level.getLiquid(i7, i8, i9) == Liquid.none and \
               (not self.level.isLit(i7, i8, i9) or math.floor(self.level.rand.random() * 5) == 0):
                for i10 in range(3):
                    xx = i7
                    yy = i8
                    zz = i9
                    for i14 in range(3):
                        xx += math.floor(self.level.rand.random() * 6) - math.floor(self.level.rand.random() * 6)
                        yy += math.floor(self.level.rand.random() * 1) - math.floor(self.level.rand.random() * 1)
                        zz += math.floor(self.level.rand.random() * 6) - math.floor(self.level.rand.random() * 6)
                        if xx >= 0 and zz >= 1 and yy >= 0 and \
                           yy < self.level.depth - 2 and xx < self.level.width and zz < self.level.height and \
                           self.level.isSolidTile(xx, yy - 1, zz) and not \
                           self.level.isSolidTile(xx, yy, zz) and not \
                           self.level.isSolidTile(xx, yy + 1, zz):
                            x = xx + 0.5
                            y = yy + 1.0
                            z = zz + 0.5
                            if entity:
                                xd = x - entity.x
                                yd = y - entity.y
                                zd = z - entity.z
                                if xd * xd + yd * yd + zd * zd < 256.0:
                                    continue
                            else:
                                xd = x - self.level.xSpawn
                                yd = y - self.level.ySpawn
                                zd = z - self.level.zSpawn
                                if xd * xd + yd * yd + zd * zd < 256.0:
                                    continue

                            if mobType == 0:
                                Zombie(self.level, x, y, z)
                            elif mobType == 1:
                                Skeleton(self.level, x, y, z)
                            elif mobType == 2:
                                Pig(self.level, x, y, z)
                            elif mobType == 3:
                                Creeper(self.level, x, y, z)
                            elif mobType == 4:
                                Spider(self.level, x, y, z)

                            sheep = Sheep(self.level, x, y, z)
                            if self.level.isFree(sheep.bb):
                                mobs += 1
                                self.level.addEntity(sheep)

        return mobs
