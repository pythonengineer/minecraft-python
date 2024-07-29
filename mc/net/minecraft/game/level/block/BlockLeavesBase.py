from mc.net.minecraft.game.level.block.Block import Block

class BlockLeavesBase(Block):

    def __init__(self, blocks, blockId, tex, material, _):
        super().__init__(blocks, blockId, tex, material)
        self.__renderThrough = True

    def isOpaqueCube(self):
        return False

    def shouldSideBeRendered(self, world, x, y, z, layer):
        if not self.__renderThrough and world.getBlockId(x, y, z) == self.blockID:
            return False
        else:
            return super().shouldSideBeRendered(world, x, y, z, layer)
