from mc.net.minecraft.game.level.block.Block import Block

class BlockLeavesBase(Block):

    def __init__(self, blocks, blockId, tex, _):
        super().__init__(blocks, blockId, tex)
        self.__graphicsLevel = True

    def isOpaqueCube(self):
        return False

    def shouldSideBeRendered(self, world, x, y, z, layer):
        if not self.__graphicsLevel and world.getBlockId(x, y, z) == self.blockID:
            return False
        else:
            return super().shouldSideBeRendered(world, x, y, z, layer)
