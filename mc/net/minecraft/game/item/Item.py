class Item:

    def __init__(self, itemId):
        self.shiftedIndex = itemId

    def getIconIndex(self):
        return self.iconIndex

    def onItemUse(self, stack, world, x, y, z, sideHit):
        pass

    def getStrVsBlock(self, block):
        return 1.0

    def onPlaced(self, stack, player):
        return False
