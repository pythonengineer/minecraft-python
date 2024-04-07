from mc.net.minecraft.client.render.Tessellator import tessellator
from mc import Resources
from pyglet import gl

class FontRenderer:

    def __init__(self, settings, name, textures):
        self.__settings = settings
        self.__charList = [0] * 256
        texture = Resources.textures[name + '1']
        w = texture[0]
        h = texture[1]
        rawPixels = texture[2]

        for i in range(128):
            xt = i % 16
            yt = i // 16

            emptyColumn = False
            for x in range(8):
                if emptyColumn:
                    break

                xPixel = (xt << 3) + x
                emptyColumn = True
                for y in range(8):
                    if not emptyColumn:
                        break

                    yPixel = ((yt << 3) + y) * w
                    pixel = rawPixels[xPixel + yPixel] & 255
                    if pixel > 128:
                        emptyColumn = False

            if i == 32:
                x = 4

            self.__charList[i] = x

        self.__character = textures.getTexture(name + '2')

    def drawStringWithShadow(self, string, x, y, color):
        self.__renderString(string, x + 1, y + 1, color, True)
        self.drawString(string, x, y, color)

    def drawString(self, string, x, y, color):
        self.__renderString(string, x, y, color, False)

    def __renderString(self, string, x, y, color, darken=False):
        if string is not None:
            if darken:
                color = (color & 0xFCFCFC) >> 2

            gl.glBindTexture(gl.GL_TEXTURE_2D, self.__character)
            t = tessellator
            t.startDrawingQuads()
            t.setColorOpaque_I(color)
            xo = 0
            i = 0
            while i < len(string):
                if string[i] == '&' and len(string) > i + 1:
                    cc = '0123456789abcdef'.index(string[i + 1])
                    if cc < 0:
                        cc = 15

                    br = (cc & 8) << 3
                    b = (cc & 1) * 191 + br
                    g = ((cc & 2) >> 1) * 191 + br
                    r = ((cc & 4) >> 2) * 191 + br
                    color = r
                    if self.__settings.anaglyph:
                        br = (color * 30 + g * 59 + b * 11) // 100
                        g = (color * 30 + g * 70) // 100
                        b = (color * 30 + b * 70) // 100
                        g = g

                    color = r << 16 | g << 8 | b
                    i += 2
                    if i >= len(string):
                        break

                    if darken:
                        color = (color & 0xFCFCFC) >> 2

                    t.setColorOpaque_I(color)

                ix = ord(string[i]) % ord('\020') << 3
                iy = ord(string[i]) // ord('\020') << 3
                t.addVertexWithUV(x + xo, y + 7.99, 0.0,
                                  ix / 128.0, (iy + 7.99) / 128.0)
                t.addVertexWithUV(x + xo + 7.99, y + 7.99, 0.0,
                                  (ix + 7.99) / 128.0, (iy + 7.99) / 128.0)
                t.addVertexWithUV(x + xo + 7.99, y, 0.0,
                                  (ix + 7.99) / 128.0, iy / 128.0)
                t.addVertexWithUV(x + xo, y, 0.0,
                                  ix / 128.0, iy / 128.0)

                xo += self.__charList[ord(string[i])]
                i += 1

            t.draw()

    def getStringWidth(self, string):
        if string is None:
            return 0
        else:
            length = 0
            for i, char in enumerate(string):
                if char != '&':
                    length += self.__charList[ord(char)]

            return length
