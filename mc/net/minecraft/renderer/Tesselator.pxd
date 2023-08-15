# cython: language_level=3

cimport cython

@cython.final
cdef class Tesselator:

    cdef:
        int max_floats

        object __buffer
        float[524288] __array

        int __vertices

        float __u
        float __v
        float __r
        float __g
        float __b

        bint __hasColor
        bint __hasTexture

        int __len
        int __p

        bint __noColor

    cpdef end(self)
    cdef __clear(self)
    cpdef begin(self)
    cpdef colorFloat(self, float r, float g, float b)
    cpdef colorInt(self, int r, int g, int b)
    cpdef vertexUV(self, float x, float y, float z, float u, float v)
    cpdef vertex(self, float x, float y, float z)
    cpdef color(self, int c)
    cpdef noColor(self)
