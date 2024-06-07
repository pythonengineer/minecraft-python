from mc.net.minecraft.game.level.block.Block import Block

class BlockStep(Block):

    def __init__(self, blocks, blockId, half):
        self.__blockType = half
        super().__init__(blocks, blockId, 6)
        if not self.__blockType:
            self._setBlockBounds(0.0, 0.0, 0.0, 1.0, 0.5, 1.0)

    def getBlockTexture(self, face):
        return 6 if face <= 1 else 5

    def isOpaqueCube(self):
        return self.__blockType

    def onNeighborBlockChange(self, world, x, y, z, blockType):
        if self == self.blocks.stairSingle:
            pass

    def onBlockAdded(self, world, x, y, z):
        if self != self.blocks.stairSingle:
            super().onBlockAdded(world, x, y, z)

        if world.getBlockId(x, y - 1, z) == self.blocks.stairSingle.blockID:
            world.setBlockWithNotify(x, y, z, 0)
            world.setBlockWithNotify(x, y - 1, z, self.blocks.stairDouble.blockID)

    def idDropped(self):
        return self.blocks.stairSingle.blockID

    def renderAsNormalBlock(self):
        return self.__blockType

    def shouldSideBeRendered(self, world, x, y, z, layer):
        if layer == 1:
            return True
        elif not super().shouldSideBeRendered(world, x, y, z, layer):
            return False
        elif layer == 0:
            return True
        else:
            return world.getBlockId(x, y, z) != self.blockID
