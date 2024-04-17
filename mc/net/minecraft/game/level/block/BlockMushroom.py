from mc.net.minecraft.game.level.block.BlockFlower import BlockFlower

class BlockMushroom(BlockFlower):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)
        self._setBlockBounds(0.3, 0.0, 0.3, 0.7, 0.4, 0.7)

    def updateTick(self, world, x, y, z):
        below = world.getBlockId(x, y - 1, z)
        if not world.isFullyLit(x, y, z) or not self.blocks.opaqueCubeLookup[below]:
            world.setBlockWithNotify(x, y, z, 0)
