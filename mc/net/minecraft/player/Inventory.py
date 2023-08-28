from mc.net.minecraft.User import User

class Inventory:

    def __init__(self):
        self.selectedSlot = 0
        self.slots = [0] * 9
        for i in range(9):
            self.slots[i] = User.creativeTiles[i].id

    def getSelected(self):
        return self.slots[self.selectedSlot]

    def getSlotContainsID(self, slot):
        for i in range(len(self.slots)):
            if slot == self.slots[i]:
                return i

        return -1

    def scrollHotbar(self, dy):
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1

        self.selectedSlot -= dy
        while self.selectedSlot < 0:
            self.selectedSlot += len(self.slots)

        while self.selectedSlot >= len(self.slots):
            self.selectedSlot -= len(self.slots)

    def getSlotContainsTile(self, tile):
        if tile:
            slot = self.getSlotContainsID(tile.id)
            if slot >= 0:
                self.slots[slot] = self.slots[self.selectedSlot]

            self.slots[self.selectedSlot] = tile.id
