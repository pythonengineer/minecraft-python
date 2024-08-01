from mc.net.minecraft.game.item.Item import Item

class ItemTool(Item):

    def __init__(self, items, itemId, attackDmg, strength, affectedBlocks):
        super().__init__(items, itemId)
        self.__blocksEffectiveAgainst = affectedBlocks
        self._maxStackSize = 1
        self._maxDamage = 32 << strength
        self.__efficiencyOnProperMaterial = strength + 1 << 1
        self.__damageVsEntity = attackDmg + strength

    def getStrVsBlock(self, block):
        for b in self.__blocksEffectiveAgainst:
            if b == block:
                return self.__efficiencyOnProperMaterial

        return 1.0

    def hitEntity(self, stack):
        stack.damageItem(2)

    def onBlockDestroyed(self, stack):
        stack.damageItem(1)

    def getDamageVsEntity(self):
        return self.__damageVsEntity
