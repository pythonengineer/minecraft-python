# cython: language_level=3

cimport cython

@cython.final
cdef class AxisAlignedBB:

    cdef:
        float __epsilon

        public float minX
        public float minY
        public float minZ
        public float maxX
        public float maxY
        public float maxZ

    cpdef AxisAlignedBB addCoord(self, float xa, float ya, float za)
    cdef float calculateXOffset(self, AxisAlignedBB c, float xa)
    cdef float calculateYOffset(self, AxisAlignedBB c, float ya)
    cdef float calculateZOffset(self, AxisAlignedBB c, float za)
    cpdef void offset(self, float xa, float ya, float za)
    cdef AxisAlignedBB copy(self)
    cpdef calculateIntercept(self, vec1, vec2)
    cdef bint __isVecInYZ(self, xa)
    cdef bint __isVecInXZ(self, ya)
    cdef bint __isVecInXY(self, za)
