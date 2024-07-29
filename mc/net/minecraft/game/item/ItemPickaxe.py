from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.level.block.Blocks import blocks

class ItemPickaxe(ItemTool):
    __blocksEffectiveAgainst = (blocks.cobblestone, blocks.stairDouble, blocks.stairSingle,
                                blocks.stone, blocks.cobblestoneMossy, blocks.oreIron,
                                blocks.blockSteel, blocks.oreCoal, blocks.blockGold,
                                blocks.oreGold, blocks.oreDiamond, blocks.blockDiamond)

    def __init__(self, items, itemId, damage):
        super().__init__(items, itemId, damage, self.__blocksEffectiveAgainst)
