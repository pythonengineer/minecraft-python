from mc.net.minecraft.game.item.Item import Item

class ItemSword(Item):

    def __init__(self, items, itemId, strength):
        super().__init__(items, itemId)
        self._maxStackSize = 1
        self._maxDamage = 32 << strength
        self.__weaponDamage = 4 + (strength << 1)

    def getStrVsBlock(self, block):
        return 1.5

    def hitEntity(self, stack):
        stack.damageItem(1)

    def onBlockDestroyed(self, stack):
        stack.damageItem(2)

    def getDamageVsEntity(self):
        return self.__weaponDamage