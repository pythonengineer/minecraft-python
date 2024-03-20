class Slot:

    def __init__(self, inventory, slotIndex, xPos, yPos):
        self.__inventory = inventory
        self.slotIndex = slotIndex
        self.xDisplayPosition = xPos
        self.yDisplayPosition = yPos

    def getIsMouseOverSlot(self, x, y):
        w = (self.__inventory.width - 176) // 2
        h = (self.__inventory.height - 184) // 2
        x -= w
        y -= h
        return x >= self.xDisplayPosition - 1 and \
               x < self.xDisplayPosition + 16 + 1 and \
               y >= self.yDisplayPosition - 1 and \
               y < self.yDisplayPosition + 16 + 1

