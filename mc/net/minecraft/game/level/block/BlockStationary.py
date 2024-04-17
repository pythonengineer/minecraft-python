from mc.net.minecraft.game.level.block.BlockFlowing import BlockFlowing
from mc.net.minecraft.game.level.material.Material import Material

class BlockStationary(BlockFlowing):

    def __init__(self, blocks, blockId, material):
        super().__init__(blocks, blockId, material)
        self._movingId = blockId - 1
        self._stillId = blockId
        self._setTickOnLoad(False)

    def updateTick(self, world, x, y, z):
        pass

    def onNeighborBlockChange(self, world, x, y, z, blockType):
        hasAirNeighbor = False
        if self._canFlow(world, x - 1, y, z): hasAirNeighbor = True
        if self._canFlow(world, x + 1, y, z): hasAirNeighbor = True
        if self._canFlow(world, x, y, z - 1): hasAirNeighbor = True
        if self._canFlow(world, x, y, z + 1): hasAirNeighbor = True
        if self._canFlow(world, x, y - 1, z): hasAirNeighbor = True

        if blockType != 0:
            material = self.blocks.blocksList[blockType].getBlockMaterial()
            if self._material == Material.water and material == Material.lava or \
               material == Material.water and self._material == Material.lava:
                world.setBlockWithNotify(x, y, z, self.blocks.stone.blockID)
                return

        if self.blocks.fire.canBlockIdCatchFire(blockType):
            hasAirNeighbor = True

        if hasAirNeighbor:
            world.setTileNoUpdate(x, y, z, self._movingId)
            world.scheduleBlockUpdate(x, y, z, self._movingId)
