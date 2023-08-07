# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport floor, isnan

from mc.net.minecraft.HitResult import HitResult
from mc.net.minecraft.level.tile.Tile cimport Tile
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.LevelGen import LevelGen
from mc.net.minecraft.phys.AABB import AABB

import random
import gzip

@cython.final
cdef class Level:
    TILE_UPDATE_INTERVAL = 400

    def __cinit__(self):
        self.update_interval = self.TILE_UPDATE_INTERVAL

        self.levelListeners = set()

        self.unprocessed = 0

    def __init__(self, int w, int h, int d):
        self.width = w
        self.height = h
        self.depth = d

        self.__lightDepths = <int*>malloc(sizeof(int) * (w * h))
        for i in range(w * h):
            self.__lightDepths[i] = 0

        if not self.load():
            blocks = LevelGen(w, h, d).generateMap()
            self.__blocks = <char*>malloc(sizeof(char) * (w * h * d))
            for i in range(len(blocks)):
                self.__blocks[i] = blocks[i]

        self.calcLightDepths(0, 0, w, h)

    def __dealloc__(self):
        free(self.__blocks)
        free(self.__lightDepths)

    def load(self):
        cdef char* b

        try:
            with gzip.open('level.dat', 'rb') as f:
                blocks = bytearray(f.read())

            b = <char*>malloc(sizeof(char) * len(blocks))
            for i in range(len(blocks)):
                b[i] = blocks[i]

            self.__blocks = b

            self.calcLightDepths(0, 0, self.width, self.height)
            for levelListener in self.levelListeners:
                levelListener.allChanged()

            return True
        except Exception as e:
            print(e)

        return False

    def save(self):
        try:
            b = bytearray(self.width * self.height * self.depth)
            for i in range(len(b)):
                b[i] = self.__blocks[i]

            with gzip.open('level.dat', 'wb') as f:
                f.write(b)
        except Exception as e:
            print(e)

    cdef calcLightDepths(self, int x0, int y0, int x1, int y1):
        cdef int x, z, oldDepth, y, yl0, yl1

        for x in range(x0, x0 + x1):
            for z in range(y0, y0 + y1):
                oldDepth = self.__lightDepths[(x + z * self.width)]
                y = self.depth - 1
                while y > 0 and not self.isLightBlocker(x, y, z):
                    y -= 1

                self.__lightDepths[(x + z * self.width)] = y

                if oldDepth != y:
                    yl0 = oldDepth if oldDepth < y else y
                    yl1 = oldDepth if oldDepth > y else y
                    for levelListener in self.levelListeners:
                        levelListener.lightColumnChanged(x, z, yl0, yl1)

    def addListener(self, levelListener):
        self.levelListeners.add(levelListener)

    def removeListener(self, levelListener):
        self.levelListeners.remove(levelListener)

    cdef inline bint isLightBlocker(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        return tile.blocksLight() if tile else False

    cpdef getCubes(self, aABB):
        cdef int x0, x1, y0, y1, z0, z1, x, y, z
        cdef Tile tile

        aABBs = set()
        x0 = <int>aABB.x0
        x1 = <int>(aABB.x1 + 1.0)
        y0 = <int>aABB.y0
        y1 = <int>(aABB.y1 + 1.0)
        z0 = <int>aABB.z0
        z1 = <int>(aABB.z1 + 1.0)

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
                    if tile:
                        aabb = tile.getAABB(x, y, z)
                        if aabb:
                            aABBs.add(aabb)

        return aABBs

    cpdef bint setTile(self, int x, int y, int z, int type_):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return False
        if type_ == self.__blocks[(y * self.height + z) * self.width + x]:
            return False

        self.__blocks[(y * self.height + z) * self.width + x] = type_
        self.calcLightDepths(x, z, 1, 1)
        for levelListener in self.levelListeners:
            levelListener.tileChanged(x, y, z)

        return True

    cpdef inline bint isLit(self, int x, int y, int z):
        x = int(x)
        y = int(y)
        z = int(z)
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return True

        return y >= self.__lightDepths[x + z * self.width]

    cpdef inline int getTile(self, int x, int y, int z):
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return 0

        return self.__blocks[(y * self.height + z) * self.width + x]

    cpdef inline bint isSolidTile(self, int x, int y, int z):
        cdef Tile tile = tiles.tiles[self.getTile(x, y, z)]
        if not tile:
            return False

        return tile.isSolid()

    cpdef tick(self):
        cdef int ticks, i, x, y, z
        cdef Tile tile

        self.unprocessed += self.width * self.height * self.depth
        ticks = self.unprocessed // self.update_interval
        self.unprocessed -= ticks * self.update_interval
        for i in range(ticks):
            x = <int>floor(self.width * random.random())
            y = <int>floor(self.depth * random.random())
            z = <int>floor(self.height * random.random())
            tile = tiles.tiles[self.getTile(x, y, z)]
            if tile:
                tile.tick(self, x, y, z, random)

    cpdef clip(self, vec1, vec2):
        cdef int x0, y0, z0, x1, y1, z1
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

                    if self.getTile(x1, y1, z1):
                        return HitResult(0, x1, y1, z1, sideHit)
