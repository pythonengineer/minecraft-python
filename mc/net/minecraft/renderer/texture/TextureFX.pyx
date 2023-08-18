# cython: language_level=3

cdef class TextureFX:

    def __init__(self, iconIndex):
        self.iconIndex = iconIndex
        self.imageData = [0] * 1024

    cpdef onTick(self):
        pass
