from mc.CompatibilityShims import BufferUtils, rshift
from mc import Resources
from pyglet import gl

class Textures:
    __idMap = {}
    idBuffer = BufferUtils.createUintBuffer(1)
    textureBuffer = BufferUtils.createByteBuffer(262144)
    textureList = []

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

        self.textureBuffer.clear()

        if not isinstance(img, tuple):
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

            self.textureBuffer.put(b6)
            self.textureBuffer.position(0).limit(len(b6))
        else:
            self.textureBuffer.put(img[2], 0, len(img[2]))
            self.textureBuffer.position(0).limit(len(img[2]))

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.textureBuffer)

        return id_

    def registerTextureFX(self, textureFX):
        self.textureList.append(textureFX)
        textureFX.onTick()
