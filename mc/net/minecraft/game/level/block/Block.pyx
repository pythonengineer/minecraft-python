# cython: language_level=3

from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from mc.net.minecraft.game.level.material.Material cimport Material
from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
from mc.net.minecraft.game.entity.player.ItemStack import ItemStack
from mc.net.minecraft.game.physics.AxisAlignedBB import AxisAlignedBB

import random

cdef class Block:

    def __init__(self, blocks, int blockId, int tex=0):
        self.blocks = blocks
        self.blockID = blockId
        if tex:
            self.blockIndexInTexture = tex
        self.blockIsDropped = True
        self.stepSound = blocks.soundPowderFootstep
        self.blockParticleGravity = 1.0
        self._setBlockBounds(0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        self.blocks.opaqueCubeLookup[blockId] = self.isOpaqueCube()
        self.blocks.lightOpacity[blockId] = 255 if self.isOpaqueCube() else 0
        self.blocks.canBlockGrass[blockId] = self.renderAsNormalBlock()
        self.blocks.isBlockFluid[blockId] = False

    def setLightOpacity(self, int opacity):
        self.blocks.lightOpacity[self.blockID] = opacity
        return self

    def setLightValue(self, float value):
        self.blocks.lightValue[self.blockID] = <int>(8.0 * value)
        return self

    cpdef bint renderAsNormalBlock(self):
        return True

    cpdef int getRenderType(self):
        return 0

    def setHardness(self, float pitch):
        self.__hardness = <int>(pitch * 20.0)
        return self

    def _setTickOnLoad(self, bint tick):
        self.blocks.tickOnLoad[self.blockID] = tick

    def _setBlockBounds(self, float minX, float minY, float minZ,
                        float maxX, float maxY, float maxZ):
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ

    cdef float getBlockBrightness(self, World world, int x, int y, int z):
        return world.getBlockLightValue(x, y, z)

    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer):
        return not world.isBlockNormalCube(x, y, z)

    cpdef int getBlockTexture(self, int face):
        return self.blockIndexInTexture

    def getSelectedBoundingBoxFromPool(self, int x, int y, int z):
        return AxisAlignedBB(x + self.minX, y + self.minY, z + self.minZ,
                             x + self.maxX, y + self.maxY, z + self.maxZ)

    def getCollisionBoundingBoxFromPool(self, int x, int y, int z):
        return AxisAlignedBB(x + self.minX, y + self.minY, z + self.minZ,
                             x + self.maxX, y + self.maxY, z + self.maxZ)

    cpdef bint isOpaqueCube(self):
        return True

    cpdef void updateTick(self, World world, int x, int y, int z, random) except *:
        pass

    def onBlockDestroyedByPlayer(self, World world, int x, int y, int z):
        pass

    cpdef int getBlockMaterial(self):
        return Material.air

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        pass

    def onBlockPlaced(self, World world, int x, int y, int z):
        pass

    cdef int tickRate(self):
        return 5

    def onBlockAdded(self, World world, int x, int y, int z):
        pass

    def onBlockRemoval(self, World world, int x, int y, int z):
        pass

    cpdef int quantityDropped(self, random):
        return 1

    cpdef int idDropped(self):
        return self.blockID

    def blockStrength(self):
        return self.__hardness

    def dropBlockAsItem(self, World world, int x, int y, int z):
        self.dropBlockAsItemWithChance(world, x, y, z, 1.0)

    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance):
        cdef int i
        cdef float xx, yy, zz

        for i in range(self.quantityDropped(world.rand)):
            if world.rand.random() > chance:
                continue

            xx = world.rand.random() * 0.7 + 0.15
            yy = world.rand.random() * 0.7 + 0.15
            zz = world.rand.random() * 0.7 + 0.15
            item = EntityItem(
                world, x + xx, y + yy, z + zz,
                ItemStack(self.blocks.blocksList[self.idDropped()], 1)
            )
            item.delayBeforeCanPickup = 20
            world.spawnEntityInWorld(item)

    cdef bint isExplosionResistant(self):
        return self.blockIsDropped

    cdef collisionRayTrace(self, int x, int y, int z, v0, v1):
        v0 = v0.addVector(-x, -y, -z)
        v1 = v1.addVector(-x, -y, -z)
        vec36 = v0.getIntermediateWithXValue(v1, self.minX)
        vec37 = v0.getIntermediateWithXValue(v1, self.maxX)
        vec38 = v0.getIntermediateWithYValue(v1, self.minY)
        vec39 = v0.getIntermediateWithYValue(v1, self.maxY)
        vec310 = v0.getIntermediateWithZValue(v1, self.minZ)
        v1 = v0.getIntermediateWithZValue(v1, self.maxZ)
        if not self.__isVecInsideYZBounds(vec36):
            vec36 = None
        if not self.__isVecInsideYZBounds(vec37):
            vec37 = None
        if not self.__isVecInsideXZBounds(vec38):
            vec38 = None
        if not self.__isVecInsideXZBounds(vec39):
            vec39 = None
        if not self.__isVecInsideXYBounds(vec310):
            vec310 = None
        if not self.__isVecInsideXYBounds(v1):
            v1 = None

        vec311 = None
        if vec36:
            vec311 = vec36

        if vec37 and (not vec311 or v0.distanceTo(vec37) < v0.distanceTo(vec311)):
            vec311 = vec37
        if vec38 and (not vec311 or v0.distanceTo(vec38) < v0.distanceTo(vec311)):
            vec311 = vec38
        if vec39 and (not vec311 or v0.distanceTo(vec39) < v0.distanceTo(vec311)):
            vec311 = vec39
        if vec310 and (not vec311 or v0.distanceTo(vec310) < v0.distanceTo(vec311)):
            vec311 = vec310

        if v1 and (not vec311 or v0.distanceTo(v1) < v0.distanceTo(vec311)):
            vec311 = v1

        if not vec311:
            return

        cdef char v01 = -1
        if vec311 == vec36:
            v01 = 4
        elif vec311 == vec37:
            v01 = 5
        elif vec311 == vec38:
            v01 = 0
        elif vec311 == vec39:
            v01 = 1
        elif vec311 == vec310:
            v01 = 2
        elif vec311 == v1:
            v01 = 3

        return MovingObjectPosition(x, y, z, v01, vec311.addVector(x, y, z))

    cdef bint __isVecInsideYZBounds(self, vec):
        if vec:
            return vec.yCoord >= self.minY and vec.yCoord <= self.maxY and vec.zCoord >= self.minZ and vec.zCoord <= self.maxZ
        else:
            return False

    cdef bint __isVecInsideXZBounds(self, vec):
        if vec:
            return vec.xCoord >= self.minX and vec.xCoord <= self.maxX and vec.zCoord >= self.minZ and vec.zCoord <= self.maxZ
        else:
            return False

    cdef bint __isVecInsideXYBounds(self, vec):
        if vec:
            return vec.xCoord >= self.minX and vec.xCoord <= self.maxX and vec.yCoord >= self.minY and vec.yCoord <= self.maxY
        else:
            return False

    def onBlockDestroyedByExplosion(self, world, x, y, z):
        pass

    cdef int getRenderBlockPass(self):
        return 0
