from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks

class RecipesWeapons:

    @staticmethod
    def addRecipes(craftingManager):
        for i in range(5):
            if i == 0:
                madeOf = blocks.planks
                sword = items.swordWood
            elif i == 1:
                madeOf = blocks.cobblestone
                sword = items.swordStone
            elif i == 2:
                madeOf = items.ingotIron
                sword = items.swordSteel
            elif i == 3:
                madeOf = items.diamond
                sword = items.swordDiamond
            elif i == 4:
                madeOf = items.ingotGold
                sword = items.swordGold

            craftingManager.addRecipe(ItemStack(sword),
                                      ('X', 'X', '#', ord('#'),
                                       items.stick, ord('X'), madeOf))
