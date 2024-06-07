from mc.net.minecraft.game.item.ItemFood import ItemFood

class ItemSoup(ItemFood):

    def __init__(self, items, itemId, healAmount):
        super().__init__(items, 26, 8)

    def onItemRightClick(self, stack, world, player):
        from mc.net.minecraft.game.item.ItemStack import ItemStack
        super().onItemRightClick(stack, world, player)
        return ItemStack(self.items.bowlEmpty)
