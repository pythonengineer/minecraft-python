from mc.CompatibilityShims import BufferUtils, rshift
from mc import Resources
from pyglet import gl

class Textures:
    __idMap = {}
    idBuffer = BufferUtils.createUintBuffer(1)

    def getTextureId(self, resourceName):
        if resourceName in self.__idMap:
            return self.__idMap[resourceName]
        else:
            id_ = self.addTexture(Resources.textures[resourceName])
            self.__idMap[resourceName] = id_
            return id_

    def addTexture(self, img):
        self.idBuffer.clear()
        gl.glGenTextures(1, self.idBuffer)
        id_ = self.idBuffer.get(0)

        gl.glBindTexture(gl.GL_TEXTURE_2D, id_)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        if not isinstance(img, tuple):
            w = img.width
            h = img.height
            if h > 32:
                img.crop((0, 32, 64, 32))
                h = 32
            rgb = list(img.getdata())
        else:
            w = img[0]
            h = img[1]

        if not isinstance(img, tuple):
            pixels = BufferUtils.createByteBuffer(w * h << 2).clear()
            b6 = bytearray(w * h << 2)

            def convertPixel(c):
                x = c[0] << 16 | c[1] << 8 | c[2] | c[3] << 24
                if x >= 1 << 31:
                    x -= 1 << 32
                return x

            rgb = [convertPixel(pixel) for pixel in rgb]

            for i in range(w * h):
                a = rshift(rgb[i], 24)
                r = rgb[i] >> 16 & 255
                g = rgb[i] >> 8 & 255
                b = rgb[i] & 255
                b6[i << 2] = r
                b6[(i << 2) + 1] = g
                b6[(i << 2) + 2] = b
                b6[(i << 2) + 3] = a

            pixels.put(b6)
            pixels.position(0).limit(len(b6))
        else:
            pixels = BufferUtils.createIntBuffer(w * h << 2).clear()
            pixels.put(img[2], 0, len(img[2]))
            pixels.position(0).limit(len(img[2]))

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pixels)

        return id_
