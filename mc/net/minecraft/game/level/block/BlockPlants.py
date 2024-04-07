from mc.net.minecraft.game.level.block.Block import Block

class BlockPlants(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex)
        self.blockIndexInTexture = tex
        self._setTickOnLoad(True)
        self._setBlockBounds(0.3, 0.0, 0.3, 0.7, 0.6, 0.7)

    def updateTick(self, world, x, y, z, random):
        if not world.multiplayerWorld:
            below = world.getBlockId(x, y - 1, z)
            if not world.isHalfLit(x, y, z) or \
               (below != self.blocks.dirt.blockID and below != self.blocks.grass.blockID):
                world.setBlockWithNotify(x, y, z, 0)

    def getCollisionBoundingBoxFromPool(self, x, y, z):
        return None

    def isOpaqueCube(self):
        return False

    def renderAsNormalBlock(self):
        return False

    def getRenderType(self):
        return 1
