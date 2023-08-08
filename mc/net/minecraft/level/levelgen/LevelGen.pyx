# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport floor, sin, cos, pi

from mc.net.minecraft.level.Level cimport Level
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.level.levelgen.synth.Distort cimport Distort
from mc.net.minecraft.level.levelgen.synth.PerlinNoise cimport PerlinNoise
from mc.CompatibilityShims import getMillis, getNs
from mc.cCompatibilityShims cimport Random

@cython.final
cdef class LevelGen:

    cdef:
        Random __random
        object __minecraft
        int __coords[0x100000]
        int __width
        int __height
        int __depth
        char* __blocks

    def __cinit__(self):
        self.__random = Random()

    def __init__(self, levelLoaderListener):
        self.__minecraft = levelLoaderListener

    def generateLevel(self, str userName, int width, int height, int depth):
        cdef int *heightmap
        cdef int i, i13, i34, i5, i15, i41, w, h, d, ix, iy, iz, i17, id_, count
        cdef int length, l, xx, yy, zz, ii, target, i37
        cdef long tileCount
        cdef float x, y, z, dir1, dira1, dir2, dira2, size, xd, yd, zd, dd
        cdef double d14, d16, d20, d36
        cdef Distort distort8, distort9, distort32
        cdef PerlinNoise perlinNoise

        self.__minecraft.beginLevelLoading('Generating level')

        self.__width = width
        self.__height = height
        self.__depth = depth

        self.__blocks = <char*>malloc(sizeof(char) * (self.__width * self.__height * self.__depth))

        self.__minecraft.levelLoadUpdate('Raising..')

        distort8 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        distort9 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        perlinNoise = PerlinNoise(self.__random, 8)
        heightmap = <int*>malloc(sizeof(int) * (self.__width * self.__height))

        for i in range(width):
            for i13 in range(height):
                d14 = distort8.getValue(i, i13) / 8.0 - 8.0
                d16 = distort9.getValue(i, i13) / 8.0 + 8.0
                if perlinNoise.getValue(i, i13) / 8.0 > 2.0:
                    d16 = d14

                d20 = max(d14, d16)
                d20 = (d20 * d20 * d20 / 100.0 + d20 * 3.0) / 8.0
                heightmap[i + i13 * width] = <int>d20

        self.__minecraft.levelLoadUpdate('Eroding..')

        distort9 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        distort32 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))

        for i34 in range(width):
            for i5 in range(height):
                d36 = distort9.getValue(i34 << 1, i5 << 1) / 8.0
                i15 = 1 if distort32.getValue(i34 << 1, i5 << 1) > 0.0 else 0
                if d36 > 2.0:
                    i41 = <int>(((heightmap[i34 + i5 * width] - i15) // 2 << 1) + i15)
                    heightmap[i34 + i5 * width] = i41

        self.__minecraft.levelLoadUpdate('Soiling..')

        w = self.__width
        d = self.__depth
        h = self.__height
        for ix in range(w):
            for iy in range(d):
                for iz in range(h):
                    i = (iy * self.__height + iz) * self.__width + ix
                    i41 = heightmap[ix + iz * w] + d // 2
                    i17 = i41 - 2
                    id_ = 0
                    if iy == i41 and (iy >= d // 2 - 1):
                        id_ = tiles.grass.id
                    elif iy <= i41:
                        id_ = tiles.dirt.id

                    if iy <= i17:
                        id_ = tiles.rock.id

                    self.__blocks[i] = id_

        self.__minecraft.levelLoadUpdate('Carving..')

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

        self.__minecraft.levelLoadUpdate('Watering..')

        before = getNs()
        tileCount = 0
        target = tiles.calmWater.id
        for ix in range(self.__width):
            tileCount += self.__floodFillLiquid(ix, self.__depth // 2 - 1, 0, 0, target)
            tileCount += self.__floodFillLiquid(ix, self.__depth // 2 - 1, self.__height - 1, 0, target)
        for iy in range(self.__height):
            tileCount += self.__floodFillLiquid(0, self.__depth // 2 - 1, iy, 0, target)
            tileCount += self.__floodFillLiquid(self.__width - 1, self.__depth // 2 - 1, iy, 0, target)

        i37 = self.__width * self.__height // 200
        for i in range(i37):
            ix = <int>floor(self.__random.randFloat() * self.__width)
            iy = self.__depth // 2 - 1 - <int>floor(self.__random.randFloatM(3))
            iz = <int>floor(self.__random.randFloat() * self.__height)
            if self.__blocks[(iy * self.__height + iz) * self.__width + ix] == 0:
                tileCount += self.__floodFillLiquid(ix, iy, iz, 0, target)

        after = getNs()
        print('Flood filled ' + str(tileCount) + ' tiles in ' + str((after - before) / 1000000.0) + ' ms')

        self.__minecraft.levelLoadUpdate('Melting..')
        self.__addLava()

        (<Level>self.__minecraft.level).setData(width, depth, height, self.__blocks)
        self.__minecraft.level.createTime = getMillis()
        self.__minecraft.level.creator = userName
        self.__minecraft.level.name = 'A Nice World'

        free(heightmap)

        return True

    cdef __addLava(self):
        cdef int lavaCount, size, i, x, y, z

        lavaCount = 0
        size = self.__width * self.__height * self.__depth // 10000
        for i in range(size):
            x = <int>floor(self.__random.randFloatM(self.__width))
            y = <int>floor(self.__random.randFloatM(self.__depth // 2 - 4))
            z = <int>floor(self.__random.randFloatM(self.__height))
            if self.__blocks[(y * self.__height + z) * self.__width + x] == 0:
                lavaCount += 1
                self.__floodFillLiquid(x, y, z, 0, tiles.calmLava.id)

        print('LavaCount:', lavaCount)

    cdef long __floodFillLiquid(self, int x, int y, int z, int source, int tt):
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
        while p > 0:
            p -= 1
            cl = self.__coords[p]
            if p == 0 and len(coordBuffer) > 0:
                print('IT HAPPENED!')
                coordBuffer.pop(-1)
                self.__coords = <int*>malloc(len(coordBuffer) * sizeof(int))
                for i in range(len(coordBuffer)):
                    self.__coords[i] = coordBuffer[i]
                p = sizeof(self.__coords)

            z0 = cl >> wBits & hMask
            y0 = cl >> wBits + hBits
            x0 = cl & wMask

            x1 = x0
            for cl in range(cl, -1, -1):
                if self.__blocks[cl - 1] != 0:
                    break

                x0 -= 1

            while x1 < self.__width and self.__blocks[cl + x1 - x0] == 0:
                x1 += 1

            z1 = cl >> wBits & hMask
            y1 = cl >> wBits + hBits
            if z1 != z0 or y1 != y0:
                print('hoooly fuck') # sic

            lastNorth = False
            lastSouth = False
            lastBelow = False
            tileCount += x1 - x0

            for x0 in range(x0, x1):
                self.__blocks[cl] = target
                if z0 > 0:
                    north = self.__blocks[cl - self.__width] == source
                    if north and not lastNorth:
                        if p == sizeof(self.__coords):
                            coordBuffer.append(self.__coords)
                            self.__coords = <int*>malloc(0x100000 * sizeof(int))
                            p = 0

                        self.__coords[p] = cl - self.__width
                        p += 1

                    lastNorth = north

                if z0 < self.__height - 1:
                    south = self.__blocks[cl + self.__width] == source
                    if south and not lastSouth:
                        if p == sizeof(self.__coords):
                            coordBuffer.append(self.__coords)
                            self.__coords = <int*>malloc(0x100000 * sizeof(int))
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
                        if p == sizeof(self.__coords):
                            coordBuffer.append(self.__coords)
                            self.__coords = <int*>malloc(0x100000 * sizeof(int))
                            p = 0

                        self.__coords[p] = cl - upStep
                        p += 1

                    lastBelow = below

                cl += 1

        return tileCount
