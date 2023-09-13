# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc
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
        object __levelLoaderListener
        int __coords[0x100000]
        int __width
        int __height
        int __depth
        int __waterLevel
        char* __blocks

    def __cinit__(self):
        self.__random = Random()

    def __init__(self, desc):
        self.__levelLoaderListener = desc

    def generateLevel(self, str userName, int width, int height, int depth):
        cdef int *heightmap
        cdef int i, i13, i34, i5, i15, i41, w, h, d, ix, iy, iz, i42, i16, i46, \
                 id_, rock, count, length, l, xx, yy, zz, ii, target, i37
        cdef float f6, x, y, z, dir1, dira1, dir2, dira2, dir3, size, xd, yd, zd
        cdef double d14, d16, d21, start, end, d36
        cdef Distort distort8, distort9, distort32
        cdef PerlinNoise perlinNoise
        cdef Level level

        self.__levelLoaderListener.beginLevelLoading('Generating level')

        self.__width = width
        self.__height = height
        self.__depth = 64
        self.__waterLevel = 32
        self.__blocks = <char*>malloc(sizeof(char) * (self.__width * self.__height << 6))

        self.__levelLoaderListener.levelLoadUpdate('Raising..')

        distort8 = Distort(PerlinNoise(self.__random, 8),
                                       PerlinNoise(self.__random, 8))
        distort9 = Distort(PerlinNoise(self.__random, 8),
                                       PerlinNoise(self.__random, 8))
        perlinNoise = PerlinNoise(self.__random, 6)
        heightmap = <int*>malloc(sizeof(int) * (self.__width * self.__height))
        f6 = 1.3

        for i in range(self.__width):
            for i13 in range(self.__height):
                d14 = distort8.getValue(i * f6, i13 * f6) / 6.0 - 4.0
                d16 = distort9.getValue(i * f6, i13 * f6) / 5.0 + 6.0
                if perlinNoise.getValue(i, i13) / 8.0 > 0.0:
                    d16 = d14

                d21 = max(d14, d16) / 2.0
                if d21 < 0.0:
                    d21 *= 0.8

                heightmap[i + i13 * self.__width] = <int>d21

        self.__levelLoaderListener.levelLoadUpdate('Eroding..')

        distort9 = Distort(PerlinNoise(self.__random, 8),
                                       PerlinNoise(self.__random, 8))
        distort32 = Distort(PerlinNoise(self.__random, 8),
                                        PerlinNoise(self.__random, 8))
        for i34 in range(self.__width):
            for i5 in range(self.__height):
                d36 = distort9.getValue(i34 << 1, i5 << 1) / 8.0
                i15 = 1 if distort32.getValue(i34 << 1, i5 << 1) > 0.0 else 0
                if d36 > 2.0:
                    i41 = ((heightmap[i34 + i5 * self.__width] - i15) // 4) + i15
                    heightmap[i34 + i5 * self.__width] = i41

        self.__levelLoaderListener.levelLoadUpdate('Soiling..')

        w = self.__width
        h = self.__height
        d = self.__depth
        perlinNoise = PerlinNoise(self.__random, 8)
        for ix in range(w):
            for iy in range(h):
                i42 = <int>(perlinNoise.getValue(ix, iy) / 24.0) - 4
                i16 = heightmap[ix + iy * w] + self.__waterLevel
                i46 = i16 + i42
                heightmap[ix + iy * w] = max(i16, i46)
                if heightmap[ix + iy * w] > d - 2:
                    heightmap[ix + iy * w] = d - 2
                if heightmap[ix + iy * w] < 1:
                    heightmap[ix + iy * w] = 1

                for iz in range(d):
                    i = (iz * h + iy) * w + ix
                    id_ = 0
                    if iz <= i16:
                        id_ = tiles.dirt.id
                    if iz <= i46:
                        id_ = tiles.rock.id
                    if iz == 0:
                        id_ = tiles.lava.id

                    self.__blocks[i] = id_

        self.__levelLoaderListener.levelLoadUpdate('Carving..')

        count = w * h * d // 256 // 64 << 1
        rock = <int>tiles.rock.id
        for i in range(count):
            x = self.__random.randFloatM(w)
            y = self.__random.randFloatM(d)
            z = self.__random.randFloatM(h)
            length = <int>(self.__random.randFloat() + self.__random.randFloatM(200.0))
            dir1 = self.__random.randFloat() * pi * 2.0
            dira1 = 0.0
            dir2 = self.__random.randFloat() * pi * 2.0
            dira2 = 0.0
            dir3 = self.__random.randFloat() * self.__random.randFloat()

            for l in range(length):
                x = x + sin(dir1) * cos(dir2)
                z = z + cos(dir1) * cos(dir2)
                y = y + sin(dir2)

                dir1 += dira1 * 0.2
                dira1 *= 0.9
                dira1 += self.__random.randFloat() - self.__random.randFloat()

                dir2 += dira2 * 0.5
                dir2 *= 0.5
                dira2 *= 0.75
                dira2 += self.__random.randFloat() - self.__random.randFloat()

                if self.__random.randFloat() >= 0.25:
                    x += (self.__random.randFloat() * 4.0 - 2.0) * 0.2
                    y += (self.__random.randFloat() * 4.0 - 2.0) * 0.2
                    z += (self.__random.randFloat() * 4.0 - 2.0) * 0.2
                    size = (d - y) / d
                    size = 1.2 + (size * 3.5 + 1.0) * dir3
                    size = sin(l * pi / length) * size
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

        self.__addOre(tiles.coalOre.id, 90, 1, 4)
        self.__addOre(tiles.ironOre.id, 70, 2, 4)
        self.__addOre(tiles.goldOre.id, 50, 3, 4)
        self.__levelLoaderListener.levelLoadUpdate('Watering..')

        target = tiles.calmWater.id

        for ix in range(self.__width):
            self.__floodFillWithLiquid(ix, self.__depth // 2 - 1, 0, 0, target)
            self.__floodFillWithLiquid(ix, self.__depth // 2 - 1, self.__height - 1, 0, target)

        for iy in range(self.__height):
            self.__floodFillWithLiquid(0, self.__depth // 2 - 1, iy, 0, target)
            self.__floodFillWithLiquid(self.__width - 1, self.__depth // 2 - 1, iy, 0, target)

        i37 = self.__width * self.__height // 8000
        for i in range(i37):
            ix = self.__random.nextInt(self.__width)
            iy = self.__waterLevel - 1 - self.__random.nextInt(2)
            iz = self.__random.nextInt(self.__height)
            if self.__blocks[(iy * self.__height + iz) * self.__width + ix] == 0:
                self.__floodFillWithLiquid(ix, iy, iz, 0, target)

        self.__levelLoaderListener.levelLoadUpdate('Melting..')
        self.__addLava()
        self.__levelLoaderListener.levelLoadUpdate('Growing..')
        self.__addBeaches(heightmap)
        self.__levelLoaderListener.levelLoadUpdate('Planting..')
        self.__addFlowers(heightmap)
        self.__addMushrooms(heightmap)

        level = Level()
        level.waterLevel = self.__waterLevel
        level.setData(width, 64, height, self.__blocks)
        level.createTime = getMillis()
        level.creator = userName
        level.name = 'A Nice World'

        self.__generateTrees(level, heightmap)

        return level

    cdef __addBeaches(self, int* heightmap):
        cdef int w, h, d, x, y, heightmap1, heightmap2, i13
        cdef bint z9, z10
        cdef char heightmap3
        cdef PerlinNoise perlinNoise1, perlinNoise2

        w = self.__width
        h = self.__height
        d = self.__depth
        perlinNoise1 = PerlinNoise(self.__random, 8)
        perlinNoise2 = PerlinNoise(self.__random, 8)

        for x in range(w):
            for y in range(h):
                z9 = perlinNoise1.getValue(x, y) > 8.0
                z10 = perlinNoise2.getValue(x, y) > 12.0
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

    cdef __generateTrees(self, Level level, int* heightmap):
        cdef int w, size, i4, x, y, z, i7, i8, i9, i10

        w = self.__width
        size = w * self.__height // 4000
        for i4 in range(size):
            i8 = self.__random.nextInt(w)
            i9 = self.__random.nextInt(self.__height)
            for i7 in range(20):
                x = i8
                z = i9
                for i10 in range(20):
                    x += self.__random.nextInt(6) - self.__random.nextInt(6)
                    z += self.__random.nextInt(6) - self.__random.nextInt(6)
                    if x >= 0 and z >= 0 and x < w and z < self.__height:
                        y = heightmap[x + z * w] + 1
                        if self.__random.nextInt(4) == 0:
                            level.maybeGrowTree(x, y, z)

    cdef __addFlowers(self, int* heightmap):
        cdef int i, j, k, n2, n3, n4, n5, x, y, z, tile

        n2 = self.__width * self.__height // 3000
        for i in range(n2):
            n3 = self.__random.nextInt(2)
            n4 = self.__random.nextInt(self.__width)
            n5 = self.__random.nextInt(self.__height)
            for j in range(10):
                x = n4
                z = n5
                for k in range(5):
                    x += self.__random.nextInt(6) - self.__random.nextInt(6)
                    z += self.__random.nextInt(6) - self.__random.nextInt(6)
                    if (n3 >= 2 and self.__random.nextInt(4) != 0) or x < 0 or z < 0 or x >= self.__width or z >= self.__height:
                        continue

                    y = heightmap[x + z * self.__width] + 1
                    if self.__blocks[(y * self.__height + z) * self.__width + x] & 0xFF:
                        continue

                    tile = (y * self.__height + z) * self.__width + x
                    if self.__blocks[((y - 1) * self.__height + z) * self.__width + x] & 0xFF != tiles.grass.id:
                        continue

                    if n3 == 0:
                        self.__blocks[tile] = tiles.flower.id
                    elif n3 == 1:
                        self.__blocks[tile] = tiles.rose.id

    cdef __addMushrooms(self, int* heightmap):
        cdef int tile, n, size, n4, n5, n6, n7, x, y, z

        size = self.__width * self.__height * self.__depth // 2000
        for i in range(size):
            n4 = self.__random.nextInt(2)
            n5 = self.__random.nextInt(self.__width)
            n6 = self.__random.nextInt(self.__depth)
            n7 = self.__random.nextInt(self.__height)
            for j in range(20):
                x = n5
                y = n6
                z = n7
                for k in range(5):
                    x += self.__random.nextInt(6) - self.__random.nextInt(6)
                    y += self.__random.nextInt(2) - self.__random.nextInt(2)
                    z += self.__random.nextInt(6) - self.__random.nextInt(6)
                    if (n4 >= 2 and self.__random.nextInt(4) == 0) or x < 0 or z < 0 or y < 1 or x >= self.__width or z >= self.__height or y >= heightmap[x + z * self.__width] - 1:
                        continue

                    if self.__blocks[(y * self.__height + z) * self.__width + x] & 0xFF:
                        continue

                    tile = (y * self.__height + z) * self.__width + x
                    if self.__blocks[((y - 1) * self.__height + z) * self.__width + x] & 0xFF != tiles.rock.id:
                        continue

                    if n4 == 0:
                        self.__blocks[tile] = tiles.mushroomBrown.id
                    elif n4 == 1:
                        self.__blocks[tile] = tiles.mushroomRed.id

    cdef __addOre(self, int face, int i2, int i3, int i4):
        cdef int w, h, d, size, i8, i12, i17, i19, i20, i21, i26
        cdef float f9, f10, f11, f12, f13, f14, f15, f16, f18, f22, f23, f24

        w = self.__width
        h = self.__height
        d = self.__depth
        size = w * h * d // 256 // 64 * i2 // 100
        for i8 in range(size):
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
                f14 *= 0.9
                f14 = self.__random.randFloat() - self.__random.randFloat()
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
                               i19 >= 1 and i20 >= 1 and i21 >= 1 and i19 < w - 1 and \
                               i20 < d - 1 and i21 < h - 1:
                                i26 = (i20 * h + i21) * w + i19
                                if self.__blocks[i26] == tiles.rock.id:
                                    self.__blocks[i26] = face

    cdef __addLava(self):
        cdef int size, i, x, y, z

        size = self.__width * self.__height * self.__depth // 20000
        for i in range(size):
            x = self.__random.nextInt(self.__width)
            y = <int>(self.__random.randFloat() * self.__random.randFloat() * (self.__waterLevel - 3))
            z = self.__random.nextInt(self.__height)
            if self.__blocks[(y * self.__height + z) * self.__width + x] == 0:
                self.__floodFillWithLiquid(x, y, z, 0, tiles.calmLava.id)

    cdef long __floodFillWithLiquid(self, int x, int y, int z, int source, int tt):
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
                coordBuffer.pop(-1)
                self.__coords = <int*>malloc(len(coordBuffer) * sizeof(int))
                for i in range(len(coordBuffer)):
                    self.__coords[i] = coordBuffer[i]
                p = sizeof(self.__coords)

            z0 = cl >> wBits & hMask
            y0 = cl >> wBits + hBits

            x0 = cl & wMask
            x1 = x0

            while x0 > 0 and self.__blocks[cl - 1] == 0:
                x0 -= 1
                cl -= 1

            while x1 < self.__width and self.__blocks[cl + x1 - x0] == 0:
                x1 += 1

            z1 = cl >> wBits & hMask
            y1 = cl >> wBits + hBits
            if z1 != z0 or y1 != y0:
                print('Diagonal flood!?')

            lastNorth = False
            lastSouth = False
            lastBelow = False
            tileCount += x1 - x0

            while x0 < x1:
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
                x0 += 1

        return tileCount
