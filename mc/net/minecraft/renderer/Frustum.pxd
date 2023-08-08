# cython: language_level=3

cdef class Frustum:

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

        object _proj
        object _modl
        object _clip

        float[16] __proj
        float[16] __modl
        float[16] __clip

        float[6][4] __m_Frustum

    cpdef calculateFrustum(self)
    cdef __normalizePlane(self, int side)
    cpdef bint cubeInFrustum(self, aabb)
