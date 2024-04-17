# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport sqrt, floor, isnan

from mc.net.minecraft.game.physics.MovingObjectPosition import MovingObjectPosition
from mc.net.minecraft.game.level.material.Material import Material
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.net.minecraft.game.physics.Vec3D import Vec3D
from mc.net.minecraft.game.level.EntityMap cimport EntityMap
from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils cimport Random

import random
import time
import gc

cdef class NextTickListEntry:

    cdef:
        public int xCoord
        public int yCoord
        public int zCoord
        public int blockID
        public int scheduledTime

    def __init__(self, int x, int y, int z, int blockID):
        self.xCoord = x
        self.yCoord = y
        self.zCoord = z
        self.blockID = blockID

cdef class World:
    MAX_TICKS = 100

    def __cinit__(self):
        cdef int i
        cdef float br
        cdef Block block

        self.__maxTicks = World.MAX_TICKS

        for i in range(16):
            br = 1.0 - i / 15.0
            self.__lightBrightnessTable[i] = (1.0 - br) / (br * 3.0 + 1.0) * 0.9 + 0.1

        for i, block in enumerate(blocks.blocksList):
            self.__isBlockNormal[i] = False if block is None else block.isOpaqueCube()

        self.rotSpawn = 0.0

        self.defaultFluid = blocks.waterMoving.blockID

        self.__worldAccesses = set()
        self.__tickList = set()

        self.__rand = Random()
        self.__randId = random.getrandbits(31)

        self.skyColor = 0x99CCFF
        self.fogColor = 0xFFFFFF
        self.cloudColor = 0xFFFFFF

        self.__updateLCG = 0
        self.__playTime = 0

        self.multiplier = 3
        self.addend = 1013904223

        self.survivalWorld = True

        self.skyBrightness = 1.0

    def __dealloc__(self):
        free(self.__blocks)
        free(self.__data)
        free(self.__heightMap)

    def load(self):
        if not self.__blocks:
            raise RuntimeError('The level is corrupt!')

        self.__worldAccesses = set()
        self.__heightMap = <int*>malloc(sizeof(int) * (self.width * self.length))
        for i in range(self.width * self.length):
            self.__heightMap[i] = self.height

        self.__updateSkylight(0, 0, self.width, self.length)
        self.__randId = random.getrandbits(31)
        self.__tickList = set()

        if not self.entityMap:
            self.entityMap = EntityMap(self.width, self.height, self.length)

    def generate(self, int w, int h, int d, bytearray b):
        cdef int x, y, z, i, skyBrightness, br
        cdef char blockId

        self.width = w
        self.height = h
        self.length = d
        self.__blocks = <char*>malloc(sizeof(char) * len(b))
        self.__data = <char*>malloc(sizeof(char) * len(b))

        for i in range(256):
            self.__lightOpacity[i] = blocks.lightOpacity[i]
            self.__lightValue[i] = blocks.lightValue[i]

        for x in range(self.width):
            for z in range(self.length):
                y = 0
                while y < self.height:
                    blockId = 0
                    if y < self.groundLevel - 1:
                        blockId = blocks.bedrock.blockID
                    elif y < self.groundLevel:
                        if self.groundLevel > self.waterLevel and self.defaultFluid == blocks.waterMoving.blockID:
                            blockId = blocks.grass.blockID
                        else:
                            blockId = blocks.dirt.blockID
                    elif y < self.waterLevel:
                        blockId = self.defaultFluid

                    b[(y * self.length + z) * self.width + x] = blockId
                    if y == 0 and x != 0 and z != 0 and x != self.width - 1 and z != self.length - 1:
                        y = self.height - 2

                    y += 1

        for i in range(len(b)):
            self.__blocks[i] = b[i]
            self.__data[i] = 0

        self.__heightMap = <int*>malloc(sizeof(int) * (w * d))
        for i in range(w * d):
            self.__heightMap[i] = h

        skyBrightness = <int>(15.0 * self.skyBrightness)
        for x in range(self.width):
            for z in range(self.length):
                y = self.height - 1
                while y > 0 and self.__lightOpacity[self.getBlockId(x, y, z)] == 0:
                    y -= 1

                self.__heightMap[x + y * self.width] = z + 1

                for y in range(self.height):
                    br = self.__heightMap[x + z * self.width]
                    br = skyBrightness if y >= br else 0
                    blockId = self.__blocks[(y * self.length + z) * self.width + x]
                    if br < self.__lightValue[blockId]:
                        br = self.__lightValue[blockId]

                    self.__data[(y * self.length + z) * self.width + x] = <char>br

        for x in range(self.width):
            for z in range(self.length):
                self.__updateLight(x, 0, z, x + 1, self.height, z + 1)

        for worldAccess in self.__worldAccesses:
            worldAccess.loadRenderers()

        self.__tickList.clear()
        self.findSpawn()
        self.load()
        gc.collect()

    cdef findSpawn(self):
        cdef int i, x, z, y

        rand = random.Random()
        x = 0
        y = 0
        z = 0
        while True:
            i = 0
            while True:
                i += 1
                x = <int>floor(rand.random() * (self.width // 2)) + self.width // 4
                z = <int>floor(rand.random() * (self.length // 2)) + self.length // 4
                y = self.__getFirstUncoveredBlock(x, z) + 1
                if y >= 4:
                    break

            if i == 10000:
                self.xSpawn = x
                self.ySpawn = -100
                self.zSpawn = z
                break

            if y > self.waterLevel:
                self.xSpawn = x
                self.ySpawn = y
                self.zSpawn = z
                break

    cdef void __updateSkylight(self, int x0, int y0, int x1, int y1) except *:
        cdef int x, z, oldDepth, y, yl0, yl1

        for x in range(x0, x0 + x1):
            for z in range(y0, y0 + y1):
                oldDepth = self.__heightMap[x + z * self.width]
                y = self.height - 1
                while y > 0 and not self.__lightOpacity[self.getBlockId(x, y, z)]:
                    y -= 1

                self.__heightMap[x + z * self.width] = y + 1

                if oldDepth != y:
                    yl0 = oldDepth if oldDepth < y else y
                    yl1 = oldDepth if oldDepth > y else y
                    self.__updateLight(x, yl0, z, x + 1, yl1, z + 1)

        self.__updateLight(0, 0, 0, 10, 10, 10)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef void __updateLight(self, int x0, int y0, int z0, int x1, int y1, int z1):
        cdef int i, x, y, z, count, br, counter, depth, opacity, newDepth
        cdef int* floodFillCounters
        cdef char block

        floodFillCounters = <int*>malloc(sizeof(int) * 8192)
        for i in range(8192):
            floodFillCounters[i] = 0

        count = 0
        for x in range(x0, x1):
            for z in range(z0, z1):
                for y in range(y0, y1):
                    floodFillCounters[count] = x << 20 | y << 10 | z
                    count += 1

        br = <int>(15.0 * self.skyBrightness)

        while count > 0:
            while count > 8176:
                count -= 1
                counter = floodFillCounters[count]
                x = counter >> 20 & 1023
                y = counter >> 10 & 1023
                z = counter & 1023
                self.__updateLight(x, y, z, x + 1, y + 1, z + 1)

            count -= 1
            counter = floodFillCounters[count]
            x = counter >> 20 & 1023
            y = counter >> 10 & 1023
            z = counter & 1023
            depth = self.__heightMap[x + z * self.width]
            depth = br if y >= depth else 0
            block = self.__blocks[(y * self.length + z) * self.width + x]
            opacity = self.__lightOpacity[block]
            if opacity > 100:
                depth = 0
            elif depth < 14:
                if opacity == 0:
                    opacity = 1

                newDepth = 0
                if x > 0:
                    newDepth = (self.__data[(y * self.length + z) * self.width + (x - 1)] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth
                if x < self.width - 1:
                    newDepth = (self.__data[(y * self.length + z) * self.width + x + 1] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth
                if y > 0:
                    newDepth = (self.__data[((y - 1) * self.length + z) * self.width + x] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth
                if y < self.height - 1:
                    newDepth = (self.__data[((y + 1) * self.length + z) * self.width + x] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth
                if z > 0:
                    newDepth = (self.__data[(y * self.length + (z - 1)) * self.width + x] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth
                if z < self.length - 1:
                    newDepth = (self.__data[(y * self.length + z + 1) * self.width + x] & 255) - opacity
                    if newDepth > depth:
                        depth = newDepth

            depth = max(depth, self.__lightValue[block])

            if x < x0:
                x0 = x
            elif x > x1:
                x1 = x
            if y > y1:
                y1 = y
            elif y < y0:
                y0 = y
            if z < z0:
                z0 = z
            elif z > z1:
                z1 = z

            if (self.__data[(y * self.length + z) * self.width + x] & 255) != depth:
                self.__data[(y * self.length + z) * self.width + x] = <char>depth
                if x > 0 and (self.__data[(y * self.length + z) * self.width + (x - 1)] & 255) != depth - 1:
                    floodFillCounters[count] = x - 1 << 20 | y << 10 | z
                    count += 1
                if x < self.width - 1 and (self.__data[(y * self.length + z) * self.width + x + 1] & 255) != depth - 1:
                    floodFillCounters[count] = x + 1 << 20 | y << 10 | z
                    count += 1
                if y > 0 and (self.__data[((y - 1) * self.length + z) * self.width + x] & 255) != depth - 1:
                    floodFillCounters[count] = x << 20 | y - 1 << 10 | z
                    count += 1
                if y < self.height - 1 and (self.__data[((y + 1) * self.length + z) * self.width + x] & 255) != depth - 1:
                    floodFillCounters[count] = x << 20 | y + 1 << 10 | z
                    count += 1
                if z > 0 and (self.__data[(y * self.length + (z - 1)) * self.width + x] & 255) != depth - 1:
                    floodFillCounters[count] = x << 20 | y << 10 | z - 1
                    count += 1
                if z < self.length - 1 and (self.__data[(y * self.length + z + 1) * self.width + x] & 255) != depth - 1:
                    floodFillCounters[count] = x << 20 | y << 10 | z + 1
                    count += 1

        for worldAccess in self.__worldAccesses:
            worldAccess.markBlockRangeNeedsUpdate(x0, y0, z0, x1, y1, z1)

        free(floodFillCounters)

    def addWorldAccess(self, worldAccess):
        self.__worldAccesses.add(worldAccess)

    def finalize(self):
        pass

    def removeWorldAccess(self, worldAccess):
        self.__worldAccesses.remove(worldAccess)

    def getCollidingBoundingBoxes(self, AxisAlignedBB box):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Block block
        cdef AxisAlignedBB aabb

        boxes = []
        minX = <int>box.minX
        maxX = <int>box.maxX + 1
        minY = <int>box.minY
        maxY = <int>box.maxY + 1
        minZ = <int>box.minZ
        maxZ = <int>box.maxZ + 1
        if box.minX < 0.0:
            minX -= 1
        if box.minY < 0.0:
            minY -= 1
        if box.minZ < 0.0:
            minZ -= 1

        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    block = blocks.blocksList[self.getBlockId(x, y, z)]
                    if block:
                        aabb = block.getCollisionBoundingBoxFromPool(x, y, z)
                        if aabb and box.intersectsWith(aabb):
                            boxes.append(aabb)
                    elif self.groundLevel < 0 and (y < self.groundLevel or y < self.waterLevel):
                        aabb = blocks.bedrock.getCollisionBoundingBoxFromPool(x, y, z)
                        if aabb and box.intersectsWith(aabb):
                            boxes.append(aabb)

        return boxes

    cdef swap(self, int x0, int y0, int z0, int x1, int y1, int z1):
        cdef int block1 = self.getBlockId(x0, y0, z0)
        cdef int block2 = self.getBlockId(x1, y1, z1)
        self.setBlock(x0, y0, z0, block2)
        self.setBlock(x1, y1, z1, block1)
        self.notifyBlocksOfNeighborChange(x0, y0, z0, block2)
        self.notifyBlocksOfNeighborChange(x1, y1, z1, block1)

    cpdef bint setBlock(self, int x, int y, int z, int blockType):
        if x <= 0 or y <= 0 or z <= 0 or x >= self.width - 1 or y >= self.height - 1 or z >= self.length - 1:
            return False

        cdef char oldBlock = self.__blocks[(y * self.length + z) * self.width + x]
        if blockType == oldBlock:
            return False

        if blockType == 0 and (x == 0 or z == 0 or x == self.width - 1 or \
            z == self.length - 1) and y >= self.groundLevel and y < self.waterLevel:
            blockType = blocks.waterMoving.blockID

        self.__blocks[(y * self.length + z) * self.width + x] = <char>blockType
        if oldBlock != 0:
            blocks.blocksList[oldBlock].onBlockRemoval(self, x, y, z)

        if blockType != 0:
            blocks.blocksList[blockType].onBlockAdded(self, x, y, z)

        self.__updateSkylight(x, z, 1, 1)
        self.__updateLight(x, y, z, x + 1, y + 1, z + 1)

        for worldAccess in self.__worldAccesses:
            worldAccess.markBlockAndNeighborsNeedsUpdate(x, y, z)

        return True

    cpdef bint setBlockWithNotify(self, int x, int y, int z, int blockType):
        if self.setBlock(x, y, z, blockType):
            self.notifyBlocksOfNeighborChange(x, y, z, blockType)
            return True
        else:
            return False

    cpdef notifyBlocksOfNeighborChange(self, int x, int y, int z, int blockType):
        self.__notifyBlockOfNeighborChange(x - 1, y, z, blockType)
        self.__notifyBlockOfNeighborChange(x + 1, y, z, blockType)
        self.__notifyBlockOfNeighborChange(x, y - 1, z, blockType)
        self.__notifyBlockOfNeighborChange(x, y + 1, z, blockType)
        self.__notifyBlockOfNeighborChange(x, y, z - 1, blockType)
        self.__notifyBlockOfNeighborChange(x, y, z + 1, blockType)

    cpdef bint setTileNoUpdate(self, int x, int y, int z, int blockType):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.height or z >= self.length:
            return False
        if blockType == self.__blocks[(y * self.length + z) * self.width + x]:
            return False

        self.__blocks[(y * self.length + z) * self.width + x] = <char>blockType
        self.__updateLight(x, y, z, x + 1, y + 1, z + 1)
        return True

    cdef __notifyBlockOfNeighborChange(self, int x, int y, int z, int blockType):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.height or z >= self.length:
            return

        cdef Block block = blocks.blocksList[self.__blocks[(y * self.length + z) * self.width + x]]
        if block:
            block.onNeighborBlockChange(self, x, y, z, blockType)

    cpdef inline bint isHalfLit(self, int x, int y, int z):
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        if z < 0:
            z = 0
        elif z >= self.length:
            z = self.length - 1

        return self.__getBlockMetadata(x, y, z) > 3

    cpdef inline bint isFullyLit(self, int x, int y, int z):
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        if z < 0:
            z = 0
        elif z >= self.length:
            z = self.length - 1

        return self.__getBlockMetadata(x, y, z) < 14

    cpdef inline int getBlockId(self, int x, int y, int z):
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        if z < 0:
            z = 0
        elif z >= self.length:
            z = self.length - 1

        return self.__blocks[(y * self.length + z) * self.width + x] & 255

    cpdef inline bint isBlockNormalCube(self, int x, int y, int z):
        return self.__isBlockNormal[self.getBlockId(x, y, z)]

    cpdef void updateEntities(self):
        self.entityMap.updateEntities()

    @cython.cdivision(True)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef tick(self):
        cdef int wShift, lShift, h, w, d, ticks, i, randValue, x, z, y, blockId
        cdef char b
        cdef NextTickListEntry posType

        self.__playTime += 1

        wShift = 1
        lShift = 1

        while 1 << wShift < self.width:
            wShift += 1
        while 1 << lShift < self.length:
            lShift += 1

        l = self.length - 1
        w = self.width - 1
        h = self.height - 1

        ticks = min(len(self.__tickList), self.__maxTicks)
        for i in range(ticks):
            posType = self.__tickList.pop()
            if posType.scheduledTime > 0:
                posType.scheduledTime -= 1
                self.__tickList.add(posType)
            else:
                b = self.__blocks[(posType.yCoord * self.length + posType.zCoord) * self.width + posType.xCoord]
                if self.__isInLevelBounds(posType.xCoord, posType.yCoord, posType.zCoord) and \
                   b == posType.blockID and b > 0:
                    blocks.blocksList[b].updateTick(self, posType.xCoord,
                                                    posType.yCoord, posType.zCoord)

        self.__updateLCG += self.width * self.length * self.height
        ticks = self.__updateLCG // 200
        self.__updateLCG -= ticks * 200
        for i in range(ticks):
            self.__randId = self.__randId * self.multiplier + self.addend
            randValue = self.__randId >> 2
            x = randValue & w
            z = randValue >> wShift & l
            y = randValue >> wShift + lShift & h
            blockId = self.__blocks[(y * self.length + z) * self.width + x]
            if blocks.tickOnLoad[blockId]:
                blocks.blocksList[blockId].updateTick(self, x, y, z)

    def entitiesInLevelList(self, cls):
        count = 0
        for obj in self.entityMap.entities:
            if isinstance(obj, cls):
                count += 1

        return count

    cdef inline bint __isInLevelBounds(self, int x, int y, int z):
        return x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.height and z < self.length

    cpdef inline int getGroundLevel(self):
        return self.groundLevel

    cpdef inline int getWaterLevel(self):
        return self.waterLevel

    cdef bint getIsAnyLiquid(self, AxisAlignedBB box):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Block block

        minX = <int>floor(box.minX)
        maxX = <int>floor(box.maxX + 1.0)
        minY = <int>floor(box.minY)
        maxY = <int>floor(box.maxY + 1.0)
        minZ = <int>floor(box.minZ)
        maxZ = <int>floor(box.maxZ + 1.0)
        if box.minX < 0.0:
            minX -= 1
        if box.minY < 0.0:
            minY -= 1
        if box.minZ < 0.0:
            minZ -= 1

        if minX < 0: minX = 0
        if minY < 0: minY = 0
        if minZ < 0: minZ = 0
        if maxX > self.width: maxX = self.width
        if maxY > self.height: maxY = self.height
        if maxZ > self.length: maxZ = self.length
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    block = blocks.blocksList[self.getBlockId(x, y, z)]
                    if block and block.getBlockMaterial() != Material.air:
                        return True

        return False

    cdef bint isBoundingBoxBurning(self, AxisAlignedBB box):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z, blockId

        minX = <int>floor(box.minX)
        maxX = <int>floor(box.maxX + 1.0)
        minY = <int>floor(box.minY)
        maxY = <int>floor(box.maxY + 1.0)
        minZ = <int>floor(box.minZ)
        maxZ = <int>floor(box.maxZ + 1.0)
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    blockId = self.getBlockId(x, y, z)
                    if blockId == blocks.fire.blockID or blockId == blocks.lavaMoving.blockID or \
                       blockId == blocks.lavaStill.blockID:
                        return True

        return False

    cdef bint handleMaterialAcceleration(self, AxisAlignedBB box, int material):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Block block

        minX = <int>floor(box.minX)
        maxX = <int>floor(box.maxX + 1.0)
        minY = <int>floor(box.minY)
        maxY = <int>floor(box.maxY + 1.0)
        minZ = <int>floor(box.minZ)
        maxZ = <int>floor(box.maxZ + 1.0)
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    block = blocks.blocksList[self.getBlockId(x, y, z)]
                    if block and block.getBlockMaterial() == material:
                        return True

        return False

    cpdef inline scheduleBlockUpdate(self, int x, int y, int z, int blockType):
        cdef int tickDelay
        cdef NextTickListEntry posType

        posType = NextTickListEntry(x, y, z, blockType)
        if blockType > 0:
            tickDelay = (<Block>blocks.blocksList[blockType]).tickRate()
            posType.scheduledTime = tickDelay

        self.__tickList.add(posType)

    cpdef bint checkIfAABBIsClear(self, AxisAlignedBB aabb):
        return len(self.entityMap.getEntitiesWithinAABBExcludingEntity(None, aabb)) == 0

    def getEntitiesWithinAABBExcludingEntity(self, entity, AxisAlignedBB aabb):
        return self.entityMap.getEntitiesWithinAABBExcludingEntity(entity, aabb)

    cpdef inline bint isSolid(self, float x, float y, float z, float offset):
        if self.__isBlockOpaque(x - 0.1, y - 0.1, z - 0.1):
            return True
        elif self.__isBlockOpaque(x - 0.1, y - 0.1, z + 0.1):
            return True
        elif self.__isBlockOpaque(x - 0.1, y + 0.1, z - 0.1):
            return True
        elif self.__isBlockOpaque(x - 0.1, y + 0.1, z + 0.1):
            return True
        elif self.__isBlockOpaque(x + 0.1, y - 0.1, z - 0.1):
            return True
        elif self.__isBlockOpaque(x + 0.1, y - 0.1, z + 0.1):
            return True
        elif self.__isBlockOpaque(x + 0.1, y + 0.1, z - 0.1):
            return True
        else:
            return self.__isBlockOpaque(x + 0.1, y + 0.1, z + 0.1)

    cdef inline bint __isBlockOpaque(self, float x, float y, float z):
        cdef int block = self.getBlockId(<int>x, <int>y, <int>z)
        return block > 0 and (<Block>blocks.blocksList[block]).isOpaqueCube()

    cpdef __getFirstUncoveredBlock(self, int x, int z):
        cdef int blockId, y
        y = self.height
        blockId = self.getBlockId(x, y - 1, z)
        while (blockId == 0 or \
               (<Block>blocks.blocksList[blockId]).getBlockMaterial() != Material.air) and y > 0:
            y -= 1
            blockId = self.getBlockId(x, y - 1, z)

        return y

    cpdef setSpawnLocation(self, int x, int y, int z, float rotationYaw):
        self.xSpawn = x
        self.ySpawn = y
        self.zSpawn = z
        self.rotSpawn = rotationYaw

    cpdef inline float getBlockLightValue(self, int x, int y, int z):
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        if z < 0:
            z = 0
        elif z >= self.length:
            z = self.length - 1

        return self.__lightBrightnessTable[self.__data[(y * self.length + z) * self.width + x]]

    cdef inline char __getBlockMetadata(self, int x, int y, int z):
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        if z < 0:
            z = 0
        elif z >= self.length:
            z = self.length - 1

        return self.__data[(y * self.length + z) * self.width + x]

    cpdef inline int getBlockMaterial(self, int x, int y, int z):
        cdef int block = self.getBlockId(x, y, z)
        if block == 0:
            return Material.air

        return (<Block>blocks.blocksList[block]).getBlockMaterial()

    cpdef inline bint isWater(self, int x, int y, int z):
        cdef int block = self.getBlockId(x, y, z)
        return block > 0 and (<Block>blocks.blocksList[block]).getBlockMaterial() == Material.water

    @cython.cdivision(True)
    def rayTraceBlocks(self, vec1, vec2):
        cdef int x0, y0, z0, x1, y1, z1, radius, blockId
        cdef float x, y, z, xSide, ySide, zSide, xd, yd, zd
        cdef char sideHit
        cdef Block block

        if isnan(vec1.xCoord) or isnan(vec1.yCoord) or isnan(vec1.zCoord):
            return None
        if isnan(vec2.xCoord) or isnan(vec2.yCoord) or isnan(vec2.zCoord):
            return None

        x0 = <int>floor(vec2.xCoord)
        y0 = <int>floor(vec2.yCoord)
        z0 = <int>floor(vec2.zCoord)
        x1 = <int>floor(vec1.xCoord)
        y1 = <int>floor(vec1.yCoord)
        z1 = <int>floor(vec1.zCoord)
        radius = 20
        blockId = self.getBlockId(x1, y1, z1)
        while radius >= 0:
            radius -= 1

            if isnan(vec1.xCoord) or isnan(vec1.yCoord) or isnan(vec1.zCoord):
                return None

            if x1 == x0 and y1 == y0 and z1 == z0:
                return None

            x = 999.0
            y = 999.0
            z = 999.0
            if x0 > x1:
                x = x1 + 1.0
            elif x0 < x1:
                x = x1

            if y0 > y1:
                y = y1 + 1.0
            elif y0 < y1:
                y = y1

            if z0 > z1:
                z = z1 + 1.0
            elif z0 < z1:
                z = z1

            xSide = 999.0
            ySide = 999.0
            zSide = 999.0
            xd = vec2.xCoord - vec1.xCoord
            yd = vec2.yCoord - vec1.yCoord
            zd = vec2.zCoord - vec1.zCoord
            if x != 999.0:
                xSide = (x - vec1.xCoord) / xd

            if y != 999.0:
                ySide = (y - vec1.yCoord) / yd

            if z != 999.0:
                zSide = (z - vec1.zCoord) / zd

            sideHit = 0
            if xSide < ySide and xSide < zSide:
                if x0 > x1:
                    sideHit = 4
                else:
                    sideHit = 5

                vec1.xCoord = x
                vec1.yCoord += yd * xSide
                vec1.zCoord += zd * xSide
            elif ySide < zSide:
                if y0 > y1:
                    sideHit = 0
                else:
                    sideHit = 1

                vec1.xCoord += xd * ySide
                vec1.yCoord = y
                vec1.zCoord += zd * ySide
            else:
                if z0 > z1:
                    sideHit = 2
                else:
                    sideHit = 3

                vec1.xCoord += xd * zSide
                vec1.yCoord += yd * zSide
                vec1.zCoord = z

            posVec = Vec3D(vec1.xCoord, vec1.yCoord, vec1.zCoord)
            posVec.xCoord = floor(vec1.xCoord)
            x1 = <int>posVec.xCoord
            if sideHit == 5:
                x1 -= 1
                posVec.xCoord += 1.0

            posVec.yCoord = floor(vec1.yCoord)
            y1 = <int>posVec.yCoord
            if sideHit == 1:
                y1 -= 1
                posVec.yCoord += 1.0

            posVec.zCoord = floor(vec1.zCoord)
            z1 = <int>posVec.zCoord
            if sideHit == 3:
                z1 -= 1
                posVec.zCoord += 1.0

            blockId = self.getBlockId(x1, y1, z1)
            if blockId > 0:
                block = blocks.blocksList[blockId]
                if block.getBlockMaterial() == Material.air and block.isCollidable():
                    if block.renderAsNormalBlock():
                        hitResult = block.collisionRayTrace(x1, y1, z1, vec1, vec2)
                        if hitResult:
                            return hitResult
                    else:
                        hitResult = block.collisionRayTrace(x1, y1, z1, vec1, vec2)
                        if hitResult:
                            return hitResult

    cpdef bint growTrees(self, int x, int y, int z):
        cdef int xx, yy, zz, i, leafExt, leafExtLeft, offset, logs, zd
        cdef bint willGrow
        cdef char block

        logs = self.__rand.nextInt(3) + 4
        willGrow = True

        if y <= 0 or y + logs + 1 > self.height:
            return False

        for yy in range(y, y + 2 + logs):
            offset = 1
            if yy == y:
                offset = 0

            if yy >= y + 1 + logs - 2:
                offset = 2

            for xx in range(x - offset, x + offset + 1):
                if not willGrow:
                    break

                for zz in range(z - offset, z + offset + 1):
                    if not willGrow:
                        break

                    if xx >= 0 and yy >= 0 and zz >= 0 and xx < self.width and yy < self.height and zz < self.length:
                        block = self.__blocks[(yy * self.length + zz) * self.width + xx] & 0xFF
                        if block != 0:
                            willGrow = False
                    else:
                        willGrow = False

        if not willGrow:
            return False

        block = self.__blocks[((y - 1) * self.length + z) * self.width + x] & 0xFF
        if (block != blocks.grass.blockID and block != blocks.dirt.blockID) or y >= self.height - logs - 1:
            return False

        self.setBlockWithNotify(x, y - 1, z, blocks.dirt.blockID)
        for yy in range(y - 3 + logs, y + logs + 1):
            leafExtLeft = yy - (y + logs)
            leafExt = 1 - leafExtLeft // 2
            for xx in range(x - leafExt, x + leafExt + 1):
                willGrow = xx - x
                for zz in range(z - leafExt, z + leafExt + 1):
                    zd = zz - z
                    if abs(willGrow) == leafExt and abs(zd) == leafExt and \
                       (self.__rand.nextInt(2) == 0 or leafExtLeft == 0):
                        continue

                    self.setBlockWithNotify(xx, yy, zz, blocks.leaves.blockID)

        for i in range(logs):
            self.setBlockWithNotify(x, y + i, z, blocks.wood.blockID)

        return True

    def getPlayerEntity(self):
        return self.playerEntity

    def releaseEntitySkin(self, entity):
        self.entityMap.insert(entity)
        entity.setWorld(self)

    def onPickup(self, entity):
        self.entityMap.remove(entity)

    def createExplosion(self, entity, float x, float y, float z, float radius):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, xx, yy, zz, blockId
        cdef float xd, yd, zd, d
        cdef Block block

        minX = <int>(x - 4.0 - 1.0)
        maxX = <int>(x + 4.0 + 1.0)
        minY = <int>(y - 4.0 - 1.0)
        maxY = <int>(y + 4.0 + 1.0)
        minZ = <int>(z - 4.0 - 1.0)
        maxZ = <int>(z + 4.0 + 1.0)

        for xx in range(minX, maxX):
            for yy in range(maxY - 1, minY - 1, -1):
                for zz in range(minZ, maxZ):
                    xd = xx + 0.5 - x
                    yd = yy + 0.5 - y
                    zd = zz + 0.5 - z
                    if xx >= 0 and yy >= 0 and zz >= 0 and xx < self.width and yy < self.height and \
                       zz < self.length and xd * xd + yd * yd + zd * zd < 16.0:
                        blockId = self.getBlockId(xx, yy, zz)
                        if blockId > 0:
                            block = <Block>blocks.blocksList[blockId]
                            if not block.getCanExplode():
                                continue

                            block.dropBlockAsItemWithChance(self, xx, yy, zz, 0.3)
                            self.setBlockWithNotify(xx, yy, zz, 0)
                            block.onBlockDestroyedByExplosion(self, xx, yy, zz)

        entities = self.entityMap.getEntities(None, minX, minY, minZ, maxX, maxY, maxZ)
        for e in entities:
            xd = e.posX - x
            yd = e.posY - y
            zd = e.posZ - z
            d = sqrt(xd * xd + yd * yd + zd * zd) / 4.0
            if d <= 1.0:
                e.attackEntityFrom(None, <int>((1.0 - d) * 15.0 + 1.0))

    def findSubclassOf(self, cls):
        for entity in self.entityMap.entities:
            if isinstance(entity, cls):
                return entity

    def getMapHeight(self, int x, int z):
        return self.__heightMap[x + z * self.width]

    def playSoundAtEntity(self, entity, name, float volume, float pitch):
        cdef float d, xd, yd, zd
        for worldAccess in self.__worldAccesses:
            d = 16.0
            if volume > 1.0:
                d = 16.0 * volume

            xd = self.playerEntity.posX - entity.posX
            yd = self.playerEntity.posY - entity.posY
            zd = self.playerEntity.posZ - entity.posZ
            if xd * xd + yd * yd + zd * zd < d * d:
                worldAccess.playSound(
                    name, entity.posX, entity.posY - entity.yOffset,
                    entity.posZ, volume, pitch
                )

    def playSoundEffect(self, float x, float y, float z, str name,
                        float volume, float pitch):
        cdef float d, xd, yd, zd
        for worldAccess in self.__worldAccesses:
            d = 16.0
            if volume > 1.0:
                d = 16.0 * volume

            xd = x - self.playerEntity.posX
            yd = y - self.playerEntity.posY
            zd = z - self.playerEntity.posZ
            if xd * xd + yd * yd + zd * zd < d * d:
                worldAccess.playSound(name, x, y, z, volume, pitch)

    def extinguishFire(self, int x, int y, int z, int sideHit):
        if sideHit == 0:
            y -= 1
        elif sideHit == 1:
            y += 1
        elif sideHit == 2:
            z -= 1
        elif sideHit == 3:
            z += 1
        elif sideHit == 4:
            x -= 1
        elif sideHit == 5:
            x += 1

        if self.getBlockId(x, y, z) == blocks.fire.blockID:
            self.playSoundEffect(
                x + 0.5, y + 0.5, z + 0.5, 'random.fizz', 0.5,
                2.6 + (self.__rand.randFloat() - self.__rand.randFloat()) * 0.8
            )
            self.setBlockWithNotify(x, y, z, 0)
