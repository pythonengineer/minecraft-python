# cython: language_level=3

cimport cython

@cython.final
cdef class AxisAlignedBB:

    cdef:
        float __epsilon

        public float x0
        public float y0
        public float z0
        public float x1
        public float y1
        public float z1

    cpdef AxisAlignedBB addCoord(self, float xa, float ya, float za)
    cdef float clipXCollide(self, AxisAlignedBB c, float xa)
    cdef float clipYCollide(self, AxisAlignedBB c, float ya)
    cdef float clipZCollide(self, AxisAlignedBB c, float za)
    cpdef void offset(self, float xa, float ya, float za)
    cdef AxisAlignedBB copy(self)
    cpdef calculateIntercept(self, vec1, vec2)
    cdef bint __isVecInYZ(self, xa)
    cdef bint __isVecInXZ(self, ya)
    cdef bint __isVecInXY(self, za)
