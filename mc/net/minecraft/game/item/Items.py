from mc.net.minecraft.game.item.ItemFlintAndSteel import ItemFlintAndSteel
from mc.net.minecraft.game.item.ItemBlock import ItemBlock
from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.item.ItemFood import ItemFood
from mc.net.minecraft.game.item.ItemBow import ItemBow
from mc.net.minecraft.game.item.Item import Item
from mc.net.minecraft.game.level.block.Blocks import blocks

class Items:

    def __init__(self):
        self.itemsList = [None] * 1024
        for i in range(256):
            if blocks.blocksList[i]:
                self.itemsList[i] = ItemBlock(self, i)

        shovel = ItemTool(self, 256, (blocks.grass, blocks.dirt, blocks.sand, blocks.gravel))
        shovel.iconIndex = 52
        pickaxe = ItemTool(self, 257, (blocks.cobblestone, blocks.stairDouble, blocks.stairSingle,
                                       blocks.stone, blocks.cobblestoneMossy, blocks.oreIron,
                                       blocks.blockSteel, blocks.oreCoal, blocks.blockGold,
                                       blocks.oreGold))
        pickaxe.iconIndex = 68
        axe = ItemTool(self, 258, (blocks.planks, blocks.bookShelf, blocks.wood))
        axe.iconIndex = 84

        flint = ItemFlintAndSteel(self, 259)
        flint.iconIndex = 5

        apple = ItemFood(self, 260, 4)
        apple.iconIndex = 4

        bow = ItemBow(self, 261)
        bow.iconIndex = 21

        self.arrow = Item(self, 262)
        self.arrow.iconIndex = 37

        self.itemsList[256:263] = [shovel, pickaxe, axe, flint, apple, bow, self.arrow]

items = Items()
