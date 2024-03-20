class InventoryPlayer:

    def __init__(self):
        self.currentItem = 0
        self.mainInventory = [None] * 64

    def getCurrentItem(self):
        return self.mainInventory[self.currentItem]

    def getInventorySlotContainItem(self, slot):
        for i in range(len(self.mainInventory)):
            if self.mainInventory[i] and slot == self.mainInventory[i].itemID:
                return i

        return -1

    def getFirstEmptyStack(self):
        for i in range(len(self.mainInventory)):
            if not self.mainInventory[i]:
                return i

        return -1

    def setInventorySlotContents(self, selectedItem, slotIndex):
        stack = self.mainInventory[slotIndex]
        self.mainInventory[slotIndex] = self.mainInventory[selectedItem]
        self.mainInventory[selectedItem] = stack

    def grabTexture(self, index):
        index = self.getInventorySlotContainItem(index)
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

    def consumeInventoryItem(self, index):
        index = self.getInventorySlotContainItem(index)
        if index < 0:
            return False

        self.mainInventory[index].stackSize -= 1
        if self.mainInventory[index].stackSize <= 0:
            self.mainInventory[index] = None

        return True
