# cython: language_level=3

cimport cython

from libc.stdlib cimport malloc
from libc.math cimport sin, cos, pi

from mc.net.minecraft.level.NoiseMap import NoiseMap
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.cCompatibilityShims cimport Random

@cython.final
cdef class LevelGen:

    cdef:
        Random __random
        int __width
        int __height
        int __depth

    def __cinit__(self):
        self.__random = Random()

    def __init__(self, width, height, depth):
        self.__width = width
        self.__height = height
        self.__depth = depth

    cpdef generateMap(self):
        cdef int w, h, d, i, ix, iy, iz, dh1, dh2, cfh, dh, rh, id_, count, length, l
        cdef int xx, yy, zz, ii
        cdef float x, y, z, dir1, dira1, dir2, dira2, size, xd, yd, zd, dd

        w = self.__width
        h = self.__height
        d = self.__depth
        heightmap1 = NoiseMap(0).read(w, h)
        heightmap2 = NoiseMap(0).read(w, h)
        cf = NoiseMap(1).read(w, h)
        rockMap = NoiseMap(1).read(w, h)
        blocks = <char*>malloc(sizeof(char) * (w * h * d))
        for i in range(w * h * d):
            blocks[i] = 0

        for ix in range(w):
            for iy in range(d):
                for iz in range(h):
                    dh1 = heightmap1[ix + iz * w]
                    dh2 = heightmap2[ix + iz * w]
                    cfh = cf[ix + iz * w]

                    if cfh < 128:
                        dh2 = dh1

                    dh = dh1
                    if dh2 > dh:
                        dh = dh2
                    else:
                        dh2 = dh1

                    dh = dh // 8 + d // 3

                    rh = rockMap[ix + iz * w] // 8 + d // 3
                    if rh > dh - 2:
                        rh = dh - 2

                    i = (iy * h + iz) * w + ix
                    id_ = 0
                    if iy == dh:
                        id_ = tiles.grass.id
                    elif iy < dh:
                        id_ = tiles.dirt.id
                    if iy <= rh:
                        id_ = tiles.rock.id

                    blocks[i] = id_

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
                x += sin(dir1) * cos(dir2)
                z += cos(dir1) * cos(dir2)
                y += sin(dir2)

                dir1 += dira1 * 0.2
                dira1 *= 0.9
                dira1 += self.__random.randFloat() - self.__random.randFloat()

                dir2 += dira2 * 0.5
                dir2 *= 0.5
                dira2 *= 0.9
                dira2 += self.__random.randFloat() - self.__random.randFloat()

                size = sin(l * pi / length) * 2.5 + 1.0

                for xx in range(int(x - size), int(x + size) + 1):
                    for yy in range(int(y - size), int(y + size) + 1):
                        for zz in range(int(z - size), int(z + size) + 1):
                            xd = xx - x
                            yd = yy - y
                            zd = zz - z
                            dd = xd * xd + yd * yd * 2.0 + zd * zd
                            if dd < size * size and xx >= 1 and yy >= 1 and zz >= 1 and xx < w - 1 and yy < d - 1 and zz < h - 1:
                                ii = (yy * h + zz) * w + xx
                                if blocks[ii] == tiles.rock.id:
                                    blocks[ii] = 0

        b = bytearray(w * h * d)
        for i in range(len(b)):
            b[i] = blocks[i]

        return b
