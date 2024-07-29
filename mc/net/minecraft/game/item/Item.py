from mc.JavaUtils import Random

class Item:
    TOTAL_STACK_SIZE = 100
    MAX_DAMAGE = 32
    _rand = Random()

    def __init__(self, items, itemId):
        self.items = items
        self.shiftedIndex = itemId + 256
        items.itemsList[itemId + 256] = self
        self._maxStackSize = Item.TOTAL_STACK_SIZE
        self._maxDamage = Item.MAX_DAMAGE

    def setIconIndex(self, iconIndex):
        self._iconIndex = iconIndex
        return self

    def getIconIndex(self):
        return self._iconIndex

    def onItemUse(self, stack, world, x, y, z, sideHit):
        pass

    def getStrVsBlock(self, block):
        return 1.0

    def onItemRightClick(self, stack, world, player):
        return stack

    def getItemStackLimit(self):
        return self._maxStackSize

    def onPlaced(self, world, x, y, z):
        return False

    def getMaxDamage(self):
        return self._maxDamage

    def hitEntity(self, stack):
        pass

    def onBlockDestroyed(self, stack):
        pass

    def getDamageVsEntity(self):
        return 1

    def canHarvestBlock(self, block):
        return False
