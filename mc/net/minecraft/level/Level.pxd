# cython: language_level=3

cimport cython

@cython.final
cdef class Level:

    cdef:
        int update_interval

        public str name
        public str creator
        public object createTime

        public set levelListeners
        public object rand
        public int randValue

        public int unprocessed

        public int multiplier
        public unsigned long addend

        public int width
        public int height
        public int depth

        char* __blocks
        int* __heightMap

    cdef setData(self, int w, int d, int h, char* blocks)
    cdef __calcLightDepths(self, int x0, int y0, int x1, int y1)
    cdef inline bint isLightBlocker(self, int x, int y, int z)
    cpdef getCubes(self, box)
    cpdef bint setTile(self, int x, int y, int z, int type_)
    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_)
    cdef __updateNeighborAt(self, int x, int y, int z, int type_)
    cpdef inline bint isLit(self, int x, int y, int z)
    cpdef inline int getTile(self, int x, int y, int z)
    cpdef tick(self)
    cpdef bint containsAnyLiquid(self, box)
    cpdef bint containsLiquid(self, box, int liquidId)
    cpdef clip(self, vec1, vec2)
