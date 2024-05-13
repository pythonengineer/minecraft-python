from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockGrass(Block):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 2)
        self.blockIndexInTexture = 3
        self._setTickOnLoad(True)

    def getBlockTexture(self, face):
        if face == 1: return 0
        if face == 0: return 2
        return 3

    def updateTick(self, world, x, y, z, random):
        if not world.isHalfLit(x, y + 1, z) and world.getBlockMaterial(x, y + 1, z) == Material.air:
            if random.nextInt(4) == 0:
                world.setBlockWithNotify(x, y, z, self.blocks.dirt.blockID)
        else:
            xt = x + random.nextInt(3) - 1
            yt = y + random.nextInt(5) - 3
            zt = z + random.nextInt(3) - 1
            if world.getBlockId(xt, yt, zt) == self.blocks.dirt.blockID and \
               world.isHalfLit(xt, yt + 1, zt) and \
               world.getBlockMaterial(x, y + 1, z) == Material.air:
                world.setBlockWithNotify(xt, yt, zt, self.blocks.grass.blockID)

    def idDropped(self):
        return self.blocks.dirt.idDropped()
