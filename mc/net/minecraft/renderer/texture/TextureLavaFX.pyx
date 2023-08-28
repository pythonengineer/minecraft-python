# cython: language_level=3

from libc.string cimport memcpy
from libc.math cimport sin, pi

from mc.net.minecraft.renderer.texture.TextureFX cimport TextureFX
from mc.net.minecraft.level.tile.Tiles import tiles
from mc.cCompatibilityShims cimport Random

cdef class TextureLavaFX(TextureFX):

    cdef:
        Random __random
        float __red[256]
        float __green[256]
        float __blue[256]
        float __alpha[256]

    def __init__(self):
        TextureFX.__init__(self, tiles.lava.tex)
        self.__random = Random()
        for i in range(256):
            self.__red[i] = 0.0
            self.__green[i] = 0.0
            self.__blue[i] = 0.0
            self.__alpha[i] = 0.0

    cpdef onTick(self):
        cdef int i1, i2, i4, i5, i6, i7, i8, i9
        cdef float f3
        cdef float f10[256]

        for i1 in range(16):
            for i2 in range(16):
                f3 = 0.0
                i4 = <int>(sin(i2 * pi * 2.0 / 16.0) * 1.2000000476837158)
                i5 = <int>(sin(i1 * pi * 2.0 / 16.0) * 1.2000000476837158)

                for i6 in range(i1 - 1, i1 + 2):
                    for i7 in range(i2 - 1, i2 + 2):
                        i8 = i6 + i4 & 15
                        i9 = i7 + i5 & 15
                        f3 += self.__red[i8 + (i9 << 4)]

                self.__green[i1 + (i2 << 4)] = f3 / 10.0 + (self.__blue[(i1 & 15) + \
                                                            ((i2 & 15) << 4)] + \
                                                            self.__blue[(i1 + 1 & 15) + ((i2 & 15) << 4)] + \
                                                            self.__blue[(i1 + 1 & 15) + ((i2 + 1 & 15) << 4)] + \
                                                            self.__blue[(i1 & 15) + ((i2 + 1 & 15) << 4)]) / 4.0 * 0.8
                self.__blue[i1 + (i2 << 4)] += self.__alpha[i1 + (i2 << 4)] * 0.01
                if self.__blue[i1 + (i2 << 4)] < 0.0:
                    self.__blue[i1 + (i2 << 4)] = 0.0

                self.__alpha[i1 + (i2 << 4)] -= 0.06
                if self.__random.randFloat() < 0.005:
                    self.__alpha[i1 + (i2 << 4)] = 1.5

        memcpy(f10, self.__green, sizeof(self.__green))
        self.__green = self.__red
        self.__red = f10

        for i2 in range(256):
            f3 = self.__red[i2] * 2.0
            if f3 > 1.0:
                f3 = 1.0

            if f3 < 0.0:
                f3 = 0.0

            i5 = <int>(f3 * 100.0 + 155.0)
            i6 = <int>(f3 * f3 * 255.0)
            i7 = <int>(f3 * f3 * f3 * f3 * 128.0)
            self.imageData[i2 << 2] = <char>i5
            self.imageData[(i2 << 2) + 1] = <char>i6
            self.imageData[(i2 << 2) + 2] = <char>i7
            self.imageData[(i2 << 2) + 3] = -1
