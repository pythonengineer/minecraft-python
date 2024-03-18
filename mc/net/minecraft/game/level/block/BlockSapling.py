from mc.net.minecraft.game.level.block.BlockFlower import BlockFlower

import math

class BlockSapling(BlockFlower):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, 6, 15)
        b = 0.4
        self._setBlockBounds(0.5 - b, 0.0, 0.5 - b, b + 0.5, b * 2.0, b + 0.5)

    def updateTick(self, world, x, y, z, random):
        below = world.getBlockId(x, y - 1, z)
        if world.isHalfLit(x, y, z) and (below == self.blocks.dirt.blockID or \
           below == self.blocks.grass.blockID):
            if math.floor(5 * random.random()) == 0:
                world.setTileNoUpdate(x, y, z, 0)
                if not world.growTrees(x, y, z):
                    world.setTileNoUpdate(x, y, z, self.blockID)
        else:
            world.setBlockWithNotify(x, y, z, 0)
