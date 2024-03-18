# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport sin, cos, pi

from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorDistort cimport NoiseGeneratorDistort
from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorOctaves cimport NoiseGeneratorOctaves
from mc.CompatibilityShims cimport Random

@cython.final
cdef class LevelGenerator:

    cdef:
        Random rand
        public object progressBar
        int floodFillBlocks[0x100000]
        public int width
        public int depth
        public int height
        public int waterLevel
        char* blocksByteArray

    def __cinit__(self):
        self.rand = Random()

    def __init__(self, desc):
        self.progressBar = desc

    def generateLevel(self, str userName, int width, int depth, int height):
        cdef int *heightmap
        cdef int i, i13, i34, i5, i15, i41, w, h, d, ix, iy, iz, i42, i16, i46, \
                 blockId, stone, count, length, l, xx, yy, zz, ii, target, i37
        cdef float f6, x, y, z, dir1, dira1, dir2, dira2, dir3, size, xd, yd, zd
        cdef double d14, d16, d21, start, end, d36
        cdef NoiseGeneratorDistort distort8, distort9, distort32
        cdef NoiseGeneratorOctaves perlinNoise
        cdef World world

        self.progressBar.beginLevelLoading('Generating level')

        self.width = width
        self.depth = depth
        self.height = 64
        self.waterLevel = 32
        self.blocksByteArray = <char*>malloc(sizeof(char) * (self.width * self.depth << 6))

        self.progressBar.displayProgressMessage('Raising..')

        distort8 = NoiseGeneratorDistort(NoiseGeneratorOctaves(self.rand, 8),
                                         NoiseGeneratorOctaves(self.rand, 8))
        distort9 = NoiseGeneratorDistort(NoiseGeneratorOctaves(self.rand, 8),
                                         NoiseGeneratorOctaves(self.rand, 8))
        perlinNoise = NoiseGeneratorOctaves(self.rand, 6)
        heightmap = <int*>malloc(sizeof(int) * (self.width * self.depth))
        f6 = 1.3

        for i in range(self.width):
            for i13 in range(self.depth):
                d14 = distort8.generateNoise(i * f6, i13 * f6) / 6.0 - 4.0
                d16 = distort9.generateNoise(i * f6, i13 * f6) / 5.0 + 6.0
                if perlinNoise.generateNoise(i, i13) / 8.0 > 0.0:
                    d16 = d14

                d21 = max(d14, d16) / 2.0
                if d21 < 0.0:
                    d21 *= 0.8

                heightmap[i + i13 * self.width] = <int>d21

        self.progressBar.displayProgressMessage('Eroding..')

        distort9 = NoiseGeneratorDistort(NoiseGeneratorOctaves(self.rand, 8),
                                         NoiseGeneratorOctaves(self.rand, 8))
        distort32 = NoiseGeneratorDistort(NoiseGeneratorOctaves(self.rand, 8),
                                          NoiseGeneratorOctaves(self.rand, 8))
        for i34 in range(self.width):
            for i5 in range(self.depth):
                d36 = distort9.generateNoise(i34 << 1, i5 << 1) / 8.0
                i15 = 1 if distort32.generateNoise(i34 << 1, i5 << 1) > 0.0 else 0
                if d36 > 2.0:
                    i41 = ((heightmap[i34 + i5 * self.width] - i15) // 4) + i15
                    heightmap[i34 + i5 * self.width] = i41

        self.progressBar.displayProgressMessage('Soiling..')

        w = self.width
        d = self.depth
        h = self.height
        perlinNoise = NoiseGeneratorOctaves(self.rand, 8)
        for ix in range(w):
            for iy in range(d):
                i42 = <int>(perlinNoise.generateNoise(ix, iy) / 24.0) - 4
                i16 = heightmap[ix + iy * w] + self.waterLevel
                i46 = i16 + i42
                heightmap[ix + iy * w] = max(i16, i46)
                if heightmap[ix + iy * w] > h - 2:
                    heightmap[ix + iy * w] = h - 2
                if heightmap[ix + iy * w] < 1:
                    heightmap[ix + iy * w] = 1

                for iz in range(h):
                    i = (iz * d + iy) * w + ix
                    blockId = 0
                    if iz <= i16:
                        blockId = blocks.dirt.blockID
                    if iz <= i46:
                        blockId = blocks.stone.blockID
                    if iz == 0:
                        blockId = blocks.lavaMoving.blockID

                    self.blocksByteArray[i] = blockId

        self.progressBar.displayProgressMessage('Carving..')

        count = w * h * d // 256 // 64 << 1
        stone = <int>blocks.stone.blockID
        for i in range(count):
            x = self.rand.randFloatM(w)
            y = self.rand.randFloatM(h)
            z = self.rand.randFloatM(d)
            length = <int>(self.rand.randFloat() + self.rand.randFloatM(200.0))
            dir1 = self.rand.randFloat() * pi * 2.0
            dira1 = 0.0
            dir2 = self.rand.randFloat() * pi * 2.0
            dira2 = 0.0
            dir3 = self.rand.randFloat() * self.rand.randFloat()

            for l in range(length):
                x = x + sin(dir1) * cos(dir2)
                z = z + cos(dir1) * cos(dir2)
                y = y + sin(dir2)

                dir1 += dira1 * 0.2
                dira1 *= 0.9
                dira1 += self.rand.randFloat() - self.rand.randFloat()

                dir2 += dira2 * 0.5
                dir2 *= 0.5
                dira2 *= 0.75
                dira2 += self.rand.randFloat() - self.rand.randFloat()

                if self.rand.randFloat() >= 0.25:
                    x += (self.rand.randFloat() * 4.0 - 2.0) * 0.2
                    y += (self.rand.randFloat() * 4.0 - 2.0) * 0.2
                    z += (self.rand.randFloat() * 4.0 - 2.0) * 0.2
                    size = (h - y) / h
                    size = 1.2 + (size * 3.5 + 1.0) * dir3
                    size = sin(l * pi / length) * size
                    for xx in range(<int>(x - size), <int>(x + size) + 1):
                        for yy in range(<int>(y - size), <int>(y + size) + 1):
                            for zz in range(<int>(z - size), <int>(z + size) + 1):
                                xd = xx - x
                                yd = yy - y
                                zd = zz - z
                                dd = xd * xd + yd * yd * 2.0 + zd * zd
                                if dd < size * size and xx >= 1 and yy >= 1 and zz >= 1 and xx < w - 1 and yy < h - 1 and zz < d - 1:
                                    ii = (yy * d + zz) * w + xx
                                    if self.blocksByteArray[ii] == stone:
                                        self.blocksByteArray[ii] = 0

        self.populateOre(blocks.oreCoal.blockID, 90, 1, 4)
        self.populateOre(blocks.oreIron.blockID, 70, 2, 4)
        self.populateOre(blocks.oreGold.blockID, 50, 3, 4)
        self.progressBar.displayProgressMessage('Watering..')

        target = blocks.waterStill.blockID

        for ix in range(self.width):
            self.floodFill(ix, self.height // 2 - 1, 0, 0, target)
            self.floodFill(ix, self.height // 2 - 1, self.depth - 1, 0, target)

        for iy in range(self.depth):
            self.floodFill(0, self.height // 2 - 1, iy, 0, target)
            self.floodFill(self.width - 1, self.height // 2 - 1, iy, 0, target)

        i37 = self.width * self.depth // 8000
        for i in range(i37):
            ix = self.rand.nextInt(self.width)
            iy = self.waterLevel - 1 - self.rand.nextInt(2)
            iz = self.rand.nextInt(self.depth)
            if self.blocksByteArray[(iy * self.depth + iz) * self.width + ix] == 0:
                self.floodFill(ix, iy, iz, 0, target)

        self.progressBar.displayProgressMessage('Melting..')
        self.__addLava()
        self.progressBar.displayProgressMessage('Growing..')
        self.__addBeaches(heightmap)
        self.progressBar.displayProgressMessage('Planting..')
        self.__addBlockFlowers(heightmap)
        self.__addMushrooms(heightmap)

        b = bytearray(self.width * self.depth << 6)
        for i in range(len(b)):
            b[i] = self.blocksByteArray[i]

        world = World()
        world.waterLevel = self.waterLevel
        world.generate(width, 64, depth, b)

        self.__generateTrees(world, heightmap)

        free(self.blocksByteArray)

        return world

    cdef __addBeaches(self, int* heightmap):
        cdef int w, h, d, x, y, heightmap1, heightmap2, i13
        cdef bint z9, z10
        cdef char heightmap3
        cdef NoiseGeneratorOctaves perlinNoise1, perlinNoise2

        w = self.width
        d = self.depth
        h = self.height
        perlinNoise1 = NoiseGeneratorOctaves(self.rand, 8)
        perlinNoise2 = NoiseGeneratorOctaves(self.rand, 8)

        for x in range(w):
            for y in range(d):
                z9 = perlinNoise1.generateNoise(x, y) > 8.0
                z10 = perlinNoise2.generateNoise(x, y) > 12.0
                heightmap1 = heightmap[x + y * w]
                heightmap2 = (heightmap1 * d + y) * w + x
                i13 = self.blocksByteArray[((heightmap1 + 1) * d + y) * w + x] & 255
                if (i13 == blocks.waterMoving.blockID or i13 == blocks.waterStill.blockID) and \
                   heightmap1 <= h // 2 - 1 and z10:
                    self.blocksByteArray[heightmap2] = blocks.gravel.blockID

                if i13 == 0:
                    heightmap3 = blocks.grass.blockID
                    if heightmap1 <= h // 2 - 1 and z9:
                        heightmap3 = blocks.sand.blockID

                    self.blocksByteArray[heightmap2] = heightmap3

    cdef __generateTrees(self, World world, int* heightmap):
        cdef int w, size, i4, x, y, z, i7, i8, i9, i10

        w = self.width
        size = w * self.depth // 4000
        for i4 in range(size):
            i8 = self.rand.nextInt(w)
            i9 = self.rand.nextInt(self.depth)
            for i7 in range(20):
                x = i8
                z = i9
                for i10 in range(20):
                    x += self.rand.nextInt(6) - self.rand.nextInt(6)
                    z += self.rand.nextInt(6) - self.rand.nextInt(6)
                    if x >= 0 and z >= 0 and x < w and z < self.depth:
                        y = heightmap[x + z * w] + 1
                        if self.rand.nextInt(4) == 0:
                            world.growTrees(x, y, z)

    cdef __addBlockFlowers(self, int* heightmap):
        cdef int i, j, k, n2, n3, n4, n5, x, y, z, block

        n2 = self.width * self.depth // 3000
        for i in range(n2):
            n3 = self.rand.nextInt(2)
            n4 = self.rand.nextInt(self.width)
            n5 = self.rand.nextInt(self.depth)
            for j in range(10):
                x = n4
                z = n5
                for k in range(5):
                    x += self.rand.nextInt(6) - self.rand.nextInt(6)
                    z += self.rand.nextInt(6) - self.rand.nextInt(6)
                    if (n3 >= 2 and self.rand.nextInt(4) != 0) or x < 0 or z < 0 or x >= self.width or z >= self.depth:
                        continue

                    y = heightmap[x + z * self.width] + 1
                    if self.blocksByteArray[(y * self.depth + z) * self.width + x] & 0xFF:
                        continue

                    block = (y * self.depth + z) * self.width + x
                    if self.blocksByteArray[((y - 1) * self.depth + z) * self.width + x] & 0xFF != blocks.grass.blockID:
                        continue

                    if n3 == 0:
                        self.blocksByteArray[block] = blocks.plantYellow.blockID
                    elif n3 == 1:
                        self.blocksByteArray[block] = blocks.plantRed.blockID

    cdef __addMushrooms(self, int* heightmap):
        cdef int block, n, size, n4, n5, n6, n7, x, y, z

        size = self.width * self.depth * self.height // 2000
        for i in range(size):
            n4 = self.rand.nextInt(2)
            n5 = self.rand.nextInt(self.width)
            n6 = self.rand.nextInt(self.height)
            n7 = self.rand.nextInt(self.depth)
            for j in range(20):
                x = n5
                y = n6
                z = n7
                for k in range(5):
                    x += self.rand.nextInt(6) - self.rand.nextInt(6)
                    y += self.rand.nextInt(2) - self.rand.nextInt(2)
                    z += self.rand.nextInt(6) - self.rand.nextInt(6)
                    if (n4 >= 2 and self.rand.nextInt(4) == 0) or \
                       x < 0 or z < 0 or y < 1 or x >= self.width or \
                       z >= self.depth or y >= heightmap[x + z * self.width] - 1:
                        continue

                    if self.blocksByteArray[(y * self.depth + z) * self.width + x] & 0xFF:
                        continue

                    block = (y * self.depth + z) * self.width + x
                    if self.blocksByteArray[((y - 1) * self.depth + z) * self.width + x] & 0xFF != blocks.stone.blockID:
                        continue

                    if n4 == 0:
                        self.blocksByteArray[block] = blocks.mushroomBrown.blockID
                    elif n4 == 1:
                        self.blocksByteArray[block] = blocks.mushroomRed.blockID

    cdef populateOre(self, int face, int freq, int _, int __):
        cdef int w, d, h, size, i8, i12, i17, x, y, z, block
        cdef float f9, f10, f11, f12, f13, f14, f15, f16, f18, f22, f23, f24

        w = self.width
        d = self.depth
        h = self.height
        size = w * d * h // 256 // 64 * freq // 100
        for i8 in range(size):
            f9 = self.rand.randFloatM(w)
            f10 = self.rand.randFloatM(h)
            f11 = self.rand.randFloatM(d)
            i12 = <int>((self.rand.randFloat() + self.rand.randFloat()) * 75.0 * freq / 100.0)
            f13 = self.rand.randFloat() * pi * 2.0
            f14 = 0.0
            f15 = self.rand.randFloat() * pi * 2.0
            f16 = 0.0

            for i17 in range(i12):
                f9 = f9 + sin(f13) * cos(f15)
                f11 = f11 + cos(f13) * cos(f15)
                f10 = f10 + sin(f15)
                f13 += f14 * 0.2
                f14 *= 0.9
                f14 = self.rand.randFloat() - self.rand.randFloat()
                f15 = (f15 + f16 * 0.5) * 0.5
                f16 = (f16 * 0.9) + (self.rand.randFloat() - self.rand.randFloat())
                f18 = sin(i17 * pi / i12) * freq / 100.0 + 1.0

                for x in range(<int>(f9 - f18), <int>(f9 + f18 + 1)):
                    for y in range(<int>(f10 - f18), <int>(f10 + f18 + 1)):
                        for z in range(<int>(f11 - f18), <int>(f11 + f18 + 1)):
                            f22 = x - f9
                            f23 = y - f10
                            f24 = z - f11
                            if f22 * f22 + f23 * f23 * 2.0 + f24 * f24 < f18 * f18 and \
                               x >= 1 and y >= 1 and z >= 1 and x < w - 1 and \
                               y < h - 1 and z < d - 1:
                                block = (y * d + z) * w + x
                                if self.blocksByteArray[block] == blocks.stone.blockID:
                                    self.blocksByteArray[block] = face

    cdef __addLava(self):
        cdef int size, i, x, y, z

        size = self.width * self.depth * self.height // 20000
        for i in range(size):
            x = self.rand.nextInt(self.width)
            y = <int>(self.rand.randFloat() * self.rand.randFloat() * (self.waterLevel - 3))
            z = self.rand.nextInt(self.depth)
            if self.blocksByteArray[(y * self.depth + z) * self.width + x] == 0:
                self.floodFill(x, y, z, 0, blocks.lavaStill.blockID)

    cdef long floodFill(self, int x, int y, int z, int source, int tt):
        cdef int target, p, wBits, hBits, hMask, wMask, upStep, cl, i, z0, y0, x0, x1
        cdef int z1, y1
        cdef bint lastNorth, lastSouth, lastBelow, north, south, below
        cdef long blockCount
        cdef char belowId

        target = tt
        coordBuffer = []
        p = 0

        wBits = 1
        hBits = 1
        while 1 << wBits < self.width:
            wBits += 1
        while 1 << hBits < self.depth:
            hBits += 1
        hMask = self.depth - 1
        wMask = self.width - 1
        self.floodFillBlocks[p] = ((y << hBits) + z << wBits) + x
        p += 1
        blockCount = 0
        upStep = self.width * self.depth
        while p > 0:
            p -= 1
            cl = self.floodFillBlocks[p]
            if p == 0 and len(coordBuffer) > 0:
                coordBuffer.pop(-1)
                self.floodFillBlocks = <int*>malloc(len(coordBuffer) * sizeof(int))
                for i in range(len(coordBuffer)):
                    self.floodFillBlocks[i] = coordBuffer[i]
                p = sizeof(self.floodFillBlocks)

            z0 = cl >> wBits & hMask
            y0 = cl >> wBits + hBits

            x0 = cl & wMask
            x1 = x0

            while x0 > 0 and self.blocksByteArray[cl - 1] == 0:
                x0 -= 1
                cl -= 1

            while x1 < self.width and self.blocksByteArray[cl + x1 - x0] == 0:
                x1 += 1

            z1 = cl >> wBits & hMask
            y1 = cl >> wBits + hBits
            if z1 != z0 or y1 != y0:
                print('Diagonal flood!?')

            lastNorth = False
            lastSouth = False
            lastBelow = False
            blockCount += x1 - x0

            while x0 < x1:
                self.blocksByteArray[cl] = target
                if z0 > 0:
                    north = self.blocksByteArray[cl - self.width] == source
                    if north and not lastNorth:
                        if p == sizeof(self.floodFillBlocks):
                            coordBuffer.append(self.floodFillBlocks)
                            self.floodFillBlocks = <int*>malloc(0x100000 * sizeof(int))
                            p = 0

                        self.floodFillBlocks[p] = cl - self.width
                        p += 1

                    lastNorth = north

                if z0 < self.depth - 1:
                    south = self.blocksByteArray[cl + self.width] == source
                    if south and not lastSouth:
                        if p == sizeof(self.floodFillBlocks):
                            coordBuffer.append(self.floodFillBlocks)
                            self.floodFillBlocks = <int*>malloc(0x100000 * sizeof(int))
                            p = 0

                        self.floodFillBlocks[p] = cl + self.width
                        p += 1

                    lastSouth = south

                if y0 > 0:
                    belowId = self.blocksByteArray[cl - upStep]
                    if target == blocks.lavaMoving.blockID or target == blocks.lavaStill.blockID:
                        if belowId == blocks.waterMoving.blockID or belowId == blocks.waterStill.blockID:
                            self.blocksByteArray[cl - upStep] = blocks.stone.blockID

                    below = belowId == source
                    if below and not lastBelow:
                        if p == sizeof(self.floodFillBlocks):
                            coordBuffer.append(self.floodFillBlocks)
                            self.floodFillBlocks = <int*>malloc(0x100000 * sizeof(int))
                            p = 0

                        self.floodFillBlocks[p] = cl - upStep
                        p += 1

                    lastBelow = below

                cl += 1
                x0 += 1

        return blockCount
