from mc.net.minecraft.game.item.Item import Item
from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.item.recipe.ShapedRecipes import ShapedRecipes
from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.block.Blocks import blocks

class CraftingManager:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance:
            return cls.instance

        cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.__recipes = []
        for i in range(4):
            if i == 0:
                madeOf = blocks.planks
                pickaxe = items.pickaxeWood
                shovel = items.shovelWood
                axe = items.axeWood
                sword = items.swordWood
            elif i == 1:
                madeOf = blocks.cobblestone
                pickaxe = items.pickaxeStone
                shovel = items.shovelStone
                axe = items.axeStone
                sword = items.swordStone
            elif i == 2:
                madeOf = items.ingotIron
                pickaxe = items.pickaxeSteel
                shovel = items.shovel
                axe = items.axeSteel
                sword = items.swordSteel
            else:
                madeOf = items.diamond
                pickaxe = items.pickaxeDiamond
                shovel = items.shovelDiamond
                axe = items.axeDiamond
                sword = items.swordDiamond

            self.__addRecipe(
                ItemStack(pickaxe),
                ('XXX', ' # ', ' # ', ord('#'), items.stick, ord('X'), madeOf)
            )
            self.__addRecipe(
                ItemStack(shovel),
                ('X', '#', '#', ord('#'), items.stick, ord('X'), madeOf)
            )
            self.__addRecipe(
                ItemStack(axe),
                ('XX', 'X#', ' #', ord('#'), items.stick, ord('X'), madeOf)
            )
            self.__addRecipe(
                ItemStack(sword),
                ('X', 'X', '#', ord('#'), items.stick, ord('X'), madeOf)
            )

        self.__addRecipe(
            ItemStack(items.stick, 4), ('#', '#', ord('#'), blocks.planks)
        )
        self.__addRecipe(
            ItemStack(blocks.blockGold), ('##', '##', ord('#'), items.ingotGold)
        )
        self.__addRecipe(
            ItemStack(blocks.blockSteel), ('##', '##', ord('#'), items.ingotIron)
        )
        self.__addRecipe(
            ItemStack(blocks.blockDiamond), ('##', '##', ord('#'), items.diamond)
        )
        self.__addRecipe(
            ItemStack(blocks.torch, 4),
            ('X', '#', ord('X'), items.coal, ord('#'), items.stick)
        )

    def __addRecipe(self, stack, solution):
        slotLocations = ''
        slot = 0
        recipeWidth = 0
        recipeHeight = 0
        while isinstance(solution[slot], str):
            slots = solution[slot]
            slot += 1
            recipeHeight += 1
            recipeWidth = len(slots)
            slotLocations += slots

        slot2item = {}
        while slot < len(solution):
            slots = solution[slot]
            idx = 0
            if isinstance(solution[slot + 1], Item):
                idx = solution[slot + 1].shiftedIndex
            elif isinstance(solution[slot + 1], Block):
                idx = solution[slot + 1].blockID

            slot2item[slots] = idx
            slot += 2

        recipeItems = [0] * recipeWidth * recipeHeight
        for i in range(recipeWidth * recipeHeight):
            slot = slotLocations[i]
            if slot2item.get(ord(slot)):
                recipeItems[i] = slot2item.get(ord(slot))
            else:
                recipeItems[i] = -1

        self.__recipes.append(
            ShapedRecipes(recipeWidth, recipeHeight, recipeItems, stack)
        )

    def addRecipe(self, craftItems):
        for recipe in self.__recipes:
            if recipe.matches(craftItems):
                return recipe.getCraftingResult()

        return None
