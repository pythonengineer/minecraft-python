# cython: language_level=3

cimport cython

@cython.final
cdef class AABB:

    cdef:
        float __epsilon

        public float x0
        public float y0
        public float z0
        public float x1
        public float y1
        public float z1

    cpdef AABB expand(self, float xa, float ya, float za)
    cdef float clipXCollide(self, AABB c, float xa)
    cdef float clipYCollide(self, AABB c, float ya)
    cdef float clipZCollide(self, AABB c, float za)
    cpdef void move(self, float xa, float ya, float za)
    cdef AABB copy(self)
