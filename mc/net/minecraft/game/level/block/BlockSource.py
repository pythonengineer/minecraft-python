from mc.net.minecraft.game.level.block.Block import Block

class BlockSource(Block):

    def __init__(self, blocks, blockId, source):
        super().__init__(blocks, blockId, blocks.blocksList[source].blockIndexInTexture)
        self.__source = source

    def onBlockAdded(self, world, x, y, z):
        super().onBlockAdded(world, x, y, z)
        if world.getBlockId(x - 1, y, z) == 0:
            world.setBlockWithNotify(x - 1, y, z, self.__source)
        if world.getBlockId(x + 1, y, z) == 0:
            world.setBlockWithNotify(x + 1, y, z, self.__source)
        if world.getBlockId(x, y, z - 1) == 0:
            world.setBlockWithNotify(x, y, z - 1, self.__source)
        if world.getBlockId(x, y, z + 1) == 0:
            world.setBlockWithNotify(x, y, z + 1, self.__source)
