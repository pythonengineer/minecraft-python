from mc.net.minecraft.game.level.block.Block import Block

class BlockOre(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)

    def idDropped(self):
        from mc.net.minecraft.game.item.Items import items
        if self.blockID == self.blocks.oreCoal.blockID:
            return items.coal.shiftedIndex
        elif self.blockID == self.blocks.oreDiamond.blockID:
            return items.diamond.shiftedIndex
        else:
            return self.blockID

    def quantityDropped(self, random):
        return 1 if self.idDropped() == self.blockID else random.nextInt(3) + 1
