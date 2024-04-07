# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.level.World cimport World

cdef class BlockFluid(Block):

    def __init__(self, blocks, int blockId, int material):
        Block.__init__(self, blocks, blockId)
        self._material = material

        self.blockIndexInTexture = 14
        if material == Material.lava:
            self.blockIndexInTexture = 30

        self.blocks.isBlockFluid[blockId] = True

        self._movingId = blockId
        self._stillId = blockId + 1

        self._setBlockBounds(0.01, -0.09, 0.01, 1.01, 0.90999997, 1.01)
        self._setTickOnLoad(True)

    cpdef int getBlockTexture(self, int face):
        if self._material == Material.lava or face == 1 or face == 0:
            return self.blockIndexInTexture
        else:
            return self.blockIndexInTexture + 32

    cpdef bint renderAsNormalBlock(self):
        return False

    def onBlockPlaced(self, World world, int x, int y, int z):
        world.scheduleBlockUpdate(x, y, z, self._movingId)

    cpdef void updateTick(self, World world, int x, int y, int z, random) except *:
        cdef bint firstLoop, hasChanged, change
        hasChanged = False
        change = False
        firstLoop = True
        while (change and self._material != Material.lava) or firstLoop:
            y -= 1
            firstLoop = False
            if world.getBlockId(x, y, z) != 0 or not self.__canFlow(world, x, y, z):
                break

            change = world.setBlockWithNotify(x, y, z, self._movingId)
            if change:
                hasChanged = True

        y += 1
        if self._material == Material.water or not hasChanged:
            hasChanged |= self.__flow(world, x - 1, y, z)
            hasChanged |= self.__flow(world, x + 1, y, z)
            hasChanged |= self.__flow(world, x, y, z - 1)
            hasChanged |= self.__flow(world, x, y, z + 1)

        if hasChanged:
            world.scheduleBlockUpdate(x, y, z, self._movingId)
        else:
            world.setTileNoUpdate(x, y, z, self._stillId)

    cdef bint __canFlow(self, World world, int x, int y, int z):
        cdef int xx, yy, zz

        if self._material == Material.water:
            for xx in range(x - 2, x + 3):
                for yy in range(y - 2, y + 3):
                    for zz in range(z - 2, z + 3):
                        if world.getBlockId(xx, yy, zz) == self.blocks.sponge.blockID:
                            return False

        return True

    cdef bint __flow(self, World world, int x, int y, int z):
        if world.getBlockId(x, y, z) == 0:
            if not self.__canFlow(world, x, y, z):
                return False

            if world.setBlockWithNotify(x, y, z, self._movingId):
                world.scheduleBlockUpdate(x, y, z, self._movingId)

        return False

    cdef float getBlockBrightness(self, World world, int x, int y, int z):
        return 100.0 if self._material == Material.lava else world.getBlockLightValue(x, y, z)

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

    def getCollisionBoundingBoxFromPool(self, int x, int y, int z):
        return None

    cpdef bint isOpaqueCube(self):
        return False

    cpdef int getBlockMaterial(self):
        return self._material

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        cdef int material

        if blockType != 0:
            material = (<Block>self.blocks.blocksList[blockType]).getBlockMaterial()
            if self._material == Material.water and material == Material.lava or \
               material == Material.water and self._material == Material.lava:
                world.setBlockWithNotify(x, y, z, self.blocks.stone.blockID)
                return

        world.scheduleBlockUpdate(x, y, z, blockType)

    cdef int tickRate(self):
        return 25 if self._material == Material.lava else 5

    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance):
        pass

    def dropBlockAsItem(self, World world, int x, int y, int z):
        pass

    cpdef int quantityDropped(self, random):
        return 0

    cdef int getRenderBlockPass(self):
        return 1 if self._material == Material.water else 0
