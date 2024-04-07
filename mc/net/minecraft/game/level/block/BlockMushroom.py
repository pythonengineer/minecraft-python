from mc.net.minecraft.game.level.block.BlockPlants import BlockPlants

class BlockMushroom(BlockPlants):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)
        self._setBlockBounds(0.3, 0.0, 0.3, 0.7, 0.4, 0.7)

    def updateTick(self, world, x, y, z, random):
        below = world.getBlockId(x, y - 1, z)
        if world.isHalfLit(x, y, z) or below != self.blocks.stone.blockID and \
           below != self.blocks.gravel.blockID and \
           below != self.blocks.cobblestone.blockID:
            world.setBlockWithNotify(x, y, z, 0)
