from mc.JavaUtils import Random

class Item:
    TOTAL_STACK_SIZE = 100
    _rand = Random()

    def __init__(self, items, itemId):
        self.items = items
        self.shiftedIndex = itemId + 256
        items.itemsList[itemId + 256] = self
        self._maxStackSize = Item.TOTAL_STACK_SIZE
        print(f'Setting items[{(itemId + 256)}] to {self}')

    def getIconIndex(self):
        return self.iconIndex

    def onItemUse(self, stack, world, x, y, z, sideHit):
        pass

    def getStrVsBlock(self, block):
        return 1.0

    def onItemRightClick(self, stack, world, player):
        return False

    def getItemStackLimit(self):
        return self._maxStackSize

    def onPlaced(self, world, x, y, z):
        return False
