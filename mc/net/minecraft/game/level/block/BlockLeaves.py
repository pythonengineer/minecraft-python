from mc.net.minecraft.game.level.block.BlockLeavesBase import BlockLeavesBase
from mc.net.minecraft.game.level.material.Material import Material

class BlockLeaves(BlockLeavesBase):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 18, 22, Material.plants, True)

    def quantityDropped(self, random):
        if random.nextInt(6) == 0:
            return 1
        else:
            return 0

    def idDropped(self):
        return self.blocks.sapling.blockID
