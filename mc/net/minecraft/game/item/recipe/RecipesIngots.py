from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks

class RecipesIngots:
    __recipeItems = (
        (blocks.blockGold, items.ingotGold),
        (blocks.blockSteel, items.ingotIron),
        (blocks.blockDiamond, items.diamond)
    )

    def addRecipes(self, craftingManager):
        for block, item in RecipesIngots.__recipeItems:
            craftingManager.addRecipe(ItemStack(block), ['###', '###', '###', ord('#'), item])
            craftingManager.addRecipe(ItemStack(item, 9), ['#', ord('#'), block])
