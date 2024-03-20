from mc.net.minecraft.game.level.block.Block import Block

import random

class BlockOre(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)

    def idDropped(self):
        if self == self.blocks.oreCoal:
            return self.blocks.stairSingle.blockID
        elif self == self.blocks.oreGold:
            return self.blocks.goldBlock.blockID
        elif self == self.blocks.oreIron:
            return self.blocks.ironBlock.blockID
        else:
            return self.blockID

    def quantityDropped(self, random):
        return int(random.random() * 3) + 1
