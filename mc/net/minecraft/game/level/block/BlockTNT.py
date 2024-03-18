from mc.net.minecraft.game.level.block.Block import Block

class BlockTNT(Block):

    def __init__(self, blocks):
        super().__init__(blocks, 46, 8)

    def getBlockTexture(self, face):
        if face == 0:
            return self.blockIndexInTexture + 2
        elif face == 1:
            return self.blockIndexInTexture + 1
        else:
            return self.blockIndexInTexture

    def quantityDropped(self):
        return 0

    def wasExploded(self, world, x, y, z):
        world.createExplosion(x, y - 1, z, self.blocks.planks.blockID)
