# cython: language_level=3

cimport cython

@cython.final
cdef class Level:

    cdef:
        int update_interval

        public str name
        public str creator
        public object createTime

        public float rotSpawn

        set __levelListeners
        public object rand
        public int randValue
        set __tickList

        public set entities

        bint __networkMode

        public object rendererContext

        public int unprocessed
        int __tickCount

        public int multiplier
        public unsigned long addend

        public int width
        public int height
        public int depth

        char* __blocks
        int* __heightMap

        public int xSpawn
        public int ySpawn
        public int zSpawn

    cdef setData(self, int w, int d, int h, char* blocks)
    cdef findSpawn(self)
    cdef void calcLightDepths(self, int x0, int y0, int x1, int y1) except *
    cdef inline bint isLightBlocker(self, int x, int y, int z) except *
    cpdef bint setTileNoNeighborChange(self, int x, int y, int z, int type_)
    cdef bint netSetTileNoNeighborChange(self, int x, int y, int z, int type_)
    cpdef bint setTile(self, int x, int y, int z, int type_)
    cpdef updateNeighborsAt(self, int x, int y, int z, int type_)
    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_)
    cdef __neighborChanged(self, int x, int y, int z, int type_)
    cpdef inline bint isLit(self, int x, int y, int z)
    cpdef inline int getTile(self, int x, int y, int z) except *
    cpdef void tickEntities(self)
    cpdef void tick(self)
    cdef inline bint isSolidTile(self, int x, int y, int z)
    cdef inline bint __isInLevelBounds(self, int x, int y, int z)
    cpdef inline float getGroundLevel(self)
    cpdef inline float getWaterLevel(self)
    cpdef bint containsAnyLiquid(self, box)
    cpdef bint containsLiquid(self, box, int liquidId)
    cpdef inline addToTickNextTick(self, int x, int y, int z, int type_)
    cpdef bint isFree(self, aabb)
    cpdef inline bint isSolid(self, int x, int y, int z, int f4)
    cdef inline bint __isSolidTile(self, int x, int y, int z)
    cdef int getHighestTile(self, int x, int z)
    cpdef setSpawnPos(self, int x, int y, int z, float yRot)
    cpdef inline float getBrightness(self, int x, int y, int z)
    cpdef inline bint isWater(self, int x, int y, int z)
