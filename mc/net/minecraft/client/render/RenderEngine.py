from mc.CompatibilityShims import BufferUtils
from mc import Resources
from pyglet import gl

import ctypes

class RenderEngine:

    def __init__(self, options):
        self.options = options
        self.textureMap = {}
        self.textureContentsMap = {}
        self.glBuffer = gl.GLuint(1)
        self.imageData = BufferUtils.createByteBuffer(262144)
        self.textureList = []
        self.clampTexture = False

    def getTexture(self, resourceName):
        if resourceName in self.textureMap:
            return self.textureMap[resourceName]
        else:
            gl.glGenTextures(1, ctypes.byref(self.glBuffer))
            id_ = self.glBuffer.value
            if resourceName.startswith('##'):
                self.setupTexture(RenderEngine.unwrapImageByColumns(Resources.textures[resourceName]), id_)
            else:
                self.setupTexture(Resources.textures[resourceName], id_)

            self.textureMap[resourceName] = id_
            return id_

    def getTextureImg(self, img):
        gl.glGenTextures(1, ctypes.byref(self.glBuffer))
        id_ = self.glBuffer.value
        self.setupTexture(img, id_)
        self.textureContentsMap[id_] = img
        return id_

    @staticmethod
    def unwrapImageByColumns(img):
        return img

    def setupTexture(self, img, id_):
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

        self.imageData.clear()

        if not isinstance(img, tuple):
            argb = bytearray(w * h << 2)

            def convertPixel(c):
                x = c[0] << 16 | c[1] << 8 | c[2] | c[3] << 24
                if x >= 1 << 31:
                    x -= 1 << 32

                return x

            rgb = [convertPixel(pixel) for pixel in rgb]

            for i in range(w * h):
                a = (rgb[i] % 0x100000000) >> 24
                r = rgb[i] >> 16 & 255
                g = rgb[i] >> 8 & 255
                b = rgb[i] & 255
                if self.options.anaglyph:
                    nr = (r * 30 + g * 59 + b * 11) // 100
                    g = (r * 30 + g * 70) // 100
                    b = (r * 30 + b * 70) // 100
                    r = nr

                argb[i << 2] = r
                argb[(i << 2) + 1] = g
                argb[(i << 2) + 2] = b
                argb[(i << 2) + 3] = a

            self.imageData.putBytes(argb)
            self.imageData.position(0).limit(len(argb))
        else:
            rgb = list(img[2])
            if self.options.anaglyph:
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

            self.imageData.putBytes(argb)
            self.imageData.position(0).limit(len(argb))

        if self.clampTexture:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
        else:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        self.imageData.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h,
                                    0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)

    def registerTextureFX(self, textureFx):
        self.textureList.append(textureFx)
        textureFx.onTick()
