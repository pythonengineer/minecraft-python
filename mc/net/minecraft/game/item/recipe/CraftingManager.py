from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack

class CraftingManager:

    @staticmethod
    def addRecipe(craftItems):
        if craftItems[0] == items.apple.shiftedIndex:
            return ItemStack(items.arrow.shiftedIndex)
