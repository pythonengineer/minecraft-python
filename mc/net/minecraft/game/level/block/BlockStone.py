from mc.net.minecraft.game.level.block.Block import Block

class BlockStone(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)

    def isDropped(self):
        return self.blocks.cobblestone.blockID
