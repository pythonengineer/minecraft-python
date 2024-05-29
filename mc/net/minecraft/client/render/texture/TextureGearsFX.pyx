# cython: language_level=3
# cython: cdivision=True, boundscheck=False, wraparound=False, nonecheck=False

from libc.math cimport sin, cos, pi

from mc.net.minecraft.client.render.texture.TextureFX cimport TextureFX
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils cimport random
from mc import Resources

cdef class TextureGearsFX(TextureFX):

    cdef:
        int __gearRotation
        int __gearColor[1024]
        int __gearMiddleColor[1024]
        int __gearRotationDir

    def __init__(self, idx):
        TextureFX.__init__(self, blocks.cog.blockIndexInTexture + idx)
        self.__gearRotationDir = (idx << 1) - 1
        self.__gearRotation = 2

        color = Resources.textures['misc/gear.png'][2]
        for i in range(len(color)):
            self.__gearColor[i] = color[i]

        color = Resources.textures['misc/gearmiddle.png'][2]
        for i in range(len(color)):
            self.__gearMiddleColor[i] = color[i]

    cpdef onTick(self):
        cdef int pixelX, pixelY, texX, texY, color, midColor, r, g, b, a, pixel
        cdef float x, y, gearX, gearY, gearXT, gearYT

        self.__gearRotation += self.__gearRotationDir & 63
        x = sin(self.__gearRotation / 64.0 * pi * 2.0)
        y = cos(self.__gearRotation / 64.0 * pi * 2.0)

        for pixelX in range(16):
            for pixelY in range(16):
                gearX = (pixelX / 15.0 - 0.5) * 31.0
                gearY = (pixelY / 15.0 - 0.5) * 31.0
                gearXT = y * gearX - x * gearY
                gearYT = y * gearY + x * gearX
                texX = <int>(gearXT + 16.0)
                texY = <int>(gearYT + 16.0)
                color = 0
                if texX >= 0 and texY >= 0 and texX < 32 and texY < 32:
                    color = self.__gearColor[texX + (texY << 5)]
                    midColor = self.__gearMiddleColor[pixelX + (pixelY << 4)]
                    if ((midColor % 0x100000000) >> 24) > 128:
                        color = midColor

                r = <int>(color >> 16 & 255)
                g = <int>(color >> 8 & 255)
                b = <int>(color & 255)
                a = 255 if ((color % 0x100000000) >> 24) > 128 else 0
                pixel = pixelX + (pixelY << 4)
                self.imageData[pixel << 2] = <char>r
                self.imageData[(pixel << 2) + 1] = <char>g
                self.imageData[(pixel << 2) + 2] = <char>b
                self.imageData[(pixel << 2) + 3] = <char>a
