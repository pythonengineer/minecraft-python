from pyglet import gl as opengl

from mc import Resources
from mc.CompatibilityShims import BufferUtils


class Textures:

    idMap = {}
    lastId = -9999999

    @classmethod
    def loadTexture(cls, resourceName, mode):
        if resourceName in cls.idMap:
            return cls.idMap[resourceName]

        ib = BufferUtils.createUintBuffer(1).clear()

        opengl.glGenTextures(1, ib)
        id_ = ib.get(0)

        cls.bind(id_)

        opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, mode)
        opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, mode)

        img = Resources.textures[resourceName]
        w = img[0]
        h = img[1]

        pixels = BufferUtils.createIntBuffer(w * h * 4).clear()
        pixels.put(img[2], 0, len(img[2]))

        opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, opengl.GL_RGBA, w, h, 0, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE, pixels)

        return id_

    @classmethod
    def bind(cls, id_):
        if id_ != cls.lastId:
            opengl.glBindTexture(opengl.GL_TEXTURE_2D, id_)
            cls.lastId = id_
