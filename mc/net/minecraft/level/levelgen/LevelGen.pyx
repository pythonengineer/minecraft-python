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
        object __loadingScreen
        int __coords[0x100000]
        int __width
        int __height
        int __depth
        char* __blocks

    def __cinit__(self):
        self.__random = Random()

    def __init__(self, progressListener):
        self.__loadingScreen = progressListener

    def generateLevel(self, str userName, int width, int height, int depth):
        cdef int *heightmap
        cdef int *oldHeightmap
        cdef int i, i13, i34, i5, i15, i41, w, d, h, ix, iy, iz, i42, i16, i46, \
                 id_, rock, count, length, l, xx, yy, zz, ii, target, i37
        cdef float f6, x, y, z, dir1, dira1, dir2, dira2, size, xd, yd, zd
        cdef double d14, d16, d21, start, end, d36
        cdef long tileCount
        cdef Distort distort8, distort9, distort32
        cdef PerlinNoise perlinNoise
        cdef Level level

        self.__loadingScreen.beginLevelLoading('Generating level')

        self.__width = width
        self.__height = height
        self.__depth = 64
        self.__blocks = <char*>malloc(sizeof(char) * (self.__width * self.__height << 6))

        self.__loadingScreen.levelLoadUpdate('Raising..')

        distort8 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        distort9 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        perlinNoise = PerlinNoise(self.__random, 8)
        heightmap = <int*>malloc(sizeof(int) * (self.__width * self.__height))
        f6 = 1.3

        for i in range(self.__width):
            for i13 in range(self.__height):
                d14 = distort8.getValue(i * f6, i13 * f6) / 8.0 - 8.0
                d16 = distort9.getValue(i * f6, i13 * f6) / 6.0 + 6.0
                if perlinNoise.getValue(i, i13) / 8.0 > 0.0:
                    d16 = d14

                d21 = max(d14, d16) / 2.0
                if d21 < 0.0:
                    d21 *= 0.8

                heightmap[i + i13 * self.__width] = <int>d21

        oldHeightmap = heightmap
        self.__loadingScreen.levelLoadUpdate('Eroding..')

        distort9 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))
        distort32 = Distort(PerlinNoise(self.__random, 8), PerlinNoise(self.__random, 8))

        for i34 in range(width):
            for i5 in range(height):
                d36 = distort9.getValue(i34 << 1, i5 << 1) / 8.0
                i15 = 1 if distort32.getValue(i34 << 1, i5 << 1) > 0.0 else 0
                if d36 > 2.0:
                    i41 = ((heightmap[i34 + i5 * self.__width] - i15) // 4) + i15
                    heightmap[i34 + i5 * self.__width] = i41

        self.__loadingScreen.levelLoadUpdate('Soiling..')

        heightmap = oldHeightmap
        w = self.__width
        d = self.__depth
        h = self.__height
        perlinNoise = PerlinNoise(self.__random, 8)
        for ix in range(w):
            for iy in range(h):
                i42 = <int>(perlinNoise.getValue(ix, iy) / 24.0) - 4
                i16 = heightmap[ix + iy * w] + d // 2
                i46 = i16 + i42
                heightmap[ix + iy * w] = max(i16, i46)

                for iz in range(d):
                    i = (iz * h + iy) * w + ix
                    id_ = 0
                    if iz <= i16:
                        id_ = tiles.dirt.id
                    if iz <= i46:
                        id_ = tiles.rock.id

                    self.__blocks[i] = id_

        self.__loadingScreen.levelLoadUpdate('Carving..')

        count = w * h * d // 256 // 64
        rock = <int>tiles.rock.id
        for i in range(count):
            x = self.__random.randFloatM(w)
            y = self.__random.randFloatM(d)
            z = self.__random.randFloatM(h)
            length = <int>(self.__random.randFloat() + self.__random.randFloatM(75.0))
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

                if self.__random.randFloat() >= 0.3:
                    x = x + self.__random.randFloat() * 4.0 - 2.0
                    y = y + self.__random.randFloat() * 4.0 - 2.0
                    z = z + self.__random.randFloat() * 4.0 - 2.0
                    size = sin(l * pi / length) * 2.5 + 1.0

                    for xx in range(<int>(x - size), <int>(x + size) + 1):
                        for yy in range(<int>(y - size), <int>(y + size) + 1):
                            for zz in range(<int>(z - size), <int>(z + size) + 1):
                                xd = xx - x
                                yd = yy - y
                                zd = zz - z
                                dd = xd * xd + yd * yd * 2.0 + zd * zd
                                if dd < size * size and xx >= 1 and yy >= 1 and zz >= 1 and xx < self.__width - 1 and yy < self.__depth - 1 and zz < self.__height - 1:
                                    ii = (yy * self.__height + zz) * self.__width + xx
                                    if self.__blocks[ii] == rock:
                                        self.__blocks[ii] = 0

        self.__carveTunnels(tiles.oreCoal.id, 90, 1, 4)
        self.__carveTunnels(tiles.oreIron.id, 70, 2, 4)
        self.__carveTunnels(tiles.oreGold.id, 50, 3, 4)
        self.__loadingScreen.levelLoadUpdate('Watering..')

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
            ix = self.__random.randInt(self.__width)
            iy = self.__depth // 2 - 1 - self.__random.randInt(3)
            iz = self.__random.randInt(self.__height)
            if self.__blocks[(iy * self.__height + iz) * self.__width + ix] == 0:
                tileCount += self.__floodFillLiquid(ix, iy, iz, 0, target)

        after = getNs()
        print('Flood filled ' + str(tileCount) + ' tiles in ' + str((after - before) / 1000000.0) + ' ms')

        self.__loadingScreen.levelLoadUpdate('Melting..')
        self.__addLava()
        self.__loadingScreen.levelLoadUpdate('Growing..')
        self.__addBeaches(heightmap)
        self.__loadingScreen.levelLoadUpdate('Planting..')
        self.__plantTrees(heightmap)

        level = Level()
        level.setData(width, 64, height, self.__blocks)
        level.createTime = getMillis()
        level.creator = userName
        level.name = 'A Nice World'
        return level

    cdef __addBeaches(self, int* heightmap):
        cdef int w, h, d, x, y, heightmap1, heightmap2, i13
        cdef bint z9, z10
        cdef char heightmap3
        cdef PerlinNoise perlinNoise5
        cdef PerlinNoise perlinNoise6

        w = self.__width
        h = self.__height
        d = self.__depth
        perlinNoise5 = PerlinNoise(self.__random, 8)
        perlinNoise6 = PerlinNoise(self.__random, 8)

        for x in range(w):
            for y in range(h):
                z9 = perlinNoise5.getValue(x, y) > 8.0
                z10 = perlinNoise6.getValue(x, y) > 12.0
                heightmap1 = heightmap[x + y * w]
                heightmap2 = (heightmap1 * h + y) * w + x
                i13 = self.__blocks[((heightmap1 + 1) * h + y) * w + x] & 255
                if (i13 == tiles.water.id or i13 == tiles.calmWater.id) and heightmap1 <= d // 2 - 1 and z10:
                    self.__blocks[heightmap2] = tiles.gravel.id

                if i13 == 0:
                    heightmap3 = tiles.grass.id
                    if heightmap1 <= d // 2 - 1 and z9:
                        heightmap3 = tiles.sand.id

                    self.__blocks[heightmap2] = heightmap3

    cdef __plantTrees(self, int* heightmap):
        cdef int w, i3, i4, i8, i9, i7, i10, i11, i12, i14
        cdef int i16, i17, i20, i19, i18, i21, i22
        cdef bint z13
        cdef char b15

        w = self.__width
        i3 = w * self.__height // 4000

        for i4 in range(i3):
            i8 = self.__random.randInt(w)
            i9 = self.__random.randInt(self.__height)
            for i7 in range(20):
                for i10 in range(20):
                    i8 += self.__random.randInt(6) - self.__random.randInt(6)
                    i9 += self.__random.randInt(6) - self.__random.randInt(6)
                    if i8 >= 0 and i9 >= 0 and i8 < w and i9 < self.__height:
                        i11 = heightmap[i8 + i9 * w] + 1
                        i12 = self.__random.randInt(3) + 4
                        z13 = True

                        for i14 in range(i11, i11 + 2 + i12):
                            b15 = 1
                            if i14 >= i11 + 1 + i12 - 2:
                                b15 = 2

                            for i16 in range(i8 - b15, i8 + b15 + 1):
                                if not z13:
                                    break

                                for i17 in range(i9 - b15, i9 + b15 + 1):
                                    if not z13:
                                        break

                                    if i16 >= 0 and i14 >= 0 and i17 >= 0 and i16 < w and i14 < self.__depth and i17 < self.__height:
                                        if (self.__blocks[(i14 * self.__height + i17) * w + i16] & 255) != 0:
                                            z13 = False
                                    else:
                                        z13 = False

                        if z13:
                            i14 = (i11 * self.__height + i9) * w + i8
                            if (self.__blocks[((i11 - 1) * self.__height + i9) * w + i8] & 255) == tiles.grass.id and i11 < self.__depth - i12 - 1:
                                self.__blocks[i14 - 1 * w * self.__height] = tiles.dirt.id

                                for i16 in range(i11 - 3 + i12, i11 + i12 + 1):
                                    i17 = i16 - (i11 + i12)
                                    i18 = <int>(1 - i17 / 2)

                                    for i21 in range(i8 - i18, i8 + i18 + 1):
                                        i22 = i21 - i8

                                        for i19 in range(i9 - i18, i9 + i18 + 1):
                                            i20 = i19 - i9
                                            if abs(i22) != i18 or abs(i20) != i18 or floor(self.__random.randInt(2)) != 0 and i17 != 0:
                                                self.__blocks[(i16 * self.__height + i19) * w + i21] = tiles.leaf.id

                                for i16 in range(i12):
                                    self.__blocks[i14 + i16 * w * self.__height] = tiles.log.id

    cdef __carveTunnels(self, int face, int i2, int i3, int i4):
        cdef int w, h, d, i7, i8, i12, i17, i19, i20, i21, i26
        cdef float f9, f10, f11, f12, f13, f14, f15, f16, f18, f22, f23, f24

        w = self.__width
        h = self.__height
        d = self.__depth
        i7 = w * h * d // 256 // 64 * i2 // 100
        for i8 in range(i7):
            f9 = self.__random.randFloatM(w)
            f10 = self.__random.randFloatM(d)
            f11 = self.__random.randFloatM(h)
            i12 = <int>((self.__random.randFloat() + self.__random.randFloat()) * 75.0 * i2 / 100.0)
            f13 = self.__random.randFloat() * pi * 2.0
            f14 = 0.0
            f15 = self.__random.randFloat() * pi * 2.0
            f16 = 0.0

            for i17 in range(i12):
                f9 = f9 + sin(f13) * cos(f15)
                f11 = f11 + cos(f13) * cos(f15)
                f10 = f10 + sin(f15)
                f13 += f14 * 0.2
                f14 = (f14 * 0.9) + (self.__random.randFloat() - self.__random.randFloat())
                f15 = (f15 + f16 * 0.5) * 0.5
                f16 = (f16 * 0.9) + (self.__random.randFloat() - self.__random.randFloat())
                f18 = sin(i17 * pi / i12) * i2 / 100.0 + 1.0

                for i19 in range(<int>(f9 - f18), <int>(f9 + f18 + 1)):
                    for i20 in range(<int>(f10 - f18), <int>(f10 + f18 + 1)):
                        for i21 in range(<int>(f11 - f18), <int>(f11 + f18 + 1)):
                            f22 = i19 - f9
                            f23 = i20 - f10
                            f24 = i21 - f11
                            if f22 * f22 + f23 * f23 * 2.0 + f24 * f24 < f18 * f18 and \
                               i19 >= 1 and i20 >= 1 and i21 >= 1 and i19 < self.__width - 1 and \
                               i20 < self.__depth - 1 and i21 < self.__height - 1:
                                i26 = (i20 * self.__height + i21) * self.__width + i19
                                if self.__blocks[i26] == tiles.rock.id:
                                    self.__blocks[i26] = face

    cdef __addLava(self):
        cdef int lavaCount, i2, i, x, y, z

        lavaCount = 0
        i2 = self.__width * self.__height * self.__depth // 10000
        for i in range(i2):
            x = self.__random.randInt(self.__width)
            y = self.__random.randInt(self.__depth // 2 - 4)
            z = self.__random.randInt(self.__height)
            if self.__blocks[(y * self.__height + z) * self.__width + x] == 0:
                lavaCount += 1
                self.__floodFillLiquid(x, y, z, 0, tiles.calmLava.id)

        print('LavaCount:', lavaCount)

    cdef long __floodFillLiquid(self, int x, int y, int z, int source, int tt):
        cdef int target, p, wBits, hBits, hMask, wMask, upStep, cl, i, z0, y0, x0, x1
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
