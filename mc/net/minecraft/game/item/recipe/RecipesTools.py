from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks

class RecipesTools:
    __recipePatterns = (('XXX', ' # ', ' # '), ('X', '#', '#'), ('XX', 'X#', ' #'))
    __recipeItems = (
        (blocks.planks, blocks.cobblestone, items.ingotIron, items.diamond, items.ingotGold),
        (items.pickaxeWood, items.pickaxeStone, items.pickaxeSteel, items.pickaxeDiamond, items.pickaxeGold),
        (items.shovelWood, items.shovelStone, items.shovel, items.shovelDiamond, items.shovelGold),
        (items.axeWood, items.axeStone, items.axeSteel, items.axeDiamond, items.axeGold)
    )

    def addRecipes(self, craftingManager):
        for toolIdx, toolItem in enumerate(self.__recipeItems[0]):
            for toolType in range(len(self.__recipeItems) - 1):
                toolResult = self.__recipeItems[toolType + 1][toolIdx]
                craftingManager.addRecipe(
                    ItemStack(toolResult),
                    [self.__recipePatterns[toolType][0], self.__recipePatterns[toolType][1],
                     self.__recipePatterns[toolType][2], ord('#'), items.stick,
                     ord('X'), toolItem]
                )
