# cython: language_level=3

cdef class Random:

    cdef float randFloatM(self, float multiply)
    cdef float randFloat(self)
    cdef int randInt(self, int limit)
