# cython: language_level=3

cimport cython

@cython.final
cdef class FontRenderer:

    cdef:
        object __options
        int[256] __charWidth
        int __fontTextureName

    cdef __renderString(self, str string, int x, int y, int color, bint darken=?)
