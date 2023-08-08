# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport floor, isnan

from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.phys.AABB import AABB

import random

@cython.final
cdef class Level:
    TILE_UPDATE_INTERVAL = 200

    def __cinit__(self):
        self.update_interval = self.TILE_UPDATE_INTERVAL

        self.name = ''
        self.creator = ''
        self.createTime = 0

        self.levelListeners = set()
        self.rand = random.Random()
        self.randValue = self.rand.getrandbits(31)

        self.unprocessed = 0

        self.multiplier = 1664525
        self.addend = 1013904223

    def __dealloc__(self):
        free(self.__blocks)
        free(self.__heightMap)

    def setDataBytes(self, int w, int d, int h, bytearray blocks):
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
            self.__heightMap[i] = 0
        self.__calcLightDepths(0, 0, w, h)

        for levelListener in self.levelListeners:
            levelListener.allChanged()

    def getBlocks(self):
        blocks = bytearray(self.width * self.height * self.depth)
        for i in range(len(blocks)):
            blocks[i] = self.__blocks[i]

        return blocks

    cdef __calcLightDepths(self, int x0, int y0, int x1, int y1):
        cdef int x, z, oldDepth, y, yl0, yl1
        cdef Tile tile

        for x in range(x0, x0 + x1):
            for z in range(y0, y0 + y1):
                oldDepth = self.__heightMap[x + z * self.width]
                y = self.depth - 1
                while y > 0:
                    tile = tiles.tiles[self.getTile(x, y, z)]
                    if tile and tile.blocksLight():
                        break
                    else:
                        y -= 1

                self.__heightMap[x + z * self.width] = y + 1

                if oldDepth != y:
                    yl0 = oldDepth if oldDepth < y else y
                    yl1 = oldDepth if oldDepth > y else y
                    for levelListener in self.levelListeners:
                        levelListener.setDirty(x - 1, yl0 - 1, z - 1,
                                               x + 1, yl1 + 1, z + 1)

    cdef inline bint isLightBlocker(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return tile.blocksLight() if tile else False

    cpdef getCubes(self, box):
        cdef int x0, x1, y0, y1, z0, z1, x, y, z
        cdef Tile tile

        boxes = set()
        x0 = <int>floor(box.x0)
        x1 = <int>floor(box.x1 + 1)
        y0 = <int>floor(box.y0)
        y1 = <int>floor(box.y1 + 1)
        z0 = <int>floor(box.z0)
        z1 = <int>floor(box.z1 + 1)

        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
                        tile = tiles.tiles[self.getTile(x, y, z)]
                        if tile:
                            aabb = tile.getAABB(x, y, z)
                            if aabb:
                                boxes.add(aabb)
                    elif x < 0 or y < 0 or z < 0 or x >= self.width or z >= self.height:
                        aabb = tiles.unbreakable.getAABB(x, y, z)
                        if aabb:
                            boxes.add(aabb)

        return boxes

    cpdef bint setTile(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return False
        if type_ == self.__blocks[(y * self.height + z) * self.width + x]:
            return False

        self.__blocks[(y * self.height + z) * self.width + x] = type_

        self.__updateNeighborAt(x - 1, y, z, type_)
        self.__updateNeighborAt(x + 1, y, z, type_)
        self.__updateNeighborAt(x, y - 1, z, type_)
        self.__updateNeighborAt(x, y + 1, z, type_)
        self.__updateNeighborAt(x, y, z - 1, type_)
        self.__updateNeighborAt(x, y, z + 1, type_)
        self.__calcLightDepths(x, z, 1, 1)

        for levelListener in self.levelListeners:
            levelListener.setDirty(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)

        return True

    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return False
        if type_ == self.__blocks[(y * self.height + z) * self.width + x]:
            return False

        self.__blocks[(y * self.height + z) * self.width + x] = type_
        return True

    cdef __updateNeighborAt(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return

        cdef Tile tile = tiles.tiles[self.__blocks[(y * self.height + z) * self.width + x]]
        if tile:
            tile.neighborChanged(self, x, y, z, type_)

    cpdef inline bint isLit(self, int x, int y, int z):
        return y >= self.__heightMap[x + z * self.width] if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height else True

    cpdef inline int getTile(self, int x, int y, int z):
        if x >= 0 and y >= 0 and z >= 0 and x < self.width and y < self.depth and z < self.height:
            return self.__blocks[(y * self.height + z) * self.width + x]
        else:
            return 0

    cpdef tick(self):
        cdef int i1, i2, h, w, d, ticks, i, value, x, y, z
        cdef Tile tile

        i1 = 1
        i2 = 1

        while 1 << i1 < self.width:
            i1 += 1
        while 1 << i2 < self.height:
            i2 += 1

        h = self.height - 1
        w = self.width - 1
        d = self.depth - 1

        self.unprocessed += self.width * self.height * self.depth
        ticks = self.unprocessed // self.update_interval
        self.unprocessed -= ticks * self.update_interval
        for i in range(ticks):
            self.randValue = self.randValue * self.multiplier + self.addend
            value = self.randValue >> 2
            x = value & w
            z = value >> i1 & h
            y = value >> i1 + i2 & d
            id_ = self.__blocks[(y * self.height + z) * self.width + x]
            if tiles.rock.shouldTick[id_]:
                (<Tile>tiles.tiles[id_]).tick(self, x, y, z, self.rand)

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
                    if tile and tile.getLiquidType() > 0:
                        return True

        return False

    cpdef bint containsLiquid(self, box, int liquidId):
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
                    if tile and tile.getLiquidType() == liquidId:
                        return True

        return False

    cpdef clip(self, vec1, vec2):
        cdef int x0, y0, z0, x1, y1, z1, tileId
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

                while not isnan(vec1.x) and not isnan(vec1.y) and not isnan(vec1.z):
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

                    tileId = self.getTile(x1, y1, z1)
                    if tileId > 0 and (<Tile>tiles.tiles[tileId]).getLiquidType() == 0:
                        return HitResult(0, x1, y1, z1, sideHit)
