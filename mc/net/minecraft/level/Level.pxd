# cython: language_level=3

cimport cython

@cython.final
cdef class Level:

    cdef:
        int update_interval

        public set levelListeners

        public int unprocessed

        public int width
        public int height
        public int depth

        char* __blocks
        int* __lightDepths

    cdef generateMap(self)
    cdef calcLightDepths(self, int x0, int y0, int x1, int y1)
    cdef inline bint isLightBlocker(self, int x, int y, int z)
    cpdef getCubes(self, aABB)
    cpdef bint setTile(self, int x, int y, int z, int type_)
    cpdef inline bint isLit(self, int x, int y, int z)
    cpdef inline int getTile(self, int x, int y, int z)
    cpdef inline bint isSolidTile(self, int x, int y, int z)
    cpdef tick(self)
    cpdef clip(self, vec1, vec2)
