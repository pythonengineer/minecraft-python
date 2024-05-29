from mc.net.minecraft.game.Inventory import Inventory

class InventoryCrafting(Inventory):
    STACK_LIMIT = 100

    def __init__(self, eventHandler):
        self.__eventHandler = eventHandler
        self.stackList = [None] * 9

    def getSizeInventory(self):
        return 9

    def getStackInSlot(self, slot):
        return self.stackList[slot]

    def getInvName(self):
        return 'Crafting'

    def setInventorySlotContents(self, slot, stack):
        self.stackList[slot] = stack
        self.__eventHandler.onCraftMatrixChanged()

    def getInventoryStackLimit(self):
        return 1
