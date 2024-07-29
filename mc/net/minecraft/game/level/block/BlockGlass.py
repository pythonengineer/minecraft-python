from mc.net.minecraft.game.level.block.Block import Block

class BlockGlass(Block):

    def __init__(self, blocks, blockId, tex, material, _):
        super().__init__(blocks, 20, 49, material)
        self.__renderThrough = False

    def isOpaqueCube(self):
        return False

    def shouldSideBeRendered(self, world, x, y, z, layer):
        block = world.getBlockId(x, y, z)
        if not self.__renderThrough and block == self.blockID:
            return False
        else:
            return super().shouldSideBeRendered(world, x, y, z, layer)
