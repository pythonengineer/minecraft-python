from mc.net.minecraft.game.level.block.Block import Block

class BlockSponge(Block):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 19)
        self.blockIndexInTexture = 48

    def onBlockAdded(self, world, x, y, z):
        for xx in range(x - 2, x + 3):
            for yy in range(y - 2, y + 3):
                for zz in range(z - 2, z + 3):
                    if world.isWater(xx, yy, zz):
                        world.setBlock(xx, yy, zz, 0)

    def onBlockRemoval(self, world, x, y, z):
        for xx in range(x - 2, x + 3):
            for yy in range(y - 2, y + 3):
                for zz in range(z - 2, z + 3):
                    world.notifyBlocksOfNeighborChange(xx, yy, zz,
                                                       world.getBlockId(xx, yy, zz))
