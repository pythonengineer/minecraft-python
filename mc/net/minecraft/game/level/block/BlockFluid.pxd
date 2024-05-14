# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.JavaUtils cimport Random

cdef class BlockFluid(Block):

    cdef:
        public int _material
        public int _stillId
        public int _movingId

    cpdef int getBlockTexture(self, int face)
    cpdef bint renderAsNormalBlock(self)
    cpdef void updateTick(self, World world, int x, int y, int z, Random random) except *
    cdef bint update(self, World world, int x, int y, int z, int _)
    cpdef bint _canFlow(self, World world, int x, int y, int z)
    cdef bint __extinguishFireLava(self, World world, int x, int y, int z)
    cdef bint __flow(self, World world, int x, int y, int z)
    cdef float getBlockBrightness(self, World world, int x, int y, int z)
    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer)
    cdef bint isCollidable(self)
    cpdef bint isOpaqueCube(self)
    cpdef int getBlockMaterial(self)
    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *
    cdef int tickRate(self)
    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance)
    cpdef int quantityDropped(self, Random random)
    cdef int getRenderBlockPass(self)
    cpdef void randomDisplayTick(self, World world, int x, int y, int z, Random random) except *
