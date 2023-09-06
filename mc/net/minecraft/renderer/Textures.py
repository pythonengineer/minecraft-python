from mc.CompatibilityShims import BufferUtils, rshift
from mc import Resources
from pyglet import gl

class Textures:
    idMap = {}
    pixelsMap = {}
    ib = BufferUtils.createUintBuffer(1)
    pixels = BufferUtils.createByteBuffer(262144)
    textureList = []

    def __init__(self, options):
        self.options = options

    def loadTexture(self, resourceName):
        if resourceName in self.idMap:
            return self.idMap[resourceName]
        else:
            self.ib.clear()
            gl.glGenTextures(1, self.ib)
            id_ = self.ib.get(0)
            if resourceName.startswith('##'):
                self.addTextureId(Textures.addTexture(Resources.textures[resourceName]), id_)
            else:
                self.addTextureId(Resources.textures[resourceName], id_)

            self.idMap[resourceName] = id_
            return id_

    def loadTextureImg(self, img):
        self.ib.clear()
        gl.glGenTextures(1, self.ib)
        id_ = self.ib.get(0)
        self.addTextureId(img, id_)
        self.pixelsMap[id_] = img
        return id_

    @staticmethod
    def addTexture(img):
        return img

    def addTextureId(self, img, id_):
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

        self.pixels.clear()

        if not isinstance(img, tuple):
            argb = bytearray(w * h << 2)

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
                if self.options.anaglyph3d:
                    nr = (r * 30 + g * 59 + b * 11) // 100
                    g = (r * 30 + g * 70) // 100
                    b = (r * 30 + b * 70) // 100
                    r = nr

                argb[i << 2] = r
                argb[(i << 2) + 1] = g
                argb[(i << 2) + 2] = b
                argb[(i << 2) + 3] = a

            self.pixels.put(argb)
            self.pixels.position(0).limit(len(argb))
        else:
            rgb = list(img[2])
            if self.options.anaglyph3d:
                argb = bytearray(w * h << 2)
                for i in range(w * h):
                    r = rgb[i << 2] & 255
                    g = rgb[(i << 2) + 1] & 255
                    b = rgb[(i << 2) + 2] & 255
                    a = rgb[(i << 2) + 3] & 255

                    nr = (r * 30 + g * 59 + b * 11) // 100
                    g = (r * 30 + g * 70) // 100
                    b = (r * 30 + b * 70) // 100
                    r = nr

                    argb[i << 2] = r
                    argb[(i << 2) + 1] = g
                    argb[(i << 2) + 2] = b
                    argb[(i << 2) + 3] = a
            else:
                argb = rgb

            self.pixels.put(argb)
            self.pixels.position(0).limit(len(argb))

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.pixels)

    def addDynamicTexture(self, dynamicTexture):
        self.textureList.append(dynamicTexture)
        dynamicTexture.tick()
