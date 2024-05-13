from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.AILiving import AILiving

class MobSpawner:

    def __init__(self, world):
        self.__level = world

    def spawnMobs(self):
        size = self.__level.width * self.__level.length * self.__level.height // 64 // 64 // 64
        if self.__level.rand.nextInt(100) < size and \
           self.__level.entitiesInLevelList(EntityLiving) < size * 20:
            self.spawnMob(size, self.__level.playerEntity, None)

    def spawnMob(self, count, entity, loader):
        mobs = 0
        for i in range(count):
            self.__level.rand.nextInt(5)
            blockX = self.__level.rand.nextInt(self.__level.width)
            blockY = int(min(self.__level.rand.nextFloat(),
                             self.__level.rand.nextFloat()) * self.__level.height)
            blockZ = self.__level.rand.nextInt(self.__level.length)
            if not self.__level.isBlockNormalCube(blockX, blockY, blockZ) and \
               self.__level.getBlockMaterial(blockX, blockY, blockZ) == Material.air and \
               (not self.__level.isHalfLit(blockX, blockY, blockZ) or \
                self.__level.rand.nextInt(5) == 0):
                for j in range(8):
                    xx = blockX
                    yy = blockY
                    zz = blockZ
                    for k in range(3):
                        xx += self.__level.rand.nextInt(6) - self.__level.rand.nextInt(6)
                        yy += self.__level.rand.nextInt(1) - self.__level.rand.nextInt(1)
                        zz += self.__level.rand.nextInt(6) - self.__level.rand.nextInt(6)
                        if xx >= 0 and zz >= 0 and yy >= 0 and \
                           yy < self.__level.height - 2 and xx < self.__level.width and zz < self.__level.length and \
                           self.__level.isBlockNormalCube(xx, yy - 1, zz) and not \
                           self.__level.isBlockNormalCube(xx, yy, zz) and not \
                           self.__level.isBlockNormalCube(xx, yy + 1, zz):
                            x = xx + 0.5
                            y = yy + 1.0
                            z = zz + 0.5
                            if entity:
                                xd = x - entity.posX
                                yd = y - entity.posY
                                zd = z - entity.posZ
                            else:
                                xd = x - self.__level.xSpawn
                                yd = y - self.__level.ySpawn
                                zd = z - self.__level.zSpawn

                            if xd * xd + yd * yd + zd * zd < 256.0:
                                continue

                            mob = EntityLiving(self.__level)
                            yaw = self.__level.rand.nextFloat() * 360.0
                            mob.setPositionAndRotation(x, y, z, yaw, 0.0)
                            mob.setAI(AILiving())
                            if self.__level.checkIfAABBIsClearSpawn(mob.boundingBox):
                                mobs += 1
                                self.__level.spawnEntityInWorld(mob)

        return mobs
