# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc
from libc.math cimport floor, sin, cos, pi

from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.CompatibilityShims import getMillis, getNs
from mc.cCompatibilityShims cimport Random

@cython.final
cdef class LevelGen:

    cdef:
        Random __random
        object __levelLoaderListener
        int __coords[0x100000]
        int __width
        int __height
        int __depth
        char* __blocks

    def __cinit__(self):
        self.__random = Random()

    def __init__(self, levelLoaderListener):
        self.__levelLoaderListener = levelLoaderListener

    def generateLevel(self, Level level, str userName, int width, int height, int depth):
        self.__levelLoaderListener.beginLevelLoading('Generating level')

        self.__width = width
        self.__height = height
        self.__depth = depth

        self.__blocks = <char*>malloc(sizeof(char) * (self.__width * self.__height * self.__depth))

        self.__levelLoaderListener.levelLoadUpdate('Raising..')
        heightMap = self.__buildHeightmap(width, height)
        self.__levelLoaderListener.levelLoadUpdate('Eroding..')
        self.__buildBlocks(heightMap)
        self.__levelLoaderListener.levelLoadUpdate('Carving..')
        self.carveTunnels()
        self.__levelLoaderListener.levelLoadUpdate('Watering..')
        self.addWater()
        self.__levelLoaderListener.levelLoadUpdate('Melting..')
        self.addLava()

        level.setData(width, depth, height, self.__blocks)
        level.createTime = getMillis()
        level.creator = userName
        level.name = 'A Nice World'
        return True

    cdef __buildBlocks(self, heightMap):
        cdef int w, h, d, x, y, z, dh, rh, i, id_

        w = self.__width
        h = self.__height
        d = self.__depth

        for x in range(w):
            for y in range(d):
                for z in range(h):
                    dh = d // 2
                    rh = d // 3
                    i = (y * h + z) * w + x
                    id_ = 0
                    if y == dh and (y >= d // 2 - 1):
                        id_ = tiles.grass.id
                    elif y <= dh:
                        id_ = tiles.dirt.id
                    if y <= rh:
                        id_ = tiles.rock.id
                    self.__blocks[i] = id_

    cdef __buildHeightmap(self, width, height):
        heightmap = [0.0] * width * height
        return heightmap

    cdef carveTunnels(self):
        cdef int w, h, d, count, i, length, l, xx, yy, zz, ii
        cdef float x, y, z, dir1, dira1, dir2, dira2, size, xd, yd, zd, dd

        w = self.__width
        h = self.__height
        d = self.__depth

        count = w * h * d // 256 // 64
        for i in range(count):
            x = self.__random.randFloatM(w)
            y = self.__random.randFloatM(d)
            z = self.__random.randFloatM(h)
            length = <int>(self.__random.randFloat() + self.__random.randFloat() * 150.0)
            dir1 = self.__random.randFloat() * pi * 2.0
            dira1 = 0.0
            dir2 = self.__random.randFloat() * pi * 2.0
            dira2 = 0.0

            for l in range(length):
                x = x + sin(dir1) * cos(dir2)
                z = z + cos(dir1) * cos(dir2)
                y = y + sin(dir2)

                dir1 += dira1 * 0.2
                dira1 *= 0.9
                dira1 += self.__random.randFloat() - self.__random.randFloat()

                dir2 += dira2 * 0.5
                dir2 *= 0.5
                dira2 *= 0.9
                dira2 += self.__random.randFloat() - self.__random.randFloat()

                size = sin(l * pi / length) * 2.5 + 1.0

                for xx in range(<int>(x - size), <int>(x + size) + 1):
                    for yy in range(<int>(y - size), <int>(y + size) + 1):
                        for zz in range(<int>(z - size), <int>(z + size) + 1):
                            xd = xx - x
                            yd = yy - y
                            zd = zz - z
                            dd = xd * xd + yd * yd * 2.0 + zd * zd
                            if dd < size * size and xx >= 1 and yy >= 1 and zz >= 1 and xx < w - 1 and yy < d - 1 and zz < h - 1:
                                ii = (yy * h + zz) * w + xx
                                if self.__blocks[ii] == tiles.rock.id:
                                    self.__blocks[ii] = 0

    cdef addWater(self):
        cdef int source, target, x, y, z, i
        cdef long tileCount

        before = getNs()
        tileCount = 0
        source = 0
        target = tiles.calmWater.id
        for x in range(self.__width):
            tileCount += self.floodFillLiquid(x, self.__depth // 2 - 1, 0, source, target)
            tileCount += self.floodFillLiquid(x, self.__depth // 2 - 1, self.__height - 1, source, target)
        for y in range(self.__height):
            tileCount += self.floodFillLiquid(0, self.__depth // 2 - 1, y, source, target)
            tileCount += self.floodFillLiquid(self.__width - 1, self.__depth // 2 - 1, y, source, target)
        for i in range(self.__width * self.__height // 5000):
            x = <int>floor(self.__random.randFloat() * self.__width)
            y = self.__depth // 2 - 1
            z = <int>floor(self.__random.randFloat() * self.__height)
            if self.__blocks[(y * self.__height + z) * self.__width + x] == 0:
                tileCount += self.floodFillLiquid(x, y, z, 0, target)
        after = getNs()
        print('Flood filled ' + str(tileCount) + ' tiles in ' + str((after - before) / 1000000.0) + ' ms')

    cdef addLava(self):
        cdef int lavaCount, i, x, y, z
        lavaCount = 0
        for i in range(self.__width * self.__height * self.__depth // 10000):
            x = <int>floor(self.__random.randFloatM(self.__width))
            y = <int>floor(self.__random.randFloatM(self.__depth // 2))
            z = <int>floor(self.__random.randFloatM(self.__height))
            if self.__blocks[(y * self.__height + z) * self.__width + x] == 0:
                lavaCount += 1
                self.floodFillLiquid(x, y, z, 0, tiles.calmLava.id)
        print('LavaCount:', lavaCount)

    cdef long floodFillLiquid(self, int x, int y, int z, int source, int tt):
        cdef int target, p, wBits, hBits, hMask, wMask, upStep, cl, z0, y0, x0, x1
        cdef int z1, y1
        cdef bint lastNorth, lastSouth, lastBelow, north, south, below
        cdef long tileCount
        cdef char belowId

        target = tt
        coordBuffer = []
        p = 0

        wBits = 1
        hBits = 1
        while 1 << wBits < self.__width:
            wBits += 1
        while 1 << hBits < self.__height:
            hBits += 1
        hMask = self.__height - 1
        wMask = self.__width - 1
        self.__coords[p] = ((y << hBits) + z << wBits) + x
        p += 1
        tileCount = 0
        upStep = self.__width * self.__height
        x1 = 0
        xx = 0
        while p > 0 and xx < x1:
            p -= 1
            cl = self.__coords[p]

            z0 = cl >> wBits & hMask
            y0 = cl >> wBits + hBits
            x0 = cl & wMask

            x1 = x0
            while self.__blocks[cl - 1] == source:
                x0 -= 1
                cl -= 1
                if x0 <= 0:
                    break

            while x1 < self.__width and self.__blocks[(cl + x1 - x0)] == source:
                x1 += 1

            z1 = cl >> wBits & hMask
            y1 = cl >> wBits + hBits

            if z1 != z0 or y1 != y0:
                print('hoooly fuck') # sic

            lastNorth = False
            lastSouth = False
            lastBelow = False

            tileCount += x1 - x0
            xx = x0
            continue

            self.__blocks[cl] = target

            if z0 > 0:
                north = self.__blocks[cl - self.__width] == source

                if north and not lastNorth:
                    if p == len(self.__coords):
                        coordBuffer.append(self.__coords)
                        self.__coords = [0] * 1048576
                        p = 0

                    self.__coords[p] = cl - self.__width
                    p += 1

                lastNorth = north

            if z0 < self.__height - 1:
                south = self.__blocks[cl + self.__width] == source
                if south and not lastSouth:
                    if p == len(self.__coords):
                        coordBuffer.append(self.__coords)
                        self.__coords = [0] * 1048576
                        p = 0

                    self.__coords[p] = cl + self.__width
                    p += 1

                lastSouth = south

            if y0 > 0:
                belowId = self.__blocks[cl - upStep]
                if target == tiles.lava.id or target == tiles.calmLava.id:
                    if belowId == tiles.water.id or belowId == tiles.calmWater.id:
                        self.__blocks[cl - upStep] = tiles.rock.id

                below = belowId == source
                if below and not lastBelow:
                    if p == len(self.__coords):
                        coordBuffer.append(self.__coords)
                        self.__coords = [0] * 1048576
                        p = 0

                    self.__coords[p] = cl - upStep
                    p += 1

                lastBelow = below

            cl += 1
            xx += 1

        return tileCount
