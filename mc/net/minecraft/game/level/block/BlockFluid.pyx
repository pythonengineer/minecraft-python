# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.level.World cimport World
from mc.JavaUtils cimport Random

cdef class BlockFluid(Block):

    def __init__(self, blocks, int blockId, material):
        Block.__init__(self, blocks, blockId, material)

        self.blockIndexInTexture = 14
        if material == Material.lava:
            self.blockIndexInTexture = 30

        self.blocks.isBlockContainer[blockId] = True

        self._movingId = blockId
        self._stillId = blockId + 1

        self._setBlockBounds(0.01, -0.09, 0.01, 1.01, 0.90999997, 1.01)
        self._setTickOnLoad(True)
        self.setResistance(2.0)

    cpdef int getBlockTexture(self, int face):
        if self.material == Material.lava or face == 1 or face == 0:
            return self.blockIndexInTexture
        else:
            return self.blockIndexInTexture + 32

    cpdef bint renderAsNormalBlock(self):
        return False

    cpdef void updateTick(self, World world, int x, int y, int z, Random random) except *:
        self.update(world, x, y, z, 0)

    cdef bint update(self, World world, int x, int y, int z, int _):
        cdef bint hasChanged = False
        cdef bint change = False
        while True:
            y -= 1
            if not self._canFlow(world, x, y, z):
                break

            change = world.setBlockWithNotify(x, y, z, self._movingId)
            if change:
                hasChanged = True

            if not change or self.material == Material.lava:
                break

        y += 1
        if self.material == Material.water or not hasChanged:
            hasChanged |= self.__flow(world, x - 1, y, z)
            hasChanged |= self.__flow(world, x + 1, y, z)
            hasChanged |= self.__flow(world, x, y, z - 1)
            hasChanged |= self.__flow(world, x, y, z + 1)

        if self.material == Material.lava:
            hasChanged |= self.__extinguishFireLava(world, x - 1, y, z)
            hasChanged |= self.__extinguishFireLava(world, x + 1, y, z)
            hasChanged |= self.__extinguishFireLava(world, x, y, z - 1)
            hasChanged |= self.__extinguishFireLava(world, x, y, z + 1)

        if hasChanged:
            world.scheduleBlockUpdate(x, y, z, self._movingId)
        else:
            world.setTileNoUpdate(x, y, z, self._stillId)

        return hasChanged

    cpdef bint _canFlow(self, World world, int x, int y, int z):
        cdef int blockId, xx, yy, zz

        blockId = world.getBlockId(x, y, z)
        if blockId != 0 and blockId != self.blocks.fire.blockID:
            return False

        if self.material == Material.water:
            for xx in range(x - 2, x + 3):
                for yy in range(y - 2, y + 3):
                    for zz in range(z - 2, z + 3):
                        if world.getBlockId(xx, yy, zz) == self.blocks.sponge.blockID:
                            return False

        return True

    cdef bint __extinguishFireLava(self, World world, int x, int y, int z):
        if self.blocks.fire.getChanceOfNeighborsEncouragingFire(world.getBlockId(x, y, z)):
            self.blocks.fire.fireSpread(world, x, y, z)
            return True
        else:
            return False

    cdef bint __flow(self, World world, int x, int y, int z):
        cdef bint isSet

        if not self._canFlow(world, x, y, z):
            return False

        isSet = world.setBlockWithNotify(x, y, z, self._movingId)
        if isSet:
            world.scheduleBlockUpdate(x, y, z, self._movingId)

        return False

    cdef float getBlockBrightness(self, World world, int x, int y, int z):
        return 100.0 if self.material == Material.lava else world.getBlockLightValue(x, y, z)

    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer):
        cdef int block
        if x >= 0 and y >= 0 and z >= 0 and x < world.width and z < world.length:
            block = world.getBlockId(x, y, z)
            if block != self._movingId and block != self._stillId:
                if layer == 1 and (world.getBlockId(x - 1, y, z) == 0 or world.getBlockId(x + 1, y, z) == 0 or
                                   world.getBlockId(x, y, z - 1) == 0 or world.getBlockId(x, y, z + 1) == 0):
                    return True
                else:
                    return Block.shouldSideBeRendered(self, world, x, y, z, layer)

        return False

    cpdef bint isCollidable(self):
        return False

    def getCollisionBoundingBoxFromPool(self, int x, int y, int z):
        return None

    cpdef bint isOpaqueCube(self):
        return False

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        if blockType != 0:
            material = self.blocks.blocksList[blockType].material
            if self.material == Material.water and material == Material.lava or \
               material == Material.water and self.material == Material.lava:
                world.setBlockWithNotify(x, y, z, self.blocks.stone.blockID)

        world.scheduleBlockUpdate(x, y, z, self.blockID)

    cdef int tickRate(self):
        return 25 if self.material == Material.lava else 5

    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance):
        pass

    def dropBlockAsItem(self, World world, int x, int y, int z):
        pass

    cpdef int quantityDropped(self, Random random):
        return 0

    cdef int getRenderBlockPass(self):
        return 1 if self.material == Material.water else 0

    cpdef void randomDisplayTick(self, World world, int x, int y, int z, Random random) except *:
        cdef float posX, posY, posZ
        if self.material == Material.lava and \
           world.getBlockMaterial(x, y + 1, z) == Material.air and not \
           world.isBlockNormalCube(x, y + 1, z) and random.nextInt(100) == 0:
            posX = x + random.nextFloat()
            posY = y + self.maxY
            posZ = z + random.nextFloat()
            world.spawnParticle('lava', posX, posY, posZ, 0.0, 0.0, 0.0)
