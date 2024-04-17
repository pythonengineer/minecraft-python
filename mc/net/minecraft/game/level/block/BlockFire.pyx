# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.JavaUtils cimport Random

cdef class BlockFire(Block):

    cdef:
        Random __rand
        int[256] __chanceToEncourageFire
        int[256] __abilityToCatchFire

    def __cinit__(self):
        self.__rand = Random()

    def __init__(self, blocks, int blockId, int tex):
        Block.__init__(self, blocks, 51, 31)
        self.__setBurnRate(self.blocks.planks.blockID, 5, 20)
        self.__setBurnRate(self.blocks.wood.blockID, 5, 5)
        self.__setBurnRate(self.blocks.leaves.blockID, 30, 60)
        self.__setBurnRate(self.blocks.bookShelf.blockID, 30, 20)
        self.__setBurnRate(self.blocks.tnt.blockID, 15, 100)
        for i in range(16):
            self.__setBurnRate(self.blocks.clothRed.blockID + i, 30, 60)

        self._setTickOnLoad(True)

    cdef __setBurnRate(self, int block, int chance, int ability):
        self.__chanceToEncourageFire[block] = chance
        self.__abilityToCatchFire[block] = ability

    def getCollisionBoundingBoxFromPool(self, x, y, z):
        return None

    cpdef bint isOpaqueCube(self):
        return False

    cpdef bint renderAsNormalBlock(self):
        return False

    cpdef int getRenderType(self):
        return 3

    cpdef int quantityDropped(self):
        return 0

    cpdef void updateTick(self, World world, int x, int y, int z) except *:
        cdef int xx, yy, zz, highChance, chance
        if self.__canNeighborCatchFire(world, x, y, z) or \
           world.isBlockNormalCube(x, y - 1, z) and self.__rand.nextInt(5) != 0:
            if self.__rand.nextInt(4) == 0 and not self.canBlockCatchFire(world, x, y - 1, z):
                world.setBlockWithNotify(x, y, z, 0)
            else:
                self.__tryToCatchBlockOnFire(world, x + 1, y, z, 300)
                self.__tryToCatchBlockOnFire(world, x - 1, y, z, 300)
                self.__tryToCatchBlockOnFire(world, x, y - 1, z, 100)
                self.__tryToCatchBlockOnFire(world, x, y + 1, z, 200)
                self.__tryToCatchBlockOnFire(world, x, y, z - 1, 300)
                self.__tryToCatchBlockOnFire(world, x, y, z + 1, 300)

                for xx in range(x - 1, x + 2):
                    for zz in range(z - 1, z + 2):
                        for yy in range(y - 1, y + 5):
                            if xx != x or yy != y or zz != z:
                                highChance = 100
                                if yy > y + 1:
                                    highChance = 100 + (yy - (y + 1)) * 100

                                chance = 0
                                if world.getBlockId(xx, yy, zz) == 0:
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx + 1, yy, zz, 0
                                    )
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx - 1, yy, zz, chance
                                    )
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx, yy - 1, zz, chance
                                    )
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx, yy + 1, zz, chance
                                    )
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx, yy, zz - 1, chance
                                    )
                                    chance = self.__getChanceToEncourageFire(
                                        world, xx, yy, zz + 1, chance
                                    )

                                if chance > 0 and self.__rand.nextInt(highChance) <= chance:
                                    world.setBlockWithNotify(xx, yy, zz, self.blockID)
        else:
            world.setBlockWithNotify(x, y, z, 0)

    cdef __tryToCatchBlockOnFire(self, World world, int x, int y, int z, int chance):
        cdef int ability
        cdef bint isTNT

        ability = self.__abilityToCatchFire[world.getBlockId(x, y, z)]
        if self.__rand.nextInt(chance) < ability:
            isTNT = world.getBlockId(x, y, z) == self.blocks.tnt.blockID
            if self.__rand.nextInt(2) == 0:
                world.setBlockWithNotify(x, y, z, self.blockID)
            else:
                world.setBlockWithNotify(x, y, z, 0)

            if isTNT:
                self.blocks.tnt.onBlockDestroyedByPlayer(world, x, y, z)

    cdef bint __canNeighborCatchFire(self, World world, int x, int y, int z):
        if self.canBlockCatchFire(world, x + 1, y, z):
            return True
        elif self.canBlockCatchFire(world, x - 1, y, z):
            return True
        elif self.canBlockCatchFire(world, x, y - 1, z):
            return True
        elif self.canBlockCatchFire(world, x, y + 1, z):
            return True
        elif self.canBlockCatchFire(world, x, y, z - 1):
            return True
        else:
            return self.canBlockCatchFire(world, x, y, z + 1)

    cdef bint isCollidable(self):
        return False

    cpdef bint canBlockCatchFire(self, World world, int x, int y, int z):
        return self.__chanceToEncourageFire[world.getBlockId(x, y, z)] > 0

    cdef int __getChanceToEncourageFire(self, World world, int x, int y, int z, int lastChance):
        cdef int chance = self.__chanceToEncourageFire[world.getBlockId(x, y, z)]
        return chance if chance > lastChance else lastChance

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        if not world.isBlockNormalCube(x, y - 1, z) and not self.__canNeighborCatchFire(world, x, y, z):
            world.setBlockWithNotify(x, y, z, 0)

    cpdef bint canBlockIdCatchFire(self, int blockId):
        return self.__chanceToEncourageFire[blockId] > 0

    cdef fireSpread(self, World world, int x, int y, int z):
        cdef bint isFire = self.__maybeSetFire(world, x, y + 1, z)
        if not isFire:
            isFire = self.__maybeSetFire(world, x - 1, y, z)

        if not isFire:
            isFire = self.__maybeSetFire(world, x + 1, y, z)

        if not isFire:
            isFire = self.__maybeSetFire(world, x, y, z - 1)

        if not isFire:
            isFire = self.__maybeSetFire(world, x, y, z + 1)

        if not isFire:
            isFire = self.__maybeSetFire(world, x, y - 1, z)

        if not isFire:
            world.setBlockWithNotify(x, y, z, self.blocks.fire.blockID)

    cdef bint __maybeSetFire(self, World world, int x, int y, int z):
        cdef int blockId = world.getBlockId(x, y, z)
        if blockId == self.blocks.fire.blockID:
            return True
        elif blockId == 0:
            world.setBlockWithNotify(x, y, z, self.blocks.fire.blockID)
            return True
        else:
            return False
