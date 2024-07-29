# cython: language_level=3

from mc.net.minecraft.game.level.block.BlockFluid cimport BlockFluid
from mc.net.minecraft.game.level.World cimport World
from mc.JavaUtils cimport Random

cdef class BlockFlowing(BlockFluid):

    cdef:
        int __stillId
        int __movingId
        Random __random
        int[4] __flowArray

    cpdef void updateTick(self, World world, int x, int y, int z, Random random) except *
    cdef bint update(self, World world, int x, int y, int z, int _)
    cdef bint __liquidSpread(self, World world, int x0, int y0, int z0,
                             int x1, int y1, int z1)
    cdef bint __flow(self, World world, int x0, int y0, int z0,
                     int x1, int y1, int z1)
    cpdef bint shouldSideBeRendered(self, World world, int x, int y, int z, int layer)
    cpdef bint isCollidable(self)
    cpdef bint isOpaqueCube(self)
    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *
    cdef int tickRate(self)
    cdef dropBlockAsItemWithChance(self, World world, int x, int y, int z, float chance)
    cpdef int quantityDropped(self, Random random)
    cdef int getRenderBlockPass(self)
    cdef bint __extinguishFireLava(self, World world, int x, int y, int z)
    cdef bint __fireSpread(self, World world, int x, int y, int z)
