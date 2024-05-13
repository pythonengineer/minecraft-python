from nbtlib.tag import Compound, Short, Byte

class ItemStack:

    def __init__(self, item, stackSize=1):
        from mc.net.minecraft.game.level.block.Block import Block
        self.stackSize = stackSize
        self.animationsToGo = 0
        if isinstance(item, Block):
            self.itemID = item.blockID
        elif isinstance(item, int):
            self.itemID = item
        elif isinstance(item, Compound):
            compound = item
            self.itemID = compound['id'].real
            self.stackSize = compound['Count'].real

    def splitStack(self):
        self.stackSize -= 1
        return ItemStack(self.itemID, 1)

    def getItem(self):
        from mc.net.minecraft.game.item.Items import items
        return items.itemsList[self.itemID]

    def writeToNBT(self, compound):
        compound['id'] = Short(self.itemID)
        compound['Count'] = Byte(self.stackSize)
        return compound
