from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.AILiving import AILiving

import math

class MobSpawner:

    def __init__(self, world):
        self.__worldObj = world

    def spawn(self):
        size = self.__worldObj.width * self.__worldObj.length * self.__worldObj.height // 64 // 64 // 64
        if math.floor(self.__worldObj.rand.random() * 100) < size and \
           self.__worldObj.entitiesInLevelList(EntityLiving) < size * 20:
            self.performSpawning(size, self.__worldObj.playerEntity, None)

    def performSpawning(self, count, entity, loader):
        mobs = 0
        for i in range(count):
            math.floor(self.__worldObj.rand.random() * 5)
            blockX = math.floor(self.__worldObj.rand.random() * self.__worldObj.width)
            blockY = int(min(self.__worldObj.rand.random(), self.__worldObj.rand.random()) * self.__worldObj.height)
            blockZ = math.floor(self.__worldObj.rand.random() * self.__worldObj.length)
            if not self.__worldObj.isBlockNormalCube(blockX, blockY, blockZ) and \
               self.__worldObj.getBlockMaterial(blockX, blockY, blockZ) == Material.air and \
               (not self.__worldObj.isHalfLit(blockX, blockY, blockZ) or \
                math.floor(self.__worldObj.rand.random() * 5) == 0):
                for j in range(8):
                    xx = blockX
                    yy = blockY
                    zz = blockZ
                    for k in range(3):
                        xx += math.floor(self.__worldObj.rand.random() * 6) - math.floor(self.__worldObj.rand.random() * 6)
                        yy += math.floor(self.__worldObj.rand.random() * 1) - math.floor(self.__worldObj.rand.random() * 1)
                        zz += math.floor(self.__worldObj.rand.random() * 6) - math.floor(self.__worldObj.rand.random() * 6)
                        if xx >= 0 and zz >= 0 and yy >= 0 and \
                           yy < self.__worldObj.height - 2 and xx < self.__worldObj.width and zz < self.__worldObj.length and \
                           self.__worldObj.isBlockNormalCube(xx, yy - 1, zz) and not \
                           self.__worldObj.isBlockNormalCube(xx, yy, zz) and not \
                           self.__worldObj.isBlockNormalCube(xx, yy + 1, zz):
                            x = xx + 0.5
                            y = yy + 1.0
                            z = zz + 0.5
                            if entity:
                                xd = x - entity.posX
                                yd = y - entity.posY
                                zd = z - entity.posZ
                            else:
                                xd = x - self.__worldObj.xSpawn
                                yd = y - self.__worldObj.ySpawn
                                zd = z - self.__worldObj.zSpawn

                            if xd * xd + yd * yd + zd * zd < 256.0:
                                continue

                            mob = EntityLiving(self.__worldObj)
                            yaw = self.__worldObj.rand.random() * 360.0
                            mob.setLocationAndAngles(x, y, z, yaw, 0.0)
                            mob.setEntityAI(AILiving())
                            if self.__worldObj.checkIfAABBIsClear(mob.boundingBox):
                                mobs += 1
                                self.__worldObj.spawnEntityInWorld(mob)

        return mobs
