# cython: language_level=3

cimport cython

@cython.final
cdef class Level:

    cdef:
        int update_interval

        public str name
        public str creator
        public object createTime

        set __levelListeners
        object __rand
        int __randValue

        public int unprocessed

        int __multiplier
        unsigned long __addend

        public int width
        public int height
        public int depth

        char* __blocks
        int* __lightDepths

    cdef setData(self, int w, int d, int h, char* blocks)
    cdef calcLightDepths(self, int x0, int y0, int x1, int y1)
    cdef inline bint isLightBlocker(self, int x, int y, int z)
    cpdef getCubes(self, box)
    cpdef bint setTile(self, int x, int y, int z, int type_)
    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_)
    cdef __neighborChanged(self, int x, int y, int z, int type_)
    cpdef inline bint isLit(self, int x, int y, int z)
    cpdef inline int getTile(self, int x, int y, int z)
    cpdef inline bint isSolidTile(self, int x, int y, int z)
    cpdef tick(self)
    cpdef inline float getGroundLevel(self)
    cpdef bint containsAnyLiquid(self, box)
    cpdef bint containsLiquid(self, box, int liquidId)
    cpdef clip(self, vec1, vec2)
