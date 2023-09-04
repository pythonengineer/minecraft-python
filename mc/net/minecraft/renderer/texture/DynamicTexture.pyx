# cython: language_level=3

cdef class DynamicTexture:

    def __init__(self, tex):
        self.tex = tex
        self.pixels = [0] * 1024
        self.anaglyph = False

    cpdef tick(self):
        pass
