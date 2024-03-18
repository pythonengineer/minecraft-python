from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.CompatibilityShims cimport Random

cdef class BlockGrass(Block):

    cdef:
        Random __rand

    cpdef int getBlockTexture(self, int face)
    cpdef void updateTick(self, World world, int x, int y, int z, random) except *
