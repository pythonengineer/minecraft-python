from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks

class RecipesWeapons:
    __recipePatterns = (('X', 'X', '#'),)
    __recipeItems = (
        (blocks.planks, blocks.cobblestone, items.ingotIron, items.diamond, items.ingotGold),
        (items.swordWood, items.swordStone, items.swordSteel, items.swordDiamond, items.swordGold)
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

        craftingManager.addRecipe(
            ItemStack(items.bow, 1),
            (' #X', '# X', ' #X', ord('X'),
             items.silk, ord('#'), items.stick)
        )
        craftingManager.addRecipe(
            ItemStack(items.arrow, 4),
            ('X', '#', 'Y', ord('Y'), items.feather, ord('X'),
             items.ingotIron, ord('#'), items.stick)
        )
