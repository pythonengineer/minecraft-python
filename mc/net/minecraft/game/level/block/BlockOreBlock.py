from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockOreBlock(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex, Material.iron)

    def getBlockTexture(self, face):
        if face == 1:
            return self.blockIndexInTexture - 16
        elif face == 0:
            return self.blockIndexInTexture + 16
        else:
            return self.blockIndexInTexture
