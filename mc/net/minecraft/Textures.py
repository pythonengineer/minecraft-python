__all__ = [
    'TEXTURE_ID_MAP', 'TEXTURE_ID_LAST',
    'bind', 'load',
]


from pyglet import gl as opengl

from mc import compat, resources


TEXTURE_ID_MAP = {}
TEXTURE_ID_LAST = -9999999


def bind(tid):
    global TEXTURE_ID_LAST
    if tid != TEXTURE_ID_LAST:
        opengl.glBindTexture(opengl.GL_TEXTURE_2D, tid)
        TEXTURE_ID_LAST = tid


def load(resource, mode):
    global TEXTURE_ID_MAP
    if resource in TEXTURE_ID_MAP:
        return TEXTURE_ID_MAP[resource]

    ib = compat.BufferUtils.createUintBuffer(1).clear()
    opengl.glGenTextures(1, ib)
    tid = ib.get(0)
    bind(tid)

    opengl.glTexParameteri(
        opengl.GL_TEXTURE_2D,
        opengl.GL_TEXTURE_MIN_FILTER,
        mode,
        )

    opengl.glTexParameteri(
        opengl.GL_TEXTURE_2D,
        opengl.GL_TEXTURE_MAG_FILTER,
        mode,
        )

    img = resources.textures[resource]
    pixels = compat.BufferUtils.createIntBuffer(img[0] * img[1] * 4)
    pixels.clear()
    pixels.put(img[2], 0, len(img[2]))

    opengl.glTexImage2D(
        opengl.GL_TEXTURE_2D,    # target
        0,                       # level
        opengl.GL_RGBA,          # internalformat
        img[0],                  # width
        img[1],                  # height
        0,                       # border
        opengl.GL_RGBA,          # format
        opengl.GL_UNSIGNED_BYTE, # type
        pixels,                  # data
        )

    return tid
