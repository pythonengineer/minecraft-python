# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.block.BlockFluid cimport BlockFluid
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.level.World cimport World
from mc.JavaUtils cimport Random

cdef class BlockFlowing(BlockFluid):

    def __cinit__(self):
        self.__random = Random()
        self.__flowArray[0] = 0
        self.__flowArray[1] = 1
        self.__flowArray[2] = 2
        self.__flowArray[3] = 3

    def __init__(self, blocks, int blockId, int material):
        BlockFluid.__init__(self, blocks, blockId, material)
        self.__material = material

        self.blockIndexInTexture = 14
        if material == Material.lava:
            self.blockIndexInTexture = 30

        self.blocks.isBlockContainer[blockId] = True

        self.__movingId = blockId
        self.__stillId = blockId + 1

        self._setBlockBounds(0.01, -0.09, 0.01, 1.01, 0.90999997, 1.01)
        self._setTickOnLoad(True)

    cpdef void updateTick(self, World world, int x, int y, int z, Random random) except *:
        self.update(world, x, y, z, 0)

    cdef bint update(self, World world, int x, int y, int z, int _):
        cdef int i, randSide, flowSide
        cdef bint hasChanged, change

        hasChanged = False
        change = self._canFlow(world, x - 1, y, z) or \
                 self._canFlow(world, x + 1, y, z) or \
                 self._canFlow(world, x, y, z - 1) or \
                 self._canFlow(world, x, y, z + 1)
        if change and world.getBlockMaterial(x, y - 1, z) == self.__material and not \
           world.floodFill(x, y - 1, z, self.__movingId, self.__stillId):
            return False

        hasChanged = self.__flow(world, x, y, z, x, y - 1, z)
        for i in range(4):
            randSide = self.__random.nextInt(4 - i) + i
            flowSide = self.__flowArray[i]
            self.__flowArray[i] = self.__flowArray[randSide]
            self.__flowArray[randSide] = flowSide
            if self.__flowArray[i] == 0 and not hasChanged:
                hasChanged = self.__flow(world, x, y, z, x - 1, y, z)
            if self.__flowArray[i] == 1 and not hasChanged:
                hasChanged = self.__flow(world, x, y, z, x + 1, y, z)
            if self.__flowArray[i] == 2 and not hasChanged:
                hasChanged = self.__flow(world, x, y, z, x, y, z - 1)
            if self.__flowArray[i] == 3 and not hasChanged:
                hasChanged = self.__flow(world, x, y, z, x, y, z + 1)

        if not hasChanged and change:
            if self.__random.nextInt(3) == 0:
                if self.__random.nextInt(3) == 0:
                    hasChanged = False
                    for i in range(4):
                        randSide = self.__random.nextInt(4 - i) + i
                        flowSide = self.__flowArray[i]
                        self.__flowArray[i] = self.__flowArray[randSide]
                        self.__flowArray[randSide] = flowSide
                        if self.__flowArray[i] == 0 and not hasChanged:
                            hasChanged = self.__liquidSpread(world, x, y, z, x - 1, y, z)
                        if self.__flowArray[i] == 1 and not hasChanged:
                            hasChanged = self.__liquidSpread(world, x, y, z, x + 1, y, z)
                        if self.__flowArray[i] == 2 and not hasChanged:
                            hasChanged = self.__liquidSpread(world, x, y, z, x, y, z - 1)
                        if self.__flowArray[i] == 3 and not hasChanged:
                            hasChanged = self.__liquidSpread(world, x, y, z, x, y, z + 1)
                elif self.__material == Material.lava:
                    world.setBlockWithNotify(x, y, z, self.blocks.stone.blockID)
                else:
                    world.setBlockWithNotify(x, y, z, 0)

            return False

        if self.__material == Material.water:
            hasChanged |= self.__waterAdjacent(world, x - 1, y, z)
            hasChanged |= self.__waterAdjacent(world, x + 1, y, z)
            hasChanged |= self.__waterAdjacent(world, x, y, z - 1)
            hasChanged |= self.__waterAdjacent(world, x, y, z + 1)
        if self.__material == Material.lava:
            hasChanged |= self.__extinguishFireLava(world, x - 1, y, z)
            hasChanged |= self.__extinguishFireLava(world, x + 1, y, z)
            hasChanged |= self.__extinguishFireLava(world, x, y, z - 1)
            hasChanged |= self.__extinguishFireLava(world, x, y, z + 1)

        if hasChanged:
            world.scheduleBlockUpdate(x, y, z, self.__movingId)
        else:
            world.setTileNoUpdate(x, y, z, self.__stillId)

        return hasChanged

    cdef bint __liquidSpread(self, World world, int x0, int y0, int z0,
                             int x1, int y1, int z1):
        if self._canFlow(world, x1, y1, z1):
            world.setBlockWithNotify(x1, y1, z1, self.blockID)
            world.scheduleBlockUpdate(x1, y1, z1, self.blockID)
            return True
        else:
            return False

    cdef bint __flow(self, World world, int x0, int y0, int z0,
                     int x1, int y1, int z1):
        cdef int pos

        if not self._canFlow(world, x1, y1, z1):
            return False

        pos = world.fluidFlowCheck(x0, y0, z0, self.__movingId, self.__stillId)
        if pos != -9999:
            if pos < 0:
                return False

            x0 = pos % 1024
            pos >>= 10
            z0 = pos % 1024
            y0 = pos >> 10
            y0 %= 1024
            if (y0 > y1 or not self._canFlow(world, x1, y1 - 1, z1)) and \
               y0 <= y1 and x0 != 0 and x0 != world.width - 1 and \
               z0 != 0 and z0 != world.length - 1:
                return False

            world.setBlockWithNotify(x0, y0, z0, 0)

        world.setBlockWithNotify(x1, y1, z1, self.blockID)
        world.scheduleBlockUpdate(x1, y1, z1, self.blockID)
        return True

    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer):
        cdef int block
        if x >= 0 and y >= 0 and z >= 0 and x < world.width and z < world.length:
            block = world.getBlockId(x, y, z)
            if block != self.__movingId and block != self.__stillId:
                if layer == 1 and (world.getBlockId(x - 1, y, z) == 0 or \
                                   world.getBlockId(x + 1, y, z) == 0 or
                                   world.getBlockId(x, y, z - 1) == 0 or \
                                   world.getBlockId(x, y, z + 1) == 0):
                    return True
                else:
                    return BlockFluid.shouldSideBeRendered(self, world, x, y, z, layer)
        else:
            return False

    cdef bint isCollidable(self):
        return False

    def getCollisionBoundingBoxFromPool(self, int x, int y, int z):
        return None

    cpdef bint isOpaqueCube(self):
        return False

    cpdef int getBlockMaterial(self):
        return self.__material

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        pass

    cdef int tickRate(self):
        return 25 if self.__material == Material.lava else 5

    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance):
        pass

    def dropBlockAsItem(self, World world, int x, int y, int z):
        pass

    cpdef int quantityDropped(self, Random random):
        return 0

    cdef int getRenderBlockPass(self):
        return 1 if self.__material == Material.water else 0

    cdef bint __waterAdjacent(self, World world, int x, int y, int z):
        if world.getBlockId(x, y, z) == self.blocks.fire.blockID:
            world.setBlockWithNotify(x, y, z, 0)
            return True
        elif world.getBlockId(x, y, z) != self.blocks.lavaMoving.blockID and \
             world.getBlockId(x, y, z) != self.blocks.lavaStill.blockID:
            return False
        else:
            world.setBlockWithNotify(x, y, z, self.blocks.stone.blockID)
            return True

    cdef bint __extinguishFireLava(self, World world, int x, int y, int z):
        if self.blocks.fire.canBlockIdCatchFire(world.getBlockId(x, y, z)):
            self.blocks.fire.fireSpread(world, x, y, z)
            return True
        else:
            return False
