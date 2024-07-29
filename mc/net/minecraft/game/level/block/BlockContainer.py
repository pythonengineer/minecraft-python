from mc.net.minecraft.game.level.block.Block import Block

class BlockContainer(Block):

    def __init__(self, blocks, blockId, material):
        super().__init__(blocks, blockId, material)

    def onBlockAdded(self, world, x, y, z):
        super().onBlockAdded(world, x, y, z)
        world.setBlockTileEntity(x, y, z, self._getBlockEntity())

    def onBlockRemoval(self, world, x, y, z):
        super().onBlockRemoval(world, x, y, z)
        world.removeBlockTileEntity(x, y, z)

    def _getBlockEntity(self):
        return None
