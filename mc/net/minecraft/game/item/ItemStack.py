from mc.net.minecraft.game.item.Items import items

class ItemStack:

    def __init__(self, item, stackSize=1):
        from mc.net.minecraft.game.level.block.Block import Block
        self.stackSize = stackSize
        self.animationsToGo = 0
        if isinstance(item, Block):
            self.itemID = item.blockID
            self.stackSize = 99
        elif isinstance(item, int):
            self.itemID = item

    def getItem(self):
        return items.itemsList[self.itemID]
