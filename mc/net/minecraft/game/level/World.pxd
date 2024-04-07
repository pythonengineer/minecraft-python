# cython: language_level=3

cimport cython

from mc.net.minecraft.game.level.EntityMap cimport EntityMap
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB

@cython.final
cdef class World:

    cdef:
        int __maxTicks
        float[9] __lightBrightnessTable

        public int width
        public int length
        public int height

        char* __blocks
        char* __data

        public int xSpawn
        public int ySpawn
        public int zSpawn

        public float rotSpawn

        set __worldAccesses
        set __tickList

        int* __heightMap

        public object rand
        int __randId

        public EntityMap entityMap

        public int waterLevel
        public int skyColor
        public int fogColor
        public int cloudColor

        int __updateLCG
        int __playTime

        public int multiplier
        public unsigned long addend

        public object playerEntity

        public bint multiplayerWorld
        public bint survivalWorld

        int[295936] __floodFillCounters

    cdef findSpawn(self)
    cdef void __updateSkylight(self, int x0, int y0, int x1, int y1) except *
    cdef void __updateLight(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cdef swap(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cpdef bint setBlock(self, int x, int y, int z, int blockType)
    cpdef bint setBlockWithNotify(self, int x, int y, int z, int blockType)
    cpdef notifyBlocksOfNeighborChange(self, int x, int y, int z, int blockType)
    cpdef inline bint setTileNoUpdate(self, int x, int y, int z, int blockType)
    cdef __notifyBlockOfNeighborChange(self, int x, int y, int z, int blockType)
    cpdef inline bint isHalfLit(self, int x, int y, int z)
    cpdef inline int getBlockId(self, int x, int y, int z)
    cpdef void updateEntities(self)
    cpdef tick(self)
    cpdef inline bint isBlockNormalCube(self, int x, int y, int z)
    cdef inline bint __isInLevelBounds(self, int x, int y, int z)
    cpdef inline float getGroundLevel(self)
    cpdef inline float getWaterLevel(self)
    cdef bint getIsAnyLiquid(self, AxisAlignedBB box)
    cdef bint handleMaterialAcceleration(self, AxisAlignedBB box, int liquidId)
    cpdef inline scheduleBlockUpdate(self, int x, int y, int z, int blockType)
    cpdef bint checkIfAABBIsClear(self, AxisAlignedBB aabb)
    cpdef inline bint isSolid(self, float x, float y, float z, float offset)
    cdef inline bint __isBlockOpaque(self, float x, float y, float z)
    cpdef __getFirstUncoveredBlock(self, int x, int z)
    cpdef setSpawnLocation(self, int x, int y, int z, float rotationYaw)
    cpdef inline float getBlockLightValue(self, int x, int y, int z)
    cpdef inline int getBlockMaterial(self, int x, int y, int z)
    cpdef inline bint isWater(self, int x, int y, int z)
    cpdef bint growTrees(self, int x, int y, int z)
