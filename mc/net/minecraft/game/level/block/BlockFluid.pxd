# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World

cdef class BlockFluid(Block):

    cdef:
        public int _material
        public int _stillId
        public int _movingId

    cpdef int getBlockTexture(self, int face)
    cpdef bint renderAsNormalBlock(self)
    cpdef void updateTick(self, World world, int x, int y, int z, random) except *
    cdef bint __canFlow(self, World world, int x, int y, int z)
    cdef bint __flow(self, World world, int x, int y, int z)
    cdef float getBlockBrightness(self, World world, int x, int y, int z)
    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer)
    cpdef bint isOpaqueCube(self)
    cpdef int getBlockMaterial(self)
    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *
    cdef int tickRate(self)
    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance)
    cpdef int quantityDropped(self, random)
    cdef int getRenderBlockPass(self)
