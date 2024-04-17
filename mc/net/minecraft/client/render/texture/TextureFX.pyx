# cython: language_level=3

cdef class TextureFX:

    def __init__(self, tex):
        self.iconIndex = tex
        self.imageData = [0] * 1024
        self.anaglyphEnabled = False
        self.textureId = 0

    cpdef onTick(self):
        pass
