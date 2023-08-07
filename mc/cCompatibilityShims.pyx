# cython: language_level=3

from libc.stdlib cimport srand, rand, RAND_MAX
from libc.time cimport time

cdef class Random:

    def __init__(self, seed=0):
        if seed == 0:
            srand(time(NULL))
        else:
            srand(seed)

    cdef float randFloatM(self, float multiply):
        return self.randFloat() * multiply

    cdef float randFloat(self):
        return rand() / <float>RAND_MAX

    cdef int randInt(self, int limit):
        cdef int divisor, retval

        divisor = RAND_MAX // (limit + 1)
        retval = limit + 1
        while retval > limit:
            retval = rand() // divisor

        return retval
