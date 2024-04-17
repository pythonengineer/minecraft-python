from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.ItemBlock import ItemBlock
from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.item.ItemFood import ItemFood
from mc.net.minecraft.game.item.ItemFlintAndSteel import ItemFlintAndSteel

class Items:

    def __init__(self):
        self.itemsList = [None] * 1024
        for i in range(256):
            if blocks.blocksList[i]:
                self.itemsList[i] = ItemBlock(i)

        shovel = ItemTool(256, (blocks.grass, blocks.dirt, blocks.sand, blocks.gravel))
        shovel.iconIndex = 52
        pickaxe = ItemTool(257, (blocks.cobblestone, blocks.stairDouble, blocks.stairSingle,
                                 blocks.stone, blocks.cobblestoneMossy, blocks.oreIron,
                                 blocks.blockSteel, blocks.oreCoal, blocks.blockGold,
                                 blocks.oreGold))
        pickaxe.iconIndex = 68
        axe = ItemTool(258, (blocks.planks, blocks.bookShelf, blocks.wood))
        axe.iconIndex = 84

        flint = ItemFlintAndSteel(259)
        flint.iconIndex = 5

        self.apple = ItemFood(260, 4)
        self.apple.iconIndex = 4

        self.itemsList[256:261] = [shovel, pickaxe, axe, flint, self.apple]

items = Items()
