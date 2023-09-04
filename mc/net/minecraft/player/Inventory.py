class Inventory:

    def __init__(self):
        self.selected = 0
        self.slots = [0] * 9
        self.count = [0] * 9
        self.popTime = [0] * 9
        for i in range(9):
            self.slots[i] = -1
            self.count[i] = 0

    def getSelected(self):
        return self.slots[self.selected]

    def containsTileAt(self, slot):
        for i in range(len(self.slots)):
            if slot == self.slots[i]:
                return i

        return -1

    def swapPaint(self, dy):
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        self.selected -= dy
        while self.selected < 0:
            self.selected += len(self.slots)

        while self.selected >= len(self.slots):
            self.selected -= len(self.slots)

    def removeResource(self, index):
        index = self.containsTileAt(index)
        if index < 0:
            return False

        self.count[index] -= 1
        if self.count[index] <= 0:
            self.slots[index] = -1

        return True
