from mc.net.minecraft.game.level.block.BlockLeavesBase import BlockLeavesBase

import math

class BlockLeaves(BlockLeavesBase):

    def __init__(self, blocks):
        super().__init__(blocks, 18, 22)

    def quantityDropped(self, random):
        if math.floor(10 * random.random()) == 0:
            return 1
        else:
            return 0

    def idDropped(self):
        return self.blocks.sapling.blockID
