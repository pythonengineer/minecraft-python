from mc.net.minecraft.game.item.Item import Item

class ItemSword(Item):

    def __init__(self, items, itemId):
        super().__init__(items, itemId)
        self._maxStackSize = 1

    def getStrVsBlock(self, block):
        return 1.5
