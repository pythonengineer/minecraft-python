from mc.net.minecraft.game.level.block.Block import Block

class BlockSource(Block):

    def __init__(self, blocks, blockId, fluid):
        super().__init__(blocks, blockId, blocks.blocksList[fluid].blockIndexInTexture)
        self.__fluid = fluid

    def onBlockAdded(self, world, x, y, z):
        super().onBlockAdded(world, x, y, z)
        if world.getBlockId(x - 1, y, z) == 0:
            world.setBlockWithNotify(x - 1, y, z, self.__fluid)
        if world.getBlockId(x + 1, y, z) == 0:
            world.setBlockWithNotify(x + 1, y, z, self.__fluid)
        if world.getBlockId(x, y, z - 1) == 0:
            world.setBlockWithNotify(x, y, z - 1, self.__fluid)
        if world.getBlockId(x, y, z + 1) == 0:
            world.setBlockWithNotify(x, y, z + 1, self.__fluid)
