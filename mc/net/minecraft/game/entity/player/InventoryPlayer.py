from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.Inventory import Inventory

class InventoryPlayer(Inventory):
    PLAYER_STACK_LIMIT = 64

    def __init__(self):
        self.currentItem = 0
        self.mainInventory = [None] * 40

    def getCurrentItem(self):
        return self.mainInventory[self.currentItem]

    def __getInventorySlotContainItem(self, slot):
        for i in range(len(self.mainInventory)):
            if self.mainInventory[i] and self.mainInventory[i].itemID == slot:
                return i

        return -1

    def __storeItemStack(self):
        for i in range(len(self.mainInventory)):
            if not self.mainInventory[i]:
                return i

        return -1

    def getFirstEmptyStack(self, index):
        index = self.__getInventorySlotContainItem(index)
        if index >= 0 and index < 9:
            self.currentItem = index

    def swapPaint(self, dy):
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        self.currentItem -= dy
        while self.currentItem < 0:
            self.currentItem += 9

        while self.currentItem >= 9:
            self.currentItem -= 9

    def tick(self):
        for i in range(len(self.mainInventory)):
            if self.mainInventory[i] and self.mainInventory[i].animationsToGo > 0:
                self.mainInventory[i].animationsToGo -= 1

    def consumeInventoryItem(self, item):
        slot = self.__getInventorySlotContainItem(item)
        if slot < 0:
            return False

        self.mainInventory[slot].stackSize -= 1
        if self.mainInventory[slot].stackSize <= 0:
            self.mainInventory[slot] = None

        return True

    def addItemStackToInventory(self, stack):
        stackSize = stack.stackSize
        itemId = stack.itemID
        maybeSlot = 0
        slot = 0
        while True:
            if maybeSlot >= len(self.mainInventory):
                slot = -1
                break

            if self.mainInventory[maybeSlot] and self.mainInventory[maybeSlot].itemID == itemId:
                item = self.mainInventory[maybeSlot]
                if self.mainInventory[maybeSlot].stackSize < item.getItem().getItemStackLimit() and \
                   self.mainInventory[maybeSlot].stackSize < InventoryPlayer.PLAYER_STACK_LIMIT:
                    slot = maybeSlot
                    break

            maybeSlot += 1

        if slot < 0:
            slot = self.__storeItemStack()

        if slot >= 0:
            if not self.mainInventory[slot]:
                self.mainInventory[slot] = ItemStack(itemId, 0)

            stackExcess = stackSize
            item = self.mainInventory[slot]
            if stackSize > item.getItem().getItemStackLimit() - self.mainInventory[slot].stackSize:
                item = self.mainInventory[slot]
                stackExcess = item.getItem().getItemStackLimit() - self.mainInventory[slot].stackSize

            stackExcess = min(
                stackExcess,
                InventoryPlayer.PLAYER_STACK_LIMIT - self.mainInventory[slot].stackSize
            )
            if stackExcess == 0:
                stackSize = stackSize
            else:
                stackSize -= stackExcess
                self.mainInventory[slot].stackSize += stackExcess
                self.mainInventory[slot].animationsToGo = 5

        stack.stackSize = stackSize
        if stack.stackSize == 0:
            return True
        else:
            slot = self.__storeItemStack()
            if slot >= 0:
                self.mainInventory[slot] = stack
                self.mainInventory[slot].animationsToGo = 5
                return True
            else:
                return False

    def decrStackSize(self, slot, size):
        if not self.mainInventory[slot]:
            return None

        if self.mainInventory[slot].stackSize <= size:
            stack = self.mainInventory[slot]
            self.mainInventory[slot] = None
            return stack
        else:
            stack = self.mainInventory[slot].splitStack(size)
            if self.mainInventory[slot].stackSize == 0:
                self.mainInventory[slot] = None

            return stack

    def setInventorySlotContents(self, slot, stack):
        self.mainInventory[slot] = stack

    def getSizeInventory(self):
        return len(self.mainInventory)

    def getStackInSlot(self, slot):
        return self.mainInventory[slot]

    def getInvName(self):
        return 'Inventory'

    def getInventoryStackLimit(self):
        return InventoryPlayer.PLAYER_STACK_LIMIT
