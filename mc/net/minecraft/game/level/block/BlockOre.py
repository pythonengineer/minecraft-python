from mc.net.minecraft.game.level.block.Block import Block

import random

class BlockOre(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)

    def quantityDropped(self):
        return int(random.random() * 3) + 1
