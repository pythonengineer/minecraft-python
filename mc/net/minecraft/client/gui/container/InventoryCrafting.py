from mc.net.minecraft.game.Inventory import Inventory

class InventoryCrafting(Inventory):
    STACK_LIMIT = 64

    def __init__(self, eventHandler, width, height):
        self.__inventoryWidth = width * height
        self.__stackList = [None] * self.__inventoryWidth
        self.__eventHandler = eventHandler

    def getSizeInventory(self):
        return self.__inventoryWidth

    def getStackInSlot(self, slot):
        return self.__stackList[slot]

    def getInvName(self):
        return 'Crafting'

    def decrStackSize(self, slot, size):
        if not self.__stackList[slot]:
            return None

        if self.__stackList[slot].stackSize <= size:
            stack = self.__stackList[slot]
            self.__stackList[slot] = None
            self.__eventHandler.guiCraftingItemsCheck()
            return stack
        else:
            stack = self.__stackList[slot].splitStack(size)
            if self.__stackList[slot].stackSize == 0:
                self.__stackList[slot] = None

            self.__eventHandler.guiCraftingItemsCheck()
            return stack

    def setInventorySlotContents(self, slot, stack):
        self.__stackList[slot] = stack
        self.__eventHandler.guiCraftingItemsCheck()

    def getInventoryStackLimit(self):
        return InventoryCrafting.STACK_LIMIT
