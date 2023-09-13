# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport floor, isnan

from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.liquid.Liquid import Liquid
from mc.net.minecraft.phys.AABB cimport AABB
from mc.net.minecraft.model.Vec3 import Vec3
from mc.net.minecraft.level.BlockMap cimport BlockMap
from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.sound.SoundPos import SoundPos

import random
import gc

cdef class Coord:

    cdef:
        public int x
        public int y
        public int z
        public int id
        public int time

    def __init__(self, int x, int y, int z, int id_):
        self.x = x
        self.y = y
        self.z = z
        self.id = id_

@cython.final
cdef class Level:
    TILE_UPDATE_INTERVAL = 200

    def __cinit__(self):
        self.update_interval = self.TILE_UPDATE_INTERVAL

        self.name = ''
        self.creator = ''
        self.createTime = 0

        self.rotSpawn = 0.0

        self.__levelListeners = set()
        self.rand = random.Random()
        self.randValue = self.rand.getrandbits(31)
        self.__tickList = set()

        self.unprocessed = 0
        self.__tickCount = 0

        self.multiplier = 3
        self.addend = 1013904223

    def __dealloc__(self):
        free(self.__blocks)
        free(self.__heightMap)

    def __reduce__(self):
        blocks = bytearray(self.width * self.height << 6)
        for i in range(len(blocks)):
            blocks[i] = self.__blocks[i]

        return (rebuild, (self.name, self.creator, self.createTime, self.rotSpawn,
                          set(), 0, self.__tickCount, 0, 0, self.width,
                          self.height, self.depth, blocks, self.xSpawn,
                          self.ySpawn, self.zSpawn))

    def init(self):
        if not self.__blocks:
            raise RuntimeError('The level is corrupt!')

        self.__levelListeners = set()
        self.__heightMap = <int*>malloc(sizeof(int) * (self.width * self.height))
        for i in range(self.width * self.height):
            self.__heightMap[i] = self.depth

        self.calcLightDepths(0, 0, self.width, self.height)
        self.rand = random.Random()
        self.randValue = self.rand.getrandbits(31)
        self.__tickList = set()

        if self.waterLevel == 0:
            self.waterLevel = self.depth // 2
        if self.skyColor == 0:
            self.skyColor = 0x99CCFF
        if self.fogColor == 0:
            self.fogColor = 0xFFFFFF
        if self.cloudColor == 0:
            self.cloudColor = 0xFFFFFF

        if self.xSpawn == 0 and self.ySpawn == 0 and self.zSpawn == 0:
            self.findSpawn()

        if not self.blockMap:
            self.blockMap = BlockMap(self.width, self.depth, self.height)

    def initTransient(self, str name, str creator, object createTime, float rotSpawn,
                      int tickCount, int width, int depth, int height,
                      bytearray blocks, int xSpawn, int ySpawn, int zSpawn):
        self.name = name
        self.creator = creator
        self.createTime = createTime
        self.xSpawn = xSpawn
        self.ySpawn = ySpawn
        self.zSpawn = zSpawn
        self.rotSpawn = rotSpawn
        self.__tickCount = tickCount
        self.width = width
        self.depth = depth
        self.height = height

        self.__blocks = <char*>malloc(sizeof(char) * len(blocks))
        for i in range(len(blocks)):
            self.__blocks[i] = blocks[i]

        self.init()

    def setDataLegacy(self, int w, int d, int h, bytearray blocks):
        cdef char* b
        b = <char*>malloc(sizeof(char) * len(blocks))
        for i in range(len(blocks)):
            b[i] = blocks[i]
        self.setData(w, d, h, b)

    cdef setData(self, int w, int d, int h, char* blocks):
        self.width = w
        self.depth = d
        self.height = h
        self.__blocks = blocks
        self.__heightMap = <int*>malloc(sizeof(int) * (w * h))
        for i in range(w * h):
            self.__heightMap[i] = d
        self.calcLightDepths(0, 0, w, h)

        for levelListener in self.__levelListeners:
            levelListener.compileSurroundingGround()

        self.__tickList.clear()
        self.findSpawn()
        self.init()
        gc.collect()

    cdef findSpawn(self):
        cdef int i, x, z, y

        rand = random.Random()

        i = 0
        x = 0
        z = 0
        y = 0
        while y <= self.getWaterLevel():
            i += 1
            x = <int>floor(self.rand.random() * self.width // 2) + self.width // 4
            z = <int>floor(self.rand.random() * self.height // 2) + self.height // 4
            y = self.getHighestTile(x, z) + 1
            if i == 10000:
                self.xSpawn = x
                self.ySpawn = -100
                self.zSpawn = z
                return

        self.xSpawn = x
        self.ySpawn = y
        self.zSpawn = z

    cdef void calcLightDepths(self, int x0, int y0, int x1, int y1) except *:
        cdef int x, z, oldDepth, y, yl0, yl1

        for x in range(x0, x0 + x1):
            for z in range(y0, y0 + y1):
                oldDepth = self.__heightMap[x + z * self.width]
                y = self.depth - 1
                while y > 0 and not self.isLightBlocker(x, y, z):
                    y -= 1

                self.__heightMap[x + z * self.width] = y

                if oldDepth != y:
                    yl0 = oldDepth if oldDepth < y else y
                    yl1 = oldDepth if oldDepth > y else y
                    for levelRenderer in self.__levelListeners:
                        levelRenderer.setDirty(x - 1, yl0 - 1, z - 1, x + 1, yl1 + 1, z + 1)

    def addListener(self, levelRenderer):
        self.__levelListeners.add(levelRenderer)

    def finalize(self):
        pass

    def removeListener(self, levelRenderer):
        self.__levelListeners.remove(levelRenderer)

    cdef inline bint isLightBlocker(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return tile.blocksLight() if tile else False

    def getCubes(self, AABB box):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Tile tile
        cdef AABB aabb

        boxes = []
        minX = <int>box.x0
        maxX = <int>box.x1 + 1
        minY = <int>box.y0
        maxY = <int>box.y1 + 1
        minZ = <int>box.z0
        maxZ = <int>box.z1 + 1
        if box.x0 < 0.0:
            minX -= 1
        if box.y0 < 0.0:
            minY -= 1
        if box.z0 < 0.0:
            minZ -= 1

        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
                        tile = tiles.tiles[self.getTile(x, y, z)]
                        if tile:
                            aabb = tile.getTileAABB(x, y, z)
                            if aabb and box.intersectsInner(aabb):
                                boxes.append(aabb)
                    elif x < 0 or y < 0 or z < 0 or x >= self.width or z >= self.height:
                        aabb = tiles.unbreakable.getTileAABB(x, y, z)
                        if aabb and box.intersectsInner(aabb):
                            boxes.append(aabb)

        return boxes

    cdef swap(self, int x0, int y0, int z0, int x1, int y1, int z1):
        cdef int i7, i8

        if not self.__networkMode:
            i7 = self.getTile(x0, y0, z0)
            i8 = self.getTile(x1, y1, z1)
            self.setTileNoNeighborChange(x0, y0, z0, i8)
            self.setTileNoNeighborChange(x1, y1, z1, i7)
            self.updateNeighborsAt(x0, y0, z0, i8)
            self.updateNeighborsAt(x1, y1, z1, i7)

    cpdef bint setTileNoNeighborChange(self, int x, int y, int z, int type_):
        return False if self.__networkMode else self.netSetTileNoNeighborChange(x, y, z, type_)

    cdef bint netSetTileNoNeighborChange(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return False
        if type_ == self.__blocks[(y * self.height + z) * self.width + x]:
            return False

        if type_ == 0 and (x == 0 or z == 0 or x == self.width - 1 or z == self.height - 1) and \
           y >= self.getGroundLevel() and y < self.getWaterLevel():
            type_ = tiles.water.id

        cdef char b5 = self.__blocks[(y * self.height + z) * self.width + x]
        self.__blocks[(y * self.height + z) * self.width + x] = type_
        if b5 != 0:
            tiles.tiles[b5].onTileRemoved(self, x, y, z)

        if type_ != 0:
            tiles.tiles[type_].onTileAdded(self, x, y, z)

        self.calcLightDepths(x, z, 1, 1)

        for levelRenderer in self.__levelListeners:
            levelRenderer.setDirty(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)

        return True

    cpdef bint setTile(self, int x, int y, int z, int type_):
        if self.__networkMode:
            return False
        elif self.setTileNoNeighborChange(x, y, z, type_):
            self.updateNeighborsAt(x, y, z, type_)
            return True
        else:
            return False

    def netSetTile(self, int x, int y, int z, int type_):
        if self.netSetTileNoNeighborChange(x, y, z, type_):
            self.updateNeighborsAt(x, y, z, type_)
            return True
        else:
            return False

    cpdef updateNeighborsAt(self, int x, int y, int z, int type_):
        self.__neighborChanged(x - 1, y, z, type_)
        self.__neighborChanged(x + 1, y, z, type_)
        self.__neighborChanged(x, y - 1, z, type_)
        self.__neighborChanged(x, y + 1, z, type_)
        self.__neighborChanged(x, y, z - 1, type_)
        self.__neighborChanged(x, y, z + 1, type_)

    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return False
        if type_ == self.__blocks[(y * self.height + z) * self.width + x]:
            return False

        self.__blocks[(y * self.height + z) * self.width + x] = type_
        return True

    cdef __neighborChanged(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return

        cdef Tile tile = tiles.tiles[self.__blocks[(y * self.height + z) * self.width + x]]
        if tile:
            tile.neighborChanged(self, x, y, z, type_)

    cpdef inline bint isLit(self, int x, int y, int z):
        return y >= self.__heightMap[x + z * self.width] if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height else True

    cpdef inline int getTile(self, int x, int y, int z):
        if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
            return self.__blocks[(y * self.height + z) * self.width + x] & 255
        else:
            return 0

    cpdef inline bint isSolidTile(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return False if tile is None else tile.isSolid()

    cpdef void tickEntities(self):
        self.blockMap.tickAll()

    @cython.cdivision(True)
    cpdef tick(self):
        cdef int i1, i2, h, w, d, ticks, i, i12, x, z, y, id_
        cdef char b
        cdef Coord posType

        self.__tickCount += 1

        i1 = 1
        i2 = 1

        while 1 << i1 < self.width:
            i1 += 1
        while 1 << i2 < self.height:
            i2 += 1

        h = self.height - 1
        w = self.width - 1
        d = self.depth - 1

        if self.__tickCount % 5 == 0:
            ticks = len(self.__tickList)
            for i in range(ticks):
                posType = self.__tickList.pop()
                if posType.time > 0:
                    posType.time -= 1
                    self.__tickList.add(posType)
                else:
                    b = self.__blocks[(posType.y * self.height + posType.z) * self.width + posType.x]
                    if self.__isInLevelBounds(posType.x, posType.y, posType.z) and b == posType.id and b > 0:
                        (<Tile>tiles.tiles[b]).tick(self, posType.x, posType.y, posType.z, self.rand)

        self.unprocessed += self.width * self.height * self.depth
        ticks = self.unprocessed // self.update_interval
        self.unprocessed -= ticks * self.update_interval
        for i in range(ticks):
            self.randValue = self.randValue * self.multiplier + self.addend
            i12 = self.randValue >> 2
            x = i12 & w
            z = i12 >> i1 & h
            y = i12 >> i1 + i2 & d
            id_ = self.__blocks[(y * self.height + z) * self.width + x]
            if tiles.rock.shouldTick[id_]:
                (<Tile>tiles.tiles[id_]).tick(self, x, y, z, self.rand)

    def countInstanceOf(self, cls):
        count = 0
        for obj in self.blockMap.all:
            if isinstance(obj, cls):
                count += 1

        return count

    cdef inline bint __isInLevelBounds(self, int x, int y, int z):
        return x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height

    cpdef inline float getGroundLevel(self):
        return self.getWaterLevel() - 2.0

    cpdef inline float getWaterLevel(self):
        return self.waterLevel

    cdef bint containsAnyLiquid(self, AABB box):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Tile tile

        minX = <int>floor(box.x0)
        maxX = <int>floor(box.x1 + 1.0)
        minY = <int>floor(box.y0)
        maxY = <int>floor(box.y1 + 1.0)
        minZ = <int>floor(box.z0)
        maxZ = <int>floor(box.z1 + 1.0)
        if box.x0 < 0.0:
            minX -= 1
        if box.y0 < 0.0:
            minY -= 1
        if box.z0 < 0.0:
            minZ -= 1

        if minX < 0: minX = 0
        if minY < 0: minY = 0
        if minZ < 0: minZ = 0
        if maxX > self.width: maxX = self.width
        if maxY > self.depth: maxY = self.depth
        if maxZ > self.height: maxZ = self.height
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    tile = tiles.tiles[self.getTile(x, y, z)]
                    if tile and tile.getLiquidType() != Liquid.none:
                        return True

        return False

    cdef bint containsLiquid(self, AABB box, int liquid):
        cdef int minX, maxX, minY, maxY, minZ, maxZ, x, y, z
        cdef Tile tile

        minX = <int>floor(box.x0)
        maxX = <int>floor(box.x1 + 1.0)
        minY = <int>floor(box.y0)
        maxY = <int>floor(box.y1 + 1.0)
        minZ = <int>floor(box.z0)
        maxZ = <int>floor(box.z1 + 1.0)
        if box.x0 < 0.0:
            minX -= 1
        if box.y0 < 0.0:
            minY -= 1
        if box.z0 < 0.0:
            minZ -= 1

        if minX < 0: minX = 0
        if minY < 0: minY = 0
        if minZ < 0: minZ = 0
        if maxX > self.width: maxX = self.width
        if maxY > self.depth: maxY = self.depth
        if maxZ > self.height: maxZ = self.height
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    tile = tiles.tiles[self.getTile(x, y, z)]
                    if tile and tile.getLiquidType() == liquid:
                        return True

        return False

    cpdef inline addToTickNextTick(self, int x, int y, int z, int type_):
        cdef int tickDelay
        cdef Coord posType

        if not self.__networkMode:
            posType = Coord(x, y, z, type_)
            if type_ > 0:
                tickDelay = (<Tile>tiles.tiles[type_]).getTickDelay()
                posType.time = tickDelay

            self.__tickList.add(posType)

    cpdef bint isFree(self, AABB aabb):
        return len(self.blockMap.getEntitiesWithinAABBExcludingEntity(None, aabb)) == 0

    def findEntities(self, entity, AABB aabb):
        return self.blockMap.getEntitiesWithinAABBExcludingEntity(entity, aabb)

    cpdef inline bint isSolid(self, int x, int y, int z, int offset):
        if self.__isBlockOpaque(x - offset, y - offset, z - offset):
            return True
        elif self.__isBlockOpaque(x - offset, y - offset, z + offset):
            return True
        elif self.__isBlockOpaque(x - offset, y + offset, z - offset):
            return True
        elif self.__isBlockOpaque(x - offset, y + offset, z + offset):
            return True
        elif self.__isBlockOpaque(x + offset, y - offset, z - offset):
            return True
        elif self.__isBlockOpaque(x + offset, y - offset, z + offset):
            return True
        elif self.__isBlockOpaque(x + offset, y + offset, z - offset):
            return True
        else:
            return self.__isBlockOpaque(x + offset, y + offset, z + offset)

    cdef inline bint __isBlockOpaque(self, int x, int y, int z):
        cdef int tile = self.getTile(int(x), int(y), int(z))
        return tile > 0 and (<Tile>tiles.tiles[tile]).isSolid()

    cpdef getHighestTile(self, int x, int z):
        cdef int i
        i = self.depth
        while (self.getTile(x, i - 1, z) == 0 or (<Tile>tiles.tiles[self.getTile(x, i - 1, z)]).getLiquidType() != Liquid.none) and i > 0:
            i -= 1

        return i

    cpdef setSpawnPos(self, int x, int y, int z, float yRot):
        self.xSpawn = x
        self.ySpawn = y
        self.zSpawn = z
        self.rotSpawn = yRot

    cpdef inline float getBrightness(self, int x, int y, int z):
        return 1.0 if self.isLit(x, y, z) else 0.6

    cpdef inline int getLiquid(self, int x, int y, int z):
        cdef int tile = self.getTile(x, y, z)
        if tile == 0:
            return Liquid.none

        return (<Tile>tiles.tiles[tile]).getLiquidType()

    cpdef inline bint isWater(self, int x, int y, int z):
        cdef int tile = self.getTile(x, y, z)
        return tile > 0 and (<Tile>tiles.tiles[tile]).getLiquidType() == Liquid.water

    def setNetworkMode(self, bint mode):
        self.__networkMode = mode

    def clip(self, vec1, vec2):
        cdef int x0, y0, z0, x1, y1, z1, i, tileId
        cdef float f9, f10, f11, f12, f13, f14, f15, f16, f17
        cdef char sideHit
        cdef Tile tile

        if isnan(vec1.x) or isnan(vec1.y) or isnan(vec1.z):
            return None
        if isnan(vec2.x) or isnan(vec2.y) or isnan(vec2.z):
            return None

        x0 = <int>floor(vec2.x)
        y0 = <int>floor(vec2.y)
        z0 = <int>floor(vec2.z)
        x1 = <int>floor(vec1.x)
        y1 = <int>floor(vec1.y)
        z1 = <int>floor(vec1.z)
        i = 20
        tileId = self.getTile(x1, y1, z1)
        while i >= 0:
            i -= 1

            if isnan(vec1.x) or isnan(vec1.y) or isnan(vec1.z):
                return None

            if x1 == x0 and y1 == y0 and z1 == z0:
                return None

            f9 = 999.0
            f10 = 999.0
            f11 = 999.0
            if x0 > x1:
                f9 = x1 + 1.0
            elif x0 < x1:
                f9 = x1

            if y0 > y1:
                f10 = y1 + 1.0
            elif y0 < y1:
                f10 = y1

            if z0 > z1:
                f11 = z1 + 1.0
            elif z0 < z1:
                f11 = z1

            f12 = 999.0
            f13 = 999.0
            f14 = 999.0
            f15 = vec2.x - vec1.x
            f16 = vec2.y - vec1.y
            f17 = vec2.z - vec1.z
            if f9 != 999.0:
                f12 = (f9 - vec1.x) / f15

            if f10 != 999.0:
                f13 = (f10 - vec1.y) / f16

            if f11 != 999.0:
                f14 = (f11 - vec1.z) / f17

            sideHit = 0
            if f12 < f13 and f12 < f14:
                if x0 > x1:
                    sideHit = 4
                else:
                    sideHit = 5

                vec1.x = f9
                vec1.y += f16 * f12
                vec1.z += f17 * f12
            elif f13 < f14:
                if y0 > y1:
                    sideHit = 0
                else:
                    sideHit = 1

                vec1.x += f15 * f13
                vec1.y = f10
                vec1.z += f17 * f13
            else:
                if z0 > z1:
                    sideHit = 2
                else:
                    sideHit = 3

                vec1.x += f15 * f14
                vec1.y += f16 * f14
                vec1.z = f11

            posVec = Vec3(vec1.x, vec1.y, vec1.z)
            posVec.x = floor(vec1.x)
            x1 = <int>posVec.x
            if sideHit == 5:
                x1 -= 1
                posVec.x += 1.0

            posVec.y = floor(vec1.y)
            y1 = <int>posVec.y
            if sideHit == 1:
                y1 -= 1
                posVec.y += 1.0

            posVec.z = floor(vec1.z)
            z1 = <int>posVec.z
            if sideHit == 3:
                z1 -= 1
                posVec.z += 1.0

            tileId = self.getTile(x1, y1, z1)
            if tileId > 0:
                tile = tiles.tiles[tileId]
                if tile.getLiquidType() == Liquid.none:
                    if tile.isOpaque():
                        return HitResult(x1, y1, z1, sideHit, posVec)

                    hitResult = tile.clip(x1, y1, z1, vec1, vec2)
                    if hitResult:
                        return hitResult

    def playSoundAtEntity(self, name, entity, float volume, float pitch):
        cdef float dist = 16.0 * volume
        if self.rendererContext and self.rendererContext.soundPlayer and self.rendererContext.options.sound:
            audioInfo = self.rendererContext.soundEngine.getAudioInfo(name, volume, pitch)
            if audioInfo:
                if self.rendererContext.player.distanceTo(entity.x,
                                                          entity.y,
                                                          entity.z) < dist * dist:
                    self.rendererContext.soundPlayer.play(audioInfo,
                                                          SoundPos(entity.x,
                                                                   entity.y - entity.heightOffset,
                                                                   entity.z))

    def playSound(self, name, float x, float y, float z, float volume, float pitch):
        cdef float dist = 16.0 * volume
        if self.rendererContext and self.rendererContext.soundPlayer and self.rendererContext.options.sound:
            audioInfo = self.rendererContext.soundEngine.getAudioInfo(name, volume, pitch)
            if audioInfo:
                if self.rendererContext.player.getDistanceSq(x, y, z) < dist * dist:
                    self.rendererContext.soundPlayer.play(audioInfo, SoundPos(x, y, z))

    cpdef bint maybeGrowTree(self, int x, int y, int z):
        cdef int xx, yy, zz, tile, n5, n6, n7, n9, n10, n11

        n9 = <int>floor(self.rand.random() * 3) + 4
        n10 = 1
        for yy in range(y, y + 2 + n9):
            n7 = 1
            if yy == y:
                n7 = 0

            if yy >= y + 1 + n9 - 2:
                n7 = 2

            for xx in range(x - n7, x + n7 + 1):
                if n10 == 0:
                    break

                for zz in range(z - n7, z + n7 + 1):
                    if n10 == 0:
                        break

                    if xx >= 0 and yy >= 0 and zz >= 0 and xx < self.width and yy < self.depth and zz < self.height:
                        tile = self.__blocks[(yy * self.height + zz) * self.width + xx] & 0xFF
                        if tile == 0:
                            continue

                        n10 = 0
                        continue

                    n10 = 0

        if n10 == 0:
            return False

        tile = self.__blocks[((y - 1) * self.height + z) * self.width + x] & 0xFF
        if tile != tiles.grass.id or y >= self.depth - n9 - 1:
            return False

        self.setTile(x, y - 1, z, tiles.dirt.id)
        yy = y - 3 + n9
        for yy in range(y - 3 + n9, y + n9 + 1):
            n6 = yy - (y + n9)
            n5 = 1 - n6 // 2
            for xx in range(x - n5, x + n5 + 1):
                n10 = xx - x
                for zz in range(z - n5, z + n5 + 1):
                    n11 = zz - z
                    if abs(n10) == n5 and abs(n11) == n5 and (<int>floor(self.rand.random() * 2) == 0 or n6 == 0):
                        continue

                    self.setTile(xx, yy, zz, tiles.leaf.id)

        for n7 in range(n9):
            self.setTile(x, y + n7, z, tiles.log.id)

        return True

    def getPlayer(self):
        return self.player

    def addEntity(self, entity):
        self.blockMap.insert(entity)
        entity.setLevel(self)

    def removeEntity(self, entity):
        self.blockMap.remove(entity)

    cpdef explode(self, entity, float x, float y, float z, float radius):
        cdef int x0, x1, y0, y1, z0, z1, i, n, j, tileId
        cdef float f5, f6, f7, d
        cdef Tile tile

        x0 = <int>(x - radius - 1.0)
        x1 = <int>(x + radius + 1.0)
        y0 = <int>(y - radius - 1.0)
        y1 = <int>(y + radius + 1.0)
        z0 = <int>(z - radius - 1.0)
        z1 = <int>(z + radius + 1.0)

        for i in range(x0, x1):
            for n in range(y1 - 1, y0 - 1, -1):
                for j in range(z0, z1):
                    f6 = i + 0.5 - x
                    f5 = n + 0.5 - y
                    f7 = j + 0.5 - z
                    if i < 0 or n < 0 or j < 0 or \
                       i >= self.width or n >= self.depth or j >= self.height or \
                       not (f6 * f6 + f5 * f5 + f7 * f7 < radius * radius):
                        continue

                    tileId = self.getTile(i, n, j)
                    if tileId > 0:
                        tile = tiles.tiles[tileId]
                        if tile.isExplodeable():
                            tile.spawnResources(0.3)
                            self.setTile(i, n, j, 0)

        entities = self.blockMap.getEntitiesExcludingEntity(entity, x0, y0, z0, x1, y1, z1)
        for e in entities:
            d = e.distanceTo(x, y, z) / radius
            if d <= 1.0:
                e.hurt(entity, <int>((1.0 - d) * 15.0 + 1.0))

    def findSubclassOf(self, cls):
        for entity in self.blockMap.all:
            if isinstance(entity, cls):
                return entity

    def removeAllNonCreativeModeEntities(self):
        self.blockMap.removeAllNonCreativeModeEntities()

cpdef object rebuild(str name, str creator, object createTime, float rotSpawn,
                     set entities, int unprocessed, int tickCount, int multiplier,
                     unsigned long addend, int width, int height, int depth,
                     bytearray blocks, int xSpawn, int ySpawn, int zSpawn):
    l = Level()
    l.initTransient(name, creator, createTime, rotSpawn,
                    tickCount, width, depth, height,
                    blocks, xSpawn, ySpawn, zSpawn)
    return l
