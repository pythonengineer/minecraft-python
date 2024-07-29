from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material

class BlockOre(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex, Material.wood)

    def idDropped(self):
        from mc.net.minecraft.game.item.Items import items
        if self.blockID == self.blocks.oreCoal.blockID:
            return items.coal.shiftedIndex
        elif self.blockID == self.blocks.oreDiamond.blockID:
            return items.diamond.shiftedIndex
        else:
            return self.blockID

    def quantityDropped(self, random):
        return 1

    def onBlockPlaced(self, world, x, y, z):
        from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
        from mc.net.minecraft.game.item.Items import items
        from mc.net.minecraft.game.item.ItemStack import ItemStack
        itemId = 0
        if self.blockID == self.blocks.oreCoal.blockID:
            itemId = items.coal.shiftedIndex
        elif self.blockID == self.blocks.oreDiamond.blockID:
            itemId = items.diamond.shiftedIndex
        elif self.blockID == self.blocks.oreIron.blockID:
            itemId = items.ingotIron.shiftedIndex
        elif self.blockID == self.blocks.oreGold.blockID:
            itemId = items.ingotGold.shiftedIndex

        for i in range(1):
            if world.rand.nextFloat() <= 1.0:
                itemX = world.rand.nextFloat() * 0.7 + 0.15
                itemY = world.rand.nextFloat() * 0.7 + 0.15
                itemZ = world.rand.nextFloat() * 0.7 + 0.15
                item = EntityItem(world, x + itemX, y + itemY, z + itemZ,
                                  ItemStack(itemId))
                item.delayBeforeCanPickup = 10
                world.spawnEntityInWorld(item)

        return True
