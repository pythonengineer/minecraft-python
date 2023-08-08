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
    cpdef inline colorRGB(self, float r, float g, float b)
    cpdef inline colorByte(self, char r, char g, char b)
    cpdef vertexUV(self, float x, float y, float z, float u, float v)
    cpdef vertex(self, float x, float y, float z)
    cpdef inline color(self, int c)
