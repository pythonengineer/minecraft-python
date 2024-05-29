class Slot:

    def __init__(self, guiHandler, inventory, slotIndex, xPos, yPos):
        self.__guiHandler = guiHandler
        self.inventory = inventory
        self.slotIndex = slotIndex
        self.xDisplayPosition = xPos
        self.yDisplayPosition = yPos

    def getIsMouseOverSlot(self, x, y):
        w = (self.__guiHandler.width - self.__guiHandler.xSize) // 2
        h = (self.__guiHandler.height - self.__guiHandler.ySize) // 2
        x -= w
        y -= h
        return x >= self.xDisplayPosition - 1 and \
               x < self.xDisplayPosition + 16 + 1 and \
               y >= self.yDisplayPosition - 1 and \
               y < self.yDisplayPosition + 16 + 1

    def onPickupFromSlot(self):
        pass

    def isItemValid(self):
        return True

    def getCurrentItemStack(self):
        return self.inventory.getStackInSlot(self.slotIndex)

    def putStack(self, stack):
        self.inventory.setInventorySlotContents(self.slotIndex, stack)
