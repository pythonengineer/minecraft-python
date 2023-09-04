# cython: language_level=3

cimport cython

from libc.stdlib cimport srand, rand, RAND_MAX
from libc.time cimport time

cdef bint Random_seeded = False

cdef class Random:

    property seeded:

        def __get__(self):
            return Random_seeded

        def __set__(self, x):
            global Random_seeded
            Random_seeded = x

    def __init__(self, seed=0):
        if not self.seeded:
            if seed == 0:
                srand(time(NULL))
            else:
                srand(seed)

            self.seeded = True

    cdef float randFloatM(self, float multiply):
        return self.randFloat() * multiply

    cdef float randFloat(self):
        return rand() / <float>RAND_MAX

    @cython.cdivision(True)
    cdef int nextInt(self, int limit):
        cdef double scaleFactor
        cdef int value

        if not isinstance(limit, int) or limit <= 0:
            raise ValueError('limit must be a positive integer')

        scaleFactor = limit / (RAND_MAX + 1.0)
        value = <int>(rand() * scaleFactor)

        return value
