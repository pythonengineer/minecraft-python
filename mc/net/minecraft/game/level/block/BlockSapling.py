from mc.net.minecraft.game.level.block.BlockPlants import BlockPlants

import math

class BlockSapling(BlockPlants):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, 6, 15)
        self._setBlockBounds(10.0 * 0.01, 0.0, 10.0 * 0.01, 0.9, 0.8, 0.9)

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
