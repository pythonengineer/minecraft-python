from mc.net.minecraft.level.tile.Tiles import tiles
from mc.net.minecraft.User import User

class Inventory:
    POP_TIME_DURATION = 5

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

    def __containsTileAt(self, slot):
        for i in range(len(self.slots)):
            if slot == self.slots[i]:
                return i

        return -1

    def grabTexture(self, index, replace):
        index = self.__containsTileAt(index)
        if index >= 0:
            self.selected = index
        elif replace and index > 0 and tiles.tiles[index] in User.creativeTiles:
            self.replaceTile(tiles.tiles[id])

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

    def replaceSlot(self, index):
        if index >= 0:
            self.replaceTile(User.creativeTiles[index])

    def replaceTile(self, tile):
        if tile:
            index = self.__containsTileAt(tile.id)
            if index >= 0:
                self.slots[index] = self.slots[self.selected]

            self.slots[self.selected] = tile.id

    def addResource(self, index):
        slot = self.__containsTileAt(index)
        if slot < 0:
            slot = self.__containsTileAt(-1)

        if slot < 0:
            return False
        elif self.count[slot] >= 99:
            return False

        self.slots[slot] = index
        self.count[slot] += 1
        self.popTime[slot] = Inventory.POP_TIME_DURATION
        return True

    def tick(self):
        for i in range(len(self.popTime)):
            if self.popTime[i] > 0:
                self.popTime[i] -= 1

    def removeResource(self, index):
        index = self.__containsTileAt(index)
        if index < 0:
            return False

        self.count[index] -= 1
        if self.count[index] <= 0:
            self.slots[index] = -1

        return True
