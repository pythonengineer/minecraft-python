# cython: language_level=3

cimport cython

from mc.CompatibilityShims cimport FloatBuffer

@cython.final
cdef class Tessellator:

    cdef:
        int max_floats

        FloatBuffer __byteBuffer
        float[524288] __rawBuffer

        int __vertexCount

        float __textureU
        float __textureV
        float __r
        float __g
        float __b

        bint __hasColor
        bint __hasTexture

        int __colors
        int __addedVertices

        bint __drawMode

    cpdef void draw(self)
    cdef void __reset(self)
    cpdef void startDrawingQuads(self)
    cpdef inline void setColorOpaque_F(self, float r, float g, float b)
    cpdef void addVertexWithUV(self, float x, float y, float z, float u, float v)
    cpdef void addVertex(self, float x, float y, float z)
    cpdef inline void setColorOpaque_I(self, int c)
    cpdef inline void disableColor(self)
