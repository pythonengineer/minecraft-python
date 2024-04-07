from mc.CompatibilityShims import BufferUtils
from mc import Resources
from pyglet import gl

import ctypes

class RenderEngine:

    def __init__(self, options):
        self.__options = options
        self.__textureMap = {}
        self.__textureContentsMap = {}
        self.__singleIntBuffer = gl.GLuint(1)
        self.__imageData = BufferUtils.createByteBuffer(262144)
        self.__textureList = []
        self.__clampTexture = False

    def setClampTexture(self, clampTexture):
        self.__clampTexture = clampTexture

    def getTexture(self, resourceName):
        if resourceName in self.__textureMap:
            return self.__textureMap[resourceName]
        else:
            gl.glGenTextures(1, ctypes.byref(self.__singleIntBuffer))
            id_ = self.__singleIntBuffer.value
            if resourceName.startswith('##'):
                self.__setupTexture(RenderEngine.__unwrapImageByColumns(Resources.textures[resourceName]), id_)
            else:
                self.__setupTexture(Resources.textures[resourceName], id_)

            self.__textureMap[resourceName] = id_
            return id_

    def getTextureImg(self, img):
        gl.glGenTextures(1, ctypes.byref(self.__singleIntBuffer))
        id_ = self.__singleIntBuffer.value
        self.__setupTexture(img, id_)
        self.__textureContentsMap[id_] = img
        return id_

    @staticmethod
    def __unwrapImageByColumns(img):
        return img

    def __setupTexture(self, img, id_):
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

        self.__imageData.clear()

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
                if self.__options.anaglyph:
                    nr = (r * 30 + g * 59 + b * 11) // 100
                    g = (r * 30 + g * 70) // 100
                    b = (r * 30 + b * 70) // 100
                    r = nr

                argb[i << 2] = r
                argb[(i << 2) + 1] = g
                argb[(i << 2) + 2] = b
                argb[(i << 2) + 3] = a

            self.__imageData.putBytes(argb)
            self.__imageData.position(0).limit(len(argb))
        else:
            rgb = list(img[2])
            if self.__options.anaglyph:
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

            self.__imageData.putBytes(argb)
            self.__imageData.position(0).limit(len(argb))

        if self.__clampTexture:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
        else:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        self.__imageData.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h,
                                      0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)

    def registerTextureFX(self, textureFx):
        self.__textureList.append(textureFx)
        textureFx.onTick()

    def updateDynamicTextures(self):
        for texture in self.__textureList:
            texture.anaglyphEnabled = self.__options.anaglyph
            texture.onTick()
            self.__imageData.clear()
            self.__imageData.putBytes(texture.imageData)
            self.__imageData.position(0).limit(len(texture.imageData))
            self.__imageData.glTexSubImage2D(gl.GL_TEXTURE_2D, 0,
                                             texture.iconIndex % 16 << 4,
                                             texture.iconIndex // 16 << 4,
                                             16, 16, gl.GL_RGBA,
                                             gl.GL_UNSIGNED_BYTE)

    def refreshTextures(self):
        for id_, img in self.__textureContentsMap.items():
            self.__setupTexture(img, id_)

        for string, id_ in self.__textureMap.items():
            if string.startswith('##'):
                img = RenderEngine.__unwrapImageByColumns(Resources.textures[string[2:]])
            else:
                img = Resources.textures[string]

                self.__setupTexture(img, id_)
