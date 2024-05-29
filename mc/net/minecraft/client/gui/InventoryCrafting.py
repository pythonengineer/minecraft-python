from mc.net.minecraft.game.Inventory import Inventory

class InventoryCrafting(Inventory):
    STACK_LIMIT = 64

    def __init__(self, eventHandler):
        self.__eventHandler = eventHandler
        self.stackList = [None] * 9

    def getSizeInventory(self):
        return 9

    def getStackInSlot(self, slot):
        return self.stackList[slot]

    def getInvName(self):
        return 'Crafting'

    def decrStackSize(self, slot, size):
        if not self.stackList[slot]:
            return None

        if self.stackList[slot].stackSize <= 1:
            stack = self.stackList[slot]
            self.stackList[slot] = None
            self.__eventHandler.onCraftMatrixChanged()
            return stack
        else:
            stack = self.stackList[slot].splitStack(1)
            if self.stackList[slot].stackSize == 0:
                self.stackList[slot] = None

            self.__eventHandler.onCraftMatrixChanged()
            return stack

    def setInventorySlotContents(self, slot, stack):
        self.stackList[slot] = stack
        self.__eventHandler.onCraftMatrixChanged()

    def getInventoryStackLimit(self):
        return 1
