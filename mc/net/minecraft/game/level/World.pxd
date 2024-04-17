# cython: language_level=3

cimport cython

from mc.net.minecraft.game.level.EntityMap cimport EntityMap
from mc.net.minecraft.game.physics.AxisAlignedBB cimport AxisAlignedBB
from mc.JavaUtils cimport Random

@cython.final
cdef class World:

    cdef:
        int __maxTicks
        float[16] __lightBrightnessTable

        public int width
        public int length
        public int height

        char* __blocks
        char* __data

        public int xSpawn
        public int ySpawn
        public int zSpawn

        public float rotSpawn

        public int defaultFluid

        set __worldAccesses
        set __tickList

        int* __heightMap

        Random __rand
        int __randId

        public EntityMap entityMap

        public int waterLevel
        public int groundLevel
        public int cloudHeight

        public int skyColor
        public int fogColor
        public int cloudColor

        int __updateLCG
        int __playTime

        public int multiplier
        public unsigned long addend

        public object playerEntity

        public bint survivalWorld

        public float skyBrightness

        int[256] __lightOpacity
        int[256] __lightValue
        bint[256] __isBlockNormal

    cdef findSpawn(self)
    cdef void __updateSkylight(self, int x0, int y0, int x1, int y1) except *
    cdef void __updateLight(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cdef swap(self, int x0, int y0, int z0, int x1, int y1, int z1)
    cpdef bint setBlock(self, int x, int y, int z, int blockType)
    cpdef bint setBlockWithNotify(self, int x, int y, int z, int blockType)
    cpdef notifyBlocksOfNeighborChange(self, int x, int y, int z, int blockType)
    cpdef bint setTileNoUpdate(self, int x, int y, int z, int blockType)
    cdef __notifyBlockOfNeighborChange(self, int x, int y, int z, int blockType)
    cpdef inline bint isHalfLit(self, int x, int y, int z)
    cpdef inline bint isFullyLit(self, int x, int y, int z)
    cpdef inline int getBlockId(self, int x, int y, int z)
    cpdef void updateEntities(self)
    cpdef tick(self)
    cpdef inline bint isBlockNormalCube(self, int x, int y, int z)
    cdef inline bint __isInLevelBounds(self, int x, int y, int z)
    cpdef inline int getGroundLevel(self)
    cpdef inline int getWaterLevel(self)
    cdef bint getIsAnyLiquid(self, AxisAlignedBB box)
    cdef bint isBoundingBoxBurning(self, AxisAlignedBB box)
    cdef bint handleMaterialAcceleration(self, AxisAlignedBB box, int liquidId)
    cpdef inline scheduleBlockUpdate(self, int x, int y, int z, int blockType)
    cpdef bint checkIfAABBIsClear(self, AxisAlignedBB aabb)
    cpdef inline bint isSolid(self, float x, float y, float z, float offset)
    cdef inline bint __isBlockOpaque(self, float x, float y, float z)
    cpdef __getFirstUncoveredBlock(self, int x, int z)
    cpdef setSpawnLocation(self, int x, int y, int z, float rotationYaw)
    cpdef inline float getBlockLightValue(self, int x, int y, int z)
    cdef inline char __getBlockMetadata(self, int x, int y, int z)
    cpdef inline int getBlockMaterial(self, int x, int y, int z)
    cpdef inline bint isWater(self, int x, int y, int z)
    cpdef bint growTrees(self, int x, int y, int z)
