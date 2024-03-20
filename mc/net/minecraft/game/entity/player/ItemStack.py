class ItemStack:

    def __init__(self, item, stackSize=1):
        from mc.net.minecraft.game.level.block.Block import Block
        self.stackSize = stackSize

        self.itemID = -1
        self.iconIndex = -1
        self.animationsToGo = 0
        if isinstance(item, Block):
            self.itemID = item.blockID
        elif isinstance(item, ItemStack):
            self.itemID = item.itemID
            self.iconIndex = item.iconIndex
        elif isinstance(item, int):
            self.iconIndex = item
