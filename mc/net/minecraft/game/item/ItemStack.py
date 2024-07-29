from mc.net.minecraft.game.item.Items import items

from nbtlib.tag import Compound, Short, Byte

class ItemStack:

    def __init__(self, obj, stackSize=1, damage=0):
        self.stackSize = stackSize
        self.itemDamage = damage
        self.animationsToGo = 0
        if hasattr(obj, 'blockID'):
            self.itemID = obj.blockID
        elif isinstance(obj, int):
            self.itemID = obj
        elif isinstance(obj, Compound):
            compound = obj
            self.itemID = compound['id'].real
            self.stackSize = compound['Count'].real
            self.itemDamage = compound['Damage'].real
        elif hasattr(obj, 'shiftedIndex'):
            self.itemID = obj.shiftedIndex

    def splitStack(self, portion):
        self.stackSize -= portion
        return ItemStack(self.itemID, portion, self.itemDamage)

    def getItem(self):
        return items.itemsList[self.itemID]

    def writeToNBT(self, compound):
        compound['id'] = Short(self.itemID)
        compound['Count'] = Byte(self.stackSize)
        compound['Damage'] = Short(self.itemDamage)
        return compound

    def isItemStackDamageable(self):
        return items.itemsList[self.itemID].getMaxDamage()

    def damageItem(self, damage):
        self.itemDamage += damage
        if self.itemDamage > self.isItemStackDamageable():
            self.stackSize = max(0, self.stackSize - 1)
            self.itemDamage = 0
