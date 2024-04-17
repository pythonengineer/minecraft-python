from mc.net.minecraft.game.item.Item import Item

class ItemTool(Item):

    def __init__(self, itemId, affectedBlocks):
        super().__init__(itemId)
        self.__blocksEffectiveAgainst = affectedBlocks
        self.__efficiencyOnProperMaterial = 4.0

    def getStrVsBlock(self, block):
        for b in self.__blocksEffectiveAgainst:
            if b == block:
                return self.__efficiencyOnProperMaterial

        return 1.0
