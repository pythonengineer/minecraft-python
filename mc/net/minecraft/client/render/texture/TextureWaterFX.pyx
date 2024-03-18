# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

from libc.string cimport memcpy

from mc.net.minecraft.client.render.texture.TextureFX cimport TextureFX
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.CompatibilityShims cimport Random

cdef class TextureWaterFX(TextureFX):

    cdef:
        Random __random
        float __red[256]
        float __green[256]
        float __blue[256]
        float __alpha[256]
        int __tickCounter

    def __init__(self):
        TextureFX.__init__(self, blocks.waterMoving.blockIndexInTexture)
        self.__random = Random()
        for i in range(256):
            self.__red[i] = 0.0
            self.__green[i] = 0.0
            self.__blue[i] = 0.0
            self.__alpha[i] = 0.0

        self.__tickCounter = 0

    cpdef onTick(self):
        cdef int i1, i2, i4, i5, i6, r, g, b, a, nr
        cdef float f3, f8
        cdef float f7[256]

        self.__tickCounter += 1

        for i1 in range(16):
            for i2 in range(16):
                f3 = 0.0

                for i4 in range(i1 - 1, i1 + 2):
                    i5 = i4 & 15
                    i6 = i2 & 15
                    f3 += self.__red[i5 + (i6 << 4)]

                self.__green[i1 + (i2 << 4)] = f3 / 3.3 + self.__blue[i1 + (i2 << 4)] * 0.8

        for i1 in range(16):
            for i2 in range(16):
                self.__blue[i1 + (i2 << 4)] += self.__alpha[i1 + (i2 << 4)] * 0.05
                if self.__blue[i1 + (i2 << 4)] < 0.0:
                    self.__blue[i1 + (i2 << 4)] = 0.0

                self.__alpha[i1 + (i2 << 4)] -= 0.1
                if self.__random.randFloat() < 0.05:
                    self.__alpha[i1 + (i2 << 4)] = 0.5

        memcpy(f7, self.__green, sizeof(self.__green))
        self.__green = self.__red
        self.__red = f7

        for i2 in range(256):
            f3 = self.__red[i2]
            if f3 > 1.0:
                f3 = 1.0

            if f3 < 0.0:
                f3 = 0.0

            f8 = f3 * f3
            r = <int>(32.0 + f8 * 32.0)
            g = <int>(50.0 + f8 * 64.0)
            b = 255
            a = <int>(146.0 + f8 * 50.0)
            if self.anaglyphEnabled:
                nr = (r * 30 + g * 59 + 2805) // 100
                g = (r * 30 + g * 70) // 100
                b = (r * 30 + 17850) // 100
                r = nr

            self.imageData[i2 << 2] = <char>r
            self.imageData[(i2 << 2) + 1] = <char>g
            self.imageData[(i2 << 2) + 2] = <char>b
            self.imageData[(i2 << 2) + 3] = <char>a
