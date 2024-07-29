# cython: language_level=3

cimport cython

from mc.JavaUtils cimport IntBuffer

@cython.final
cdef class Tessellator:

    cdef:
        int max_ints

        IntBuffer __byteBuffer
        int[:] __rawBuffer

        int __vertexCount

        float __textureU
        float __textureV

        int __color

        bint __hasColor
        bint __hasTexture

        int __colors
        int __addedVertices
        int __rawBufferIndex

        bint __drawMode

    cpdef void draw(self)
    cdef void __reset(self)
    cpdef void startDrawingQuads(self)
    cpdef inline void setColorOpaque_F(self, float r, float g, float b)
    cdef inline void __setColorOpaque(self, int r, int g, int b)
    cpdef void addVertexWithUV(self, float x, float y, float z, float u, float v)
    cpdef void addVertex(self, float x, float y, float z)
    cpdef inline void setColorOpaque_I(self, int c)
    cpdef inline void disableColor(self)
