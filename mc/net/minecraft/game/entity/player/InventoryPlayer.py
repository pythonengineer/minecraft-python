from mc.net.minecraft.game.entity.player.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks

class InventoryPlayer:
    MAX_STACK = 99

    def __init__(self):
        self.currentSlot = 0
        self.mainInventory = [None] * 64

    def getCurrentItem(self):
        return self.mainInventory[self.currentSlot]

    def __getInventorySlotContainItem(self, slot):
        for i in range(len(self.mainInventory)):
            if self.mainInventory[i] and slot == self.mainInventory[i].itemID:
                return i

        return -1

    def __getFirstEmptyStack(self):
        for i in range(len(self.mainInventory)):
            if not self.mainInventory[i]:
                return i

        return -1

    def getFirstEmptyStack(self, index):
        index = self.__getInventorySlotContainItem(index)
        if index >= 0 and index < 9:
            self.currentSlot = index

    def swapPaint(self, dy):
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        self.currentSlot -= dy
        while self.currentSlot < 0:
            self.currentSlot += 9

        while self.currentSlot >= 9:
            self.currentSlot -= 9

    def tick(self):
        for i in range(len(self.mainInventory)):
            if self.mainInventory[i] and self.mainInventory[i].animationsToGo > 0:
                self.mainInventory[i].animationsToGo -= 1

    def removeResource(self, index):
        index = self.__getInventorySlotContainItem(index)
        if index < 0:
            return False

        self.mainInventory[index].stackSize -= 1
        if self.mainInventory[index].stackSize <= 0:
            self.mainInventory[index] = None

        return True

    def setInventorySlotContents(self, selectedItem, slotIndex):
        stack = self.mainInventory[slotIndex]
        self.mainInventory[slotIndex] = self.mainInventory[selectedItem]
        self.mainInventory[selectedItem] = stack

    def addItemStackToInventory(self, stack):
        if stack.itemID > 0:
            item = stack.itemID
            slot = self.__getInventorySlotContainItem(item)
            if slot < 0:
                slot = self.__getFirstEmptyStack()

            if slot >= 0:
                if not self.mainInventory[slot]:
                    self.mainInventory[slot] = ItemStack(blocks.blocksList[item], 0)

                if self.mainInventory[slot].stackSize < InventoryPlayer.MAX_STACK:
                    self.mainInventory[slot].stackSize += 1
                    self.mainInventory[slot].animationsToGo = 5
                    return True
        else:
            slot = self.__getFirstEmptyStack()
            if slot >= 0:
                self.mainInventory[slot] = stack
                return True

        return False
