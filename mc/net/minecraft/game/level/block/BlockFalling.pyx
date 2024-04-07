# cython: language_level=3

from mc.net.minecraft.game.level.block.Block cimport Block
from mc.net.minecraft.game.level.material.Material cimport Material
from mc.net.minecraft.game.level.World cimport World

cdef class BlockFalling(Block):

    def onBlockPlaced(self, World world, int x, int y, int z):
        self.__fall(world, x, y, z)

    cpdef void onNeighborBlockChange(self, World world, int x, int y, int z, int blockType) except *:
        self.__fall(world, x, y, z)

    cdef __fall(self, World world, int x, int y, int z):
        cdef int newY, blockId, material
        cdef bint stop

        newY = y
        while True:
            blockId = world.getBlockId(x, newY - 1, z)
            if blockId == 0:
                stop = True
            else:
                material = self.blocks.blocksList[blockId].getBlockMaterial()
                stop = True if material == Material.water else material == Material.lava

            if not stop or newY <= 0:
                if newY != y:
                    blockId = world.getBlockId(x, newY, z)
                    if blockId > 0 and self.blocks.blocksList[blockId].getBlockMaterial() != Material.air:
                        world.setTileNoUpdate(x, newY, z, 0)

                    world.swap(x, y, z, x, newY, z)

                return

            newY -= 1
