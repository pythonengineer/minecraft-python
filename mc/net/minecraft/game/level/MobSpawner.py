from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.entity.AILiving import AILiving
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.animal.EntityPig import EntityPig
from mc.net.minecraft.game.entity.animal.EntitySheep import EntitySheep
from mc.net.minecraft.game.entity.monster.EntityCreeper import EntityCreeper
from mc.net.minecraft.game.entity.monster.EntitySkeleton import EntitySkeleton
from mc.net.minecraft.game.entity.monster.EntitySpider import EntitySpider
from mc.net.minecraft.game.entity.monster.EntityZombie import EntityZombie
from mc.JavaUtils import random

class MobSpawner:

    def __init__(self, world):
        self.__worldObj = world

    def spawnMobs(self):
        size = self.__worldObj.width * self.__worldObj.length * self.__worldObj.height // 64 // 64 // 64
        if self.__worldObj.rand.nextInt(100) < size and \
           self.__worldObj.entitiesInLevelList(EntityLiving) < size * 20:
            self.spawnMob(size, self.__worldObj.playerEntity, None)

    def spawnMob(self, count, entity, loader):
        mobs = 0
        for i in range(count):
            self.__worldObj.rand.nextInt(6)
            blockX = self.__worldObj.rand.nextInt(self.__worldObj.width)
            blockY = int(min(self.__worldObj.rand.nextFloat(),
                             self.__worldObj.rand.nextFloat()) * self.__worldObj.height)
            blockZ = self.__worldObj.rand.nextInt(self.__worldObj.length)
            if not self.__worldObj.isBlockNormalCube(blockX, blockY, blockZ) and \
               self.__worldObj.getBlockMaterial(blockX, blockY, blockZ) == Material.air and \
               (not self.__worldObj.isHalfLit(blockX, blockY, blockZ) or \
                self.__worldObj.rand.nextInt(5) == 0):
                for j in range(8):
                    xx = blockX
                    yy = blockY
                    zz = blockZ
                    for k in range(3):
                        xx += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
                        yy += self.__worldObj.rand.nextInt(1) - self.__worldObj.rand.nextInt(1)
                        zz += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
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

                            mob = None
                            choice = int(random() * 7.0)
                            if choice == 0:
                                mob = EntitySkeleton(self.__worldObj)
                            elif choice == 1:
                                mob = EntityPig(self.__worldObj)
                            elif choice == 2:
                                mob = EntityCreeper(self.__worldObj)
                            elif choice == 3:
                                mob = EntitySpider(self.__worldObj)
                            elif choice == 4:
                                mob = EntitySheep(self.__worldObj)
                            elif choice == 6:
                                mob = EntityZombie(self.__worldObj)

                            if not mob:
                                continue

                            yaw = self.__worldObj.rand.nextFloat() * 360.0
                            mob.setPositionAndRotation(x, y, z, yaw, 0.0)
                            mob.setEntityAI(AILiving())
                            if self.__worldObj.checkIfAABBIsClearSpawn(mob.boundingBox):
                                mobs += 1
                                self.__worldObj.spawnEntityInWorld(mob)

        return mobs
