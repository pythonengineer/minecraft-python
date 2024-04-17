# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

from libc.string cimport memcpy
from libc.math cimport sin, pi

from mc.net.minecraft.client.render.texture.TextureFX cimport TextureFX
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils cimport Random

cdef class TextureLavaFX(TextureFX):

    cdef:
        Random __random
        float __red[256]
        float __green[256]
        float __blue[256]
        float __alpha[256]

    def __init__(self):
        TextureFX.__init__(self, blocks.lavaMoving.blockIndexInTexture)
        self.__random = Random()
        for i in range(256):
            self.__red[i] = 0.0
            self.__green[i] = 0.0
            self.__blue[i] = 0.0
            self.__alpha[i] = 0.0

    cpdef onTick(self):
        cdef int x, z, y0, y1, xx, zz, pixel, r, g, b, nr
        cdef float value
        cdef float red[256]

        for x in range(16):
            for z in range(16):
                value = 0.0
                y0 = <int>(sin(z * pi * 2.0 / 16.0) * 1.2)
                y1 = <int>(sin(x * pi * 2.0 / 16.0) * 1.2)

                for xx in range(x - 1, x + 2):
                    for zz in range(z - 1, z + 2):
                        value += self.__red[(xx + y0 & 15) + ((zz + y1 & 15) << 4)]

                self.__green[x + (z << 4)] = value / 10.0 + (self.__blue[(x & 15) + \
                    ((z & 15) << 4)] + \
                    self.__blue[(x + 1 & 15) + ((z & 15) << 4)] + \
                    self.__blue[(x + 1 & 15) + ((z + 1 & 15) << 4)] + \
                    self.__blue[(x & 15) + ((z + 1 & 15) << 4)]) / 4.0 * 0.8
                self.__blue[x + (z << 4)] += self.__alpha[x + (z << 4)] * 0.01
                if self.__blue[x + (z << 4)] < 0.0:
                    self.__blue[x + (z << 4)] = 0.0

                self.__alpha[x + (z << 4)] -= 0.06
                if self.__random.randFloat() < 0.005:
                    self.__alpha[x + (z << 4)] = 1.5

        memcpy(red, self.__green, sizeof(self.__green))
        self.__green = self.__red
        self.__red = red

        for pixel in range(256):
            value = self.__red[pixel] * 2.0
            if value > 1.0:
                value = 1.0

            if value < 0.0:
                value = 0.0

            r = <int>(value * 100.0 + 155.0)
            g = <int>(value * value * 255.0)
            b = <int>(value * value * value * value * 128.0)
            if self.anaglyphEnabled:
                nr = (r * 30 + g * 59 + b * 11) // 100
                g = (r * 30 + g * 70) // 100
                b = (r * 30 + b * 70) // 100
                r = nr

            self.imageData[pixel << 2] = <char>r
            self.imageData[(pixel << 2) + 1] = <char>g
            self.imageData[(pixel << 2) + 2] = <char>b
            self.imageData[(pixel << 2) + 3] = -1
