# cython: language_level=3

cimport cython

from mc.net.minecraft.level.BlockMap cimport BlockMap
from mc.net.minecraft.phys.AABB cimport AABB

@cython.final
cdef class Level:

    cdef:
        int update_interval

        public str name
        public str creator
        public object createTime

        public int xSpawn
        public int ySpawn
        public int zSpawn

        public float rotSpawn

        set __levelListeners
        public object rand
        public int randValue
        set __tickList

        public BlockMap blockMap

        bint __networkMode

        public object rendererContext
        public bint creativeMode

        public int waterLevel
        public int skyColor
        public int fogColor
        public int cloudColor

        public int unprocessed
        int __tickCount

        public int multiplier
        public unsigned long addend

        public object player
        public object particleEngine
        public object font

        public bint growTrees

        public int width
        public int depth
        public int height

        char* __blocks
        int* __heightMap

    cdef setData(self, int w, int d, int h, char* blocks)
    cdef findSpawn(self)
    cdef void calcLightDepths(self, int x0, int y0, int x1, int y1) except *
    cdef inline bint isLightBlocker(self, int x, int y, int z)
    cdef swap(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cpdef bint setTileNoNeighborChange(self, int x, int y, int z, int type_)
    cdef bint netSetTileNoNeighborChange(self, int x, int y, int z, int type_)
    cpdef bint setTile(self, int x, int y, int z, int type_)
    cpdef updateNeighborsAt(self, int x, int y, int z, int type_)
    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int type_)
    cdef __neighborChanged(self, int x, int y, int z, int type_)
    cpdef inline bint isLit(self, int x, int y, int z)
    cpdef inline int getTile(self, int x, int y, int z)
    cpdef void tickEntities(self)
    cpdef tick(self)
    cpdef inline bint isSolidTile(self, int x, int y, int z)
    cdef inline bint __isInLevelBounds(self, int x, int y, int z)
    cpdef inline float getGroundLevel(self)
    cpdef inline float getWaterLevel(self)
    cdef bint containsAnyLiquid(self, AABB box)
    cdef bint containsLiquid(self, AABB box, int liquidId)
    cpdef inline addToTickNextTick(self, int x, int y, int z, int type_)
    cpdef bint isFree(self, AABB aabb)
    cpdef inline bint isSolid(self, int x, int y, int z, int f4)
    cdef inline bint __isBlockOpaque(self, int x, int y, int z)
    cpdef getHighestTile(self, int x, int z)
    cpdef setSpawnPos(self, int x, int y, int z, float yRot)
    cpdef inline float getBrightness(self, int x, int y, int z)
    cpdef inline int getLiquid(self, int x, int y, int z)
    cpdef inline bint isWater(self, int x, int y, int z)
    cpdef bint maybeGrowTree(self, int x, int y, int z)
    cpdef explode(self, entity, float x, float y, float z, float radius)
