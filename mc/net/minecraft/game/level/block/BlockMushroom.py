from mc.net.minecraft.game.level.block.BlockFlower import BlockFlower

class BlockMushroom(BlockFlower):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)
        b = 0.2
        self._setBlockBounds(0.5 - b, 0.0, 0.5 - b, b + 0.5, b * 2.0, b + 0.5)

    def updateTick(self, world, x, y, z, random):
        below = world.getBlockId(x, y - 1, z)
        if world.isHalfLit(x, y, z) or below != self.blocks.stone.blockID and \
           below != self.blocks.gravel.blockID and \
           below != self.blocks.cobblestone.blockID:
            world.setBlockWithNotify(x, y, z, 0)
