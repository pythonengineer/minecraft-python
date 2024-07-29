from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockLog(Block):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 17, Material.wood)
        self.blockIndexInTexture = 20

    def quantityDropped(self, random):
        return random.nextInt(3) + 3

    def idDropped(self):
        return self.blocks.planks.blockID

    def getBlockTexture(self, face):
        return 21 if face == 1 else (21 if face == 0 else 20)
