from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockBookshelf(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 47, 35, Material.wood)

    def getBlockTexture(self, face):
        return 4 if face <= 1 else self.blockIndexInTexture

    def quantityDropped(self, random):
        return 0
