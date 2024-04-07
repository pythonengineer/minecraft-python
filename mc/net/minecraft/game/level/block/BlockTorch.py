from mc.net.minecraft.game.level.block.Block import Block

class BlockTorch(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 50, 80)

    def getCollisionBoundingBoxFromPool(self, x, y, z):
        return None

    def isOpaqueCube(self):
        return False

    def renderAsNormalBlock(self):
        return False

    def getRenderType(self):
        return 2
