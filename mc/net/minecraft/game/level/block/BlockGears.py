from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockGears(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 55, 62, Material.circuits)

    def getCollisionBoundingBoxFromPool(self, x, y, z):
        return None

    def isOpaqueCube(self):
        return False

    def renderAsNormalBlock(self):
        return False

    def getRenderType(self):
        return 5

    def quantityDropped(self, random):
        return 1

    def isCollidable(self):
        return False
