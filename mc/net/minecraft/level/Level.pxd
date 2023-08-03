# cython: language_level=3

cimport cython

@cython.final
cdef class Level:

    cdef:
        public set levelListeners

        public int width
        public int height
        public int depth

        char* __blocks
        int* __lightDepths

    cdef calcLightDepths(self, int x0, int y0, int x1, int y1)
    cdef bint isTile(self, int x, int y, int z)
    cdef bint isSolidTile(self, int x, int y, int z)
    cdef bint isLightBlocker(self, int x, int y, int z)
    cpdef getCubes(self, aABB)
    cdef float getBrightness(self, int x, int y, int z)
    cpdef clip(self, vec1, vec2)
