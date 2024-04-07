# cython: language_level=3

from mc.net.minecraft.game.level.World cimport World

cdef class Block:

    cdef:
        public object blocks
        public int blockIndexInTexture
        public int blockID
        public object stepSound
        public float blockParticleGravity
        public bint blockIsDropped
        int __hardness

        public float minX
        public float minY
        public float minZ
        public float maxX
        public float maxY
        public float maxZ

    cpdef bint renderAsNormalBlock(self)
    cpdef int getRenderType(self)
    cdef float getBlockBrightness(self, World world, int x, int y, int z)
    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer)
    cpdef int getBlockTexture(self, int face)
    cpdef bint isOpaqueCube(self)
    cpdef void updateTick(self, World world, int x, int y, int z, random) except *
    cpdef int getBlockMaterial(self)
    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *
    cdef int tickRate(self)
    cpdef int quantityDropped(self, random)
    cpdef int idDropped(self)
    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance)
    cdef bint isExplosionResistant(self)
    cdef collisionRayTrace(self, int x, int y, int z, v0, v1)
    cdef bint __isVecInsideYZBounds(self, vec)
    cdef bint __isVecInsideXZBounds(self, vec)
    cdef bint __isVecInsideXYBounds(self, vec)
    cdef int getRenderBlockPass(self)
