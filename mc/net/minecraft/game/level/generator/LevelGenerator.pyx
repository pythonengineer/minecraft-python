# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

cimport cython

from libc.stdlib cimport malloc, free
from libc.math cimport sin, cos, pi

from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorCombined cimport NoiseGeneratorCombined
from mc.net.minecraft.game.level.generator.noise.NoiseGeneratorOctaves cimport NoiseGeneratorOctaves
from mc.CompatibilityShims cimport Random

@cython.final
cdef class LevelGenerator:

    cdef:
        Random __rand
        object __loadingScreen
        int __coords[1048576]
        int __width
        int __depth
        int __height
        int __waterLevel
        char* __blocks

    def __cinit__(self):
        self.__rand = Random()

    def __init__(self, loadingScreen):
        self.__loadingScreen = loadingScreen

    def generate(self, str userName, int width, int depth, int height):
        cdef int *heightmap
        cdef int i, w, h, d, ix, iy, iz, dirtLevel, stoneLevel, blockId, stone, \
                 count, length, l, xx, yy, zz, target, toFlood
        cdef bint hasNoise
        cdef float x, y, z, dir1, dira1, dir2, dira2, dir3, size, xd, yd, zd
        cdef double h1, h2, highest, start, end, noise
        cdef NoiseGeneratorCombined combined1, combined2, combined32
        cdef NoiseGeneratorOctaves perlinNoise
        cdef World world

        self.__loadingScreen.displayProgressMessage('Generating level')

        self.__width = width
        self.__depth = depth
        self.__height = 64
        self.__waterLevel = 32
        self.__blocks = <char*>malloc(sizeof(char) * (self.__width * self.__depth << 6))

        self.__loadingScreen.displayLoadingString('Raising..')

        combined1 = NoiseGeneratorCombined(NoiseGeneratorOctaves(self.__rand, 8),
                                           NoiseGeneratorOctaves(self.__rand, 8))
        combined2 = NoiseGeneratorCombined(NoiseGeneratorOctaves(self.__rand, 8),
                                           NoiseGeneratorOctaves(self.__rand, 8))
        perlinNoise = NoiseGeneratorOctaves(self.__rand, 6)
        heightmap = <int*>malloc(sizeof(int) * (self.__width * self.__depth))

        for w in range(self.__width):
            for d in range(self.__depth):
                h1 = combined1.generateNoise(w * 1.3, d * 1.3) / 6.0 + -4.0
                h2 = combined2.generateNoise(w * 1.3, d * 1.3) / 5.0 + 10.0 + -4.0
                if perlinNoise.generateNoise(w, d) / 8.0 > 0.0:
                    h2 = h1

                highest = max(h1, h2) / 2.0
                if highest < 0.0:
                    highest *= 0.8

                heightmap[w + d * self.__width] = <int>highest

        self.__loadingScreen.displayLoadingString('Eroding..')

        combined1 = NoiseGeneratorCombined(NoiseGeneratorOctaves(self.__rand, 8),
                                           NoiseGeneratorOctaves(self.__rand, 8))
        combined2 = NoiseGeneratorCombined(NoiseGeneratorOctaves(self.__rand, 8),
                                           NoiseGeneratorOctaves(self.__rand, 8))
        for w in range(self.__width):
            for d in range(self.__depth):
                noise = combined1.generateNoise(w << 1, d << 1) / 8.0
                hasNoise = 1 if combined2.generateNoise(w << 1, d << 1) > 0.0 else 0
                if noise > 2.0:
                    h = ((heightmap[w + d * self.__width] - hasNoise) // 2 << 1) + hasNoise
                    heightmap[w + d * self.__width] = h

        self.__loadingScreen.displayLoadingString('Soiling..')

        w = self.__width
        d = self.__depth
        h = self.__height
        perlinNoise = NoiseGeneratorOctaves(self.__rand, 8)
        for ix in range(w):
            for iy in range(d):
                dirtLevel = heightmap[ix + iy * w] + self.__waterLevel
                stoneLevel = dirtLevel + <int>(perlinNoise.generateNoise(ix, iy) / 24.0) - 4
                heightmap[ix + iy * w] = max(dirtLevel, stoneLevel)
                if heightmap[ix + iy * w] > h - 2:
                    heightmap[ix + iy * w] = h - 2
                if heightmap[ix + iy * w] < 1:
                    heightmap[ix + iy * w] = 1

                for iz in range(h):
                    i = (iz * d + iy) * w + ix
                    blockId = 0
                    if iz <= dirtLevel:
                        blockId = blocks.dirt.blockID
                    if iz <= stoneLevel:
                        blockId = blocks.stone.blockID
                    if iz == 0:
                        blockId = blocks.lavaMoving.blockID

                    self.__blocks[i] = blockId

        self.__loadingScreen.displayLoadingString('Carving..')

        count = w * h * d // 256 // 64 << 1
        stone = <int>blocks.stone.blockID
        for i in range(count):
            x = self.__rand.randFloatM(w)
            y = self.__rand.randFloatM(h)
            z = self.__rand.randFloatM(d)
            length = <int>(self.__rand.randFloat() + self.__rand.randFloatM(200.0))
            dir1 = self.__rand.randFloat() * pi * 2.0
            dira1 = 0.0
            dir2 = self.__rand.randFloat() * pi * 2.0
            dira2 = 0.0
            dir3 = self.__rand.randFloat() * self.__rand.randFloat()

            for l in range(length):
                x = x + sin(dir1) * cos(dir2)
                z = z + cos(dir1) * cos(dir2)
                y = y + sin(dir2)

                dir1 += dira1 * 0.2
                dira1 *= 0.9
                dira1 += self.__rand.randFloat() - self.__rand.randFloat()

                dir2 += dira2 * 0.5
                dir2 *= 0.5
                dira2 *= 12.0 / 16.0
                dira2 += self.__rand.randFloat() - self.__rand.randFloat()

                if self.__rand.randFloat() >= 0.25:
                    x += (self.__rand.randFloat() * 4.0 - 2.0) * 0.2
                    y += (self.__rand.randFloat() * 4.0 - 2.0) * 0.2
                    z += (self.__rand.randFloat() * 4.0 - 2.0) * 0.2
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
                                    blockId = (yy * d + zz) * w + xx
                                    if self.__blocks[blockId] == stone:
                                        self.__blocks[blockId] = 0

        self.__populateOres(blocks.oreCoal.blockID, 90, 1, 4)
        self.__populateOres(blocks.oreIron.blockID, 70, 2, 4)
        self.__populateOres(blocks.oreGold.blockID, 50, 3, 4)
        self.__loadingScreen.displayLoadingString('Watering..')

        target = blocks.waterStill.blockID
        for ix in range(self.__width):
            self.__floodFill(ix, self.__height // 2 - 1, 0, 0, target)
            self.__floodFill(ix, self.__height // 2 - 1, self.__depth - 1, 0, target)

        for iy in range(self.__depth):
            self.__floodFill(0, self.__height // 2 - 1, iy, 0, target)
            self.__floodFill(self.__width - 1, self.__height // 2 - 1, iy, 0, target)

        toFlood = self.__width * self.__depth // 8000
        for i in range(toFlood):
            ix = self.__rand.nextInt(self.__width)
            iy = self.__waterLevel - 1 - self.__rand.nextInt(2)
            iz = self.__rand.nextInt(self.__depth)
            if self.__blocks[(iy * self.__depth + iz) * self.__width + ix] == 0:
                self.__floodFill(ix, iy, iz, 0, target)

        self.__loadingScreen.displayLoadingString('Melting..')
        self.__addLava()
        self.__loadingScreen.displayLoadingString('Growing..')
        self.__addBeaches(heightmap)
        self.__loadingScreen.displayLoadingString('Planting..')
        self.__addFlowers(heightmap)
        self.__addMushrooms(heightmap)

        b = bytearray(self.__width * self.__depth << 6)
        for i in range(len(b)):
            b[i] = self.__blocks[i]

        world = World()
        world.waterLevel = self.__waterLevel
        world.setLevel(width, 64, depth, b)

        self.__generateTrees(world, heightmap)

        free(self.__blocks)

        return world

    cdef __addBeaches(self, int* heightmap):
        cdef int w, h, d, x, y, heightmap1, heightmap2, blockId
        cdef bint isSand, isGravel
        cdef char block
        cdef NoiseGeneratorOctaves perlinNoise1, perlinNoise2

        w = self.__width
        d = self.__depth
        h = self.__height
        perlinNoise1 = NoiseGeneratorOctaves(self.__rand, 8)
        perlinNoise2 = NoiseGeneratorOctaves(self.__rand, 8)

        for x in range(w):
            for y in range(d):
                isSand = perlinNoise1.generateNoise(x, y) > 8.0
                isGravel = perlinNoise2.generateNoise(x, y) > 12.0
                heightmap1 = heightmap[x + y * w]
                heightmap2 = (heightmap1 * d + y) * w + x
                blockId = self.__blocks[((heightmap1 + 1) * d + y) * w + x] & 0xFF
                if (blockId == blocks.waterMoving.blockID or blockId == blocks.waterStill.blockID) and \
                   heightmap1 <= h // 2 - 1 and isGravel:
                    self.__blocks[heightmap2] = blocks.gravel.blockID

                if blockId == 0:
                    block = blocks.grass.blockID
                    if heightmap1 <= h // 2 - 1 and isSand:
                        block = blocks.sand.blockID

                    self.__blocks[heightmap2] = block

    cdef __generateTrees(self, World world, int* heightmap):
        cdef int w, size, xx, x, y, z, yy, width, depth, zz

        w = self.__width
        size = w * self.__depth // 4000
        for xx in range(size):
            width = self.__rand.nextInt(w)
            depth = self.__rand.nextInt(self.__depth)
            for yy in range(20):
                x = width
                z = depth
                for zz in range(20):
                    x += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    z += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    if x >= 0 and z >= 0 and x < w and z < self.__depth:
                        y = heightmap[x + z * w] + 1
                        if self.__rand.nextInt(4) == 0:
                            world.growTrees(x, y, z)

    cdef __addFlowers(self, int* heightmap):
        cdef int i, j, k, size, kind, w, d, x, y, z, block

        size = self.__width * self.__depth // 3000
        for i in range(size):
            kind = self.__rand.nextInt(2)
            w = self.__rand.nextInt(self.__width)
            d = self.__rand.nextInt(self.__depth)
            for j in range(10):
                x = w
                z = d
                for k in range(5):
                    x += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    z += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    if (kind >= 2 and self.__rand.nextInt(4) != 0) or x < 0 or z < 0 or x >= self.__width or z >= self.__depth:
                        continue

                    y = heightmap[x + z * self.__width] + 1
                    if self.__blocks[(y * self.__depth + z) * self.__width + x] & 0xFF:
                        continue

                    block = (y * self.__depth + z) * self.__width + x
                    if self.__blocks[((y - 1) * self.__depth + z) * self.__width + x] & 0xFF != blocks.grass.blockID:
                        continue

                    if kind == 0:
                        self.__blocks[block] = blocks.plantYellow.blockID
                    elif kind == 1:
                        self.__blocks[block] = blocks.plantRed.blockID

    cdef __addMushrooms(self, int* heightmap):
        cdef int block, size, kind, w, h, d, x, y, z

        size = self.__width * self.__depth * self.__height // 2000
        for i in range(size):
            kind = self.__rand.nextInt(2)
            w = self.__rand.nextInt(self.__width)
            h = self.__rand.nextInt(self.__height)
            d = self.__rand.nextInt(self.__depth)
            for j in range(20):
                x = w
                y = h
                z = d
                for k in range(5):
                    x += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    y += self.__rand.nextInt(2) - self.__rand.nextInt(2)
                    z += self.__rand.nextInt(6) - self.__rand.nextInt(6)
                    if (kind >= 2 and self.__rand.nextInt(4) != 0) or \
                       x < 0 or z < 0 or y < 1 or x >= self.__width or \
                       z >= self.__depth or y >= heightmap[x + z * self.__width] - 1:
                        continue

                    if self.__blocks[(y * self.__depth + z) * self.__width + x] & 0xFF:
                        continue

                    block = (y * self.__depth + z) * self.__width + x
                    if self.__blocks[((y - 1) * self.__depth + z) * self.__width + x] & 0xFF != blocks.stone.blockID:
                        continue

                    if kind == 0:
                        self.__blocks[block] = blocks.mushroomBrown.blockID
                    elif kind == 1:
                        self.__blocks[block] = blocks.mushroomRed.blockID

    cdef __populateOres(self, int face, int freq, int _, int __):
        cdef int w, d, h, size, i, steps, step, x, y, z, block
        cdef float x0, y0, z0, xChange, xDecay, yChange, yDecay, pop, xd, yd, zd

        w = self.__width
        d = self.__depth
        h = self.__height
        size = w * d * h // 256 // 64 * freq // 100
        for i in range(size):
            x0 = self.__rand.randFloatM(w)
            y0 = self.__rand.randFloatM(h)
            z0 = self.__rand.randFloatM(d)
            steps = <int>((self.__rand.randFloat() + self.__rand.randFloat()) * 75.0 * freq / 100.0)
            xChange = self.__rand.randFloat() * pi * 2.0
            xDecay = 0.0
            yChange = self.__rand.randFloat() * pi * 2.0
            yDecay = 0.0

            for step in range(steps):
                x0 += sin(xChange) * cos(yChange)
                z0 += cos(xChange) * cos(yChange)
                y0 += sin(yChange)
                xChange += xDecay * 0.2
                xDecay *= 0.9
                xDecay = self.__rand.randFloat() - self.__rand.randFloat()
                yChange = (yChange + yDecay * 0.5) * 0.5
                yDecay = (yDecay * 0.9) + (self.__rand.randFloat() - self.__rand.randFloat())
                pop = sin(step * pi / steps) * freq / 100.0 + 1.0

                for x in range(<int>(x0 - pop), <int>(x0 + pop + 1)):
                    for y in range(<int>(y0 - pop), <int>(y0 + pop + 1)):
                        for z in range(<int>(z0 - pop), <int>(z0 + pop + 1)):
                            xd = x - x0
                            yd = y - y0
                            zd = z - z0
                            if xd * xd + yd * yd * 2.0 + zd * zd < pop * pop and \
                               x >= 1 and y >= 1 and z >= 1 and x < w - 1 and \
                               y < h - 1 and z < d - 1:
                                block = (y * d + z) * w + x
                                if self.__blocks[block] == blocks.stone.blockID:
                                    self.__blocks[block] = face

    cdef __addLava(self):
        cdef int size, i, x, y, z

        size = self.__width * self.__depth * self.__height // 20000
        for i in range(size):
            x = self.__rand.nextInt(self.__width)
            y = <int>(self.__rand.randFloat() * self.__rand.randFloat() * (self.__waterLevel - 3))
            z = self.__rand.nextInt(self.__depth)
            if self.__blocks[(y * self.__depth + z) * self.__width + x] == 0:
                self.__floodFill(x, y, z, 0, blocks.lavaStill.blockID)

    cdef long __floodFill(self, int x, int y, int z, int source, int tt):
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
        while 1 << wBits < self.__width:
            wBits += 1
        while 1 << hBits < self.__depth:
            hBits += 1
        hMask = self.__depth - 1
        wMask = self.__width - 1
        self.__coords[p] = ((y << hBits) + z << wBits) + x
        p += 1
        blockCount = 0
        upStep = self.__width * self.__depth
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
            blockCount += x1 - x0

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

                if z0 < self.__depth - 1:
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
                    if target == blocks.lavaMoving.blockID or target == blocks.lavaStill.blockID:
                        if belowId == blocks.waterMoving.blockID or belowId == blocks.waterStill.blockID:
                            self.__blocks[cl - upStep] = blocks.stone.blockID

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

        return blockCount
