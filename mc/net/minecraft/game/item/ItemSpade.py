from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.level.block.Blocks import blocks

class ItemSpade(ItemTool):
    __blocksEffectiveAgainst = (blocks.grass, blocks.dirt, blocks.sand, blocks.gravel)

    def __init__(self, items, itemId):
        super().__init__(items, itemId, self.__blocksEffectiveAgainst)
