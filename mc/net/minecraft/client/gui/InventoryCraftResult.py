from mc.net.minecraft.game.Inventory import Inventory

class InventoryCraftResult(Inventory):
    STACK_LIMIT = 64

    def __init__(self, eventHandler):
        self.__stackResult = [None]

    def getSizeInventory(self):
        return 1

    def getStackInSlot(self, slot):
        return self.__stackResult[slot]

    def getInvName(self):
        return 'Result'

    def setInventorySlotContents(self, slot, stack):
        self.__stackResult[slot] = stack

    def getInventoryStackLimit(self):
        return InventoryCraftResult.STACK_LIMIT
