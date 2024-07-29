from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockStone(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex, Material.rock)

    def idDropped(self):
        return self.blocks.cobblestone.blockID
