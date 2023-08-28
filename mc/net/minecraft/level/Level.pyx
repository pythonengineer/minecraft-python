# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport floor, isnan

from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.liquid.Liquid cimport Liquid
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
        public int scheduledTime

    def __init__(self, int x, int y, int z, int id_):
        self.x = x
        self.y = y
        self.z = z
        self.id = id_
        self.scheduledTime = 0

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

        self.entities = set()

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

        return (rebuild, (self.name, self.creator,
                          self.createTime, self.rotSpawn,
                          self.entities, self.unprocessed,
                          self.__tickCount, self.multiplier,
                          self.addend, self.width, self.height,
                          self.depth, blocks, self.xSpawn,
                          self.ySpawn, self.zSpawn))

    def initTransient(self, str name, str creator, object createTime, float rotSpawn,
                      set entities, int unprocessed, int tickCount, int multiplier,
                      unsigned long addend, int width, int height, int depth,
                      bytearray blocks, int xSpawn, int ySpawn, int zSpawn):
        if not blocks:
            raise RuntimeError('The level is corrupt!')

        self.name = name
        self.creator = creator
        self.createTime = createTime
        self.rotSpawn = rotSpawn
        self.entities = entities
        self.unprocessed = unprocessed
        self.__tickCount = tickCount
        self.multiplier = multiplier
        self.addend = addend
        self.width = width
        self.height = height
        self.depth = depth
        self.xSpawn = xSpawn
        self.ySpawn = ySpawn
        self.zSpawn = zSpawn

        self.__blocks = <char*>malloc(sizeof(char) * len(blocks))
        for i in range(len(blocks)):
            self.__blocks[i] = blocks[i]

        self.__levelListeners = set()
        self.__heightMap = <int*>malloc(sizeof(int) * (self.width * self.height))
        for i in range(self.width * self.height):
            self.__heightMap[i] = self.depth
        self.calcLightDepths(0, 0, self.width, self.height)
        self.rand = random.Random()
        self.randValue = self.rand.getrandbits(31)
        self.__tickList = set()
        if not self.entities:
            self.entities = set()

        if self.xSpawn == 0 and self.ySpawn == 0 and self.zSpawn == 0:
            self.findSpawn()

    def setDataLegacy(self, int w, int d, int h, bytearray blocks):
        cdef char* b
        b = <char*>malloc(sizeof(char) * len(blocks))
        for i in range(len(blocks)):
            b[i] = blocks[i]
        self.setData(w, d, h, b)

    cdef setData(self, int w, int d, int h, char* blocks):
        self.width = w
        self.height = h
        self.depth = d
        self.__blocks = blocks
        self.__heightMap = <int*>malloc(sizeof(int) * (w * h))
        for i in range(w * h):
            self.__heightMap[i] = d
        self.calcLightDepths(0, 0, w, h)

        for levelListener in self.__levelListeners:
            levelListener.compileSurroundingGround()

        self.__tickList.clear()
        self.findSpawn()
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

                self.__heightMap[x + z * self.width] = y + 1

                if oldDepth != y:
                    yl0 = oldDepth if oldDepth < y else y
                    yl1 = oldDepth if oldDepth > y else y
                    for levelListener in self.__levelListeners:
                        levelListener.setDirty(x - 1, yl0 - 1, z - 1, x + 1, yl1 + 1, z + 1)

    def addListener(self, levelRenderer):
        self.__levelListeners.add(levelRenderer)

    def finalize(self):
        pass

    def removeListener(self, levelRenderer):
        self.__levelListeners.remove(levelRenderer)

    cdef inline bint isLightBlocker(self, int x, int y, int z) except *:
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return tile.blocksLight() if tile else False

    def getCubes(self, box):
        cdef int x0, x1, y0, y1, z0, z1, x, y, z
        cdef Tile tile

        boxes = set()
        x0 = <int>box.x0
        x1 = <int>box.x1 + 1
        y0 = <int>box.y0
        y1 = <int>box.y1 + 1
        z0 = <int>box.z0
        z1 = <int>box.z1 + 1
        if box.x0 < 0.0:
            x0 -= 1
        if box.y0 < 0.0:
            y0 -= 1
        if box.z0 < 0.0:
            z0 -= 1

        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
                        tile = tiles.tiles[self.getTile(x, y, z)]
                        if tile:
                            aabb = tile.getTileAABB(x, y, z)
                            if aabb:
                                boxes.add(aabb)
                    elif x < 0 or y < 0 or z < 0 or x >= self.width or z >= self.height:
                        aabb = tiles.unbreakable.getTileAABB(x, y, z)
                        if aabb:
                            boxes.add(aabb)

        return boxes

    def swap(self, int x0, int y0, int z0, int x1, int y1, int z1):
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

        for levelListener in self.__levelListeners:
            levelListener.setDirty(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)

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

    cpdef inline int getTile(self, int x, int y, int z) except *:
        if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
            return self.__blocks[(y * self.height + z) * self.width + x] & 255
        else:
            return 0

    cdef inline bint isSolidTile(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return False if tile is None else tile.isSolid()

    cpdef void tickEntities(self):
        for entity in self.entities.copy():
            entity.tick()
            if entity.removed:
                self.entities.remove(entity)

    @cython.cdivision(True)
    cpdef void tick(self):
        cdef int i1, i2, h, w, d, ticks, i, i12, x, z, y, id_
        cdef char b

        self.__tickCount += 1

        i1 = 1
        i2 = 1

        while True:
            if 1 << i1 == self.width:
                break

            i1 += 1

        while 1 << i2 < self.height:
            i2 += 1

        h = self.height - 1
        w = self.width - 1
        d = self.depth - 1

        if self.__tickCount % 5 == 0:
            ticks = len(self.__tickList)
            for i in range(ticks):
                coord = self.__tickList.pop()
                if coord.scheduledTime > 0:
                    coord.scheduledTime -= 1
                    self.__tickList.add(coord)
                else:
                    b = self.__blocks[(coord.y * self.height + coord.z) * self.width + coord.x]
                    if self.__isInLevelBounds(coord.x, coord.y, coord.z) and b == coord.id and b > 0:
                        (<Tile>tiles.tiles[b]).tick(self, coord.x, coord.y, coord.z, self.rand)

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

    cdef inline bint __isInLevelBounds(self, int x, int y, int z):
        return x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height

    cpdef inline float getGroundLevel(self):
        return self.depth / 2 - 2

    cpdef inline float getWaterLevel(self):
        return self.depth / 2

    cpdef bint containsAnyLiquid(self, box):
        cdef int x0, x1, y0, y1, z0, z1, x, y, z
        cdef Tile tile

        x0 = <int>floor(box.x0)
        x1 = <int>floor(box.x1 + 1.0)
        y0 = <int>floor(box.y0)
        y1 = <int>floor(box.y1 + 1.0)
        z0 = <int>floor(box.z0)
        z1 = <int>floor(box.z1 + 1.0)

        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if z0 < 0: z0 = 0
        if x1 > self.width: x1 = self.width
        if y1 > self.depth: y1 = self.depth
        if z1 > self.height: z1 = self.height
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    tile = tiles.tiles[self.getTile(x, y, z)]
                    if tile and tile.getLiquidType() != Liquid.none:
                        return True

        return False

    cpdef bint containsLiquid(self, box, int liquid):
        cdef int x0, x1, y0, y1, z0, z1, x, y, z
        cdef Tile tile

        x0 = <int>floor(box.x0)
        x1 = <int>floor(box.x1 + 1.0)
        y0 = <int>floor(box.y0)
        y1 = <int>floor(box.y1 + 1.0)
        z0 = <int>floor(box.z0)
        z1 = <int>floor(box.z1 + 1.0)

        if x0 < 0: x0 = 0
        if y0 < 0: y0 = 0
        if z0 < 0: z0 = 0
        if x1 > self.width: x1 = self.width
        if y1 > self.depth: y1 = self.depth
        if z1 > self.height: z1 = self.height
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    tile = tiles.tiles[self.getTile(x, y, z)]
                    if tile and tile.getLiquidType() == liquid:
                        return True

        return False

    cpdef inline addToTickNextTick(self, int x, int y, int z, int type_):
        cdef int tickDelay
        cdef Coord coord

        if not self.__networkMode:
            coord = Coord(x, y, z, type_)
            if type_ > 0:
                tickDelay = (<Tile>tiles.tiles[type_]).getTickDelay()
                coord.scheduledTime = tickDelay

            self.__tickList.add(coord)

    cpdef bint isFree(self, aabb):
        for entity in self.entities:
            if entity.bb.intersects(aabb):
                return False

        return True

    cpdef inline bint isSolid(self, int x, int y, int z, int f4):
        if self.__isSolidTile(x - f4, y - f4, z - f4):
            return True
        elif self.__isSolidTile(x - f4, y - f4, z + f4):
            return True
        elif self.__isSolidTile(x - f4, y + f4, z - f4):
            return True
        elif self.__isSolidTile(x - f4, y + f4, z + f4):
            return True
        elif self.__isSolidTile(x + f4, y - f4, z - f4):
            return True
        elif self.__isSolidTile(x + f4, y - f4, z + f4):
            return True
        elif self.__isSolidTile(x + f4, y + f4, z - f4):
            return True
        else:
            return self.__isSolidTile(x + f4, y + f4, z + f4)

    cdef inline bint __isSolidTile(self, int x, int y, int z):
        tile = self.getTile(<int>x, <int>y, <int>z)
        return tile > 0 and (<Tile>tiles.tiles[tile]).isSolid()

    cdef int getHighestTile(self, int x, int z):
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

    cpdef inline bint isWater(self, int x, int y, int z):
        cdef int tile = self.getTile(x, y, z)
        return tile > 0 and (<Tile>tiles.tiles[tile]).getLiquidType() == Liquid.water

    def setNetworkMode(self, bint mode):
        self.__networkMode = mode

    def clip(self, vec1, vec2):
        cdef int x0, y0, z0, x1, y1, z1, i, tile
        cdef float f9, f10, f11, f12, f13, f14, f15, f16, f17
        cdef char sideHit

        if not isnan(vec1.x) and not isnan(vec1.y) and not isnan(vec1.z):
            if not isnan(vec2.x) and not isnan(vec2.y) and not isnan(vec2.z):
                x0 = <int>floor(vec2.x)
                y0 = <int>floor(vec2.y)
                z0 = <int>floor(vec2.z)
                x1 = <int>floor(vec1.x)
                y1 = <int>floor(vec1.y)
                z1 = <int>floor(vec1.z)
                i = 20
                tile = self.getTile(x1, y1, z1)
                while tile <= 0 or (<Tile>tiles.tiles[tile]).getLiquidType() != Liquid.none:
                    if i < 0:
                        return None

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

                    x1 = <int>floor(vec1.x)
                    if sideHit == 5:
                        x1 -= 1

                    y1 = <int>floor(vec1.y)
                    if sideHit == 1:
                        y1 -= 1

                    z1 = <int>floor(vec1.z)
                    if sideHit == 3:
                        z1 -= 1

                    tile = self.getTile(x1, y1, z1)

                return HitResult(0, x1, y1, z1, sideHit)

    def playSound(self, name, float x, float y, float z,
                  float volume, float pitch, entity=None):
        cdef float dist = 16.0
        if dist > 1.0:
            dist *= volume

        audioInfo = self.rendererContext.soundManager.getAudioInfo(name, volume, pitch)
        if self.rendererContext and self.rendererContext.soundPlayer and audioInfo:
            if entity:
                if self.rendererContext.player.distanceTo(entity) < dist * dist:
                    self.rendererContext.soundPlayer.play(audioInfo, SoundPos(x, y, z))
            elif self.rendererContext.player.getDistanceSq(x, y, z) < dist * dist:
                self.rendererContext.soundPlayer.play(audioInfo, SoundPos(x, y, z))

cpdef object rebuild(str name, str creator, object createTime, float rotSpawn,
                     set entities, int unprocessed, int tickCount, int multiplier,
                     unsigned long addend, int width, int height, int depth,
                     bytearray blocks, int xSpawn, int ySpawn, int zSpawn):
    l = Level()
    l.initTransient(name, creator, createTime, rotSpawn, entities, unprocessed,
                    tickCount, multiplier, addend, width, height, depth,
                    blocks, xSpawn, ySpawn, zSpawn)
    return l
