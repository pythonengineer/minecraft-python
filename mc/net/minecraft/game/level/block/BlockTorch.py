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

    def collisionRayTrace(self, world, x, y, z, v0, v1):
        if world.isBlockNormalCube(x - 1, y, z):
            self._setBlockBounds(0.0, 0.2, 0.35, 0.3, 0.8, 0.65)
        elif world.isBlockNormalCube(x + 1, y, z):
            self._setBlockBounds(0.7, 0.2, 0.35, 1.0, 0.8, 0.65)
        elif world.isBlockNormalCube(x, y, z - 1):
            self._setBlockBounds(0.35, 0.2, 0.0, 0.65, 0.8, 0.3)
        elif world.isBlockNormalCube(x, y, z + 1):
            self._setBlockBounds(0.35, 0.2, 0.7, 0.65, 0.8, 1.0)
        else:
            self._setBlockBounds(0.4, 0.0, 0.4, 0.6, 0.6, 0.6)

        return super().collisionRayTrace(world, x, y, z, v0, v1)
