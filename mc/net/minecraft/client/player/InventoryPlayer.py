from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.client.Session import Session

class InventoryPlayer:
    POP_TIME_DURATION = 5

    def __init__(self):
        self.currentItem = 0
        self.mainInventory = [0] * 9
        self.stackSize = [0] * 9
        self.animationsToGo = [0] * 9
        for i in range(9):
            self.mainInventory[i] = -1
            self.stackSize[i] = 0

    def getCurrentItem(self):
        return self.mainInventory[self.currentItem]

    def getInventorySlotContainItem(self, slot):
        for i in range(len(self.mainInventory)):
            if slot == self.mainInventory[i]:
                return i

        return -1

    def grabTexture(self, index, replace):
        index = self.getInventorySlotContainItem(index)
        if index >= 0:
            self.currentItem = index
        elif replace and index > 0 and blocks.blocksList[index] in Session.allowedBlocks:
            self.replaceSlot(blocks.blocksList[id])

    def swapPaint(self, dy):
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        self.currentItem -= dy
        while self.currentItem < 0:
            self.currentItem += len(self.mainInventory)

        while self.currentItem >= len(self.mainInventory):
            self.currentItem -= len(self.mainInventory)

    def replaceSlot(self, block):
        if block:
            index = self.getInventorySlotContainItem(block.blockID)
            if index >= 0:
                self.mainInventory[index] = self.mainInventory[self.currentItem]

            self.mainInventory[self.currentItem] = block.blockID

    def tick(self):
        for i in range(len(self.animationsToGo)):
            if self.animationsToGo[i] > 0:
                self.animationsToGo[i] -= 1

    def consumeInventoryItem(self, index):
        index = self.getInventorySlotContainItem(index)
        if index < 0:
            return False

        self.stackSize[index] -= 1
        if self.stackSize[index] <= 0:
            self.mainInventory[index] = -1

        return True
