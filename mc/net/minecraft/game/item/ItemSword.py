from mc.net.minecraft.game.item.Item import Item

class ItemSword(Item):

    def __init__(self, items, itemId, damage):
        super().__init__(items, itemId)
        self._maxStackSize = 1
        self._maxDamage = 32 << damage
        self.__weaponDamage = 4 * (damage + 1)

    def getStrVsBlock(self, block):
        return 1.5

    def hitEntity(self, stack):
        stack.damageItem(1)

    def onBlockDestroyed(self, stack):
        stack.damageItem(2)

    def getItemDamage(self):
        return self.__weaponDamage
