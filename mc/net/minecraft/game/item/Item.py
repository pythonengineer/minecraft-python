from mc.JavaUtils import Random

class Item:
    TOTAL_STACK_SIZE = 99
    _rand = Random()

    def __init__(self, items, itemId):
        self.items = items
        self.itemID = itemId
        self._maxStackSize = Item.TOTAL_STACK_SIZE

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
