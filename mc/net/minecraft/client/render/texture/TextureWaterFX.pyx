# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

from libc.string cimport memcpy

from mc.net.minecraft.client.render.texture.TextureFX cimport TextureFX
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils cimport Random

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
        cdef int x, z, y, pixel, r, g, b, a, nr
        cdef float value
        cdef float red[256]

        self.__tickCounter += 1

        for x in range(16):
            for z in range(16):
                value = 0.0
                for y in range(x - 1, x + 2):
                    value += self.__red[(y & 15) + ((z & 15) << 4)]

                self.__green[x + (z << 4)] = value / 3.3 + self.__blue[x + (z << 4)] * 0.8

        for x in range(16):
            for z in range(16):
                self.__blue[x + (z << 4)] += self.__alpha[x + (z << 4)] * 0.05
                if self.__blue[x + (z << 4)] < 0.0:
                    self.__blue[x + (z << 4)] = 0.0

                self.__alpha[x + (z << 4)] -= 0.1
                if self.__random.randFloat() < 0.05:
                    self.__alpha[x + (z << 4)] = 0.5

        memcpy(red, self.__green, sizeof(self.__green))
        self.__green = self.__red
        self.__red = red

        for pixel in range(256):
            value = self.__red[pixel]
            if value > 1.0:
                value = 1.0

            if value < 0.0:
                value = 0.0

            value *= value
            r = <int>(32.0 + value * 32.0)
            g = <int>(50.0 + value * 64.0)
            b = 255
            a = <int>(146.0 + value * 50.0)
            if self.anaglyphEnabled:
                nr = (r * 30 + g * 59 + 2805) // 100
                g = (r * 30 + g * 70) // 100
                b = (r * 30 + 17850) // 100
                r = nr

            self.imageData[pixel << 2] = <char>r
            self.imageData[(pixel << 2) + 1] = <char>g
            self.imageData[(pixel << 2) + 2] = <char>b
            self.imageData[(pixel << 2) + 3] = <char>a
