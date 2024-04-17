from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.World cimport World
from mc.net.minecraft.game.level.material.Material cimport Material
from mc.JavaUtils cimport Random

cdef class BlockGrass(Block):

    cdef:
        Random __rand

    def __cinit__(self):
        self.__rand = Random()

    def __init__(self, blocks, blockId):
        Block.__init__(self, blocks, 2)
        self.blockIndexInTexture = 3
        self._setTickOnLoad(True)

    cpdef int getBlockTexture(self, int face):
        if face == 1: return 0
        if face == 0: return 2
        return 3

    cpdef void updateTick(self, World world, int x, int y, int z) except *:
        cdef int i, xt, yt, zt

        if not world.isHalfLit(x, y + 1, z) and world.getBlockMaterial(x, y + 1, z) == Material.air:
            if self.__rand.nextInt(4) == 0:
                world.setBlockWithNotify(x, y, z, self.blocks.dirt.blockID)
        else:
            xt = x + self.__rand.nextInt(3) - 1
            yt = y + self.__rand.nextInt(5) - 3
            zt = z + self.__rand.nextInt(3) - 1
            if world.getBlockId(xt, yt, zt) == self.blocks.dirt.blockID and \
               world.isHalfLit(xt, yt + 1, zt) and \
               world.getBlockMaterial(x, y + 1, z) == Material.air:
                world.setBlockWithNotify(xt, yt, zt, self.blocks.grass.blockID)

    cpdef int idDropped(self):
        return self.blocks.dirt.idDropped()
