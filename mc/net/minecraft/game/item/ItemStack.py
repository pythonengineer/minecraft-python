from mc.net.minecraft.game.item.Items import items

from nbtlib.tag import Compound, Short, Byte

class ItemStack:

    def __init__(self, obj, stackSize=1):
        self.stackSize = stackSize
        self.animationsToGo = 0
        if hasattr(obj, 'blockID'):
            self.itemID = obj.blockID
        elif isinstance(obj, int):
            self.itemID = obj
        elif isinstance(obj, Compound):
            compound = obj
            self.itemID = compound['id'].real
            self.stackSize = compound['Count'].real
        elif hasattr(obj, 'shiftedIndex'):
            self.itemID = obj.shiftedIndex

    def splitStack(self, portion):
        self.stackSize -= portion
        return ItemStack(self.itemID, portion)

    def getItem(self):
        return items.itemsList[self.itemID]

    def writeToNBT(self, compound):
        compound['id'] = Short(self.itemID)
        compound['Count'] = Byte(self.stackSize)
        return compound
