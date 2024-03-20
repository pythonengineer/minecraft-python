# cython: language_level=3

from mc.CompatibilityShims cimport FloatBuffer

cdef class ClippingHelper:

    cdef:
        int _right
        int _left
        int _bottom
        int _top
        int _back
        int _front
        int _a
        int _b
        int _c
        int _d

        FloatBuffer __projectionMatrixBuffer
        FloatBuffer __modelviewMatrixBuffer
        FloatBuffer __clippingMatrixBuffer

        float[16] __projectionMatrix
        float[16] __modelviewMatrix
        float[16] __clippingMatrix

        float[6][4] __frustrum

    cdef __normalize(self, int side)
    cpdef bint isBoundingBoxFullyInFrustrum(self, float x0, float y0, float z0,
                                            float x1, float y1, float z1)
    cpdef bint isBoundingBoxInFrustrum(self, float x0, float y0, float z0,
                                       float x1, float y1, float z1)
    cpdef bint isVisible(self, aabb)
