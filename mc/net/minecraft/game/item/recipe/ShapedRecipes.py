from mc.net.minecraft.game.item.ItemStack import ItemStack

class ShapedRecipes:

    def __init__(self, width, height, items, output):
        self.__recipeWidth = width
        self.__recipeHeight = height
        self.__recipeItems = items
        self.__recipeOutput = output

    def matches(self, items):
        for x in range(3 - self.__recipeWidth + 1):
            for y in range(3 - self.__recipeHeight + 1):
                if self.__matches(items, x, y, True):
                    return True
                if self.__matches(items, x, y, False):
                    return True

        return False

    def __matches(self, items, x, y, small):
        for xSlot in range(3):
            for ySlot in range(3):
                row = xSlot - x
                col = ySlot - y
                idx = -1
                if row >= 0 and col >= 0 and \
                   row < self.__recipeWidth and col < self.__recipeHeight:
                    if small:
                        idx = self.__recipeItems[self.__recipeWidth - row - 1 + col * self.__recipeWidth]
                    else:
                        idx = self.__recipeItems[row + col * self.__recipeWidth]

                if items[xSlot + ySlot * 3] != idx:
                    return False

        return True

    def getCraftingResult(self):
        return ItemStack(self.__recipeOutput.itemID, self.__recipeOutput.stackSize)

    def getSize(self):
        return self.__recipeWidth * self.__recipeHeight
