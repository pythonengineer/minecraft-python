from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockDirt(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 3, 2, Material.ground)
