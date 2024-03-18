from mc.net.minecraft.game.level.block.Block import Block

class BlockGlass(Block):

    def __init__(self, blocks):
        super().__init__(blocks, 20, 49)
        self.__graphicsLevel = False

    def isOpaqueCube(self):
        return False

    def shouldSideBeRendered(self, world, x, y, z, layer):
        block = world.getBlockId(x, y, z)
        if block == self.blockID:
            return False
        else:
            return super().shouldSideBeRendered(world, x, y, z, layer)
