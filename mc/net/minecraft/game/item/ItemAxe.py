from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.level.block.Blocks import blocks

class ItemAxe(ItemTool):
    __blocksEffectiveAgainst = (blocks.planks, blocks.bookShelf,
                                blocks.wood, blocks.chest)

    def __init__(self, items, itemId, strength):
        super().__init__(items, itemId, 3, strength, self.__blocksEffectiveAgainst)
