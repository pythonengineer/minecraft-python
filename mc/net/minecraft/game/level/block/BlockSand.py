from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material
from mc.JavaUtils import Random

class BlockSand(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex, Material.sand)
        self.__rand = Random()

    def onNeighborBlockChange(self, world, x, y, z, blockType):
        newY = y
        while True:
            blockId = world.getBlockId(x, newY - 1, z)
            if blockId == 0:
                stop = True
            elif blockId == self.blocks.fire.blockID:
                stop = True
            else:
                material = self.blocks.blocksList[blockId].material
                stop = True if material == Material.water else material == Material.lava

            if not stop or newY < 0:
                if newY < 0:
                    world.setTileNoUpdate(x, y, z, 0)

                if newY != y:
                    blockId = world.getBlockId(x, newY, z)
                    if blockId > 0 and self.blocks.blocksList[blockId].material != Material.air:
                        world.setTileNoUpdate(x, newY, z, 0)

                    world.swap(x, y, z, x, newY, z)

                return

            newY -= 1
            if world.getBlockId(x, newY, z) == self.blocks.fire.blockID:
                world.setBlock(x, newY, z, 0)

    def onBlockPlaced(self, world, x, y, z):
        from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
        from mc.net.minecraft.game.item.ItemStack import ItemStack

        blockId = self.blocks.glass.blockID
        drops = self.__rand.nextInt(3) + 1
        for i in range(drops):
            if world.rand.nextFloat() <= 1.0:
                itemX = world.rand.nextFloat() * 0.7 + 0.15
                itemY = world.rand.nextFloat() * 0.7 + 0.15
                itemZ = world.rand.nextFloat() * 0.7 + 0.15
                item = EntityItem(world, x + itemX, y + itemY, z + itemZ,
                                  ItemStack(blockId))
                item.delayBeforeCanPickup = 10
                world.spawnEntityInWorld(item)

        return True
