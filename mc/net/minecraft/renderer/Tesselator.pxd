# cython: language_level=3

cimport cython

@cython.final
cdef class Tesselator:

    cdef:
        int max_floats

        object __buffer
        float[524288] __array

        public int vertices

        public float u
        public float v
        public float r
        public float g
        public float b

        public bint hasColor
        public bint hasTexture

        public int len
        public int p

        public bint noColor

    cpdef flush(self)
    cdef clear(self)
    cpdef init(self)
    cpdef tex(self, float u, float v)
    cpdef inline colorRGB(self, float r, float g, float b)
    cpdef vertexUV(self, float x, float y, float z, float u, float v)
    cpdef vertex(self, float x, float y, float z)
    cpdef inline color(self, int c)
