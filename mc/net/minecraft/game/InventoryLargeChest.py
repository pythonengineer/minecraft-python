from mc.net.minecraft.game.Inventory import Inventory

class InventoryLargeChest(Inventory):

    def __init__(self, name, upperChest, lowerChest):
        self.__name = name
        self.__upperChest = upperChest
        self.__lowerChest = lowerChest

    def getSizeInventory(self):
        return self.__upperChest.getSizeInventory() + \
               self.__lowerChest.getSizeInventory()

    def getInvName(self):
        return self.__name

    def getStackInSlot(self, slot):
        if slot >= self.__upperChest.getSizeInventory():
            return self.__lowerChest.getStackInSlot(
                slot - self.__upperChest.getSizeInventory()
            )
        else:
            return self.__upperChest.getStackInSlot(slot)

    def decrStackSize(self, slot, size):
        if slot >= self.__upperChest.getSizeInventory():
            return self.__lowerChest.decrStackSize(
                slot - self.__upperChest.getSizeInventory(), size
            )
        else:
            return self.__upperChest.decrStackSize(slot, size)

    def setInventorySlotContents(self, slot, stack):
        if slot >= self.__upperChest.getSizeInventory():
            self.__lowerChest.setInventorySlotContents(
                slot - self.__upperChest.getSizeInventory(), stack
            )
        else:
            self.__upperChest.setInventorySlotContents(slot, stack)
