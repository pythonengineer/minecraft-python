# cython: language_level=3

cimport cython

@cython.final
cdef class Tesselator:

    cdef:
        int max_vertices

        public int vertices

        public object vertexBuffer
        public object texCoordBuffer
        public object colorBuffer

        public float u
        public float v
        public float r
        public float g
        public float b

        public bint hasColor
        public bint hasTexture

    cpdef flush(self)
    cdef clear(self)
    cpdef init(self)
    cpdef tex(self, float u, float v)
    cpdef color(self, float r, float g, float b)
    cpdef vertex(self, float x, float y, float z)
